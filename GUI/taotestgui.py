from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTabWidget, QFormLayout, QLineEdit, QGroupBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon,QCursor
import json
import os
from ultils import *

class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AOI FT672")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(PATH_ICON))

        # Tạo widget chính
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Tạo layout chính (dọc)
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        # Tiêu đề
        title_label = QLabel(TITLE_PROGRAM)
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("padding: 15px; background-color: #333; color: white;")

        # Tạo QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                font: 10pt "Arial";
                padding: 5px 10px;
                min-width: 60px;
                min-height: 20px;
            }
            QTabBar::tab:selected {
                font: bold 10pt "Arial";
            }
        """)
        
        # Tab 1: Frame
        self.frame_tab = QWidget()
        self.setup_frame_tab()
        
        # Tab 2: Settings
        self.settings_tab = QWidget()
        self.setup_settings_tab()

        # Thêm các tab vào tab_widget
        self.tab_widget.addTab(self.frame_tab, "Frame")
        self.tab_widget.addTab(self.settings_tab, "Settings")

        # Thêm các thành phần vào main layout
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.tab_widget)

    def setup_frame_tab(self):
        frame_layout = QVBoxLayout()
        self.frame_tab.setLayout(frame_layout)

        # Container cho 2 label (camera và hình ảnh)
        container = QWidget()
        container_layout = QHBoxLayout()
        container.setLayout(container_layout)

        # Label cho Camera
        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setFont(QFont("Arial", 10))
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        
        # Label cho Hình ảnh
        self.image_label = QLabel("Processed Image")
        self.image_label.setFont(QFont("Arial", 10))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")

        # Thêm 2 label vào container layout
        container_layout.addWidget(self.camera_label)
        container_layout.addWidget(self.image_label)

        # Đảm bảo 2 label chia đều không gian
        container_layout.setStretch(0, 1)
        container_layout.setStretch(1, 1)

        frame_layout.addWidget(container)

    def setup_settings_tab(self):
        settings_layout = QVBoxLayout()
        self.settings_tab.setLayout(settings_layout)

        # Load config từ file JSON
        self.config = self.load_config()
        self.input_fields = {}

        # Tạo các group cho từng phần trong config
        for section, settings in self.config.items():
            group_box = QGroupBox(section)
            form_layout = QFormLayout()
            group_box.setFont(QFont("Arial", 10))
            
            # Tạo label và input cho từng key-value trong section
            for key, value in settings.items():
                label = QLabel(f"{key}:")
                label.setFont(QFont("Arial", 10))
                label.setMinimumWidth(150)
                input_field = QLineEdit(str(value))
                # Đặt chiều cao tối thiểu 20px cho input
                input_field.setStyleSheet("min-height: 20px; padding: 5px;")
                input_field.setFont(QFont("Arial", 10))
                
                # Lưu input_field với key đầy đủ (section.key)
                self.input_fields[f"{section}.{key}"] = input_field
                form_layout.addRow(label, input_field)
            
            group_box.setLayout(form_layout)
            settings_layout.addWidget(group_box)

        # Nút Save
        save_button = QPushButton("SAVE")
        save_button.setFont(QFont("Arial", 13))
        save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; min-height: 20px;")
        save_button.clicked.connect(self.save_settings)
        save_button.setCursor(QCursor(Qt.PointingHandCursor))

        # Thêm nút và stretch vào layout
        settings_layout.addWidget(save_button)
        settings_layout.addStretch()

    def load_config(self):
        # Mặc định config
        default_config = {
            "SERIAL": {
                "COM_PLC": "COM7",
                "BAUDRATE_PLC": 9600
            },
            "CAMERA": {
                "IDC": 0
            },
            "SETTING": {
                "THRESH_VALUE": 24,
                "FGLUE_OFFSET_X": -115,
                "FGLUE_OFFSET_Y": -10,
                "FGLUE_WIDTH": 115,
                "FGLUE_HEIGHT": 32,
                "CONF_TEMPLATE": 0.85,
                "CONF_FGLUE": 80.0,
                "CONF_HPART_LEFT": 99.0,
                "CONF_HPART_RIGHT": 99.0,
                "CONF_3RD": 98.8
            }
        }
        
        config_file = PATH_CONFIG
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return default_config
        return default_config

    def save_settings(self):
        # Tạo một config mới để lưu
        updated_config = {
            "SERIAL": {},
            "CAMERA": {},
            "SETTING": {}
        }
        
        # Cập nhật giá trị từ input fields
        for full_key, input_field in self.input_fields.items():
            section, key = full_key.split('.')
            # Chuyển đổi kiểu dữ liệu dựa trên giá trị mặc định
            default_value = self.config[section][key]
            if isinstance(default_value, int):
                updated_config[section][key] = int(input_field.text())
            elif isinstance(default_value, float):
                updated_config[section][key] = float(input_field.text())
            else:
                updated_config[section][key] = input_field.text()
        
        # Ghi vào file JSON
        with open(PATH_CONFIG, 'w') as f:
            json.dump(updated_config, f, indent=4)
        print("Settings saved")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.camera_label.setMinimumSize(self.width() // 3, self.height() // 3)
        self.image_label.setMinimumSize(self.width() // 3, self.height() // 3)



if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = MainUi()
    window.show()
    sys.exit(app.exec_())