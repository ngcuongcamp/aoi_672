
# import cv2
# import numpy as np

# # Hàm callback cho trackbar
# def nothing(x):
#     pass

# # Đọc ảnh
# path = r"D:\NguyenCuong\1A\FT672\hsv\orange\images\temp.png"  # Thay bằng đường dẫn ảnh của bạn
# image = cv2.imread(path)

# if image is None:
#     print(f"Không thể đọc ảnh từ {path}")
#     exit()

# # Chuyển sang HSV
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # Tạo cửa sổ cho trackbar
# cv2.namedWindow("HSV Controls")

# # Tạo trackbar với các giá trị mặc định từ hình ảnh
# cv2.createTrackbar("Blue H Min", "HSV Controls", 80, 179, nothing)   # Blue H Min: 79
# cv2.createTrackbar("Blue H Max", "HSV Controls", 179, 179, nothing)  # Blue H Max: 179
# cv2.createTrackbar("Orange H Min", "HSV Controls", 0, 179, nothing)  # Orange H Min: 0
# cv2.createTrackbar("Orange H Max", "HSV Controls", 85, 179, nothing) # Orange H Max: 85
# cv2.createTrackbar("S Min", "HSV Controls", 0, 255, nothing)         # S Min: 0
# cv2.createTrackbar("S Max", "HSV Controls", 255, 255, nothing)       # S Max: 255
# # cv2.createTrackbar("V Min", "HSV Controls", 140, 255, nothing)        # V Min: 99
# cv2.createTrackbar("V Min", "HSV Controls", 110, 255, nothing)  
# cv2.createTrackbar("V Max", "HSV Controls", 255, 255, nothing)       # V Max: 255
# cv2.createTrackbar("White/Gray S Max", "HSV Controls", 50, 255, nothing)  # White/Gray S Max: 50
# cv2.createTrackbar("Gray V Min", "HSV Controls", 106, 255, nothing)  # Gray V Min: 106
# cv2.createTrackbar("White V Min", "HSV Controls", 198, 255, nothing) # White V Min: 198

# while True:
#     # Lấy giá trị từ trackbar
#     blue_h_min = cv2.getTrackbarPos("Blue H Min", "HSV Controls")
#     blue_h_max = cv2.getTrackbarPos("Blue H Max", "HSV Controls")
#     orange_h_min = cv2.getTrackbarPos("Orange H Min", "HSV Controls")
#     orange_h_max = cv2.getTrackbarPos("Orange H Max", "HSV Controls")
#     s_min = cv2.getTrackbarPos("S Min", "HSV Controls")
#     s_max = cv2.getTrackbarPos("S Max", "HSV Controls")
#     v_min = cv2.getTrackbarPos("V Min", "HSV Controls")
#     v_max = cv2.getTrackbarPos("V Max", "HSV Controls")
#     white_gray_s_max = cv2.getTrackbarPos("White/Gray S Max", "HSV Controls")
#     gray_v_min = cv2.getTrackbarPos("Gray V Min", "HSV Controls")
#     white_v_min = cv2.getTrackbarPos("White V Min", "HSV Controls")

#     # Định nghĩa khoảng màu cho nhóm 1 (trắng, xám, xanh)
#     # Trắng: S thấp, V cao
#     lower_white = np.array([0, 0, white_v_min])
#     upper_white = np.array([179, white_gray_s_max, 255])

#     # Xám: S thấp, V trung bình-cao
#     lower_gray = np.array([0, 0, gray_v_min])
#     upper_gray = np.array([179, white_gray_s_max, 200])

#     # Xanh: Hue từ trackbar
#     lower_blue = np.array([blue_h_min, s_min, v_min])
#     upper_blue = np.array([blue_h_max, s_max, v_max])

#     # Định nghĩa khoảng màu cam (nhóm 2)
#     lower_orange = np.array([orange_h_min, s_min, v_min])
#     upper_orange = np.array([orange_h_max, s_max, v_max])

#     # Tạo mask cho từng màu
#     white_mask = cv2.inRange(hsv, lower_white, upper_white)
#     gray_mask = cv2.inRange(hsv, lower_gray, upper_gray)
#     blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

#     # Gộp mask của trắng, xám, xanh thành nhóm 1
#     group1_mask = cv2.bitwise_or(white_mask, gray_mask)  # Gộp trắng và xám
#     group1_mask = cv2.bitwise_or(group1_mask, blue_mask)  # Gộp thêm xanh

