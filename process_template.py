import cv2
import numpy as np
import os
from imutils.contours import sort_contours
current_dir = os.path.dirname(os.path.abspath(__file__))


def get_color(event, x, y, flags, param):
    """
    check rgb and hvs on point was click on image
    output: print(value : bgr,hsv)
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param[0]
        window_name = param[1]
        pixel_color = frame[y, x]  # Lấy màu sắc tại điểm (x, y)
        b, g, r = pixel_color  # Tách giá trị BGR
        print(f"COLOR_BGR ({x}, {y}): B={b}, G={g}, R={r}")
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        h, s, v = hsv[y, x]
        print(f"COLOR_HSV ({x}, {y}): H={h}, S={s}, V={v}")
        cv2.imshow(window_name, frame)


def nothing(x):
    pass


class HSV_Adjuster:
    def __init__(self):
        self.window_name = 'Image Display'
        self.trackbar_window = 'Trackbars'
        self.create_window()

    def create_window(self):
        # Tạo cửa sổ hiển thị ảnh
        cv2.namedWindow(self.window_name)
        cv2.resizeWindow(self.window_name, 640, 480)

        # Tạo cửa sổ cho các trackbar
        cv2.namedWindow(self.trackbar_window)
        cv2.resizeWindow(self.trackbar_window, 400, 250)

        # Tạo các trackbar trong cửa sổ riêng
        cv2.createTrackbar('H Lower', self.trackbar_window,
                           0, 179, nothing)
        cv2.createTrackbar('H Higher', self.trackbar_window,
                           179, 179, nothing)
        cv2.createTrackbar('S Lower', self.trackbar_window,
                           0, 255, nothing)
        cv2.createTrackbar('S Higher', self.trackbar_window,
                           50, 255, nothing)
        cv2.createTrackbar('V Lower', self.trackbar_window,
                           0, 255, nothing)
        cv2.createTrackbar('V Higher', self.trackbar_window,
                           50, 255, nothing)

    def analyze_objects(self):
        # Chuyển ảnh result sang ảnh xám để tìm contours
        gray = cv2.cvtColor(self.result, cv2.COLOR_BGR2GRAY)
        
        # Áp dụng ngưỡng để tạo ảnh nhị phân (binary image)
        _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        
        # Tìm contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sắp xếp contours theo thứ tự từ trái sang phải (tùy chọn)
        if len(contours) > 0:
            contours, _ = sort_contours(contours, method="left-to-right")
        
        # Đếm số lượng vật thể
        
        # num_objects = len(contours)
        # print(f"Số lượng vật thể trước khi lọc: {num_objects}")
        
        # Danh sách để lưu thông tin các vật thể
        objects_info = []
        
        # Biến đếm để gán ID
        object_id = 1
        
        # Phân tích từng vật thể
        for contour in contours:
            # Tính diện tích của vùng màu xanh
            area = cv2.contourArea(contour)
            
            # Bỏ qua các vật thể quá nhỏ (có thể là nhiễu)
            if area < 150:  # Ngưỡng diện tích, có thể điều chỉnh
                continue
            
            # Tìm hình chữ nhật nhỏ nhất bao quanh vật thể
            rect = cv2.minAreaRect(contour)
            (x, y), (width, height), angle = rect
            
            # Chiều dài và chiều rộng (width và height có thể cần hoán đổi tùy theo góc xoay)
            length = max(width, height)
            width = min(width, height)
            
            # Tính diện tích của hình chữ nhật bao quanh
            rect_area = length * width
            
            # Lưu thông tin vào danh sách với ID tăng dần
            objects_info.append({
                "id": object_id,
                "area": area,
                "rect_area": rect_area,
                "length": length,
                "width": width,
                "center": (x, y)
            })
            
            # Vẽ hình chữ nhật bao quanh vật thể lên ảnh (màu đỏ)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(self.result, [box], 0, (0, 0, 255), 2)  # Màu đỏ
            
            # Ghi thông tin lên ảnh (hiển thị diện tích, chiều dài, chiều rộng)
            cv2.putText(self.result, f"Obj {object_id}: {area:.0f}px^2", 
                        (int(x), int(y)-30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(self.result, f"L: {length:.0f}px, W: {width:.0f}px", 
                        (int(x), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Tăng ID cho vật thể tiếp theo
            object_id += 1
        
        # In số lượng vật thể sau khi lọc
        # print(f"Số lượng vật thể sau khi lọc: {len(objects_info)}")
        
        # In thông tin sau khi phân tích xong tất cả vật thể
        for obj in objects_info:
            print(f"\nVật thể {obj['id']}:")
            print(f" - Diện tích vùng màu xanh: {obj['area']:.2f} pixel vuông")
            print(f" - Diện tích hình chữ nhật bao quanh: {obj['rect_area']:.2f} pixel vuông")
            print(f" - Chiều dài: {obj['length']:.2f} pixel")
            print(f" - Chiều rộng: {obj['width']:.2f} pixel")

        return objects_info  # Trả về danh sách thông tin vật thể (tùy chọn)
    
    
    def analyze_black_regions(self):
        # Chuyển ảnh sang ảnh xám để tìm contours
        gray = cv2.cvtColor(self.result, cv2.COLOR_BGR2GRAY)
        
        # Áp dụng ngưỡng để tạo ảnh nhị phân
        _, binary = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        
        # Tìm contours
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sắp xếp contours từ trái sang phải
        if len(contours) > 0:
            contours, _ = sort_contours(contours, method="left-to-right")
        
        # Danh sách để lưu thông tin các vùng màu đen
        black_regions_info = []
        object_id = 1
        
        # Phân tích từng contour
        for contour in contours:
            # Tính diện tích của vùng màu đen
            area = cv2.contourArea(contour)
            
            # Bỏ qua các vùng quá nhỏ (nhiễu)
            if area < 150:
                continue
            
            # Tìm hình chữ nhật bao quanh vùng màu đen
            rect = cv2.minAreaRect(contour)
            (x, y), (width, height), angle = rect
            length = max(width, height)
            width = min(width, height)
            
            # Lưu thông tin vùng màu đen
            black_regions_info.append({
                "id": object_id,
                "area": area,
                "center": (x, y)
            })
            
            # Vẽ contour bao quanh vùng màu đen (màu đỏ)
            cv2.drawContours(self.result, [contour], -1, (0, 0, 255), 2)
            
            # Ghi thông tin diện tích lên ảnh
            cv2.putText(self.result, f"Region {object_id}: {area:.0f}px^2", 
                        (int(x), int(y)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            object_id += 1
        
        # In thông tin các vùng màu đen
        for region in black_regions_info:
            print(f"\nVùng màu đen {region['id']}:")
            print(f" - Diện tích: {region['area']:.2f} pixel vuông")
        
        return black_regions_info

    def start(self,  img):
        cv2.imshow("origin image", img)
        while True:
            frame = img.copy()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            h_lower = cv2.getTrackbarPos('H Lower', self.trackbar_window)
            h_higher = cv2.getTrackbarPos('H Higher', self.trackbar_window)
            s_lower = cv2.getTrackbarPos('S Lower', self.trackbar_window)
            s_higher = cv2.getTrackbarPos('S Higher', self.trackbar_window)
            v_lower = cv2.getTrackbarPos('V Lower', self.trackbar_window)
            v_higher = cv2.getTrackbarPos('V Higher', self.trackbar_window)

            lower_bound = np.array([h_lower, s_lower, v_lower])
            upper_bound = np.array([h_higher, s_higher, v_higher])
            mask = cv2.inRange(hsv, lower_bound, upper_bound)

            self.result = cv2.bitwise_and(frame, frame, mask=mask)
            
            # Gọi phương thức phân tích vật thể
            self.analyze_black_regions()
            
            # cv2.imshow('result', self.result)
            cv2.imshow(self.window_name, self.result)
            cv2.setMouseCallback(
                self.window_name, get_color, (self.result, self.window_name))
            if cv2.waitKey(1) & 0xFF == 27:
                break

