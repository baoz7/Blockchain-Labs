1. Yes, the parentHash of the tip block equals the hash of the block just below it.
   - Tip block parentHash: [Copy the parentHash from the VERY TOP row of the table]
   - Previous block hash: [Copy the block hash from the SECOND row of the table]

2. If a byte inside block #(tip-2) is secretly changed, the hash of block #(tip-2) will completely change. Because of this, the parentHash field in block #(tip-1) will stop matching. Honest nodes will detect this mismatch, reject the altered block, and refuse to build on it.

3. The block 3 rows above the bottom currently has [Subtract the block height of the 4th row down from the very top row's height] confirmations.

4. The 97-byte extraData hints at a Proof-of-Authority (PoA) consensus family. It differs from Bitcoin's Proof-of-Work (PoW) because PoA relies on trusted validators digitally signing blocks rather than miners using computing power to solve cryptographic puzzles.
