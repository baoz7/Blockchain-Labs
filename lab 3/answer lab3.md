### Lab 3.1 Answers

**Q1: Each extra leading zero multiplies expected work by how much? Why?**
Each extra leading zero multiplies the expected work by 16 times. This is because the hash is represented in hexadecimal (base-16). Each hex character has 16 possible values (0-9, a-f). To find a specific character (like '0'), the probability is 1/16, so it takes 16 attempts on average.

**Q2: Verifying your found nonce takes how many hash calls? What does this say about PoW?**
Verifying the found nonce takes exactly 1 hash call. This shows that Proof-of-Work is asymmetric: it is computationally expensive and difficult to solve (mine), but extremely fast and trivial for anyone else to verify.

### Lab 3.2 Answers

**Q3: For n=1,000,000 transactions, how many hashes does one proof contain?**
A Merkle proof scales logarithmically. For n=1,000,000 transactions, the tree height is log2(1,000,000) ≈ 20. Therefore, one proof contains about 20 hashes.

**Q4: Explain one real system that uses exactly this mechanism.**
Bitcoin uses this mechanism for SPV (Simplified Payment Verification) clients (light wallets). These wallets do not download the entire blockchain; they only download block headers. To verify a transaction, they request a Merkle proof from a full node, allowing them to mathematically prove a transaction is in a block using only ~20 hashes instead of downloading millions of transactions.

### Lab 3.3 Answers

**Task 1: Run twice with the same message - is the signature identical? Which RFC explains this?**
Yes, the signature is identical. Standard ECDSA usually produces different signatures due to a random nonce (k), but `eth-account` implements RFC 6979. This RFC makes ECDSA deterministic by generating the nonce `k` using a hash of the private key and the message, ensuring the exact same signature every time.

**Task 2: The tampered message recovers a different address. Explain why this proves integrity.**
The mathematical recovery function uses the signature AND the hash of the message to calculate the public key (address). If even one character in the message is changed, its hash completely changes due to the avalanche effect. When this new, wrong hash is fed into the recovery formula alongside the original signature, the math produces a completely different, random public key address. Since the recovered address doesn't match the sender's known address, we instantly know the message was tampered with.
