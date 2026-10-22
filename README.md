# THỰC HÀNH PYTHON VỚI GIAO THỨC CoAP

### Thành viên nhóm:
1. **Nguyễn Văn Hưởng** - B23DCCN378
2. **Lê Doãn Trung** - B23DCCN854
3. **Lê Quỳnh Anh** - B23DCCN028

---

## 1. Môi trường và Cấu hình

| Mục | Giá trị |
|---|---|
| Giao thức | CoAP (Constrained Application Protocol, RFC 7252 / UDP) |
| Cổng mặc định | `5683` (UDP) |
| Địa chỉ Server | `127.0.0.1` (`localhost`) |
| Ngôn ngữ & Thư viện | Python 3.x, `aiocoap` |

Cài đặt thư viện:
```bash
pip install aiocoap
```

---

## 2. Danh mục tài nguyên CoAP

| Bài | Tên tài nguyên | URI | Phương thức | Mô tả |
|---|---|---|---|---|
| **Bài 1** | Message | `coap://127.0.0.1:5683/iot/lab/message` | GET, POST | Gửi và nhận lời chào / thông tin sinh viên |
| **Bài 2** | Sensor Data | `coap://127.0.0.1:5683/iot/lab/sensor01/data` | GET | Trả về JSON nhiệt độ và độ ẩm cập nhật mỗi 3s |
| **Bài 3** | Light Status | `coap://127.0.0.1:5683/iot/lab/light01/status` | GET, PUT, Observe | Điều khiển ON/OFF và tự động đẩy trạng thái |

---

## 3. Hướng dẫn chạy và Kết quả kiểm thử

> **Nguyên tắc:** Luôn khởi chạy chương trình Server trước, sau đó mới chạy Client. Dừng chương trình bằng `Ctrl+C`.

---

### Bài 1: Gửi và nhận thông điệp CoAP cơ bản

- **Terminal 1 (Khởi chạy Server):**
  ```bash
  python bai1/coap_server_bai1.py
  ```
- **Terminal 2 (Khởi chạy Client):**
  ```bash
  python bai1/coap_client_bai1.py
  ```

#### Kết quả đạt được:
- **Tại Client:**
  ```text
  CoAP Client
  ========================================
  Sending GET request...
  URI: coap://127.0.0.1:5683/iot/lab/message
  Response:
  Code: 2.05 Content
  Payload: Xin chao tu CoAP Server
  ----------------------------------------
  Sending POST request...
  Payload: Xin chao tu CoAP Client - B23DCCN378 - Nguyen Van Huong
  Response:
  Code: 2.04 Changed
  Payload: Server da nhan thong diep
  ```
- **Tại Server:**
  ```text
  CoAP Server started on port 5683
  Resource available: coap://localhost:5683/iot/lab/message

  GET request received: /iot/lab/message
  POST request received:
  Payload: Xin chao tu CoAP Client - B23DCCN378 - Nguyen Van Huong
  Time: 23:50:39
  ----------------------------------------
  ```

---

### Bài 2: Mô phỏng cảm biến nhiệt độ và độ ẩm

- **Terminal 1 (Khởi chạy Sensor Server):**
  ```bash
  python bai2/sensor_server_bai2.py
  ```
- **Terminal 2 (Khởi chạy Monitor Client):**
  ```bash
  python bai2/monitor_client_bai2.py
  ```

#### Kết quả đạt được tại Monitor Client:
```text
Monitoring CoAP Client started...
Dang giam sat: coap://127.0.0.1:5683/iot/lab/sensor01/data
Truy van dinh ky moi 3s. Nhan Ctrl+C de dung.

[09:29:43] Received sensor data
Device: sensor01
Temperature: 39.7 C
Humidity: 71.1 %
CANH BAO: Nhiet do cao
-----------------------------------
[09:29:46] Received sensor data
Device: sensor01
Temperature: 29.3 C
Humidity: 37.5 %
CANH BAO: Do am thap
-----------------------------------
[09:29:49] Received sensor data
Device: sensor01
Temperature: 26.1 C
Humidity: 53.8 %
Trang thai: Binh thuong
-----------------------------------
```

---

### Bài 3: Điều khiển và Giám sát đèn thông minh (CoAP Observe)

- **Terminal 1 (Khởi chạy Smart Light Server):**
  ```bash
  python bai3/light_server_bai3.py
  ```
- **Terminal 2 (Khởi chạy Light Monitor Client - Đăng ký Observe):**
  ```bash
  python bai3/light_monitor_bai3.py
  ```
- **Terminal 3 (Khởi chạy Light Controller Client - Nhập lệnh điều khiển):**
  ```bash
  python bai3/light_controller_bai3.py
  ```

#### Kết quả đạt được:
- **Tại Controller Client:**
  ```text
  Nhap lenh (ON/OFF/STATUS/EXIT): ON
  Sending PUT request...
  Response Code: 2.04 Changed
  Da bat den light01
  Nhap lenh (ON/OFF/STATUS/EXIT): STATUS
  Sending GET request...
  Response:
  {"device_id": "light01", "status": "ON"}
  Nhap lenh (ON/OFF/STATUS/EXIT): TEST
  [Loi] Lenh 'TEST' khong hop le! Chi chap nhan ON, OFF, STATUS, EXIT.
  Nhap lenh (ON/OFF/STATUS/EXIT): OFF
  Sending PUT request...
  Response Code: 2.04 Changed
  Da tat den light01
  ```
- **Tại Monitor Client (Tự động nhận thông báo đẩy qua CoAP Observe, không dùng loop GET):**
  ```text
  Light Monitoring Client (CoAP Observe)
  Connecting to: coap://127.0.0.1:5683/iot/lab/light01/status
  Registering CoAP Observe...
  Observe registration successful
  [09:30:51] Initial State
  Device: light01
  Status: OFF
  -----------------------------------
  [09:31:03] State Updated
  Device: light01
  Status: ON
  -----------------------------------
  [09:31:03] State Updated
  Device: light01
  Status: OFF
  -----------------------------------
  ```
- **Tại Smart Light Server:**
  ```text
  CoAP Smart Light Server started...
  Resource: /iot/lab/light01/status
  New Observe registration received

  PUT request received:
  Device: light01
  Command: ON
  Light state changed: OFF -> ON
  Notify observers: ON

  PUT request received:
  Device: light01
  Command: OFF
  Light state changed: ON -> OFF
  Notify observers: OFF
  ```
