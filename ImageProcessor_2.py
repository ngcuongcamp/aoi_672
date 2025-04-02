from ultils import *
import cv2
import numpy as np

class ImageProcessor_2: 
    def __init__(self, image,  config_ref, thresh):
        self.main_ref = config_ref
        self.origin_img = image.copy()
        self.draw_img = image.copy()
        self.config = load_config()
        self.THRESH_VALUE = thresh
        print("Current thresh value: ", self.THRESH_VALUE)
        self.OFFSET_TRANSLATE_Y = self.config["SETTING"]["OFFSET_TRANSLATE_Y"]
        self.HEIGHT_3RD_AREA = self.config["SETTING"]["HEIGHT_3RD_AREA"]
        self.HEIGHT_AREA = self.config["SETTING"]["HEIGHT_AREA"]
        self.WIDTH_3RD_AREA =self.config["SETTING"]["WIDTH_3RD_AREA"]
        self.CONF_FGLUE = self.config["SETTING"]["CONF_FGLUE"]
        self.CONF_HPART_LEFT = self.config["SETTING"]["CONF_HPART_LEFT"]
        self.CONF_HPART_RIGHT = self.config["SETTING"]["CONF_HPART_RIGHT"]
        self.CONF_3RD = self.config["SETTING"]["CONF_3RD"]
        self.LINE_THINESS = self.config["SETTING"]["LINE_THINESS"]
        self.CONF_TEMPLATE =  self.config['SETTING']['CONF_TEMPLATE']
        
        
        # get template image 
        self.template_image = cv2.imread(PATH_TEMPLATE,cv2.IMREAD_GRAYSCALE)
        cv2.imshow('temp', self.template_image)
        
        # variables
        self.is_matching = False
        
    
    def image_handler(self): 
        """main function hanlder"""
        try: 
            maxloc = self.detect_matching()
            if maxloc is not None:
                if len(self.template_image.shape) == 2:  # Ảnh grayscale
                    h, w = self.template_image.shape
                else:  # Ảnh màu
                    h, w, _ = self.template_image.shape
                # w,h = self.template_image[::-1]
                top_left = (0, 0)
                bottom_right = (0, 0)
                fglue_top_left = (0, 0)
                fglue_bottom_right = (0, 0)
                
                top_left = maxloc
                bottom_right = (maxloc[0] + w, maxloc[1] + h)
                fglue_top_left =  (top_left[0], bottom_right[1] + self.OFFSET_TRANSLATE_Y)
                fglue_bottom_right = (bottom_right[0], bottom_right[1] + self.OFFSET_TRANSLATE_Y + self.HEIGHT_AREA)
                
                
                # cắt vùng vùng keo tiêu chuẩn (1)
                # fglue_img = self.crop_image(fglue_top_left, fglue_bottom_right)
                
                
                # xác định vùng keo trái/phải của vùng keo tiêu chuẩn (2,3)
                red_width = fglue_bottom_right[0] - fglue_top_left[0]
                half_width = red_width // 2
                
                fglue_left_top = (fglue_top_left[0], fglue_top_left[1])
                fglue_left_bottom = (fglue_top_left[0] + half_width, fglue_bottom_right[1])
                fglue_right_top = (fglue_top_left[0] + half_width, fglue_top_left[1])
                fglue_right_bottom = (fglue_bottom_right[0], fglue_bottom_right[1])
                fglue_left_img = self.crop_image(fglue_left_top, fglue_left_bottom)
                fglue_right_img = self.crop_image( fglue_right_top, fglue_right_bottom)
                
                # xác định tọa độ của vùng keo 3rd & cắt theo vùng 
                area_3rd_top_left = (top_left[0], bottom_right[1] +self.OFFSET_TRANSLATE_Y)
                area_3rd_bottom_right = (bottom_right[0], bottom_right[1] + self. OFFSET_TRANSLATE_Y+ self.HEIGHT_3RD_AREA)
                area_3rd_img = self.crop_image(area_3rd_top_left, area_3rd_bottom_right)
                
                # xác định tọa độ của vùng keo bên phải của vùng keo 3rd
                area_3rd_width_crop = area_3rd_bottom_right[0] - area_3rd_top_left[0]
                
                area_3rd_crop_top_left = (area_3rd_top_left[0] + area_3rd_width_crop - self.WIDTH_3RD_AREA, area_3rd_top_left[1])
                
                third_crop_bottom_right = (area_3rd_bottom_right[0], area_3rd_bottom_right[1])
                
                area_3rd_crop_img = self.crop_by_regions_right(area_3rd_img, self.WIDTH_3RD_AREA)
                
                area_left_side_img = self.crop_by_regions_left(fglue_left_img,20)
                
                cv2.imshow('test', area_left_side_img)
                
                
                
                # calc white px percent in image 
                # percent_s_fglue,thresh_fglue = self.calc_percent_white_px(fglue_img)
                percent_s_fglue_left,thresh_fglue_left = self.calc_percent_white_px(fglue_left_img)
                percent_s_fglue_right,thresh_fglue_right = self.calc_percent_white_px(fglue_right_img)
                percent_s_area_3rd_crop,thresh_3rd_crop = self.calc_percent_white_px(area_3rd_crop_img)
                
                # left_side_img = self.crop_by_regions_left(fglue_left_img, 10)
                # height_left_side, width_left_side = left_side_img.shape[:2]
                # top_height = 10
                
                # top_part = left_side_img[0:top_height, 0:width_left_side]
                # bottom_part = left_side_img[top_height:height_left_side, 0:width_left_side]
                
                # percent_left_side,_ = self.calc_percent_white_px(bottom_part)
                
                # print('test',percent_left_side)
                
                
                # draw rectangle on drawing image
                if percent_s_fglue_left < self.CONF_HPART_LEFT: 
                    cv2.rectangle(self.draw_img, fglue_left_top, fglue_left_bottom, RED_COLOR, self.LINE_THINESS)  # Nửa trái vùng đỏ
                if percent_s_fglue_right < self.CONF_HPART_RIGHT:
                    cv2.rectangle(self.draw_img, fglue_right_top, fglue_right_bottom, RED_COLOR, self.LINE_THINESS)  # Nửa phải vùng đỏ
                if percent_s_area_3rd_crop < self.CONF_3RD:
                    cv2.rectangle(self.draw_img, area_3rd_crop_top_left, third_crop_bottom_right, RED_COLOR, self.LINE_THINESS)
                    
                    
                
                # draw result  
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.7
                thickness = 2
                line_spacing = 40  # Khoảng cách giữa các dòng
                # Vị trí bắt đầu (góc trên bên trái)
                text_start_x = 20
                text_start_y = 40
                cv2.putText(self.draw_img, f"Area 1: {percent_s_fglue_left:.2f}%", (text_start_x, text_start_y + line_spacing), 
                    font, font_scale, self.toggle_color(percent_s_fglue_left, self.CONF_HPART_LEFT), thickness)
                cv2.putText(self.draw_img, f"Area 2: {percent_s_fglue_right:.2f}%", (text_start_x, text_start_y + 2 * line_spacing), 
                            font, font_scale, self.toggle_color(percent_s_fglue_right, self.CONF_HPART_RIGHT), thickness)
                cv2.putText(self.draw_img, f"Area 3: {percent_s_area_3rd_crop:.2f}%", (text_start_x, text_start_y + 3 * line_spacing), 
                            font, font_scale, self.toggle_color(percent_s_area_3rd_crop, self.CONF_3RD), thickness)
                
                
                if percent_s_fglue_left >= self.CONF_HPART_LEFT and percent_s_fglue_right >= self.CONF_HPART_RIGHT and percent_s_area_3rd_crop >= self.CONF_3RD: 
                    cv2.putText(self.draw_img, f"OK", (text_start_x, text_start_y + 6 * line_spacing), 
                            font, font_scale + 2, GREEN_COLOR, thickness)
                else: 
                    cv2.putText(self.draw_img, f"NG", (text_start_x, text_start_y + 6 * line_spacing), 
                            font, font_scale + 2, RED_COLOR, thickness)
                
                
                
                # display results
                # cv2.imshow('draw',self.draw_img)
                
                # # cv2.imshow("Region 1", fglue_img)
                cv2.imshow("Region 2", fglue_left_img)
                cv2.imshow("Region 3", fglue_right_img)
                cv2.imshow("Region 4", area_3rd_crop_img)
                
                
                # cv2.imshow("Thresh Area 1 ", cv2.resize(thresh_fglue, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
                cv2.imshow("Thresh Area 1", cv2.resize(thresh_fglue_left, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
                cv2.imshow("Thresh Area 2", cv2.resize(thresh_fglue_right, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
                cv2.imshow("Thresh Area 3", cv2.resize(thresh_3rd_crop, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR))
                
                # return draw image
                return self.draw_img
            
                
                
                
                
        except Exception as E: 
            print(f'Error when run main function hanlder: {E}')
            return None
    
    def crop_by_regions_right(self, img, w):
    # Tính tọa độ phần bên phải của ảnh đầu vào (img)
        right_top_left = (img.shape[1] - w, 0)  # x = chiều rộng ảnh - w, y = 0
        right_bottom_right = (img.shape[1], img.shape[0])  # x = chiều rộng ảnh, y = chiều cao ảnh
        
        # Cắt trực tiếp từ img thay vì từ self.origin_img
        y1 = right_top_left[1]
        y2 = right_bottom_right[1]
        x1 = right_top_left[0]
        x2 = right_bottom_right[0]
        
        return img[y1:y2, x1:x2]

    def crop_by_regions_left(self,img, w):
        # Điểm bắt đầu: góc trên bên trái (0, 0)
        top_left = (0, 0)
        # Điểm kết thúc: x = w, y = chiều cao ảnh
        bottom_right = (w, img.shape[0])
        # Cắt vùng từ trái
        left_region = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        return left_region
    
    def crop_image(self, top_left, bottom_right): 
        """crop image"""
        y1 = max(0, top_left[1])
        y2 = min(self.origin_img.shape[0], bottom_right[1])
        x1 = max(0, top_left[0])
        x2 = min(self.origin_img.shape[1], bottom_right[0])
        return self.origin_img[y1:y2, x1:x2]
    
    
    def detect_matching(self): 
        # convert frame to gray frame 
        gray_frame = cv2.cvtColor(self.origin_img, cv2.COLOR_BGR2GRAY)
        # detect matching area 
        res = cv2.matchTemplate(gray_frame, self.template_image, cv2.TM_CCOEFF_NORMED)
        _, maxval, _, maxloc = cv2.minMaxLoc(res)
        # if confidence value is greater than conf_template value
        print('Ti le giong template: ', maxval)
        if maxval > self.CONF_TEMPLATE: 
            self.is_matching = True
            return maxloc
        else:
            return None
    
    def toggle_color(self,value, condition):
        return GREEN_COLOR if value > condition else RED_COLOR

    def toggle_rectangle_draw(value, condition):
        return GREEN_COLOR if value > condition else RED_COLOR 
    
        
    
    def calc_percent_white_px(self,image):
        thresh = self.useThresh(image)
        white_area = cv2.countNonZero(thresh)
        total_area = thresh.shape[0] * thresh.shape[1]
        white_ratio = (white_area / total_area) * 100
        return white_ratio, thresh
    
    def useThresh(self, image): 
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(gray, self.THRESH_VALUE, 255, cv2.THRESH_BINARY)
        return thresh
    
    