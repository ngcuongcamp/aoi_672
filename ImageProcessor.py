from ultils import *
import cv2

class ImageProcessor: 
    def __init__(self, image,  config_ref):
        self.main_ref = config_ref
        self.origin_img = image 
        self.draw_img = image 
        self.config = load_config()
        self.OFFSET_TRANSLATE_Y = self.config["SETTING"]["OFFSET_TRANSLATE_Y"]
        self.HEIGHT_3RD_AREA = self.config["SETTING"]["HEIGHT_3RD_AREA"]
        self.HEIGHT_AREA = self.config["SETTING"]["HEIGHT_AREA"]
        self.WIDTH_3RD_AREA =self.config["SETTING"]["WIDTH_3RD_AREA"]
        
        
        # get template image 
        self.template_image = cv2.imread(PATH_TEMPLATE,cv2.IMREAD_GRAYSCALE)
        cv2.imshow('temp', self.template_image)
        
        # variables
        self.is_matching = False
        
    
    def image_handler(self): 
        """main function hanlder"""
        try: 
            maxloc = self.detect_matching()
            print('maxlog', maxloc)
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
                fglue_img = self.crop_image(fglue_top_left, fglue_bottom_right)
                
                
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
                area_3rd_crop_img = self.crop_by_regions(area_3rd_img, self.WIDTH_3RD_AREA)
                
                
                cv2.imshow("Red Region Full", fglue_img)
                cv2.imshow("Red Region Left", fglue_left_img)
                cv2.imshow("Red Region Right", fglue_right_img)
                
                cv2.imshow("White 3rd Region", area_3rd_img)
                cv2.imshow("3rd Region", area_3rd_crop_img)
                
                
                
        except Exception as E: 
            print(f'Error when run main function hanlder: {E}')
            return None
    def crop_by_regions(self,img, w):
        right_top_left = (img.shape[1] - w, 0)
        right_bottom_right = (img.shape[1], img.shape[0])
        right_region = self.crop_image( right_top_left, right_bottom_right)
        return right_region
    
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
        if maxval > self.config['SETTING']['CONF_TEMPLATE']: 
            self.is_matching = True
            return maxloc
        else:
            return None