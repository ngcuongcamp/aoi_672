import cv2
import numpy as np

# Hàm callback cho trackbar
def nothing(x):
    pass

# Đọc ảnh
path = r"D:\NguyenCuong\1A\FT672\hsv\black\images\temp.png"  # Thay bằng đường dẫn ảnh của bạn
image = cv2.imread(path)

if image is None:
    print(f"Không thể đọc ảnh từ {path}")
    exit()

# Chuyển sang HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Tạo cửa sổ cho trackbar
cv2.namedWindow("HSV Controls")

# Tạo trackbar cho màu xanh
cv2.createTrackbar("Blue H Min", "HSV Controls", 0, 179, nothing)  # Hue min cho màu xanh
cv2.createTrackbar("Blue H Max", "HSV Controls", 179, 179, nothing)  # Hue max cho màu xanh
cv2.createTrackbar("Blue S Min", "HSV Controls", 70, 255, nothing)  # Saturation min cho màu xanh
cv2.createTrackbar("Blue S Max", "HSV Controls", 255, 255, nothing)  # Saturation max cho màu xanh
cv2.createTrackbar("Blue V Min", "HSV Controls", 50, 255, nothing)  # Value min cho màu xanh
cv2.createTrackbar("Blue V Max", "HSV Controls", 255, 255, nothing)  # Value max cho màu xanh

# Tạo trackbar cho màu trắng
cv2.createTrackbar("White S Max", "HSV Controls", 70, 255, nothing)  # Saturation max cho màu trắng
cv2.createTrackbar("White V Min", "HSV Controls", 155, 255, nothing)  # Value min cho màu trắng

while True:
    # Lấy giá trị từ trackbar
    blue_h_min = cv2.getTrackbarPos("Blue H Min", "HSV Controls")
    blue_h_max = cv2.getTrackbarPos("Blue H Max", "HSV Controls")
    blue_s_min = cv2.getTrackbarPos("Blue S Min", "HSV Controls")
    blue_s_max = cv2.getTrackbarPos("Blue S Max", "HSV Controls")
    blue_v_min = cv2.getTrackbarPos("Blue V Min", "HSV Controls")
    blue_v_max = cv2.getTrackbarPos("Blue V Max", "HSV Controls")

    white_s_max = cv2.getTrackbarPos("White S Max", "HSV Controls")
    white_v_min = cv2.getTrackbarPos("White V Min", "HSV Controls")

    # Định nghĩa khoảng màu cho màu xanh
    lower_blue = np.array([blue_h_min, blue_s_min, blue_v_min])
    upper_blue = np.array([blue_h_max, blue_s_max, blue_v_max])

    # Định nghĩa khoảng màu cho màu trắng
    lower_white = np.array([0, 0, white_v_min])
    upper_white = np.array([179, white_s_max, 255])

    # Tạo mask cho từng màu
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    # Gộp mask cho nhóm 1 (xanh + trắng)
    group1_mask = cv2.bitwise_or(blue_mask, white_mask)

    # Áp dụng mask lên ảnh gốc
    group1_result = cv2.bitwise_and(image, image, mask=group1_mask)

    # Lưu kết quả
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\black\images\group1_result.png', group1_result)
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\black\images\group1_mask.png', group1_mask)

    # Hiển thị kết quả
    cv2.imshow("Original Image", image)
    cv2.imshow("Group 1 (Blue + White)", group1_result)
    cv2.imshow("Group 1 Mask", group1_mask)

    # Thoát khi nhấn ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()