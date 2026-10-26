**Q1: Vì sao chainId cũng nằm trong mọi giao dịch được ký?**
ChainId được thêm vào quá trình ký giao dịch (theo EIP-155) nhằm mục đích chống lại tấn công phát lại (replay attack). Khóa bí mật ký ra một chuỗi byte gắn chặt với chainId của mạng TrustKeys L1 (11968), nên nếu ai đó lấy nguyên chữ ký này đem phát lại trên mạng khác (như Ethereum mainnet có chainId=1) thì hợp đồng thông minh hoặc các node sẽ báo chữ ký không hợp lệ do sai chainId.

**Q2: Giải thích vì sao base fee đứng ở đáy (cỡ vài wei) và gasUsedRatio ~2%.**
Theo quy tắc EIP-1559, mạng lưới nhắm mục tiêu (target) mỗi block dùng khoảng 15M gas (50% dung lượng tối đa 30M). Nếu gas thực dùng thấp hơn mức 50% này, thuật toán sẽ tự động giảm base fee đi tối đa 12.5% cho block tiếp theo. Vì mạng TrustKeys L1 hiện đang vắng (gasUsedRatio chỉ ~2%, cực kỳ thấp so với mốc 50%), base fee liên tục bị thuật toán đẩy xuống qua từng block cho đến khi chạm mức sàn (floor) là một vài wei.

**Q3: eth_feeHistory trả về baseFeePerGas có độ dài N+1 nhưng gasUsedRatio độ dài N. Phần tử dư là gì và ví dùng nó làm gì?**
Phần tử dư (thứ N+1) chính là dự phóng (dự đoán) baseFeePerGas cho block tiếp theo ngay trong tương lai, được tính toán dựa trên mức độ sử dụng gas của block mới nhất. Các phần mềm ví (như MetaMask) dùng chính giá trị dự phóng này làm cơ sở để tự động thiết lập thông số `maxFeePerGas` an toàn cho người dùng, đảm bảo giao dịch không bị kẹt khi mạng biến động.

**Q4: Nếu tăng max base fee trong MetaMask nhưng giữ nguyên priority fee, effectiveGasPrice có đổi không? Vì sao?**
Không đổi. effectiveGasPrice được tính bằng `baseFee + min(maxPriorityFee, maxFee - baseFee)`. Do `baseFee` của testnet hiện tại là quá nhỏ, việc bạn nâng trần giới hạn `maxFee` chỉ đơn thuần nâng ngưỡng chịu đựng tối đa của bạn lên, còn con số thực tế bạn phải trả vẫn là phần `baseFee` rẻ mạt đó cộng thêm cái `maxPriorityFee` (tiền tip) không hề thay đổi.

**Q5: Con số 21.000 gas từ đâu ra, và vì sao giao dịch thất bại vẫn tốn gas?**
21.000 gas là chi phí cơ sở (intrinsic cost) được hard-code sẵn trong giao thức EVM cho mọi giao dịch loại tiêu chuẩn. Đây là mức phí trả cho công sức của các node trong mạng lưới để xác minh chữ ký mã hóa (ECDSA) và cập nhật số dư. Giao dịch thất bại vẫn bị trừ gas vì các validator thực tế vẫn phải tốn tài nguyên máy tính (CPU/RAM) để chạy mã giao dịch của bạn cho đến thời điểm lệnh bị hoàn tác do lỗi.

**Q6: EVM dùng 4 byte selector để nhảy tới đúng hàm thế nào, và vì sao Etherscan cần ABI?**
Khi mã EVM thực thi, nó đọc 4 byte đầu tiên của Input Data và sử dụng một khối lệnh rẽ nhánh (dispatcher) bên trong bytecode của contract (giống như switch-case) để kiểm tra khớp mã rồi nhảy tới vị trí bộ nhớ chứa lệnh của hàm đó. Tuy nhiên EVM chỉ nhìn thấy toàn byte thô; Etherscan bắt buộc phải cần file ABI (như một quyển từ điển) để hiểu định dạng kiểu dữ liệu gốc (address, uint256...) nhằm dịch ngược đống byte thô đó thành các tham số mà con người đọc được.
