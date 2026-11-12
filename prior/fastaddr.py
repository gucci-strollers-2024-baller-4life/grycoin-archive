"""Fast md5-hex -> BIP39 -> m/44'/0'/0'/0/index address, coincurve + hashlib only."""
import hashlib, hmac, struct, sys
from coincurve import PublicKey
sys.path.insert(0,'harness'); import btc          # only for the 2048-word list
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
def b58check(p):
    chk = hashlib.sha256(hashlib.sha256(p).digest()).digest()[:4]
    n = int.from_bytes(p + chk, 'big'); s = ''
    while n: n, r = divmod(n, 58); s = B58[r] + s
    return '1' * (len(p + chk) - len((p + chk).lstrip(b'\0'))) + s
def _h160(b): return hashlib.new('ripemd160', hashlib.sha256(b).digest()).digest()
def _pub(k): return PublicKey.from_valid_secret(k.to_bytes(32,'big')).format(compressed=True)
def address(md5hex, idx=0):
    mn = btc.entropy_to_mnemonic(bytes.fromhex(md5hex))
    seed = hashlib.pbkdf2_hmac('sha512', mn.encode(), b'mnemonic', 2048, 64)
    I = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    k, c = int.from_bytes(I[:32],'big') % N, I[32:]
    for i in (44, 0, 0):
        I = hmac.new(c, b'\x00' + k.to_bytes(32,'big') + struct.pack('>I', i | 0x80000000), hashlib.sha512).digest()
        k, c = (int.from_bytes(I[:32],'big') + k) % N, I[32:]
    I = hmac.new(c, _pub(k) + struct.pack('>I', 0), hashlib.sha512).digest()
    k = (int.from_bytes(I[:32],'big') + k) % N; c = I[32:]
    I = hmac.new(c, _pub(k) + struct.pack('>I', idx), hashlib.sha512).digest()
    k = (int.from_bytes(I[:32],'big') + k) % N
    return b58check(b'\x00' + _h160(_pub(k)))
if __name__ == '__main__':
    import time
    print('calibration:', address('9dd2efb9bc976c2095bd534d7b8d431c'), '(want 19TbyN5KCg1Lg7qHwezifsLVcdSa2Rj5KN)')
    t=time.time()
    for i in range(200): address('%032x' % i)
    print('rate: %.2f ms/derivation' % ((time.time()-t)/200*1000))
