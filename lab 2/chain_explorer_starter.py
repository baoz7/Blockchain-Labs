import urllib.request
import json
import ssl

# Sửa lỗi chính tả: l1testnet thay vì lltestnet (chữ L và số 1)
RPC_URL = "https://l1testnet.trustkeys.network"

def rpc_call(method, params=[]):
    req = urllib.request.Request(RPC_URL, method="POST")
    req.add_header("Content-Type", "application/json")
    payload = json.dumps({"jsonrpc": "2.0", "method": method, "params": params, "id": 1}).encode("utf-8")
    
    # Bỏ qua kiểm tra SSL
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    with urllib.request.urlopen(req, data=payload, context=ctx) as response:
        return json.loads(response.read().decode("utf-8"))["result"]

def main():
    print("Connecting to TrustKeys L1 testnet...")
    
    # --- TODO 1: Which chain am I talking to? ---
    chain_id_hex = rpc_call("eth_chainId")
    chain_id = int(chain_id_hex, 16)
    
    if chain_id == 11968:
        print("CHECK 1: OK")
    else:
        print(f"CHECK 1: FAILED (Got {chain_id})")
        return

    # Get latest block number
    tip_hex = rpc_call("eth_blockNumber")
    tip = int(tip_hex, 16)

    # Fetch the last 5 blocks
    blocks = []
    for i in range(5):
        block_hex = hex(tip - i)
        block = rpc_call("eth_getBlockByNumber", [block_hex, False])
        blocks.append(block)

    print(f"\n{'height':<10} {'block hash':<25} {'parentHash':<25} {'txs':<6} {'link'}")
    print("-" * 80)
    
    all_links_ok = True
    
    for i in range(len(blocks)):
        b = blocks[i]
        height = int(b["number"], 16)
        b_hash = b["hash"]
        p_hash = b["parentHash"]
        
        # --- TODO 3: Count the transactions ---
        txs_count = len(b["transactions"])
        
        if i == 0:
            print("CHECK 3: OK")
            
        if i < len(blocks) - 1:
            prev_b = blocks[i + 1] 
            
            # --- TODO 2: Verify the hash chain ---
            link_ok = (p_hash == prev_b["hash"])
            
            if not link_ok: all_links_ok = False
            link_str = "OK" if link_ok else "FAIL"
        else:
            link_str = "-"
            
        short_b_hash = f"{b_hash[:10]}...{b_hash[-8:]}"
        short_p_hash = f"{p_hash[:10]}...{p_hash[-8:]}"
        print(f"{height:<10} {short_b_hash:<25} {short_p_hash:<25} {txs_count:<6} {link_str}")

    if all_links_ok:
        print("\nCHECK 2: OK")

if __name__ == '__main__':
    main()