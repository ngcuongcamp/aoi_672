from PyQt5.QtCore import pyqtSignal, QThread

import serial


class Serial_Thread(QThread):
    data_received = pyqtSignal(str)
    error_signal = pyqtSignal()

    def __init__(self, port, baudrate, timeout=1.5):
        super(Serial_Thread, self).__init__()
        self.is_running = False
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout

    def connect_serial(self):
        try:
            self.serial_port = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
            )
            self.is_running = True
        except Exception as E:
            print(f"Connect Serial {self.port} Error")

    def send_signal_serial_port(self, data: str):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.write(data.strip())

    def run(self):
        try:
            self.connect_serial()
            while self.is_running:
                if self.serial_port and self.serial_port.is_open:
                    data_serial = self.serial_port.readline()
                    if len(data_serial) > 0: 
                        self.data_received.emit(data_serial.decode('utf-8'))

        except Exception as E:
            print(f"Connect Serial {self.port} Error")

    def stop(self):
        self.is_running = False
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
