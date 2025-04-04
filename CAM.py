import cv2
from GUI import MainUi
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication,)
from PyQt5.QtCore import Qt
from Serial_Thread import Serial_Thread
from Camera_Thread import Camera_Thread
from ProcessImagePoint_1 import ProcessImagePoint_1
from ProcessImagePoint_2 import ProcessImagePoint_2
from ProcessImagePoint_3 import ProcessImagePoint_3
import time
from ultils import *

class MainApp: 
    def __init__(self): 
        # init Ui 
        self.app = QApplication(sys.argv)
        self.window = MainUi()
        
        # variables 
        self.origin_image = None 
        self.display_image = None
        
        # read config 
        self.config = load_config()
        
        # init serial connect 
        self.PLC = Serial_Thread(self.config["SERIAL"]["COM_PLC"], self.config["SERIAL"]["BAUDRATE_PLC"], 0.09)
        self.PLC.error_signal.connect(self.handle_connect_error)
        self.PLC.data_received.connect(self.handle_data_received)
        self.PLC.start()
        
        # init camera 
        self.CAMERA = Camera_Thread(self.config["CAMERA"]["IDC"])
        self.CAMERA.frame_received.connect(self.handle_frame_received)
        self.CAMERA.start()
    
    def handle_frame_received(self, frame):
        self.origin_image = frame
        # frame = frame.rotate
        
        self.IS_DISPLAY_FRAME =  self.config['SETTING']['IS_DISPLAY_FRAME']
        if self.IS_DISPLAY_FRAME == 1: 
            cv2.imshow("camera", frame)
    
    def handle_update_frame(self, frame): 
        # rotate 
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_frame.shape
        bytes_per_line = channel * width
        q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.window.camera_label.setPixmap(pixmap.scaled(
            self.window.camera_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.window.camera_label.setAlignment(Qt.AlignCenter)

    
    def handle_update_frame_result(self, frame): 
        # rotate 
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = rgb_frame.shape
        bytes_per_line = channel * width
        q_image = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.window.image_label.setPixmap(pixmap.scaled(
            self.window.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        ))
        self.window.image_label.setAlignment(Qt.AlignCenter)
    
    
    def handle_data_received(self,data):
        stime = time.time()
        
        if data in [1,"1"]:
            selected_color = self.window.combobox.currentText()
            
            THRESH_VALUE = load_market_data()[selected_color]['THRESH_VALUE']
            TEMPLATE_POINT_1ST = load_market_data()[selected_color]['TEMPLATE_POINT_1ST']
            TEST_IMAGE = load_market_data()[selected_color]['IMAGE_TEST']
            
            self.origin_image = cv2.imread(TEST_IMAGE)
            Processor_1 = ProcessImagePoint_1(self.origin_image, self, thresh=THRESH_VALUE, template_path=TEMPLATE_POINT_1ST)
            
            draw_frame = Processor_1.image_handler()
            
            if draw_frame is not None: 
                self.handle_update_frame(self.origin_image)
                self.handle_update_frame_result(draw_frame)
                
                self.IS_DISPLAY_RESULT =  self.config['SETTING']['IS_DISPLAY_RESULT']
                if self.IS_DISPLAY_RESULT == 1: 
                    cv2.imshow("Result", draw_frame)
                    
                print(f"Time: {time.time() - stime} seconds")
            else:
                print("Failed to process image")
        if data in [2, "2"]:
            selected_color = self.window.combobox.currentText()
            TEST_IMAGE = load_market_data()[selected_color]['IMAGE_TEST']
            self.origin_image = cv2.imread(TEST_IMAGE)
            Processor_2 = ProcessImagePoint_2(self.origin_image, self,selected_color)
            is_break_line, is_overflow_top=Processor_2.image_handler()
            
            print('is_break_line: ', is_break_line)
            print('is_overflow_top: ', is_overflow_top)
        
        if data in [3, "3"]: 
            selected_color = self.window.combobox.currentText()
            TEST_IMAGE = load_market_data()[selected_color]['IMAGE_TEST']
            self.origin_image = cv2.imread(TEST_IMAGE)
            Processor_3 = ProcessImagePoint_3(self.origin_image, self,selected_color)
            
            Processor_3.image_handler()
            
    def handle_connect_error(self):
        print("Connection Error: ")
                
    
    def run(self):
        """Run the application."""
        self.window.showMaximized()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = MainApp()
    app.run()