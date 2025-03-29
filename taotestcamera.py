import cv2
import time
import os
import configparser

# Đọc file cấu hình config.ini
config = configparser.ConfigParser()
config.read('./temp/config.ini')

# Đọc các giá trị màu từ section [Colors]
GREEN_COLOR = tuple(map(int, config['Colors']['green_color'].split(',')))
RED_COLOR = tuple(map(int, config['Colors']['red_color'].split(',')))
PINK_COLOR = tuple(map(int, config['Colors']['pink_color'].split(',')))
ORANGE_COLOR = tuple(map(int, config['Colors']['orange_color'].split(',')))
WHITE_COLOR = tuple(map(int, config['Colors']['white_color'].split(',')))
YELLOW_COLOR = tuple(map(int, config['Colors']['yellow_color'].split(',')))
PURPLE_COLOR = tuple(map(int, config['Colors']['purple_color'].split(',')))
TRANSPARENT_COLOR = tuple(map(int, config['Colors']['transparent_color'].split(',')))

# Đọc các hằng số từ section [Constants]
THRESHOLD_VALUE = int(config['Constants']['threshold_value'])
A = int(config['Constants']['a'])
HEIGHT_AREA = int(config['Constants']['height_area'])
HEIGHT_3RD_AREA = int(config['Constants']['height_3rd_area'])
WIDTH_3RD_AREA = int(config['Constants']['width_3rd_area'])
LINE_THINESS = int(config['Constants']['line_thiness'])
CONF_TEMPLATE = float(config['Constants']['conf_template'])
CONF_1 = float(config['Constants']['conf_1'])
CONF_2 = float(config['Constants']['conf_2'])
CONF_3 = float(config['Constants']['conf_3'])
CONF_4 = float(config['Constants']['conf_4'])

# Đọc các đường dẫn từ section [Paths]
TEMPLATE_PATH = config['Paths']['template_path']
OUTPUT_IMAGE_DIR = config['Paths']['output_image_dir']

# Mở camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0 là camera mặc định, có thể thay bằng 1, 2,... nếu có nhiều camera

if not cap.isOpened():
    print("Không thể mở camera. Vui lòng kiểm tra thiết bị.")
    exit()

# Đọc khung hình đầu tiên để khởi tạo
ret, frame = cap.read()
if not ret:
    print("Không thể đọc khung hình từ camera.")
    cap.release()
    exit()

# Đọc template từ đường dẫn trong config
temp_L = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)

# Biến để lưu kết quả xử lý
processed_img_display = None

def process_image(img, temp, threshold, thresh_val):
    pt = False
    w, h = temp.shape[::-1]
    top_left = (0, 0)
    bottom_right = (0, 0)
    red_top_left = (0, 0)
    red_bottom_right = (0, 0)
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray, temp, cv2.TM_CCOEFF_NORMED)
    _, maxval, _, maxloc = cv2.minMaxLoc(res)
    
    if maxval > threshold:
        print("Max Value:", maxval)
        top_left = maxloc
        bottom_right = (maxloc[0] + w, maxloc[1] + h)
        red_top_left = (top_left[0], bottom_right[1] + A)
        red_bottom_right = (bottom_right[0], bottom_right[1] + A + HEIGHT_AREA)
        pt = True
    
    return pt, top_left, bottom_right, red_top_left, red_bottom_right

def crop_image(img, top_left, bottom_right):
    y1 = max(0, top_left[1])
    y2 = min(img.shape[0], bottom_right[1])
    x1 = max(0, top_left[0])
    x2 = min(img.shape[1], bottom_right[0])
    return img[y1:y2, x1:x2]

def crop_by_regions(img, w):
    right_top_left = (img.shape[1] - w, 0)
    right_bottom_right = (img.shape[1], img.shape[0])
    right_region = crop_image(img, right_top_left, right_bottom_right)
    return right_region

