# Quy Chuẩn Biên Tập Câu Tiếng Việt — Reverse: 1999 VI

Áp dụng cho toàn bộ văn bản hội thoại và cốt truyện của Reverse: 1999 nhằm đảm bảo tiếng Việt tự nhiên, thoát khỏi cấu trúc dịch máy thô cứng nhưng tuyệt đối giữ nguyên ý nghĩa gốc.

---

## 1. Cấu Trúc Câu và Chủ Thể

* **Lược bỏ đại từ lặp:** Tiếng Anh thường xuyên lặp lại "I, you, he, she, they". Tiếng Việt tự nhiên cho phép lược bỏ chủ ngữ trong các câu đáp ngắn hoặc chuỗi hành động liên tục khi ngữ cảnh đã hoàn toàn rõ ràng ai đang làm gì.
* **Trật tự tự nhiên:** Sắp xếp lại trật tự trạng ngữ, định ngữ theo văn phong tiếng Việt mạch lạc (Thời gian $\rightarrow$ Không gian $\rightarrow$ Chủ thể $\rightarrow$ Hành động).
* **Tránh danh từ hóa gượng ép:** Hạn chế các cụm "việc thực hiện", "sự tiến hành", "quá trình bắt đầu". Thay thế bằng động từ trực tiếp ("làm", "tiến hành", "bắt đầu").
* **Xử lý bị động:** Tiếng Anh dùng thể bị động (passive voice) rất nhiều. Trong tiếng Việt, chỉ dùng "bị" (nếu mang ý tiêu cực, thiệt hại) hoặc "được" (nếu mang ý tích cực, hưởng lợi), hoặc chuyển câu sang chủ động nếu phù hợp ngữ cảnh.

---

## 2. Bảo Toàn Thẻ Kỹ Thuật (Tags & RichText Invariants)

Game Unity sử dụng rất nhiều thẻ định dạng rich text và token thay thế biến:
* Thẻ màu sắc: `<color=#ff0000>...</color>`
* Thẻ kích thước: `<size=24>...</size>`
* Thẻ in đậm/nghiêng: `<b>...</b>`, `<i>...</i>`
* Ký tự xuống dòng: `\n`
* Biến số / tên người chơi: `{0}`, `{player_name}`, `#role#`

**Quy tắc:** Bắt buộc bảo toàn 100% các thẻ và biến, không làm gãy cặp đóng/mở thẻ. Chuỗi tiếng Việt phải chuẩn mã Unicode NFC.
