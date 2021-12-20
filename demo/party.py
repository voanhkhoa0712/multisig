
from .member import Member
from .curve import *

fool = Member('fool', 0, 0)

class Party():
    def __init__(self, _min: int, _max: int):
        self.people = [fool]
        self.signable = False
        self.now_size = 1
        self.max_size = 1 + _max
        self.min_size = 0 + _min
        self.storage = []


    def create_user(self, _name: str):
        if self.now_size == self.max_size: return False
        user = Member(_name, self.min_size, self.max_size)
        self.people.append(user)
        self.now_size = len(self.people)
        return self.people[self.now_size - 1].gen_private_poly()


    def remove_user(self, _name: str):
        if self.now_size == 1: return []
        _people = [user for user in self.people if user.name != _name]
        if len(_people) < len(self.people): 
            self.signable = False
            self.people = _people
            self.now_size = len(self.people)
        return self.list_member()


    def list_member(self) -> list[str]:
        _lname = [user.name for user in self.people if user.name != 'fool']
        return _lname


    def reset_member(self):
        self.people = [fool]
        self.now_size = 1

        
    def set_user_status(self, _name: str, _stat: str):
        for user in self.people:
            if user.name == _name:
                return user.set_status(_stat)
        return False


    def broadcast_obfused_poly(self):
        self.storage = [[]]
        for i, user in enumerate(self.people):
            if i == 0: continue
            obs_poly = user.obfuscate_poly()
            self.storage.append(obs_poly)


    def get_all_address(self) -> list[Point]:
        result = []
        for i in range(1, self.max_size):
            addr = self.people[i].p_key
            result.append(addr)
        return result


    def set_private_chall(self):
        group_addr = self.get_all_address()
        group_hash = hash_multiset(group_addr)
        for i in range(1, self.max_size):
            self.people[i].set_master_key(group_hash)


    def each_share_secret(self):
        for j in range(1, self.max_size):
            for i in range(1, self.max_size):
                y_value = self.people[i].gen_secret_share(j)
                self.people[j].recv_secret_share(y_value, i)


    def check_share_secret(self):
        for i, user in enumerate(self.people):
            if i == 0: continue
            if True != user.verify_obfuscation(i, self.storage):
                return False
            user.sum_secret_share()
        return True


    def setup_group(self):
        if self.now_size != self.max_size: 
            return False
        self.set_private_chall()
        self.broadcast_obfused_poly()
        self.each_share_secret()
        self.signable = self.check_share_secret()
        return self.signable


    def view_secret(self, _name: str):
        for user in self.people:
            if user.name == _name:
                return user.get_pair_secret()
        return False


    def view_nonce(self, _name: str):
        for user in self.people:
            if user.name == _name:
                return user.gen_pair_nonce()
        return False


    def count_signers(self) -> list[int]:
        if self.signable == False: return []
        result = []
        for i, user in enumerate(self.people):
            if user.p_once != E.INF and user.online == True:
                result.append(i)
        return result


    def rebuild_group_pkey(self, subset: list[int]) -> Point:
        pk_group = E.INF
        for signer in subset:
            pi_piece = self.people[signer].get_pkey_piece(signer, subset)
            pk_group = pk_group + pi_piece
        return pk_group

    
    def true_group_pkey(self) -> Point:
        pk_group = E.INF
        for user in self.people:
            pk_group = pk_group + user.p_key * user.chall
        return pk_group


    def public_group_nonce(self, subset: list[int]) -> Point:
        r_nonce = E.INF
        for signer in subset:
            r_nonce += self.people[signer].p_once
        return r_nonce


    def create_signature(self, e: bytes, subset: list[int]):
        v_sign = 0
        for signer in subset:
            v_sign += self.people[signer].sign_challenge(e, signer, subset)
            v_sign %= N
        return v_sign


    def clear_all_nonce(self):
        for user in self.people:
            user.clear_nonce()
        return True


    def sign_message(self, message: str):
        subset = self.count_signers()
        if len(subset) < self.min_size: return False
        subset = subset[:self.min_size]

        p = self.rebuild_group_pkey(subset)
        assert p == self.true_group_pkey()

        r = self.public_group_nonce(subset)
        e = hash_signature(p, r, message)
        s = self.create_signature(e, subset)

        assert True == self.clear_all_nonce()
        return (p, r, s)