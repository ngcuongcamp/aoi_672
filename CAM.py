from GUI import MainUi
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication,)
from PyQt5.QtCore import Qt
from Serial_Thread import Serial_Thread
from Camera_Thread import Camera_Thread
import cv2
from ImageProcessor import ImageProcessor
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
        print(stime)
        
        if data in [1,"1"]:
            # self.origin_image = cv2.imread(r'./data/temp/2f_black_3.png')
            self.origin_image = cv2.imread(PATH_IMAGE_TEST)
            self.Processor = ImageProcessor(self.origin_image, self)
            draw_frame = self.Processor.image_handler()
            
            if draw_frame is not None: 
            
                self.handle_update_frame(self.origin_image)
                self.handle_update_frame_result(draw_frame)
                
                self.IS_DISPLAY_RESULT =  self.config['SETTING']['IS_DISPLAY_RESULT']
                if self.IS_DISPLAY_RESULT == 1: 
                    cv2.imshow("Result", draw_frame)
                    
                print(f"Time: {time.time() - stime} seconds")
            else:
                print("Failed to process image")
    def handle_connect_error(self):
        print("Connection Error: ")
                
    
    def run(self):
        """Run the application."""
        self.window.showMaximized()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = MainApp()
    app.run()