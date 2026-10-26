### Task 4.1: Real Proof-of-Work

**Q1: The target has roughly how many leading zero hex digits? How many bits of work does one valid header represent (~2^?)?**
The target has roughly 19 leading zero hex digits (e.g., target = 0x034219 \* 256^(0x17-3) = 000000000000000000034219...). Because each hex digit represents 4 bits, 19 leading zeros equals 76 leading zero bits. Therefore, finding a valid header represents roughly ~2^76 hash operations (bits of work).

**Q2: Verifying the PoW took your laptop 2 hash calls. Finding it took the network ~10 minutes at ~10^20 H/s. What property of SHA-256 creates this asymmetry?**
This asymmetry is created by the **pre-image resistance** (one-way property) of SHA-256. It is computationally infeasible to reverse the function to find the right input (nonce) to produce the required number of leading zeros, forcing the network to brute-force trial and error. However, verifying the answer takes only a single forward execution (double SHA-256 = 2 calls) to prove it is mathematically correct.

### Task 4.2: Transaction anatomy & fee rate

**Q3: This tx paid ~3,600,000 sat/vB (≈ 6.73 BTC fee for 187 vB!). Look at the date. What was happening, and what does it teach about how fees are set?**
This block (#840,000) was the 4th Bitcoin halving block on April 20, 2024, which exactly coincided with the launch of the Runes protocol. Users were desperately bidding up transaction fees to secure block space to mint new tokens on the very first halving block. This teaches us that Bitcoin fees are entirely determined by a free-market blind auction for block space, not by the amount of Bitcoin being sent.

**Q4: The coinbase outputs total 4,075,061,499 sat. Subsidy is 312,500,000 sat. Where does the difference come from?**
The difference comes from the transaction fees paid by all the users who included their transactions in this block. The miner who mines the block gets to claim the newly created Bitcoin (the block subsidy) PLUS all the transaction fees combined into the coinbase transaction.

### Task 4.3: Merkle Root

**Q5: Your computed root matches the header exactly. Explain in 2-3 sentences what this proves about the block's transaction list, citing the hash property involved.**
This proves that the block's transaction list has not been tampered with and is exactly in the same order as when it was mined. Because of the **avalanche effect** and **collision resistance** properties of cryptographic hashes, changing even a single byte of one transaction or swapping their order would completely change the resulting Merkle root, making it no longer match the block header.
