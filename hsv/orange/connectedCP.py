
import cv2
import numpy as np

# Đọc ảnh nhị phân
path = r"D:\NguyenCuong\1A\FT672\hsv\orange\images\group_1_mask.png"  # Thay bằng đường dẫn ảnh của bạn
image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print(f"Không thể đọc ảnh từ {path}")
    exit()

# Đảm bảo ảnh là nhị phân
_, binary = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

# Tiền xử lý: Loại bỏ nhiễu bằng phép mở (morphological opening) - tùy chọn
kernel = np.ones((3, 3), np.uint8)
binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)

# Tìm các thành phần liên thông
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)

# Định nghĩa ngưỡng diện tích tối thiểu để coi là vùng lớn9
min_area = 10  # Có thể điều chỉnh ngưỡng này tùy theo ảnh của bạn

# Lọc các thành phần lớn dựa trên diện tích và đo chiều cao
valid_components = 0
heights = []
widths = []# Danh sách lưu chiều cao của các thành phần lớn
for i in range(1, num_labels):  # Bỏ qua nền (label 0)
    area = stats[i, cv2.CC_STAT_AREA]  # Diện tích của thành phần
    if area >= min_area:
        valid_components += 1
        height = stats[i, cv2.CC_STAT_HEIGHT]  # Chiều cao của thành phần
        heights.append(height)
        width = stats[i, cv2.CC_STAT_WIDTH]
        widths.append(width)
        print(f"Thành phần {valid_components}: Chiều cao = {height} pixel, chiều rộng: {width} pixel")

# Kiểm tra xem keo có bị đứt không
if valid_components > 1:
    print(f"Keo bị đứt! Có {valid_components} thành phần liên thông lớn.")
else:
    print("Keo không bị đứt. Chỉ có 1 thành phần liên thông lớn.")

# Hiển thị các thành phần liên thông lớn bằng màu khác nhau
output = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
for i in range(1, num_labels):  # Bỏ qua nền (label 0)
    area = stats[i, cv2.CC_STAT_AREA]
    if area >= min_area:  # Chỉ hiển thị các thành phần lớn
        output[labels == i] = [0, 255 // (i + 1), 255]  # Màu khác nhau cho từng thành phần
        
        # Lấy thông tin để vẽ chiều cao lên vật thể
        x = stats[i, cv2.CC_STAT_LEFT]  # Tọa độ x của góc trái trên
        y = stats[i, cv2.CC_STAT_TOP]   # Tọa độ y của góc trái trên
        width = stats[i, cv2.CC_STAT_WIDTH]  # Chiều rộng
        height = stats[i, cv2.CC_STAT_HEIGHT]  # Chiều cao
        
        # Tính vị trí trung tâm của vật thể để vẽ văn bản
        center_x = x + width // 2
        center_y = y + height // 2
        
        # Vẽ chiều cao lên vật thể (ở vị trí trung tâm)
        cv2.putText(output, f"H={height}", (center_x - 20, center_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        
        cv2.putText(output, f" V={width}", (center_x - 20, center_y + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

# Hiển thị kết quả
cv2.imshow("Original Binary Image", binary)
cv2.imshow("Large Connected Components", output)
cv2.waitKey(0)
cv2.destroyAllWindows()