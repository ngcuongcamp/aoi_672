from GUI import MainUi
import sys
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication,)
from PyQt5.QtCore import Qt
import json
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
        
        cv2.imshow("camera", frame)
    
    def handle_update_frame(self): 
        # frame = cv2.imread(r'D:\NguyenCuong\1A\FT672\img_2103\img\dataset_ng_white\14.png')
        # frame = cv2.imread(r'C:\Users\V3109024\Downloads\img_l\2.png')
        frame = cv2.imread(r'D:\NguyenCuong\1A\FT672\img_2103\img\dataset_ng_white\NG (2).png')
        
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
            self.origin_image = cv2.imread(r'./data/temp/2f_black_2.png')
            self.Processor = ImageProcessor(self.origin_image, self)
            self.Processor.image_handler()
            
    
    def handle_connect_error(self):
        print("Connection Error: ")
                
    
    def modify_config(self): 
        """Lưu config vào file JSON"""
        path = './data/configs/config.json'
        try:
            with open(path, "w") as f:
                json.dump(self.config, f, indent=4)
            print(f"Đã lưu config vào {path}")
        except Exception as e:
            print(f"Lỗi khi lưu config: {e}")
                
    
    def modify_and_save_config(self, key, value):
        """Modify config based on key and value, then save it"""
        try:
            # Split the key into section and subkey (e.g., "SETTING.THRESH_VALUE" -> "SETTING" and "THRESH_VALUE")
            section, subkey = key.split(".")
            if section in self.config and subkey in self.config[section]:
                old_value = self.config[section][subkey]
                self.config[section][subkey] = value
                print(f"Changed {key} from {old_value} to {value}")
                self.modify_config()  # Save the config file
            else:
                print(f"Key {key} does not exist in config")
        except ValueError:
            print(f"Key {key} is not in the correct 'SECTION.SUBKEY' format")
        except Exception as e:
            print(f"Error modifying config: {e}")
    
    def run(self):
        """Run the application."""
        self.window.showMaximized()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    app = MainApp()
    app.run()