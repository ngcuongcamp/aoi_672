import cv2
import numpy as np

# Hàm callback khi nhấp chuột
def get_hsv(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:  # Khi nhấp chuột trái
        # Lấy giá trị HSV tại vị trí (x, y)
        hsv_value = hsv[y, x]
        print(f"HSV tại vị trí ({x}, {y}): H={hsv_value[0]}, S={hsv_value[1]}, V={hsv_value[2]}")

# Đọc ảnh
path = r"D:\NguyenCuong\1A\FT672\data\temp\test_purple.png"  # Thay bằng đường dẫn ảnh của bạn
image = cv2.imread(path)

if image is None:
    print(f"Không thể đọc ảnh từ {path}")
    exit()

# Chuyển sang HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Tạo cửa sổ và gắn sự kiện nhấp chuột
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", get_hsv)

# Hiển thị ảnh và chờ nhấp chuột
while True:
    cv2.imshow("Image", image)
    if cv2.waitKey(1) & 0xFF == 27:  # Nhấn ESC để thoát
        break

cv2.destroyAllWindows()