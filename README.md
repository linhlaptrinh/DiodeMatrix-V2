# DiodeMatrix — Structured Sensor Array

<p align="center">
  <img src="https://raw.githubusercontent.com/linhlaptrinh/DiodeMatrix-V2/main/meshes/demo.gif" alt="DiodeMatrix Project Demo" width="650"/>
</p>

## 📌 Giới thiệu dự án (About The Project)

**DiodeMatrix** là hệ thống phần cứng và phần mềm giúp Robot có được **"cảm giác xúc giác" (cảm giác sờ, chạm)** thông minh. 

Thay vì dùng các cảm biến lực đắt tiền, dự án này sử dụng một **mảng ma trận các điốt quang (Photodiode Matrix)**. Khi robot chạm vào bề mặt, sự thay đổi ánh sáng bên trong cấu trúc cảm biến sẽ được các điốt quang ghi lại, từ đó máy tính sẽ tính toán ra hình dáng, độ lún và lực tác động.

### 🔄 Quy trình hoạt động đơn giản (Workflow)
```text
Cảm biến bị nhấn → Điốt quang thay đổi tín hiệu → Máy tính xử lý số liệu → Robot nhận biết lực chạm

# Khởi tạo và kích hoạt môi trường ảo (Đã có sẵn trong thư mục dự án của bạn)
source cad_env/bin/activate

# Cài đặt các thư viện bổ trợ cần thiết
pip install numpy pandas scipy matplotlib pyserial
