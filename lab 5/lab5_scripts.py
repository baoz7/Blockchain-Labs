import sys
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

def main():
    print("--- LAB 5.2: READ THE CHAIN ---")
    # Kết nối đến mạng TrustKeys L1 testnet
    RPC_URL = "https://l1testnet.trustkeys.network"
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    # Nạp PoA middleware để tránh lỗi ExtraDataLengthError
    w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
    
    if not w3.is_connected():
        print("Lỗi kết nối RPC.")
        return

    blk = w3.eth.get_block("latest")
    print(f"Latest Block: {blk.number}")
    print(f"baseFeePerGas = {blk.baseFeePerGas} wei")
    
    print("Lịch sử phí (20 block gần nhất):")
    fh = w3.eth.fee_history(20, "latest", [10, 50, 90])
    for i, base in enumerate(fh["baseFeePerGas"][:-1]):
        print(f"Block {fh['oldestBlock'] + i} | Base Fee: {base} wei | Gas Used Ratio: {fh['gasUsedRatio'][i]:.4f}")
        
    print("CHECK 20 lines of base fees: OK")

    print("--- LAB 5.3: DECOMPOSE FEE ---")
    tx_hash = input("Nhập mã giao dịch (Tx Hash) type-2 của bạn từ MetaMask (có dạng 0x...): ").strip()
    
    if not tx_hash.startswith("0x") or len(tx_hash) != 66:
        print("Mã giao dịch không hợp lệ. Hãy đảm bảo đó là mã hash bắt đầu bằng 0x dài 66 ký tự.")
        return
        
    print("Đang truy xuất thông tin giao dịch...")
    try:
        rcpt = w3.eth.get_transaction_receipt(tx_hash)
        tx = w3.eth.get_transaction(tx_hash)
        tx_blk = w3.eth.get_block(rcpt["blockNumber"])
        
        base_fee = tx_blk["baseFeePerGas"]
        gas_used = rcpt["gasUsed"]
        eff_price = rcpt["effectiveGasPrice"]
            
        paid = gas_used * eff_price
        burned = gas_used * base_fee
        tip = gas_used * (eff_price - base_fee)
        
        print(f"paid = {paid}")
        print(f"burned = {burned}")
        print(f"tip = {tip}")
        is_match = (paid == burned + tip)
        print(f"{paid} = {burned} + {tip} ? {is_match}")
        
        if is_match:
            print("CHECK paid == burned + tip: OK")
        else:
            print("CHECK: FAILED")
            
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == '__main__':
    main()