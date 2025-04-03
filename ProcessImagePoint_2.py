from ultils import *
import cv2
import numpy as np

class ProcessImagePoint_2: 
    def __init__(self, image,  config_ref, color):
        self.main_ref = config_ref
        self.origin_img = image.copy()
        self.draw_img = image.copy()
        self.process_config = load_market_data()
        self.is_matching = False
        self.color = color
        self.template_path = self.process_config[self.color]["TEMPLATE_POINT_2RD"]
        self.TEMPLATE_POINT_2RD = cv2.imread(self.template_path, cv2.IMREAD_GRAYSCALE)
        self.BLUE_H_MIN = self.process_config[self.color]["BLUE_H_MIN"]
        self.BLUE_H_MAX = self.process_config[self.color]["BLUE_H_MAX"]
        self.BLUE_S_MIN = self.process_config[self.color]["BLUE_S_MIN"]
        self.BLUE_S_MAX = self.process_config[self.color]["BLUE_S_MAX"]
        self.BLUE_V_MIN = self.process_config[self.color]["BLUE_V_MIN"]
        self.BLUE_V_MAX = self.process_config[self.color]["BLUE_V_MAX"]
        self.WHITE_S_MAX = self.process_config[self.color]["WHITE_S_MAX"]
        self.WHITE_V_MIN = self.process_config[self.color]["WHITE_V_MIN"]
        self.CONF_POINT_2RD = self.process_config[self.color]['CONF_POINT_2RD']
        self.HEIGHT_TOP_2RD = self.process_config[self.color]['HEIGHT_TOP_2RD']
        
        self.is_break_line = False
        self.is_overflow_glue = False
        
    
    def image_handler(self): 
        """main function hanlder"""
        try: 
            max_loc = self.detect_matching()
            if max_loc is not None:
                # cut and reivew here
                top_left = max_loc
                h, w = self.TEMPLATE_POINT_2RD.shape
                
                detected_image = self.origin_img[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]
                
                cv2.imshow('detected_image: ', detected_image)
                
                if detected_image is not None: 
                    group1_mask, group1_result = self.filter_glue_hsv(crop_image=detected_image)
                    
                    cv2.imshow('group_mask', group1_mask)
                    cv2.imshow('group1_result', group1_result)
                    
                    
                    is_break_line, heights = self.check_break_glue(group1_mask)
                    
                    self.is_break_line = is_break_line
                    
                    if is_break_line is False: 
                        height_object = heights[0]
                        # image height 
                        height, width = group1_mask.shape
                        height_top_area = height - height_object
                        
                        if height_top_area < self.HEIGHT_TOP_2RD: 
                            print("tràn keo đầu")
                            self.is_overflow_glue = True
                        
                
                return self.is_break_line, self.is_overflow_glue
                
        except Exception as E: 
            print(f'Error when run main function hanlder: {E}')
            return None
    
    
    
    def filter_glue_hsv(self, crop_image): 
        hsv = cv2.cvtColor(crop_image, cv2.COLOR_BGR2HSV)
        # define blue area
        lower_blue = np.array([self.BLUE_H_MIN, self.BLUE_S_MIN, self.BLUE_V_MIN])
        upper_blue = np.array([self.BLUE_H_MAX, self.BLUE_S_MAX, self.BLUE_V_MAX])
        
        # define white area 
        lower_white = np.array([0, 0, self.WHITE_V_MIN])
        upper_white = np.array([179, self.WHITE_S_MAX, 255])
        
        # create mask for each area 
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        white_mask = cv2.inRange(hsv, lower_white, upper_white)

        group1_mask = cv2.bitwise_or(blue_mask, white_mask)
        group1_result = cv2.bitwise_and(crop_image, crop_image, mask=group1_mask)
        
        # write image 
        cv2.imwrite(f'./data/templates/{self.color}/group1_result.png', group1_result)
        cv2.imwrite(f'./data/templates/{self.color}/group1_mask.png', group1_mask)
        
        return group1_mask, group1_result

    def check_break_glue(self, binary_image): 
        is_break = False
        
        _, binary = cv2.threshold(binary_image, 127, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
        
        # Tìm các thành phần liên thông
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary, connectivity=8)
        min_area = 10
        
        # Lọc các thành phần lớn dựa trên diện tích và đo chiều cao
        valid_components = 0
        heights = []
        for i in range(1, num_labels):  # Bỏ qua nền (label 0)
            area = stats[i, cv2.CC_STAT_AREA]  # Diện tích của thành phần
            if area >= min_area:
                valid_components += 1
                height = stats[i, cv2.CC_STAT_HEIGHT]  # Chiều cao của thành phần
                heights.append(height)
        if valid_components > 1: 
            is_break = True
        else: 
            is_break = False
            
        return is_break, heights
            
    def detect_matching(self): 
        # convert frame to gray frame 
        gray_frame = cv2.cvtColor(self.origin_img, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('test1',gray_frame)
        cv2.imshow('test2',self.TEMPLATE_POINT_2RD)
        
        # detect matching area 
        res = cv2.matchTemplate(gray_frame, self.TEMPLATE_POINT_2RD, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # if confidence value is greater than conf_template value
        print('ti le giong: ', max_val)
        if max_val > self.CONF_POINT_2RD: 
            self.is_matching = True
            return max_loc
        else:
            return None
    
    
    