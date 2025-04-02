import cv2
import numpy as np

# Đường dẫn ảnh
path = r"D:\NguyenCuong\1A\FT672\data\temp\f_white_ng_1.png"
temp_path_1 = r"D:\NguyenCuong\1A\FT672\data\temp\temp_test.png"
temp_path_2 = r"D:\NguyenCuong\1A\FT672\data\temp\temp_test_2.png"

# Đọc ảnh
image = cv2.imread(path)
temp_L_1 = cv2.imread(temp_path_1, cv2.IMREAD_GRAYSCALE)
temp_L_2 = cv2.imread(temp_path_2, cv2.IMREAD_GRAYSCALE)

# Kiểm tra đọc ảnh
if image is None:
    print(f"Không thể đọc ảnh từ {path}")
    exit()
if temp_L_1 is None:
    print(f"Không thể đọc template từ {temp_path_1}")
    exit()
if temp_L_2 is None:
    print(f"Không thể đọc template từ {temp_path_2}")
    exit()

origin = image.copy()
img_display = origin.copy()

# Hàm tìm kiếm template trong ảnh
def process_image(img, temp, threshold):
    w, h = temp.shape[::-1]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
    _, maxval, _, maxloc = cv2.minMaxLoc(res)

    if maxval > threshold:
        print(f"Tìm thấy template (Max Value: {maxval})")
        top_left = maxloc
        bottom_right = (maxloc[0] + w, maxloc[1] + h)
        return True, top_left, bottom_right
    return False, (0, 0), (0, 0)


def filter_blue_region(image, h_min, h_max, s_min, s_max, v_min, v_max):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([h_min, s_min, v_min])
    upper_blue = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    blue_region = cv2.bitwise_and(image, image, mask=mask)
    return blue_region, mask

# Hàm cắt ảnh theo tọa độ
def crop_image(img, top_left, bottom_right):
    x1, y1 = top_left
    x2, y2 = bottom_right
    y1 = max(0, y1)
    y2 = min(img.shape[0], y2)
    x1 = max(0, x1)
    x2 = min(img.shape[1], x2)
    if y1 >= y2 or x1 >= x2:
        print("Vùng cắt không hợp lệ!")
        return None
    return img[y1:y2, x1:x2]

# Hàm lọc màu xanh bằng HSV
# def filter_blue_region(image):
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
#     lower_blue = np.array([40, 0, 50])   # Giới hạn dưới của màu xanh
#     upper_blue = np.array([140, 255, 255])  # Giới hạn trên của màu xanh
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)
#     blue_region = cv2.bitwise_and(image, image, mask=mask)
#     return blue_region, mask

# Hàm callback cho trackbar
def on_trackbar(val):
    pass

# Danh sách lưu kết quả
results = []

# Tìm kiếm và xử lý cả hai template
for idx, temp in enumerate([temp_L_1, temp_L_2], start=1):
    found, top_left, bottom_right = process_image(img_display, temp, 0.85)
    if found:
        cropped_img = crop_image(origin, top_left, bottom_right)
        if cropped_img is not None:
            results.append((f"Cropped Image {idx}", cropped_img, top_left, bottom_right))

# Nếu tìm thấy ít nhất một template, xử lý tiếp
if results:
    cv2.namedWindow("Result")
    # Tạo window cho trackbars
    cv2.namedWindow("HSV Controls")
    
    # Tạo trackbars cho HSV
    cv2.createTrackbar("H Min", "HSV Controls", 50, 179, on_trackbar)  # Hue: 0-179
    cv2.createTrackbar("H Max", "HSV Controls", 179, 179, on_trackbar)
    cv2.createTrackbar("S Min", "HSV Controls", 0, 255, on_trackbar)   # Saturation: 0-255
    cv2.createTrackbar("S Max", "HSV Controls", 255, 255, on_trackbar)
    cv2.createTrackbar("V Min", "HSV Controls", 120, 255, on_trackbar)  # Value: 0-255
    cv2.createTrackbar("V Max", "HSV Controls", 255, 255, on_trackbar)

    while True:
        img_display_with_rect = img_display.copy()

        # Lấy giá trị từ trackbars
        h_min = cv2.getTrackbarPos("H Min", "HSV Controls")
        h_max = cv2.getTrackbarPos("H Max", "HSV Controls")
        s_min = cv2.getTrackbarPos("S Min", "HSV Controls")
        s_max = cv2.getTrackbarPos("S Max", "HSV Controls")
        v_min = cv2.getTrackbarPos("V Min", "HSV Controls")
        v_max = cv2.getTrackbarPos("V Max", "HSV Controls")

        for idx, (title, cropped_img, top_left, bottom_right) in enumerate(results, start=1):
            # Hiển thị ảnh đã cắt
            cv2.imshow(title, cropped_img)

            # Lọc vùng màu xanh với giá trị HSV từ trackbar
            blue_region, blue_mask = filter_blue_region(cropped_img, h_min, h_max, s_min, s_max, v_min, v_max)
            cv2.imshow(f"Filtered Blue Region {idx}", blue_region)
            cv2.imshow(f"Blue Mask {idx}", blue_mask)

            # Vẽ vùng tìm thấy trên ảnh gốc
            cv2.rectangle(img_display_with_rect, top_left, bottom_right, (0, 255, 0), 2)

        # Hiển thị ảnh gốc với khung chữ nhật
        cv2.imshow("Result", img_display_with_rect)

        # Thoát bằng phím ESC
        if cv2.waitKey(1) & 0xFF == 27:
            break
else:
    print("Không tìm thấy template nào.")

cv2.destroyAllWindows()
