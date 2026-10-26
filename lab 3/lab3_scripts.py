import hashlib
import time
from eth_account import Account
from eth_account.messages import encode_defunct

print("--- LAB 3.1: HASH & PoW ---")
def mine(data: bytes, k: int):
    target = "0" * k
    nonce = 0
    t0 = time.time()
    while True:
        h = hashlib.sha256(data + str(nonce).encode()).hexdigest()
        if h.startswith(target):
            return nonce, time.time() - t0
        nonce += 1

for k in range(1, 6): # Reduced to 5 for speed, original is 7
    nonce, dt = mine(b"block#1|txroot=abc|", k)
    print(f"k={k} nonce={nonce:>9} time={dt:.3f}s")


print("\n--- LAB 3.3: DIGITAL SIGNATURES ---")
acct = Account.create()
print("address:", acct.address)

msg = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 3")
sig = Account.sign_message(msg, acct.key)
print("r,s,v:", hex(sig.r), hex(sig.s), sig.v)

who = Account.recover_message(msg, signature=sig.signature)
print("recovered:", who, " match:", who == acct.address)

bad = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 4")
try:
    tampered_who = Account.recover_message(bad, signature=sig.signature)
    print("tampered recovered ->", tampered_who)
except Exception as e:
    print("tampered error ->", e)