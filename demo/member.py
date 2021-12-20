
from random import randint
from .curve import *


class Member():
    def __init__(self, _name: str, _min: int, _max: int):
        self.name = _name
        self.p_once = E.INF
        self.s_once = 0
        self.p_key = E.INF
        self.s_poly = [0] * _min
        self.x_key = 0
        self.share = [0] * _max
        self.chall = 0
        self.secret = 0
        self.online = 0

    
    def set_status(self, _stat: str):
        if _stat == 'true': self.online = 1
        if _stat == 'false': self.online = 0
        return True


    def gen_pair_nonce(self) -> list[Point, int]:
        self.s_once = randint(2, N - 1)
        self.p_once = G * self.s_once
        return self.p_once, self.s_once

    
    def clear_nonce(self):
        self.s_once = 0
        self.p_once = E.INF


    def gen_private_poly(self) -> list[Point, list[int]]:
        order = len(self.s_poly)
        for i in range(order):
            coef = randint(2, N - 1)
            self.s_poly[i] = coef
        self.p_key = G * self.s_poly[0]
        return self.p_key, self.s_poly


    def obfuscate_poly(self) -> list[Point]:
        result = []
        for coef in self.s_poly:
            obfs = coef * G
            result.append(obfs)
        result[0] *= self.chall
        return result


    def verify_obfuscation(self, index: int, obs: list[list[Point]]):
        size = len(self.share)
        for i in range(1, size):
            if i == index: continue
            y = obs[i][0]
            x = index
            for j in range(1, len(obs[i])):
                y = y + x * obs[i][j]
                x = x * x
            if y != self.share[i] * G: return False
        return True


    def set_master_key(self, group_hash: bytes):
        _chall = hash_aggregate(group_hash, self.p_key)
        _chall = bytes_to_long(_chall)
        self.chall = _chall
        self.x_key = self.s_poly[0] * _chall % N


    def gen_secret_share(self, j: int) -> int:
        order = len(self.s_poly)
        y_value = self.x_key
        for i in range(1, order):
            y_value += self.s_poly[i] * j % N
            j = j * j
        return y_value % N


    def recv_secret_share(self, y_value: int, i: int):
        self.share[i] = y_value


    def sum_secret_share(self):
        size = len(self.share)
        self.secret = 0
        for i in range(1, size):
            self.secret += self.share[i]
            self.secret %= N


    def get_pair_secret(self) -> list[int, int]:
        return self.x_key, self.secret


    def lagrange_interpolate(self, index: int, group: list[int]):
        f0 = 1
        for other in group:
            if other == index: continue
            iv = pow(index - other, -1, N)
            f0 = f0 * iv * - other % N
        f0 = f0 * self.secret % N
        return f0


    def get_pkey_piece(self, index: int, group: list[int]) -> Point:
        f0 = self.lagrange_interpolate(index, group)
        return G * f0


    def sign_challenge(self, e: bytes, index: int, group: list[int]):
        f0 = self.lagrange_interpolate(index, group)
        Si = self.s_once + f0 * bytes_to_long(e) % N
        return Si % N