def handle_thresh(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    return thresh

def calc_percent_white_px(image):
    thresh = handle_thresh(image)
    white_area = cv2.countNonZero(thresh)
    total_area = thresh.shape[0] * thresh.shape[1]
    white_ratio = (white_area / total_area) * 100
    return white_ratio, thresh

def toggle_color(value, condition):
    return GREEN_COLOR if value > condition else RED_COLOR

def crop_regions(img_display, origin, top_left, bottom_right, red_top_left, red_bottom_right):
    red_region = crop_image(origin, red_top_left, red_bottom_right)
    
    white_top_left = (top_left[0], bottom_right[1] + A)
    white_bottom_right = (bottom_right[0], bottom_right[1] + A + HEIGHT_3RD_AREA)
    white_region = crop_image(origin, white_top_left, white_bottom_right)
    
    red_width = red_bottom_right[0] - red_top_left[0]
    half_width = red_width // 2
    
    red_left_top = (red_top_left[0], red_top_left[1])
    red_left_bottom = (red_top_left[0] + half_width, red_bottom_right[1])
    red_right_top = (red_top_left[0] + half_width, red_top_left[1])
    red_right_bottom = (red_bottom_right[0], red_bottom_right[1])
    
    area_3rd_width = white_bottom_right[0] - white_top_left[0]
    third_crop_top_left = (white_top_left[0] + area_3rd_width - WIDTH_3RD_AREA, white_top_left[1])
    third_crop_bottom_right = (white_bottom_right[0], white_bottom_right[1])
    area_3rd_crop = crop_by_regions(white_region, WIDTH_3RD_AREA)
    
    red_left = crop_image(origin, red_left_top, red_left_bottom)
    red_right = crop_image(origin, red_right_top, red_right_bottom)
    
    # Xử lý ngưỡng
    red_left_thresh = handle_thresh(red_left)
    red_right_thresh = handle_thresh(red_right)
    red_thresh = handle_thresh(red_region)
    white_thresh = handle_thresh(area_3rd_crop)
    
    # Tính tỷ lệ trắng
    percent_s_red, _ = calc_percent_white_px(red_region)
    left_percent, _ = calc_percent_white_px(red_left)
    right_percent, _ = calc_percent_white_px(red_right)
    percent_3rd, _ = calc_percent_white_px(area_3rd_crop)
    
    # Vẽ các hình chữ nhật lên img_display
    if left_percent <= CONF_2:
        cv2.rectangle(img_display, red_left_top, red_left_bottom, RED_COLOR, LINE_THINESS)
    if right_percent <= CONF_3:
        cv2.rectangle(img_display, red_right_top, red_right_bottom, RED_COLOR, LINE_THINESS)
    if percent_3rd <= CONF_4:
        cv2.rectangle(img_display, third_crop_top_left, third_crop_bottom_right, RED_COLOR, LINE_THINESS)
    
    print('s red: ', percent_s_red)
    print("s left: ", left_percent)
    print("s right: ", right_percent)
    print("s 3rd: ", percent_3rd)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    line_spacing = 30
    
    text_start_x = 10
    text_start_y = 30
    
    cv2.putText(img_display, f"area 1: {left_percent:.2f}%", (text_start_x, text_start_y + line_spacing), 
                font, font_scale, toggle_color(left_percent, CONF_2), thickness)
    cv2.putText(img_display, f"area 2: {right_percent:.2f}%", (text_start_x, text_start_y + 2 * line_spacing), 
                font, font_scale, toggle_color(right_percent, CONF_3), thickness)
    cv2.putText(img_display, f"area 3: {percent_3rd:.2f}%", (text_start_x, text_start_y + 3 * line_spacing), 
                font, font_scale, toggle_color(percent_3rd, CONF_4), thickness)
    
    # Hiển thị các vùng
    cv2.imshow("Red Region Full", cv2.resize(red_region, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Left", cv2.resize(red_left, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Right", cv2.resize(red_right, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("3rd Region", cv2.resize(area_3rd_crop, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    
    cv2.imshow("Red Region Left Thresh", cv2.resize(red_left_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Right Thresh", cv2.resize(red_right_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Thresh", cv2.resize(red_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("3rd Region Thresh", cv2.resize(white_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    
    return img_display

def update_threshold(val):
    global THRESHOLD_VALUE
    THRESHOLD_VALUE = val
    print(f"Threshold: {THRESHOLD_VALUE}")

# Tạo cửa sổ và trackbar
cv2.namedWindow("Camera")  # Cửa sổ để hiển thị luồng video từ camera
cv2.namedWindow("Result")  # Cửa sổ để hiển thị kết quả xử lý
cv2.createTrackbar("Threshold", "Result", THRESHOLD_VALUE, 255, update_threshold)

# Đảm bảo thư mục lưu ảnh tồn tại
if not os.path.exists(OUTPUT_IMAGE_DIR):
    os.makedirs(OUTPUT_IMAGE_DIR)

# Vòng lặp chính để đọc và hiển thị luồng video từ camera
while True:
    # Đọc khung hình từ camera
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình từ camera.")
        break
    
    # Hiển thị luồng video gốc trên cửa sổ "Camera"
    cv2.imshow("Camera", frame)
    
    # Nếu đã xử lý trước đó, hiển thị kết quả trên cửa sổ "Result"
    if processed_img_display is not None:
        cv2.imshow("Result", processed_img_display)
    
    # Chờ phím bấm
    key = cv2.waitKey(1) & 0xFF
    
    # Nhấn phím cách (space) để xử lý khung hình hiện tại
    if key == 32:  # 32 là mã ASCII của phím cách
        origin = frame.copy()
        img_display = origin.copy()
        pt, top_left, bottom_right, red_top_left, red_bottom_right = process_image(img_display, temp_L, CONF_TEMPLATE, THRESHOLD_VALUE)
        mytime = time.time()
        cv2.imwrite(os.path.join(OUTPUT_IMAGE_DIR, f"{mytime}.png"), frame)
        
        if pt:
            processed_img_display = crop_regions(img_display, origin, top_left, bottom_right, red_top_left, red_bottom_right)
            cv2.imshow("Result", processed_img_display)  # Hiển thị kết quả trên cửa sổ "Result"
        else:
            print('Không tìm thấy template')
            processed_img_display = origin.copy()  # Hiển thị khung hình gốc nếu không tìm thấy template
            cv2.imshow("Result", processed_img_display)
    
    # Thoát nếu nhấn phím ESC
    if key == 27:
        break

# Giải phóng camera và đóng tất cả cửa sổ
cap.release()
cv2.destroyAllWindows()