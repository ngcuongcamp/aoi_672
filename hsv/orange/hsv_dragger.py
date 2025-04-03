import cv2
import numpy as np

# Hàm callback cho trackbar
def nothing(x):
    pass

# Đọc ảnh
path = r"D:\NguyenCuong\1A\FT672\hsv\orange\images\temp.png"  # Thay bằng đường dẫn ảnh của bạn
image = cv2.imread(path)

if image is None:
    print(f"Không thể đọc ảnh từ {path}")
    exit()

# Chuyển sang HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Tạo cửa sổ cho trackbar
cv2.namedWindow("HSV Controls")

# Tạo trackbar với các giá trị mặc định cho White & Blue
cv2.createTrackbar("Blue H Min", "HSV Controls", 80, 179, nothing)   # Blue H Min
cv2.createTrackbar("Blue H Max", "HSV Controls", 179, 179, nothing)  # Blue H Max
cv2.createTrackbar("S Min", "HSV Controls", 0, 255, nothing)         # S Min
cv2.createTrackbar("S Max", "HSV Controls", 255, 255, nothing)       # S Max
cv2.createTrackbar("V Min", "HSV Controls", 110, 255, nothing)       # V Min
cv2.createTrackbar("V Max", "HSV Controls", 255, 255, nothing)       # V Max
cv2.createTrackbar("White S Max", "HSV Controls", 100, 255, nothing) # White S Max
cv2.createTrackbar("White V Min", "HSV Controls", 110, 255, nothing) # White V Min

while True:
    # Lấy giá trị từ trackbar
    blue_h_min = cv2.getTrackbarPos("Blue H Min", "HSV Controls")
    blue_h_max = cv2.getTrackbarPos("Blue H Max", "HSV Controls")
    s_min = cv2.getTrackbarPos("S Min", "HSV Controls")
    s_max = cv2.getTrackbarPos("S Max", "HSV Controls")
    v_min = cv2.getTrackbarPos("V Min", "HSV Controls")
    v_max = cv2.getTrackbarPos("V Max", "HSV Controls")
    white_s_max = cv2.getTrackbarPos("White S Max", "HSV Controls")
    white_v_min = cv2.getTrackbarPos("White V Min", "HSV Controls")

    # Định nghĩa khoảng màu cho nhóm White & Blue
    # Trắng: S thấp, V cao
    lower_white = np.array([0, 0, white_v_min])
    upper_white = np.array([179, white_s_max, 255])

    # Xanh: Hue từ trackbar
    lower_blue = np.array([blue_h_min, s_min, v_min])
    upper_blue = np.array([blue_h_max, s_max, v_max])

    # Tạo mask cho từng màu
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Gộp mask của trắng và xanh
    group1_mask = cv2.bitwise_or(white_mask, blue_mask)

    # Áp dụng mask lên ảnh gốc
    group1_result = cv2.bitwise_and(image, image, mask=group1_mask)

    # Lưu kết quả
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\orange\images\group_1.png', group1_result)
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\orange\images\group_1_mask.png', group1_mask)

    # Hiển thị kết quả
    cv2.imshow("Original Image", image)
    cv2.imshow("Group 1 (White + Blue)", group1_result)
    cv2.imshow("Group 1 Mask", group1_mask)

    # Thoát khi nhấn ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()
