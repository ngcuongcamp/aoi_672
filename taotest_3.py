import cv2

# Đường dẫn đến ảnh đầu vào
path = r"D:\NguyenCuong\1A\FT672\data\temp\f_black_2.png"
# temp_L = cv2.imread(r"D:\NguyenCuong\1A\FT672\data\temp\temp_black_2.png", cv2.IMREAD_GRAYSCALE)
temp_L = cv2.imread(r"D:\NguyenCuong\1A\FT672\data\temp\temp_black.png", cv2.IMREAD_GRAYSCALE)

green_color = (0, 255, 0)
red_color = (0,0,255)
red_color = (0, 0, 255)
pink_color = (255, 0, 255)
orange_color = (0, 165, 255)
white_color = (255, 255, 255)
yellow_color = (0, 255, 255)
purple_color = (255, 0, 128)
transparent_color = (0, 0, 0, 0)

THRESHOLD_VALUE = 11
A = -2
HEIGHT_AREA = 33
HEIGHT_3RD_AREA = 38
WIDTH_3RD_AREA = 32
LINE_THINESS = 1
CONF_TEMPLATE = 0.95
CONF_1 = 97.5
CONF_2 = 97.5
CONF_3 = 97.5
CONF_4 = 97.5


image = cv2.imread(path)
origin = image.copy()
img_display = origin.copy()

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

def crop_regions(img_display, origin, top_left, bottom_right, red_top_left, red_bottom_right):
    # Cắt các vùng từ ảnh gốc (origin)
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
    
    # Vẽ các hình chữ nhật lên img_display (không ảnh hưởng đến ảnh gốc)
    # cv2.rectangle(img_display, top_left, bottom_right, green_color, 2)  # Vùng xanh
    # if percent_s_red <= CONF_1:  # Chỉ vẽ nếu không "trong suốt"
    #     cv2.rectangle(img_display, red_top_left, red_bottom_right, white_color, LINE_THINESS)  # Vùng đỏ
    if left_percent <= CONF_2:
        cv2.rectangle(img_display, red_left_top, red_left_bottom, red_color, LINE_THINESS)  # Nửa trái vùng đỏ
    if right_percent <= CONF_3:
        cv2.rectangle(img_display, red_right_top, red_right_bottom, red_color, LINE_THINESS)  # Nửa phải vùng đỏ
    if percent_3rd <= CONF_4:
        cv2.rectangle(img_display, third_crop_top_left, third_crop_bottom_right, red_color, LINE_THINESS)  # Vùng thứ 3
    
    # cv2.rectangle(img_display, red_left_top, red_left_bottom, toggle_rectangle_draw(left_percent, CONF_2), LINE_THINESS)  
    # cv2.rectangle(img_display, red_right_top, red_right_bottom, toggle_rectangle_draw(right_percent, CONF_3), LINE_THINESS)  
    # cv2.rectangle(img_display, third_crop_top_left, third_crop_bottom_right, toggle_rectangle_draw(percent_3rd, CONF_4), LINE_THINESS)  
 
    
    
    print('s red: ', percent_s_red)
    print("s left: ", left_percent)
    print("s right: ", right_percent)
    print("s 3rd: ", percent_3rd)
    
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    line_spacing = 30  # Khoảng cách giữa các dòng
    
    # Vị trí bắt đầu (góc trên bên trái)
    text_start_x = 10
    text_start_y = 30
    
    
    # cv2.putText(img_display, f"area 1: {percent_s_red:.2f}%", (text_start_x, text_start_y), font, font_scale, toggle_color(percent_s_red,CONF_1), thickness)
    
    cv2.putText(img_display, f"area 1: {left_percent:.2f}%", (text_start_x, text_start_y + line_spacing), 
                font, font_scale, toggle_color(left_percent, CONF_2), thickness)
    cv2.putText(img_display, f"area 2: {right_percent:.2f}%", (text_start_x, text_start_y + 2 * line_spacing), 
                font, font_scale, toggle_color(right_percent, CONF_3), thickness)
    cv2.putText(img_display, f"area 3: {percent_3rd:.2f}%", (text_start_x, text_start_y + 3 * line_spacing), 
                font, font_scale, toggle_color(percent_3rd, CONF_4), thickness)
    
    # # Hiển thị các vùng
    # cv2.imshow("Red Region Full", red_region)
    # cv2.imshow("Red Region Left", red_left)
    # cv2.imshow("Red Region Right", red_right)
    # cv2.imshow("3rd Region", area_3rd_crop)
    
    # cv2.imshow("Red Region Left Thresh", red_left_thresh)
    # cv2.imshow("Red Region Right Thresh", red_right_thresh)
    # cv2.imshow("Red Region Thresh", red_thresh)
    # cv2.imshow("3rd Region Thresh", white_thresh)
    
    # # Hiển thị ảnh với các hình chữ nhật
    cv2.imshow("Result", img_display)
    
    cv2.imshow("Red Region Full", cv2.resize(red_region, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Left", cv2.resize(red_left, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Right", cv2.resize(red_right, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("3rd Region", cv2.resize(area_3rd_crop, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))

    cv2.imshow("Red Region Left Thresh", cv2.resize(red_left_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Right Thresh", cv2.resize(red_right_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("Red Region Thresh", cv2.resize(red_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
    cv2.imshow("3rd Region Thresh", cv2.resize(white_thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))

    # Hiển thị ảnh với các hình chữ nhật (resize gấp 2 lần)

def update_threshold(val):
    global THRESHOLD_VALUE, img_display, temp_L, origin, A
    THRESHOLD_VALUE = val
    img_display = origin.copy()
    pt, top_left, bottom_right, red_top_left, red_bottom_right = process_image(img_display, temp_L, 0.95, THRESHOLD_VALUE)
    print(f"Threshold: {THRESHOLD_VALUE}")
    
    if pt:
        crop_regions(img_display, origin, top_left, bottom_right, red_top_left, red_bottom_right)
    else:
        print('Khong tim thay template')

def calc_percent_white_px(image):
    thresh = handle_thresh(image)
    white_area = cv2.countNonZero(thresh)
    total_area = thresh.shape[0] * thresh.shape[1]
    white_ratio = (white_area / total_area) * 100
    return white_ratio, thresh

def handle_thresh(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(gray, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
    return thresh

def toggle_color(value, condition):
    return green_color if value > condition else red_color

def toggle_rectangle_draw(value, condition):
    return green_color if value > condition else red_color 

cv2.namedWindow("Result")
cv2.createTrackbar("Threshold", "Result", THRESHOLD_VALUE, 255, update_threshold)

pt, top_left, bottom_right, red_top_left, red_bottom_right = process_image(img_display, temp_L, CONF_TEMPLATE, THRESHOLD_VALUE)

if pt:
    crop_regions(img_display, origin, top_left, bottom_right, red_top_left, red_bottom_right)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break

cv2.destroyAllWindows()