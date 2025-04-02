# # import cv2
# # import numpy as np

# # # Hàm callback cho trackbar
# # def nothing(x):
# #     pass

# # # Đọc ảnh
# # path = r"D:\NguyenCuong\1A\FT672\hsv\purple\images\temp.png"  # Thay bằng đường dẫn ảnh của bạn
# # image = cv2.imread(path)

# # if image is None:
# #     print(f"Không thể đọc ảnh từ {path}")
# #     exit()

# # # Chuyển sang HSV
# # hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # # Tạo cửa sổ cho trackbar
# # cv2.namedWindow("HSV Controls")

# # # Tạo trackbar để điều chỉnh HSV cho màu xanh và màu tím
# # cv2.createTrackbar("Blue H Min", "HSV Controls", 90, 179, nothing)   # Blue H Min: 90 (ban đầu)
# # cv2.createTrackbar("Blue H Max", "HSV Controls", 115, 179, nothing)  # Blue H Max: 115 (ban đầu)
# # cv2.createTrackbar("Purple H Min", "HSV Controls", 120, 179, nothing)  # Purple H Min: 120 (ban đầu)
# # cv2.createTrackbar("Purple H Max", "HSV Controls", 179, 179, nothing)  # Purple H Max: 179 (ban đầu)
# # cv2.createTrackbar("S Min", "HSV Controls", 50, 255, nothing)         # S Min: 50 (ban đầu)
# # cv2.createTrackbar("S Max", "HSV Controls", 255, 255, nothing)       # S Max: 255
# # cv2.createTrackbar("V Min", "HSV Controls", 110, 255, nothing)        # V Min: 110 (ban đầu)
# # cv2.createTrackbar("V Max", "HSV Controls", 255, 255, nothing)       # V Max: 255

# # while True:
# #     # Lấy giá trị từ trackbar
# #     blue_h_min = cv2.getTrackbarPos("Blue H Min", "HSV Controls")
# #     blue_h_max = cv2.getTrackbarPos("Blue H Max", "HSV Controls")
# #     purple_h_min = cv2.getTrackbarPos("Purple H Min", "HSV Controls")
# #     purple_h_max = cv2.getTrackbarPos("Purple H Max", "HSV Controls")
# #     s_min = cv2.getTrackbarPos("S Min", "HSV Controls")
# #     s_max = cv2.getTrackbarPos("S Max", "HSV Controls")
# #     v_min = cv2.getTrackbarPos("V Min", "HSV Controls")
# #     v_max = cv2.getTrackbarPos("V Max", "HSV Controls")

# #     # Định nghĩa khoảng màu xanh
# #     lower_blue = np.array([blue_h_min, s_min, v_min])
# #     upper_blue = np.array([blue_h_max, s_max, v_max])

# #     # Định nghĩa khoảng màu tím
# #     lower_purple = np.array([purple_h_min, s_min, v_min])
# #     upper_purple = np.array([purple_h_max, s_max, v_max])

# #     # Tạo mask cho màu xanh và màu tím
# #     blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
# #     purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)

# #     # Áp dụng mask lên ảnh gốc để tách riêng
# #     blue_result = cv2.bitwise_and(image, image, mask=blue_mask)
# #     purple_result = cv2.bitwise_and(image, image, mask=purple_mask)

# #     # Lưu ảnh kết quả
# #     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\blue_result.png', blue_result)
# #     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\blue_mask.png', blue_mask)
# #     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\purple_result.png', purple_result)
# #     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\purple_mask.png', purple_mask)

# #     # Hiển thị kết quả
# #     cv2.imshow("Original Image", image)
# #     cv2.imshow("Blue Mask", blue_mask)
# #     cv2.imshow("Blue Result", blue_result)
# #     cv2.imshow("Purple Mask", purple_mask)
# #     cv2.imshow("Purple Result", purple_result)

# #     # Thoát khi nhấn ESC
# #     if cv2.waitKey(1) & 0xFF == 27:
# #         break

# # cv2.destroyAllWindows()


# import cv2
# import numpy as np

# # Hàm callback cho trackbar
# def nothing(x):
#     pass

# # Đọc ảnh
# path = r"D:\NguyenCuong\1A\FT672\hsv\purple\images\temp.png"  # Thay bằng đường dẫn ảnh của bạn
# image = cv2.imread(path)

# if image is None:
#     print(f"Không thể đọc ảnh từ {path}")
#     exit()

# # Chuyển sang HSV
# hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# # Tạo cửa sổ cho trackbar
# cv2.namedWindow("HSV Controls")

# # Tạo trackbar để điều chỉnh HSV cho màu xanh, màu tím và màu trắng
# cv2.createTrackbar("Blue H Min", "HSV Controls", 90, 179, nothing)   # Blue H Min: 90 (ban đầu)
# cv2.createTrackbar("Blue H Max", "HSV Controls", 115, 179, nothing)  # Blue H Max: 115 (ban đầu)
# cv2.createTrackbar("Purple H Min", "HSV Controls", 120, 179, nothing)  # Purple H Min: 120 (ban đầu)
# cv2.createTrackbar("Purple H Max", "HSV Controls", 179, 179, nothing)  # Purple H Max: 179 (ban đầu)
# cv2.createTrackbar("S Min", "HSV Controls", 50, 255, nothing)         # S Min: 50 (ban đầu)
# cv2.createTrackbar("S Max", "HSV Controls", 255, 255, nothing)       # S Max: 255
# cv2.createTrackbar("V Min", "HSV Controls", 110, 255, nothing)       # V Min: 110 (ban đầu)
# cv2.createTrackbar("V Max", "HSV Controls", 255, 255, nothing)       # V Max: 255
# cv2.createTrackbar("White S Max", "HSV Controls", 60, 255, nothing)  # White S Max: 50 (ban đầu)
# cv2.createTrackbar("White V Min", "HSV Controls", 90, 255, nothing) # White V Min: 200 (ban đầu)

