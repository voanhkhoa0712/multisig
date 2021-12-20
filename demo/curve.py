
from Crypto.Hash import SHA256
from Crypto.Util.number import long_to_bytes
from Crypto.Util.number import bytes_to_long

from elliptic.ecc.curve import ShortWeierstrassCurve
from elliptic.ecc.curve import Point, P256


# E = ShortWeierstrassCurve('', -2, 15, 307, 311, 17, 17)

E = P256
G = E.G
N = E.n


def hash_multiset(L: list[Point]) -> bytes:
    L.sort(key = lambda P: (P.x, P.y))
    H = SHA256.new()
    for P in L:
        H.update(long_to_bytes(P.x))
        H.update(long_to_bytes(P.y))
    return H.digest()


def hash_aggregate(Lshash: bytes, P: Point) -> bytes:
    H = SHA256.new()
    H.update(Lshash)
    H.update(long_to_bytes(P.x))
    H.update(long_to_bytes(P.y))
    return H.digest()


def hash_signature(P: Point, R: Point, m: str) -> bytes:
    H = SHA256.new()
    H.update(long_to_bytes(P.x))
    H.update(long_to_bytes(P.y))
    H.update(long_to_bytes(R.x))
    H.update(long_to_bytes(R.y))
    H.update(m.encode())
    return H.digest()
