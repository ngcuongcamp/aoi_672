from ultils import *
import cv2
import numpy as np

class ProcessImagePoint_3: 
    def __init__(self, image,  config_ref, color):
        self.main_ref = config_ref
        self.origin_img = image.copy()
        self.draw_img = image.copy()
        self.color = color
        
        self.process_config = load_market_data()
        
        self.TEMPLATE_POINT_3RD =  cv2.imread(self.process_config[self.color]["TEMPLATE_POINT_3RD"], cv2.IMREAD_GRAYSCALE)
        self.TEMPLATE_POINT_4TH =  cv2.imread(self.process_config[self.color]["TEMPLATE_POINT_4TH"], cv2.IMREAD_GRAYSCALE)
        
        self.CONF_POINT_3AND4 =  self.process_config[color]['CONF_POINT_3AND4']
        
        
        self.is_matching_3rd = False
        self.is_matching_4th = False
        
        
    
    def image_handler(self): 
        """main function hanlder"""
        try: 
            max_loc = self.detect_matching(self.TEMPLATE_POINT_3RD, self.CONF_POINT_3AND4)
            if max_loc is not None:
                # cut and reivew here
                top_left = max_loc
                h, w = self.TEMPLATE_POINT_3RD.shape
                
                detected_image = self.origin_img[top_left[1]:top_left[1] + h, top_left[0]:top_left[0] + w]
                
                cv2.imshow('detected_image: ', detected_image)
                
                
                
        except Exception as E: 
            print(f'Error when run main function hanlder: {E}')
            return None
    
            
    def detect_matching(self, template_image, conf_template): 
        # convert frame to gray frame 
        gray_frame = cv2.cvtColor(self.origin_img, cv2.COLOR_BGR2GRAY)
        
        # detect matching area 
        res = cv2.matchTemplate(gray_frame, template_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # if confidence value is greater than conf_template value
        print('ti le giong: ', max_val)
        if max_val > conf_template: 
            self.is_matching = True
            return max_loc
        else:
            return None
    
    
    