# while True:
#     # Lấy giá trị từ trackbar
#     blue_h_min = cv2.getTrackbarPos("Blue H Min", "HSV Controls")
#     blue_h_max = cv2.getTrackbarPos("Blue H Max", "HSV Controls")
#     purple_h_min = cv2.getTrackbarPos("Purple H Min", "HSV Controls")
#     purple_h_max = cv2.getTrackbarPos("Purple H Max", "HSV Controls")
#     s_min = cv2.getTrackbarPos("S Min", "HSV Controls")
#     s_max = cv2.getTrackbarPos("S Max", "HSV Controls")
#     v_min = cv2.getTrackbarPos("V Min", "HSV Controls")
#     v_max = cv2.getTrackbarPos("V Max", "HSV Controls")
#     white_s_max = cv2.getTrackbarPos("White S Max", "HSV Controls")
#     white_v_min = cv2.getTrackbarPos("White V Min", "HSV Controls")

#     # Định nghĩa khoảng màu xanh
#     lower_blue = np.array([blue_h_min, s_min, v_min])
#     upper_blue = np.array([blue_h_max, s_max, v_max])

#     # Định nghĩa khoảng màu tím
#     lower_purple = np.array([purple_h_min, s_min, v_min])
#     upper_purple = np.array([purple_h_max, s_max, v_max])

#     # Định nghĩa khoảng màu trắng (S thấp, V cao)
#     lower_white = np.array([0, 0, white_v_min])
#     upper_white = np.array([179, white_s_max, 255])

#     # Tạo mask cho màu xanh, màu tím và màu trắng
#     blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     purple_mask = cv2.inRange(hsv, lower_purple, upper_purple)
#     white_mask = cv2.inRange(hsv, lower_white, upper_white)

#     # Gộp mask của màu tím và màu trắng thành một nhóm
#     purple_white_mask = cv2.bitwise_or(purple_mask, white_mask)

#     # Áp dụng mask lên ảnh gốc để tách riêng
#     blue_result = cv2.bitwise_and(image, image, mask=blue_mask)
#     purple_white_result = cv2.bitwise_and(image, image, mask=purple_white_mask)

#     # Lưu ảnh kết quả
#     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\blue_result.png', blue_result)
#     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\blue_mask.png', blue_mask)
#     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\purple_white_result.png', purple_white_result)
#     cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\purple_white_mask.png', purple_white_mask)

#     # Hiển thị kết quả
#     cv2.imshow("Original Image", image)
#     cv2.imshow("Blue Mask", blue_mask)
#     cv2.imshow("Blue Result", blue_result)
#     cv2.imshow("Purple + White Mask", purple_white_mask)
#     cv2.imshow("Purple + White Result", purple_white_result)

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
path = r"D:\NguyenCuong\1A\FT672\hsv\purple\images\temp.png"  # Thay bằng đường dẫn ảnh của bạn
image = cv2.imread(path)

if image is None:
    print(f"Không thể đọc ảnh từ {path}")
    exit()

# Chuyển sang HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Tạo cửa sổ cho trackbar
cv2.namedWindow("HSV Controls")

# Tạo trackbar để điều chỉnh HSV cho màu xanh và màu trắng
cv2.createTrackbar("Blue H Min", "HSV Controls", 0, 179, nothing)   # Blue H Min: 90 (ban đầu)
cv2.createTrackbar("Blue H Max", "HSV Controls", 115, 179, nothing)  # Blue H Max: 115 (ban đầu)
cv2.createTrackbar("S Min", "HSV Controls", 0, 255, nothing)        # S Min: 50 (ban đầu)
cv2.createTrackbar("S Max", "HSV Controls", 255, 255, nothing)       # S Max: 255
cv2.createTrackbar("V Min", "HSV Controls", 130, 255, nothing)       # V Min: 110 (ban đầu)
cv2.createTrackbar("V Max", "HSV Controls", 255, 255, nothing)       # V Max: 255
cv2.createTrackbar("White S Max", "HSV Controls", 0, 255, nothing)  # White S Max: 60 (ban đầu)
cv2.createTrackbar("White V Min", "HSV Controls", 255, 255, nothing)  # White V Min: 90 (ban đầu)

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

    # Định nghĩa khoảng màu xanh
    lower_blue = np.array([blue_h_min, s_min, v_min])
    upper_blue = np.array([blue_h_max, s_max, v_max])

    # Định nghĩa khoảng màu trắng (S thấp, V cao)
    lower_white = np.array([0, 0, white_v_min])
    upper_white = np.array([179, white_s_max, 255])

    # Tạo mask cho màu xanh và màu trắng
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)

    # Gộp mask của màu xanh và màu trắng thành Group 1
    group1_mask = cv2.bitwise_or(blue_mask, white_mask)

    # Áp dụng mask lên ảnh gốc để tách riêng
    group1_result = cv2.bitwise_and(image, image, mask=group1_mask)

    # Lưu ảnh kết quả
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\group1_result.png', group1_result)
    cv2.imwrite(r'D:\NguyenCuong\1A\FT672\hsv\purple\images\group1_mask.png', group1_mask)

    # Hiển thị kết quả
    cv2.imshow("Original Image", image)
    cv2.imshow("Group 1 (Blue + White) Mask", group1_mask)
    cv2.imshow("Group 1 (Blue + White) Result", group1_result)

    # Thoát khi nhấn ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()