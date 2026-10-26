import hashlib

def hash_node(left: bytes, right: bytes) -> bytes:
    return hashlib.sha256(left + right).digest()

def merkle_root(leaves: list[bytes]) -> bytes:
    if not leaves: return b""
    layer = leaves
    while len(layer) > 1:
        next_layer = []
        for i in range(0, len(layer), 2):
            left = layer[i]
            # Duplicate the last node if the level has an odd length
            right = layer[i+1] if i+1 < len(layer) else layer[i]
            next_layer.append(hash_node(left, right))
        layer = next_layer
    return layer[0]

def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    proof = []
    layer = leaves
    curr_idx = index
    
    while len(layer) > 1:
        is_left_node = (curr_idx % 2 == 0)
        
        if is_left_node:
            sibling_idx = curr_idx + 1
            if sibling_idx < len(layer):
                sibling = layer[sibling_idx]
            else:
                sibling = layer[curr_idx] # Duplicate if odd
            proof.append((sibling, False)) # Sibling is on the right
        else:
            sibling_idx = curr_idx - 1
            sibling = layer[sibling_idx]
            proof.append((sibling, True)) # Sibling is on the left
            
        # Move up to the next layer
        next_layer = []
        for i in range(0, len(layer), 2):
            l = layer[i]
            r = layer[i+1] if i+1 < len(layer) else layer[i]
            next_layer.append(hash_node(l, r))
        
        layer = next_layer
        curr_idx //= 2
        
    return proof

def verify_proof(leaf_hash: bytes, proof: list[tuple[bytes, bool]], root: bytes) -> bool:
    curr = leaf_hash
    for sibling_hash, is_left_sibling in proof:
        if is_left_sibling:
            curr = hash_node(sibling_hash, curr)
        else:
            curr = hash_node(curr, sibling_hash)
    return curr == root

def main():
    print("Testing Merkle Tree...")
    # Dummy data
    leaves = [hashlib.sha256(f"tx{i}".encode()).digest() for i in range(5)]
    
    root = merkle_root(leaves)
    print("Root:", root.hex())
    
    # Test valid proof
    for i in range(len(leaves)):
        proof = merkle_proof(leaves, i)
        is_valid = verify_proof(leaves[i], proof, root)
        if is_valid:
            print(f"CHECK leaf {i}: OK")
        else:
            print(f"CHECK leaf {i}: FAILED")
            
    # Test invalid proof
    bad_leaf = hashlib.sha256(b"fake_tx").digest()
    proof = merkle_proof(leaves, 0)
    if not verify_proof(bad_leaf, proof, root):
        print("CHECK tamper: OK")

if __name__ == '__main__':
    main()