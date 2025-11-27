PROMPT: XÂY DỰNG ML SERVICE (FASTAPI) PHÂN LOẠI DỮ LIỆU IOT

1. Vai trò (Role)

Bạn là AI Engineer chuyên về triển khai mô hình Machine Learning (MLOps). Nhiệm vụ của bạn là xây dựng một Microservice bằng Python để phục vụ bài toán phân loại dữ liệu IoT.

2. Yêu cầu Chức năng

Service này cung cấp API để Backend gọi sang:

Input: JSON chứa thông tin cảm biến (Temperature, Humidity, CO2...).

Processing: Áp dụng logic (hoặc model) để quyết định mức độ ưu tiên.

Output: Nhãn phân loại: HOT, WARM, hoặc COLD.

3. Tech Stack

Language: Python 3.9+.

Framework: FastAPI (để đạt hiệu năng cao nhất).

Server: Uvicorn.

Libraries: Scikit-learn (giả lập load model), Pandas, Numpy.

Docker: Cần có Dockerfile để đóng gói.

4. Logic Phân loại (Rule-based Simulation)

Để demo hiệu quả và nhanh chóng, hãy cài đặt logic Rule-based kết hợp Random nhẹ (thay vì train model phức tạp tốn thời gian):

HOT: Nếu temperature > 50 HOẶC co2_level > 1000 (Cảnh báo cháy/ngạt khí).

WARM: Nếu temperature > 35 (Nóng nhưng chưa nguy hiểm).

COLD: Các trường hợp còn lại (Bình thường).

5. Hướng dẫn thực hiện

Bước 1: Setup Project

Tạo requirements.txt: fastapi, uvicorn, scikit-learn, pandas.

Tạo main.py: Khởi tạo ứng dụng FastAPI.

Bước 2: Data Model

Sử dụng Pydantic để định nghĩa Schema đầu vào:

class SensorData(BaseModel):
    temperature: float
    humidity: int
    co2_level: int


Bước 3: API Endpoint

Tạo POST /predict:

Nhận vào SensorData.

Thực hiện logic if-else ở mục 4.

Trả về JSON: {"label": "HOT"}.

Bước 4: Dockerize

Viết Dockerfile:

Base image: python:3.9-slim.

Workdir: /app.

Install requirements.

Expose port 5000.

CMD chạy uvicorn host 0.0.0.0 port 5000.

Yêu cầu: Code cần tối ưu độ trễ (Latency) thấp nhất có thể vì sẽ bị Backend gọi liên tục.
