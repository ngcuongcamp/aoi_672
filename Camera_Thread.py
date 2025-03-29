from PyQt5.QtCore import pyqtSignal, Qt, QThread
import cv2
import numpy as np


class Camera_Thread(QThread):
    frame_received = pyqtSignal(np.ndarray)
    error_signal = pyqtSignal()

    def __init__(self, camera_id):
        super(Camera_Thread, self).__init__()
        self.is_running = True
        self.camera_id = camera_id
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        self.cap.set(cv2.CAP_PROP_SETTINGS, 1)

    def run(self):
        while self.is_running:
            try:
                ret, self.frame = self.cap.read()
                if ret:
                    self.frame_received.emit(self.frame)
                else:
                    self.error_signal.emit()
                    self.cap.release()
                    self.is_running = False
            except Exception as e:
                print("Camera Error: " + str(e))
                self.error_signal.emit()
                self.cap.release()
                self.is_running = False

    def stop(self):
        self.is_running = False
        self.requestInterruption()
        self.cap.release()
        self.quit()
