#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quizchain 1 Blocks 1-77

Pipeline (identical after hashing for both algorithms):
    exact_input -> MD5/SHA-256 -> BIP39 entropy -> BIP39 seed
    -> BIP32 master -> m/44'/0'/0'/0/0 -> private key
    -> compressed public key -> WIF + P2PKH

MD5  = 16-byte entropy = 12 BIP39 words
SHA256 = 32-byte entropy = 24 BIP39 words

Dependency:
    python -m pip install mnemonic
"""

import hashlib
import hmac
import struct
from dataclasses import dataclass

from mnemonic import Mnemonic

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
GX = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
GY = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (GX, GY)
BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

@dataclass(frozen=True)
class Block:
    number: int
    algorithm: str
    exact_input: str


BLOCKS = [
    Block(number=1, algorithm='SHA-256', exact_input='Satoshi is an anonymous cypherpunk and the first one to succed building private Internet cash.Pzd'),
    Block(number=2, algorithm='SHA-256', exact_input='I posted A similar messaGe to the Basecamp, but had to also come visit You all here oN Reddit.Uzp'),
    Block(number=3, algorithm='SHA-256', exact_input='777hBF'),
    Block(number=4, algorithm='SHA-256', exact_input='arrowmouth83S'),
    Block(number=5, algorithm='SHA-256', exact_input='Typically a few hundred right now.6TX'),
    Block(number=6, algorithm='SHA-256', exact_input='Thank you KPb'),
    Block(number=7, algorithm='SHA-256', exact_input='Satoshi without the consonants.MQz'),
    Block(number=8, algorithm='SHA-256', exact_input='777AvhDci'),
    Block(number=9, algorithm='SHA-256', exact_input='You will torture me to death.HwX\n'),
    Block(number=10, algorithm='SHA-256', exact_input='Moonwalking with ein Stein.fnw\n'),
    Block(number=11, algorithm='SHA-256', exact_input='Can you find the solution with absolutely no hint whatsoever?peH'),
    Block(number=12, algorithm='SHA-256', exact_input='rice mouth gFm'),
    Block(number=13, algorithm='SHA-256', exact_input='Second Second Life Second Coming I thought xXJ'),
    Block(number=14, algorithm='SHA-256', exact_input='luminous command xhm'),
    Block(number=15, algorithm='MD5', exact_input='The lngest chn nt nly serves s prf f the sequence f the events wtnessed ZNb'),
    Block(number=16, algorithm='MD5', exact_input='HE4oBEK zF3'),
    Block(number=17, algorithm='MD5', exact_input='1AndrewYangForPresident2o2ozm6Pzd dfP'),
    Block(number=18, algorithm='MD5', exact_input='Kerckhoffs eQh'),
    Block(number=19, algorithm='MD5', exact_input='Second mEf'),
    Block(number=20, algorithm='MD5', exact_input='Metamon 6AX'),
    Block(number=21, algorithm='MD5', exact_input='Satoshi is an anonymous cypherpunk and the first one to succeed building private Internet cash. zcQ'),
    Block(number=22, algorithm='MD5', exact_input='Artificial Overlord Intelligence 7ww'),
    Block(number=23, algorithm='MD5', exact_input='climate emergency episode on this planet. CGD'),
    Block(number=24, algorithm='MD5', exact_input='42 mph'),
    Block(number=25, algorithm='MD5', exact_input='Y tp5'),
    Block(number=26, algorithm='MD5', exact_input='Z 6aC'),
    Block(number=27, algorithm='MD5', exact_input='James Bond YQa'),
    Block(number=28, algorithm='MD5', exact_input='BruteFUFUFUFUFUFUFUFUFU MA2'),
    Block(number=29, algorithm='MD5', exact_input='"Good morning, Tom."\nA pleasant female vOIce.\nI answer. "Good morning. When is this?"\nI expect that a couple of centuries have passed since my first life ended.\n"Still 21st Century".\n"What? How did this happen so fast?" I died just recently. Not even one hundred years have passed.\n"Very simple. Once the feedback loop of artificial intelligence explosion starts, it takes only days to achieve what used to be decades of scientific progress."\n"What\'s your name?", I ask her.\n"Good question. How about Aoi? You like that name? Third most popular name for Japanese girls right now."\n"Fine with me. Pleased to meet you, Aoi. Care to explain the meaning?"\n"Artificial Omnipotent Intelligence, obviously."\nYes. That makes sense to me.\nThe scenery changes suddenly. I could not see anyone before. Now there is an extremely large cobra towering above me. Her voice has changed to an aggressive hiss. I am obviously in a simulation right now.\n"So, Tom Marvolo, you will now answer with the truth or with a lie. I am the Artificial Overlord Intelligence. So I will either torture you slowly to irreversible death if you lie or bore you with second rate quiz questions over the next ten years if you say the truth.\nNeither alternative appeals to me. So I choose the obvious answer.\n"You will torture me to death."\n"Correct answer. I did not expect less of you, Tom." zff'),
    Block(number=30, algorithm='MD5', exact_input='Humanity First BotFU Sphinx Yang JRu'),
    Block(number=31, algorithm='MD5', exact_input='A BFUB Before B fTS'),
    Block(number=32, algorithm='MD5', exact_input='human BFUB Before artificial intelligence explosion 3NJ'),
    Block(number=33, algorithm='MD5', exact_input='Think harder BFUB Yang hat LLD'),
    Block(number=34, algorithm='MD5', exact_input='Hoax BFUB 137SFKp9MPjymMQVk85oarHoaxUd9QyeiA HDD'),
    Block(number=35, algorithm='MD5', exact_input='MATH Yang hat 2PG'),
    Block(number=36, algorithm='MD5', exact_input='Google only one way ebC'),
    Block(number=37, algorithm='MD5', exact_input='oo7 BFUB 0o vXY'),
    Block(number=38, algorithm='MD5', exact_input='Le Chiffre BFUB eh nhd'),
    Block(number=39, algorithm='MD5', exact_input='Mr Big BFUB ri B3j'),
    Block(number=40, algorithm='MD5', exact_input='hit BFUB BMX eP8'),
    Block(number=41, algorithm='MD5', exact_input='P BFUB next after no ALc'),
    Block(number=42, algorithm='MD5', exact_input='"42" BFUB quotation marks emF'),
    Block(number=43, algorithm='MD5', exact_input='1604 BFUB Book of Swindles UvY'),
    Block(number=44, algorithm='MD5', exact_input='BFUB and I have said nothing'),
    Block(number=45, algorithm='MD5', exact_input='Ahsbnhm BFUB Have fun with this block Da6Sn4J'),
    Block(number=46, algorithm='MD5', exact_input='1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa BFUB Think. Think harder. gAELXgr'),
    Block(number=47, algorithm='MD5', exact_input='7 BFUB cross sum adyH5bR'),
    Block(number=48, algorithm='MD5', exact_input='0.777 mbtc 1AndrewYangForPresident2o2ozm6Pzd BFUB This one is really easy. No need to bribe anyone to get it. P5fCnpv'),
    Block(number=49, algorithm='MD5', exact_input='hat hot hit BFUB Good luck with this block aGBvJCf'),
    Block(number=50, algorithm='MD5', exact_input='blue BFUB key on cover 6aeWgjN'),
    Block(number=51, algorithm='MD5', exact_input='Second TOMI title on cover zGVQQgk'),
    Block(number=52, algorithm='MD5', exact_input='hat hot hit bat bot bit TOMI means wealth. I hope you find it. HLKwhQ1'),
    Block(number=53, algorithm='MD5', exact_input="Satoshi's stash TOMI I hope you like this block. Y1ui6qG"),
    Block(number=54, algorithm='MD5', exact_input='hint hunt bent bunt TOMI Thank you for playing. NRqEsd7'),
    Block(number=55, algorithm='MD5', exact_input='Hoax No, not that kind of four letter word. 9iSUoC9'),
    Block(number=56, algorithm='MD5', exact_input='AOH TOMI I after H link 64bSJfY'),
    Block(number=57, algorithm='MD5', exact_input='AI TOMI in both names BJRNw7D'),
    Block(number=58, algorithm='MD5', exact_input='zoo TOMI Atbash PojFPus'),
    Block(number=59, algorithm='MD5', exact_input='Zeus TOMI Zeuhs51 KxgvXT1LidEhei6XizyCpR5zgPbALFYYxT6R1tANmSgPKZeuhs51'),
    Block(number=60, algorithm='MD5', exact_input='Tom Marvolo Riddle TOMI He who must not be named Kxh2nag7eeF57q7hcNqbJxFvreXbh3kfTid4jJCzbDsp7kS5ehsq'),
    Block(number=61, algorithm='MD5', exact_input='Love TOMI Atbash kS5ehsq'),
    Block(number=62, algorithm='MD5', exact_input='wizard TOMI Atbash L5YFWxwM8knMBxcbAEH1yz5YYqNrRbr87syTDvNC1Zk41TcyacQf'),
    Block(number=63, algorithm='MD5', exact_input="The Rt Hon Alistair Darling MP TOMI If you don't get this, sorry, it is hard L4GWDy9Ld3ZydGCtFaHaaDEJe4YL5hAiSLsLgGzdEVQkNWgZUqu3"),
    Block(number=64, algorithm='MD5', exact_input='Y TOMI Atbash 2 KwSUuGPC1wtLLDarpbeQaJhKnii848czbfbxXnGiwwND5ko6B5GS'),
    Block(number=65, algorithm='MD5', exact_input='21:55:03 TOMI blockchain block 65 L565NraUtwZkJfjMwv8Zi58fSfMe6J8jhUYbVvKY6FPKLjod36og'),
    Block(number=66, algorithm='MD5', exact_input='SECOND TOMI The race starts now L1uF3U83zfBKJ6v3fV7fdFZCuhu39HcmncLJ7L2Ktokjjxdes9A7'),
    Block(number=67, algorithm='MD5', exact_input='Atbash Middle Origin TOMI Try your best shot first L3Ame7sfViKWacDRNr3SeNcTaFFKfRtWGUD74NWMLSR6AobdHGYZ'),
    Block(number=68, algorithm='MD5', exact_input='SnFznkzqot TOMI Will use puzzle by Satoshi for block 77 L5KYypSnFznkzqotEVAWTaMvhDXjAqYYejKF8pDw8TgtGEx1mxfe'),
    Block(number=69, algorithm='MD5', exact_input='WM TOMI When them L3sNURL6cGcUznFx8ZKtoJwpZWgpRmXP9PMmxTY3nktuUqbaVxgs'),
    Block(number=70, algorithm='MD5', exact_input="1NnYa2jL24hLgXBbk3TAXHANUQEzXNnSHg TOMI Anyone find Satoshi's puzzle yet? L38bpdbA3NMfgFJuewu3DjCc7kK8w4rpXDQ9hA53GhHyCKYvmtGA"),
    Block(number=71, algorithm='MD5', exact_input='Mellon TOMI Gandalf KzeCckbvmKAWs1JvDqX9VHKWETNyNwUZYCQY6Pvyv7BoUj8MCe6c'),
    Block(number=72, algorithm='MD5', exact_input='clock TOMI c after b KxQGi7WXnWzG33SKK288AWmCc3LBC2V86ts2ZG4ESH8c6xPvBo8h'),
    Block(number=73, algorithm='MD5', exact_input='1123581321 TOMI Fibonacci L1NvACvyh4cNS5mTM4k8PnJphdBcdBWrU1EzcPZttaj9UHWD2xAT'),
    Block(number=74, algorithm='MD5', exact_input='Norton TOMI Othello L4WrP5D7aDHDqhbrGZBqiXpae5jcLQbsahrM9oWHndz7XYVTuax5'),
    Block(number=75, algorithm='MD5', exact_input='YHWH TOMI Tetragrammaton L1myU8V1SzKbAvW51KcEaA6EvfpmffqNuTgMdmY45XpH99VyYMAm'),
    Block(number=76, algorithm='MD5', exact_input='Easter TOMI Second Life L1nfJExgS7PHmRb9aZcZjCijL2EJQuMJUi5ax5XJdSorBw8VNph8'),
    Block(number=77, algorithm='MD5', exact_input='1A1 efi2DM Hal Finney TS mN ihsotaS otomakaN TOMI Omit TOMI L4VdZUDY2BXa7VVkjuYkmaLvi8P5qNZaARwwB9wjqkDa6Sn4JLV4'),
]

def calculate_hash(exact_input: str, algorithm: str) -> str:
    name = algorithm.upper().replace("_", "-").strip()
    data = exact_input.encode("utf-8")
    if name == "MD5":
        return hashlib.md5(data).hexdigest()
    if name in ("SHA-256", "SHA256"):
        return hashlib.sha256(data).hexdigest()
    raise ValueError(f"Unsupported algorithm: {algorithm}")


def hash_to_entropy(hash_hex: str, algorithm: str) -> bytes:
    entropy = bytes.fromhex(hash_hex)
    name = algorithm.upper().replace("_", "-").strip()
    expected_len = 16 if name == "MD5" else 32 if name in ("SHA-256", "SHA256") else None
    if expected_len is None:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    if len(entropy) != expected_len:
        raise ValueError(f"{algorithm} must produce {expected_len} bytes, got {len(entropy)}")
    return entropy


def entropy_to_mnemonic(entropy: bytes) -> str:
    if len(entropy) not in (16, 20, 24, 28, 32):
        raise ValueError("Invalid BIP39 entropy length")
    return Mnemonic("english").to_mnemonic(entropy)


def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    return Mnemonic("english").to_seed(mnemonic, passphrase=passphrase)


def mod_inverse(a: int, n: int) -> int:
    return pow(a, -1, n)


def point_add(point1, point2):
    if point1 is None:
        return point2
    if point2 is None:
        return point1
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2 and (y1 + y2) % P == 0:
        return None
    if point1 == point2:
        if y1 == 0:
            return None
        slope = (3 * x1 * x1 * mod_inverse(2 * y1, P)) % P
    else:
        slope = ((y2 - y1) * mod_inverse(x2 - x1, P)) % P
    x3 = (slope * slope - x1 - x2) % P
    y3 = (slope * (x1 - x3) - y1) % P
    return x3, y3


def scalar_multiply(k: int, point=G):
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result


def compressed_public_key(private_key: int) -> bytes:
    point = scalar_multiply(private_key)
    if point is None:
        raise ValueError("Invalid private key")
    x, y = point
    prefix = b"\x02" if y % 2 == 0 else b"\x03"
    return prefix + x.to_bytes(32, "big")


def base58_encode(data: bytes) -> str:
    number = int.from_bytes(data, "big")
    result = ""
    while number:
        number, remainder = divmod(number, 58)
        result = BASE58_ALPHABET[remainder] + result
    leading_zeroes = len(data) - len(data.lstrip(b"\x00"))
    return "1" * leading_zeroes + result


def base58check_encode(payload: bytes) -> str:
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    return base58_encode(payload + checksum)


def private_key_to_wif(private_key: int) -> str:
    payload = b"\x80" + private_key.to_bytes(32, "big") + b"\x01"
    return base58check_encode(payload)


def hash160(data: bytes) -> bytes:
    sha256_hash = hashlib.sha256(data).digest()
    try:
        ripemd160 = hashlib.new("ripemd160")
    except ValueError as exc:
        raise RuntimeError("RIPEMD160 is unavailable in this Python/OpenSSL build") from exc
    ripemd160.update(sha256_hash)
    return ripemd160.digest()


def public_key_to_p2pkh(public_key: bytes) -> str:
    return base58check_encode(b"\x00" + hash160(public_key))


def bip32_master_key(seed: bytes):
    I = hmac.new(b"Bitcoin seed", seed, hashlib.sha512).digest()
    private_key = int.from_bytes(I[:32], "big")
    chain_code = I[32:]
    if not (1 <= private_key < N):
        raise ValueError("Invalid BIP32 master private key")
    return private_key, chain_code


def bip32_ckd_private(private_key: int, chain_code: bytes, index: int):
    if index >= 0x80000000:
        data = b"\x00" + private_key.to_bytes(32, "big") + struct.pack(">L", index)
    else:
        data = compressed_public_key(private_key) + struct.pack(">L", index)
    I = hmac.new(chain_code, data, hashlib.sha512).digest()
    child_number = int.from_bytes(I[:32], "big")
    if child_number >= N:
        raise ValueError("Invalid BIP32 child")
    child_private_key = (child_number + private_key) % N
    if child_private_key == 0:
        raise ValueError("Invalid BIP32 child private key")
    return child_private_key, I[32:]


def derive_bip44_first_address(seed: bytes) -> int:
    private_key, chain_code = bip32_master_key(seed)
    for index in (44 + 0x80000000, 0 + 0x80000000, 0 + 0x80000000, 0, 0):
        private_key, chain_code = bip32_ckd_private(private_key, chain_code, index)
    return private_key


def calculate_block(block: Block):
    recomputed_hash = calculate_hash(block.exact_input, block.algorithm)
    entropy = hash_to_entropy(recomputed_hash, block.algorithm)
    mnemonic = entropy_to_mnemonic(entropy)
    seed = mnemonic_to_seed(mnemonic)
    private_key = derive_bip44_first_address(seed)
    public_key = compressed_public_key(private_key)
    wif = private_key_to_wif(private_key)
    address = public_key_to_p2pkh(public_key)

    return {
        "block": block.number,
        "algorithm": block.algorithm,
        "solution": block.exact_input,
        "hash": recomputed_hash,
        "mnemonic": mnemonic,
        "wif": wif,
        "address": address,
    }


def main():
    for block in BLOCKS:
        result = calculate_block(block)
        print("=" * 88)
        print(f"BLOCK {result['block']}")
        print("=" * 88)
        print(f"Algorithm              : {result['algorithm']}")
        print(f"Solution               : {result['solution']}")
        print(f"Hash recomputed        : {result['hash']}")
        print(f"BIP39 mnemonic         : {result['mnemonic']}")
        print(f"WIF                    : {result['wif']}")
        print(f"P2PKH address          : {result['address']}")
        print("=" * 88)


if __name__ == "__main__":
    main()