#     # Mask nhóm 2 là màu cam
#     group2_mask = orange_mask

#     # Áp dụng mask lên ảnh gốc
#     group1_result = cv2.bitwise_and(image, image, mask=group1_mask)
#     group2_result = cv2.bitwise_and(image, image, mask=group2_mask)

#     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\orange\images\group_1.png', group1_result)
#     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\orange\images\group_1_mask.png', group1_mask)
    
#     # Hiển thị kết quả
#     cv2.imshow("Original Image", image)
#     cv2.imshow("Group 1 (White+Gray+Blue)", group1_result)
#     cv2.imshow("Group 2 (Orange)", group2_result)
#     cv2.imshow("Group 1 Mask", group1_mask)
#     cv2.imshow("Group 2 Mask", group2_mask)

#     # Thoát khi nhấn ESC
#     if cv2.waitKey(1) & 0xFF == 27:
#         break

# cv2.destroyAllWindows()


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

# Tạo trackbar với các giá trị mặc định cho Group 1 (trắng, xám, xanh)
cv2.createTrackbar("Blue H Min", "HSV Controls", 80, 179, nothing)   # Blue H Min: 79
cv2.createTrackbar("Blue H Max", "HSV Controls", 179, 179, nothing)  # Blue H Max: 179
cv2.createTrackbar("S Min", "HSV Controls", 0, 255, nothing)         # S Min: 0
cv2.createTrackbar("S Max", "HSV Controls", 255, 255, nothing)       # S Max: 255
cv2.createTrackbar("V Min", "HSV Controls", 110, 255, nothing)       # V Min: 110
cv2.createTrackbar("V Max", "HSV Controls", 255, 255, nothing)       # V Max: 255
cv2.createTrackbar("White/Gray S Max", "HSV Controls", 100, 255, nothing)  # White/Gray S Max: 50
cv2.createTrackbar("Gray V Min", "HSV Controls", 115, 255, nothing)  # Gray V Min: 106
cv2.createTrackbar("White V Min", "HSV Controls", 110, 255, nothing) # White V Min: 198

while True:
    # Lấy giá trị từ trackbar
    blue_h_min = cv2.getTrackbarPos("Blue H Min", "HSV Controls")
    blue_h_max = cv2.getTrackbarPos("Blue H Max", "HSV Controls")
    s_min = cv2.getTrackbarPos("S Min", "HSV Controls")
    s_max = cv2.getTrackbarPos("S Max", "HSV Controls")
    v_min = cv2.getTrackbarPos("V Min", "HSV Controls")
    v_max = cv2.getTrackbarPos("V Max", "HSV Controls")
    white_gray_s_max = cv2.getTrackbarPos("White/Gray S Max", "HSV Controls")
    gray_v_min = cv2.getTrackbarPos("Gray V Min", "HSV Controls")
    white_v_min = cv2.getTrackbarPos("White V Min", "HSV Controls")

    # Định nghĩa khoảng màu cho nhóm 1 (trắng, xám, xanh)
    # Trắng: S thấp, V cao
    lower_white = np.array([0, 0, white_v_min])
    upper_white = np.array([179, white_gray_s_max, 255])

    # Xám: S thấp, V trung bình-cao
    lower_gray = np.array([0, 0, gray_v_min])
    upper_gray = np.array([179, white_gray_s_max, 200])

    # Xanh: Hue từ trackbar
    lower_blue = np.array([blue_h_min, s_min, v_min])
    upper_blue = np.array([blue_h_max, s_max, v_max])

    # Tạo mask cho từng màu
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    gray_mask = cv2.inRange(hsv, lower_gray, upper_gray)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Gộp mask của trắng, xám, xanh thành nhóm 1
    group1_mask = cv2.bitwise_or(white_mask, gray_mask)  # Gộp trắng và xám
    group1_mask = cv2.bitwise_or(group1_mask, blue_mask)  # Gộp thêm xanh

    # Áp dụng mask lên ảnh gốc
    group1_result = cv2.bitwise_and(image, image, mask=group1_mask)

    # Lưu kết quả
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\orange\images\group_1.png', group1_result)
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\orange\images\group_1_mask.png', group1_mask)

    # Hiển thị kết quả
    cv2.imshow("Original Image", image)
    cv2.imshow("Group 1 (White+Gray+Blue)", group1_result)
    cv2.imshow("Group 1 Mask", group1_mask)

    # Thoát khi nhấn ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()