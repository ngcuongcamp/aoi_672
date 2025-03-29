import cv2
import numpy as np
import math
# from process_template import *

# Đường dẫn đến ảnh đầu vào
path = r"D:\NguyenCuong\1A\FT672\img_2103\img\dataset_ng_white\NG (28).png"
# path = r"D:\NguyenCuong\1A\FT672\img_2103\img\dataset_ng_white\NG (24).png"

# Đọc ảnh gốc và template
image = cv2.imread(path)
temp_L = cv2.imread(r"D:\NguyenCuong\1A\FT672\data\temp\template_2.png", cv2.IMREAD_GRAYSCALE)

# Biến toàn cục
origin = image.copy()  # Ảnh gốc không thay đổi
img_display = origin.copy()  # Ảnh để hiển thị và chỉnh sửa
threshold_value = 15  # Giá trị ngưỡng ban đầu

def TemplateMatching(img, temp, threshold, thresh_val):
    
    
    ORANGE_RECT_X_SHIFT = -115  # Dịch chuyển x của hình chữ nhật màu cam (âm: trái, dương: phải)
    ORANGE_RECT_Y_SHIFT = -10   # Dịch chuyển y của hình chữ nhật màu cam (âm: lên, dương: xuống)
    
    ORANGE_RECT_WIDTH = 115     # Chiều rộng hình chữ nhật màu cam (None: mặc định)
    ORANGE_RECT_HEIGHT = 32     # Chiều cao hình chữ nhật màu cam
    
    THRESHOLD_VALUE = thresh_val        # Ngưỡng cho binarization, lấy từ trackbar
    
    # Sao chép ảnh gốc và lấy kích thước template
    # Không thay đổi origin ở đây, chỉ dùng để cắt vùng
    pt = False
    w, h = temp.shape[::-1]     # Chiều rộng và cao của template
    
    # Chuyển ảnh sang grayscale và thực hiện template matching
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
    _, maxval, _, maxloc = cv2.minMaxLoc(res)
    
    if maxval > threshold:
        print("Max Value:", maxval)
        
        # Dịch tọa độ maxloc
        maxloc_shifted = (maxloc[0] , maxloc[1])
       
        
        # Vẽ hình chữ nhật màu xanh tại vị trí template khớp trên img
        cv2.rectangle(img, maxloc_shifted, (maxloc_shifted[0] + w, maxloc_shifted[1] + h), (0, 255, 0), 1)
        
        # Tính tọa độ cho hình chữ nhật màu cam
        bottom_left_x = maxloc_shifted[0]  + ORANGE_RECT_X_SHIFT
        bottom_left_y = maxloc_shifted[1] + h + ORANGE_RECT_Y_SHIFT
        bottom_left = (bottom_left_x, bottom_left_y)
        
        # Xác định chiều rộng của hình chữ nhật màu cam
        orange_rect_right_x = bottom_left[0] + (ORANGE_RECT_WIDTH if ORANGE_RECT_WIDTH else w)
        orange_rect_bottom_y = bottom_left[1] + ORANGE_RECT_HEIGHT
        bottom_right_2 = (orange_rect_right_x, orange_rect_bottom_y)
        
        # Vẽ hình chữ nhật màu cam trên img
        cv2.rectangle(img, bottom_left, bottom_right_2, (0, 165, 255), 1)
        
        # Vẽ hình chữ nhật màu tím (dài hơn 10px so với màu cam)
        purple_rect_right_x = bottom_left[0] + ORANGE_RECT_WIDTH  # Chiều rộng của tím bằng cam
        purple_rect_bottom_y = bottom_left[1] + ORANGE_RECT_HEIGHT + 14
        # purple_bottom_right = (purple_rect_right_x, purple_rect_bottom_y)
        # cv2.rectangle(img, bottom_left, purple_bottom_right, (255, 0, 255), 1)  # Màu tím
        
        # Khoanh 30px từ bên phải sang trái của hình chữ nhật màu tím
        purple_right_end_x = purple_rect_right_x  # Điểm kết thúc là bên phải của tím
        purple_right_start_x = purple_right_end_x - 35  # Điểm bắt đầu cách bên phải 38px
        cv2.rectangle(img, (purple_right_start_x, bottom_left_y), (purple_right_end_x, purple_rect_bottom_y), (0, 255, 255), 1)  # Màu vàng
        
        # Cắt vùng ảnh trong hình chữ nhật màu vàng từ ảnh gốc
        gold_region = origin[bottom_left_y:purple_rect_bottom_y, purple_right_start_x:purple_right_end_x]
        cv2.imwrite('./gold_region.png', gold_region)  # Lưu để kiểm tra nếu cần
        
        # Chuyển sang grayscale và áp dụng ngưỡng cho vùng vàng
        gray_gold = cv2.cvtColor(gold_region, cv2.COLOR_BGR2GRAY)
        _, gold_thresh = cv2.threshold(gray_gold, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        
        # Tính toán tỷ lệ khoảng trắng trong vùng vàng
        gold_white_area = cv2.countNonZero(gold_thresh)
        gold_total_area = gold_thresh.shape[0] * gold_thresh.shape[1]
        gold_white_ratio = (gold_white_area / gold_total_area) * 100
        
        # Hiển thị tỷ lệ trắng của vùng vàng lên ảnh img
        cv2.putText(img, f"Gold: {gold_white_ratio:.2f}%", (50, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        
        # Cắt vùng ảnh trong hình chữ nhật màu cam từ ảnh gốc (origin toàn cục)
        x_start = max(0, bottom_left[0])
        y_start = max(0, bottom_left[1])
        x_end = min(origin.shape[1], bottom_right_2[0])
        y_end = min(origin.shape[0], bottom_right_2[1])
        
        cropped_region = origin[y_start:y_end, x_start:x_end]
        gray_crop = cv2.cvtColor(cropped_region, cv2.COLOR_BGR2GRAY)
        
        # Áp dụng ngưỡng để phân tích vùng cắt
        _, crop_thresh = cv2.threshold(gray_crop, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        
        zoomed_cropped = cv2.resize(cropped_region, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        zoomed_cropped_thresh = cv2.resize(crop_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
        
        # Chia vùng thành 2 phần (trái và phải) từ ảnh gốc
        crop_width = x_end - x_start
        half_width = crop_width // 2
        
        # Tọa độ cho phần trái và phần phải
        left_x_end = x_start + half_width
        right_x_start = left_x_end
        
        # Cắt trực tiếp từ ảnh gốc
        left_part = origin[y_start:y_end, x_start:left_x_end]
        right_part = origin[y_start:y_end, right_x_start:x_end]
        
        cv2.imwrite('./left.png', left_part)
        cv2.imwrite('./right.png', right_part)
        cv2.imwrite('./gold.png', gold_region)

        
        # Chuyển sang grayscale và áp dụng ngưỡng cho từng phần
        gray_left = cv2.cvtColor(left_part, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(right_part, cv2.COLOR_BGR2GRAY)
        
        _, left_thresh = cv2.threshold(gray_left, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        _, right_thresh = cv2.threshold(gray_right, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        
        cv2.imwrite('./left_thresh.png', left_thresh)
        cv2.imwrite('./right_thresh.png', right_thresh)
        cv2.imwrite('./gold_thresh.png', gold_thresh)
        
        # Tính toán độ bao phủ của màu trắng cho từng phần
        left_white_area = cv2.countNonZero(left_thresh)
        left_total_area = left_thresh.shape[0] * left_thresh.shape[1]
        left_white_ratio = (left_white_area / left_total_area) * 100
        
        right_white_area = cv2.countNonZero(right_thresh)
        right_total_area = right_thresh.shape[0] * right_thresh.shape[1]
        right_white_ratio = (right_white_area / right_total_area) * 100
        
        # Tính toán tỷ lệ vùng trắng và đen cho toàn bộ cropped_region
        white_area = cv2.countNonZero(crop_thresh)
        total_area = crop_thresh.shape[0] * crop_thresh.shape[1]
        white_ratio = (white_area / total_area) * 100
        
        print(f"Tỷ lệ vùng trắng (toàn bộ): {white_ratio:.2f}%")
        print(f"Tỷ lệ vùng trắng (phần trái): {left_white_ratio:.2f}%")
        print(f"Tỷ lệ vùng trắng (phần phải): {right_white_ratio:.2f}%")
        print(f"Tỷ lệ vùng trắng (vùng vàng): {gold_white_ratio:.2f}%")
        
        # Ghi kết quả OK/NG lên ảnh img
        text = f"OK: {white_ratio:.2f}%" if white_ratio > 99 else f"NG: {white_ratio:.2f}%"
        color = (0, 255, 0) if white_ratio > 99 else (0, 0, 255)
        cv2.putText(img, text, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 2)
        
        # Ghi tỷ lệ trắng của từng phần lên ảnh img
        left_color = (0, 255, 0) if left_white_ratio > 98 else (0, 0, 255)
        right_color = (0, 255, 0) if right_white_ratio > 98 else (0, 0, 255)
        cv2.putText(img, f"Left: {left_white_ratio:.2f}%", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 0.7, left_color, 2)
        cv2.putText(img, f"Right: {right_white_ratio:.2f}%", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, right_color, 2)
        
        # Khoanh vùng left_part và right_part trên ảnh img
        left_rect_color = (0, 255, 0) if left_white_ratio > 98 else (0, 0, 255)  # Xanh nếu > 98%, đỏ nếu <= 98%
        right_rect_color = (0, 255, 0) if right_white_ratio > 98 else (0, 0, 255)  # Xanh nếu > 98%, đỏ nếu <= 98%
        
        # Vẽ hình chữ nhật cho phần trái và phần phải trên img
        cv2.rectangle(img, (x_start, y_start), (left_x_end, y_end), left_rect_color, 1)
        cv2.rectangle(img, (right_x_start, y_start), (x_end, y_end), right_rect_color, 1)
        
        # Hiển thị các cửa sổ ảnh
        cv2.imshow("Result", img)  # Ảnh đã khoanh và ghi chú
        cv2.imshow("Template", temp)
        cv2.imshow("Cropped", cropped_region)
        cv2.imshow("Cropped thresh", crop_thresh)
        cv2.imshow("Origin", origin)  # Ảnh gốc không khoanh
        cv2.imshow("zoomed_cropped", zoomed_cropped)
        cv2.imshow("zoomed_cropped_thresh", zoomed_cropped_thresh)
        cv2.imshow("Left Part", left_thresh)  # Hiển thị phần trái sau ngưỡng
        cv2.imshow("Right Part", right_thresh)  # Hiển thị phần phải sau ngưỡng
        cv2.imshow("Gold Region", gold_region)  # Hiển thị vùng vàng
        cv2.imshow("Gold Thresh", gold_thresh)  # Hiển thị vùng vàng
        
        
        pt = True
    
    return pt, maxloc

# Callback cho trackbar
def update_threshold(val):
    global threshold_value, img_display, temp_L, origin
    threshold_value = val
    img_display = origin.copy()  # Reset ảnh hiển thị từ origin gốc
    pt, maxloc = TemplateMatching(img_display, temp_L, 0.95, threshold_value)
    print(f"Threshold: {threshold_value}, Tọa độ Top-Left: {maxloc}")

# Tạo cửa sổ và thanh kéo
cv2.namedWindow("Result")
cv2.createTrackbar("Threshold", "Result", threshold_value, 255, update_threshold)

# Hiển thị lần đầu tiên
pt, maxloc = TemplateMatching(img_display, temp_L, 0.95, threshold_value)
print("Tọa độ Top-Left (khởi tạo):", maxloc)

# Vòng lặp chính để giữ cửa sổ và xử lý sự kiện
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # Nhấn ESC để thoát
        break

cv2.destroyAllWindows()