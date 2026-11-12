#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quizchain 2 Blocks 1-77

Pipeline (identical after hashing for both algorithms):
    exact_input -> MD5/SHA-256 -> BIP39 entropy -> BIP39 seed
    -> BIP32 master -> m/44'/0'/0'/0/0 -> private key
    -> compressed public key -> WIF + P2PKH

MD5  = 16-byte entropy = 12 BIP39 words

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
    Block(number=1, algorithm='MD5', exact_input='U2 TOMI upside down L2e6gPSXnq7KJBfkoD7cHGVZuhRUDARJz2Cc9JcSNLsKRZhH552F'),
    Block(number=2, algorithm='MD5', exact_input='L5Z66qPmUkTAsWQywjRNHDxHrX6J1X1SQedp6V8QsbaXR7rGd6ex'),
    Block(number=3, algorithm='MD5', exact_input='reorg TOMI CZ Binance L2e6gPSXnq7KJBfkoD7cHGVZuhRUDARJz2Cc9JcSNLsKRZhH552F'),
    Block(number=4, algorithm='MD5', exact_input='MasK TOMI previous block private key'),
    Block(number=5, algorithm='MD5', exact_input='bat bot bit bet but'),
    Block(number=6, algorithm='MD5', exact_input='tray around small exercise news alarm'),
    Block(number=7, algorithm='MD5', exact_input='Grycoin TOMI angry Atbash hungry'),
    Block(number=8, algorithm='MD5', exact_input='correct horse battery staple correct horse battery staple L2gi9LjJwv6oRBdBAJMo3QTNmfdqLRYxbW7o1MhC5K7NNh2JqPSZ'),
    Block(number=9, algorithm='MD5', exact_input='K-9 TOMI police dog'),
    Block(number=10, algorithm='MD5', exact_input='ghost TOMI previous block mnemonic'),
    Block(number=11, algorithm='MD5', exact_input='  TOMI one space'),
    Block(number=12, algorithm='MD5', exact_input='grycoin TOMI coy ring anagram'),
    Block(number=13, algorithm='MD5', exact_input='Pizza TOMI Laszlo Hanyecz'),
    Block(number=14, algorithm='MD5', exact_input='A1zP1eP7DivfNa'),
    Block(number=15, algorithm='MD5', exact_input='TOMI'),
    Block(number=16, algorithm='MD5', exact_input='ELiZABETH TOMI dzGTuQeg2'),
    Block(number=17, algorithm='MD5', exact_input='LV TOMI Mona Lisa'),
    Block(number=18, algorithm='MD5', exact_input='6.25 TOMI Halvening'),
    Block(number=19, algorithm='MD5', exact_input='Cypherpunks'),
    Block(number=20, algorithm='MD5', exact_input='burn address'),
    Block(number=21, algorithm='MD5', exact_input='21 million TOMI fixed money supply'),
    Block(number=22, algorithm='MD5', exact_input='Bitcoin white paper'),
    Block(number=23, algorithm='MD5', exact_input='P TOMI Pretty Good Privacy'),
    Block(number=24, algorithm='MD5', exact_input='RPOW TOMI proof of work'),
    Block(number=25, algorithm='MD5', exact_input='77 + 25 TOMI total number of blocks'),
    Block(number=26, algorithm='MD5', exact_input='sweet honey strong lion TOMI Extremely unfair riddle'),
    Block(number=27, algorithm='MD5', exact_input='UTXO TOMI unspent transaction output'),
    Block(number=28, algorithm='MD5', exact_input='Running bitcoin TOMI obvious at first sight'),
    Block(number=29, algorithm='MD5', exact_input='Key TOMI Symphosius 4'),
    Block(number=30, algorithm='MD5', exact_input='EU IQ KO TOMI Atbash foldover'),
    Block(number=31, algorithm='MD5', exact_input='black ink marks TOMI Veronese riddle'),
    Block(number=32, algorithm='MD5', exact_input='Omnipotent TOMI block 22'),
    Block(number=33, algorithm='MD5', exact_input='0078 TOMI BIP 39 word list'),
    Block(number=34, algorithm='MD5', exact_input='HQ IP TOMI Atbash foldover two to the right'),
    Block(number=35, algorithm='MD5', exact_input='May 2020 TOMI Halvening 630000'),
    Block(number=36, algorithm='MD5', exact_input='bit TOMI debit orbit habit'),
    Block(number=37, algorithm='MD5', exact_input='Quizchain player TOMI Mine with your mind'),
    Block(number=38, algorithm='MD5', exact_input='ACE TOMI odd numbered alphabet letters'),
    Block(number=39, algorithm='MD5', exact_input='four five nine TOMI BIP 39 word list numbers'),
    Block(number=40, algorithm='MD5', exact_input='hodl TOMI hold'),
    Block(number=41, algorithm='MD5', exact_input='truth rarity TOMI 1FLAMEN6rq2BqMnkUmsJBqCGWdwgVKcegd'),
    Block(number=42, algorithm='MD5', exact_input='the solution to which will of course be "42" TOMI block 41'),
    Block(number=43, algorithm='MD5', exact_input='rather between TOMI block 42 mnemonic'),
    Block(number=44, algorithm='MD5', exact_input='good solution'),
    Block(number=45, algorithm='MD5', exact_input='a) TOMI timing of dropout'),
    Block(number=46, algorithm='MD5', exact_input='Andrew Yang TOMI 46th President of the United States'),
    Block(number=47, algorithm='MD5', exact_input='21 TOMI cross sum'),
    Block(number=48, algorithm='MD5', exact_input='Think different TOMI Apple slogan'),
    Block(number=49, algorithm='MD5', exact_input="Don't be evil TOMI Google slogan"),
    Block(number=59, algorithm='MD5', exact_input='4oLvT2 TOMI address checksum'),
    Block(number=51, algorithm='MD5', exact_input='51 percent attack'),
    Block(number=52, algorithm='MD5', exact_input='bat bat bot bit bet but'),
    Block(number=53, algorithm='MD5', exact_input='https://mobile.twitter.com/lopp/status/1143879778170232833'),
    Block(number=54, algorithm='MD5', exact_input='HAS TOMI HAL BIT Caesar'),
    Block(number=55, algorithm='MD5', exact_input='FOMO TOMI fear of missing out'),
    Block(number=56, algorithm='MD5', exact_input='Maybe you were just unlucky to have an exit node without reverse lookup.'),
    Block(number=57, algorithm='MD5', exact_input='https://mobile.twitter.com/halfin/status/1153096538'),
    Block(number=58, algorithm='MD5', exact_input='That means a lot coming from you, Hal.'),
    Block(number=59, algorithm='MD5', exact_input='ET TOMI Atbash foldover two to the right'),
    Block(number=60, algorithm='MD5', exact_input='Mayer Multiple'),
    Block(number=61, algorithm='MD5', exact_input='350 TOMI .org'),
    Block(number=62, algorithm='MD5', exact_input='Tanabata'),
    Block(number=63, algorithm='MD5', exact_input='I am omnipotent Aoi'),
    Block(number=64, algorithm='MD5', exact_input='QWERTY TOMI keyboard'),
    Block(number=65, algorithm='MD5', exact_input='layer TOMI Grycoin'),
    Block(number=66, algorithm='MD5', exact_input='A young woman of Japanese ancestry who is very smart and sincere.'),
    Block(number=67, algorithm='MD5', exact_input='Thomas TOMI Harold Thomas Finney II'),
    Block(number=68, algorithm='MD5', exact_input='Seveneves TOMI palindrome'),
    Block(number=69, algorithm='MD5', exact_input='madam TOMI palindrome'),
    Block(number=70, algorithm='MD5', exact_input='Victor/Victoria'),
    Block(number=71, algorithm='MD5', exact_input='net zero TOMI carbon neutral'),
    Block(number=72, algorithm='MD5', exact_input='GND TOMI Green New Deal'),
    Block(number=73, algorithm='MD5', exact_input='carbon budget TOMI Grycoin solution'),
    Block(number=74, algorithm='MD5', exact_input='PETM TOMI second time now'),
    Block(number=75, algorithm='MD5', exact_input='reverse Turing test'),
    Block(number=76, algorithm='MD5', exact_input='NO SOLUTION'), # NO SOLUTION
    Block(number=77, algorithm='MD5', exact_input='I thought I\'d write about the last four years, an eventful time for Bitcoin and me.\n\nfor those who don\'t know me, I\'m Hal Finney. I got my start in crypto working on an early version of PGP, working closely with Phil Zimmermann. When Phil decided to start PGP Corporation, I was one of the first hires. I would work on PGP until my retirement. At the same time, I got involved with the Cypherpunks. I ran the first cryptographically based anonymous remailer, among other activitieS.\n\nfast forward to late 2008 and the announcement of Bitcoin. I\'ve noticed that cryptographic graybeards (I was in my mid 50\'s) tend to get cynical. I was more idealistic; I have always loved crypto, the mystery and the paradox of iT.\n\nwhen Satoshi announced Bitcoin on the cryptography mailing list, he got a skeptical reception at best. Cryptographers have seen too many grand schemes by clueless noobs. They tend to have a knee jerk reactioN.\n\nI was more positive. I had long been interested in cryptographic payment schemes. Plus I was lucky enough to meet and extensively correspond with both Wei Dai and Nick Szabo, generally acknowledged to have created ideas that would be realized with Bitcoin. I had made an attempt to create my own proof of work based currency, called RPOW. So I found Bitcoin facinating.\n\nwhen Satoshi announced the first release of the software, I grabbed it right away. I think I was the first person besides Satoshi to run bitcoin. I mined block 70-something, and I was the recipient of the first bitcoin transaction, when Satoshi sent ten coins to me as a test. I carried on an email conversation with Satoshi over the next few days, mostly me reporting bugs and him fixing theM.\n\nToday, Satoshi\'s true identity has become a mystery. But at the time, I thought I was dealing with a young man of Japanese ancestry who was very smart and sincere. I\'ve had the good fortune to know many brilliant people over the course of my life, so I recognize the signs.\n\nAfter a few days, bitcoin was running pretty stably, so I left it running. Those were the days when difficulty was 1, and you could find blocks with a CPU, not even a GPU. I mined several blocks over the next days. But I turned it off because it made my computer run hot, and the fan noise bothered me. In retrospect, I wish I had kept it up longer, but on the other hand I was extraordinarily lucky to be there at the beginning. It\'s one of those glass half full half empty things.\n\nThe next I heard of Bitcoin was late 2010, when I was surprised to find that it was not only still going, bitcoins actually had monetary value. I dusted off my old wallet, and was relieved to discover that my bitcoins were still there. As the price climbed up to real money, I transferred the coins into an offline wallet, where hopefully they\'ll be worth something to my heirs.\n\nSpeaking of heirs, I got a surprise in 2009, when I was suddenly diagnosed with a fatal disease. I was in the best shape of my life at the start of that year, I\'d lost a lot of weight and taken up distance running. I\'d run several half marathons, and I was starting to train for a full marathon. I worked my way up to 20+ mile runs, and I thought I was all set. That\'s when everything went wrong.\n\nMy body began to fail. I slurred my speech, lost strength in my hands, and my legs were slow to recover. In August, 2009, I was given the diagnosis of ALS, also called Lou Gehrig\'s disease, after the famous baseball player who got it.\n\nALS is a disease that kills moter neurons, which carry signals from the brain to the muscles. It causes first weakness, then gradually increasing paralysis. It is usually fatal in 2 to 5 years. My symptoms were mild at first and I continued to work, but fatigue and voice problems forced me to retire in early 2011. Since then the disease has continued its inexorable progression.\n\nToday, I am essentially paralyzed. I am fed through a tube, and my breathing is assisted through another tube. I operate the computer using a commercial eyetracker system. It also has a speech synthesizer, so this is my voice now. I spend all day in my power wheelchair. I worked up an interface using an arduino so that I can adjust my wheelchair\'s position using my eyes.\n\nIt has been an adjustment, but my life is not too bad. I can still read, listen to music, and watch TV and movies. I recently discovered that I can even write code. It\'s very slow, probably 50 times slower than I was before. But I still love programming and it gives me goals. Currently I\'m working on something Mike Hearn suggested, using the security features of modern processors, designed to support "Trusted Computing", to harden Bitcoin wallets. It\'s almost ready to release. I just have to do the documentation.\n\nAnd of course the price gyrations of bitcoins are entertaining to me. I have skin in the game. But I came by my bitcoins through luck, with little credit to me. I lived through the crash of 2011. So I\'ve seen it before. Easy come, easy go.\n\nThat\'s my story. I\'m pretty lucky overall. Even with the ALS, my life is very satisfying. But my life expectancy is limited. Those discussions about inheriting your bitcoins are of more than academic interest. My bitcoins are stored in our safe deposit box, and my son and daughter are tech savvy. I think they\'re safe enough. I\'m comfortable with my legacy.\n[edited slightly]'),
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
