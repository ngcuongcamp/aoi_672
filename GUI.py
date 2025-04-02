# from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
#                             QLabel, QPushButton, QTabWidget, QFormLayout, QLineEdit, 
#                             QGroupBox, QComboBox,)  # Thêm QComboBox
# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QFont, QIcon, QCursor
# import json
# import os
# from ultils import *

# class MainUi(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle(TITLE_PROGRAM)
#         self.setGeometry(100, 100, 800, 600)
#         self.setWindowIcon(QIcon(PATH_ICON))

#         # Tạo widget chính
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)

#         # Tạo layout chính (dọc)
#         main_layout = QVBoxLayout()
#         main_widget.setLayout(main_layout)

#         # Tiêu đề
#         title_label = QLabel(TITLE_PROGRAM)
#         title_label.setFont(QFont("Arial", 22, QFont.Bold))
#         title_label.setAlignment(Qt.AlignCenter)
#         title_label.setStyleSheet("padding: 15px; background-color: #333; color: white;")

#         # Thêm ComboBox
#         self.combobox = QComboBox()
#         self.combobox.addItems(["ORANGE", "PURPLE", "GRAY", "BLACK"])
#         self.combobox.setFont(QFont("Arial", 12))
#         self.combobox.setStyleSheet("""
#                 QComboBox {
#                     padding: 5px;
#                     min-height: 20px;
#                 }
#                 QComboBox QAbstractItemView {
#                     padding: 10px 5px;
#                     border: 1px solid gray;
#                 }
#                 QComboBox QAbstractItemView::item {
#                     height: 40px;
#                 }
#             """)
#         self.combobox.setMaximumWidth(300)  # Giới hạn chiều rộng nếu cần

#         # Thêm button tròn màu đỏ
#         self.circle_button = QPushButton()
#         self.circle_button.setFixedSize(30, 30)  # Kích thước cố định cho button tròn
#         self.circle_button.setStyleSheet("""
#             QPushButton {
#                 min-height: 40px;
#                 min-width: 40px;
#                 background-color: orange;
#                 border: 2px solid orange;
#                 border-radius: 20px;  /* Bán kính bằng 1/2 chiều rộng/cao để tạo hình tròn */
#                 margin-bottom: 10px;
#             }
#             QPushButton:hover {
#                 background-color: #cfcfcf;  /* Màu sáng hơn khi hover (tùy chọn) */
#             }
#         """)
#         self.circle_button.setCursor(QCursor(Qt.PointingHandCursor))
        
#         # Tạo QTabWidget
#         self.tab_widget = QTabWidget()
#         self.tab_widget.setStyleSheet("""
#             QTabBar::tab {
#                 font: 10pt "Arial";
#                 padding: 5px 10px;
#                 min-width: 60px;
#                 min-height: 20px;
#             }
#             QTabBar::tab:selected {
#                 font: bold 10pt "Arial";
#             }
#         """)
        
#         # Tab 1: Frame
#         self.frame_tab = QWidget()
#         self.setup_frame_tab()
        
#         # Tab 2: General
#         self.general_tab = QWidget()
#         self.setup_general_tab()

#         # Thêm các tab vào tab_widget
#         self.tab_widget.addTab(self.frame_tab, "Frame")
#         self.tab_widget.addTab(self.general_tab, "General")

#         # Thêm các thành phần vào main layout
#         main_layout.addWidget(title_label)
#         main_layout.addWidget(self.combobox)  # Thêm combobox vào layout chính
#         main_layout.addWidget(self.circle_button)  # Thêm button tròn vào layout chính
#         main_layout.addWidget(self.tab_widget)
        
#         self.combobox.currentIndexChanged.connect(self.on_combobox_changed)  # Kết nối sự kiện thay đổi của combobox
#         self.market_config = load_market_data()
#         # default load orange market
        
        
#     def on_combobox_changed(self):
        
#         # get selected title + css to button
#         selected_color = self.combobox.currentText()
#         self.circle_button.setStyleSheet(f"""
#         QPushButton {{
#             min-height: 40px;
#             min-width: 40px;
#             background-color: {selected_color};
#             border: 2px solid {selected_color};
#             border-radius: 20px;  /* Bán kính bằng 1/2 chiều rộng/cao để tạo hình tròn */
#             margin-bottom: 10px;
#         }}
#         QPushButton:hover {{
#             background-color: #cfcfcf;  /* Màu sáng hơn khi hover (tùy chọn) */
#         }}
#     """)
        
    
#     # Các phương thức khác giữ nguyên như code gốc
#     def setup_frame_tab(self):
#         frame_layout = QVBoxLayout()
#         self.frame_tab.setLayout(frame_layout)

#         # Container cho 2 label (camera và hình ảnh)
#         container = QWidget()
#         container_layout = QHBoxLayout()
#         container.setLayout(container_layout)

#         # Label cho Camera
#         self.camera_label = QLabel("Camera Feed")
#         self.camera_label.setFont(QFont("Arial", 10))
#         self.camera_label.setAlignment(Qt.AlignCenter)
#         self.camera_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        
#         # Label cho Hình ảnh
#         self.image_label = QLabel("Processed Image")
#         self.image_label.setFont(QFont("Arial", 10))
#         self.image_label.setAlignment(Qt.AlignCenter)
#         self.image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")

#         # Thêm 2 label vào container layout
#         container_layout.addWidget(self.camera_label)
#         container_layout.addWidget(self.image_label)

#         # Đảm bảo 2 label chia đều không gian
#         container_layout.setStretch(0, 1)
#         container_layout.setStretch(1, 1)

#         frame_layout.addWidget(container)

#     def setup_general_tab(self):
#         general_layout = QVBoxLayout()
#         self.general_tab.setLayout(general_layout)

#         # Load config từ file JSON
#         self.config = load_config()
#         self.input_fields = {}

#         # Tạo các group cho từng phần trong config
#         for section, generals in self.config.items():
#             group_box = QGroupBox(section)
#             form_layout = QFormLayout()
#             group_box.setFont(QFont("Arial", 10))
            
#             # Tạo label và input cho từng key-value trong section
#             for key, value in generals.items():
#                 label = QLabel(f"{key}:")
#                 label.setFont(QFont("Arial", 10))
#                 label.setMinimumWidth(150)
#                 input_field = QLineEdit(str(value))
#                 input_field.setStyleSheet("min-height: 20px; padding: 5px;")
#                 input_field.setFont(QFont("Arial", 10))
                
#                 self.input_fields[f"{section}.{key}"] = input_field
#                 form_layout.addRow(label, input_field)
            
#             group_box.setLayout(form_layout)
#             general_layout.addWidget(group_box)

#         # Nút Save
#         save_button = QPushButton("SAVE")
#         save_button.setFont(QFont("Arial", 13))
#         save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; min-height: 20px;")
#         save_button.clicked.connect(self.save_generals)
#         save_button.setCursor(QCursor(Qt.PointingHandCursor))

#         general_layout.addWidget(save_button)
#         general_layout.addStretch()

  

    

#     def save_generals(self):
#         updated_config = {
#             "SERIAL": {},
#             "CAMERA": {},
#             "SETTING": {}
#         }
        
#         for full_key, input_field in self.input_fields.items():
#             section, key = full_key.split('.')
#             default_value = self.config[section][key]
#             if isinstance(default_value, int):
#                 updated_config[section][key] = int(input_field.text())
#             elif isinstance(default_value, float):
#                 updated_config[section][key] = float(input_field.text())
#             else:
#                 updated_config[section][key] = input_field.text()
        
#         with open(PATH_CONFIG, 'w') as f:
#             json.dump(updated_config, f, indent=4)
#         print("generals saved")
    
    

#     def resizeEvent(self, event):
#         super().resizeEvent(event)
#         self.camera_label.setMinimumSize(self.width() // 3, self.height() // 3)
#         self.image_label.setMinimumSize(self.width() // 3, self.height() // 3)
        
        


from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QPushButton, QTabWidget, QFormLayout, QLineEdit, 
                            QGroupBox, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QCursor
import json
import os
from ultils import *

class MainUi(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AOI FT672")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon(PATH_ICON))

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        title_label = QLabel(TITLE_PROGRAM)
        title_label.setFont(QFont("Arial", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("padding: 15px; background-color: #333; color: white;")

        # Tạo container cho Market label, combobox và button
        top_container = QWidget()
        top_layout = QHBoxLayout()
        top_container.setLayout(top_layout)

        # Thêm title "Market"
        market_label = QLabel("MARKET: ")
        market_label.setFont(QFont("Arial", 12))
        market_label.setStyleSheet("padding-right: 20px; font-weight: bold")

        # Thêm ComboBox
        self.combobox = QComboBox()
        self.combobox.addItems(["ORANGE", "PURPLE", "GRAY", "BLACK"])
        self.combobox.setFont(QFont("Arial", 12))
        self.combobox.setStyleSheet("""
            QComboBox {
                padding: 5px;
                min-height: 20px;
                min-width: 250px;
                margin-right: 30px;
            }
            QComboBox QAbstractItemView {
                padding: 10px 5px;
                border: 1px solid gray;
            }
            QComboBox QAbstractItemView::item {
                height: 40px;
            }
        """)
        self.combobox.setMaximumWidth(300)

        # Thêm button tròn
        self.circle_button = QPushButton()
        self.circle_button.setFixedSize(40, 40)
        self.circle_button.setStyleSheet("""
            QPushButton {
                background-color: orange;
                border: 2px solid orange;
                border-radius: 20px;
                padding-left: 30px;
            }
            QPushButton:hover {
                background-color: #cfcfcf;
            }
        """)
        self.circle_button.setCursor(QCursor(Qt.PointingHandCursor))

        # Thêm các thành phần vào top_layout
        top_layout.addWidget(market_label)
        top_layout.addWidget(self.combobox)
        top_layout.addWidget(self.circle_button)
        top_layout.addStretch()  # Đẩy các thành phần về phía trái

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
        
        self.frame_tab = QWidget()
        self.setup_frame_tab()
        
        self.general_tab = QWidget()
        self.setup_general_tab()

        self.tab_widget.addTab(self.frame_tab, "Frame")
        self.tab_widget.addTab(self.general_tab, "General")

        main_layout.addWidget(title_label)
        main_layout.addWidget(top_container)  # Thêm container chứa market label, combobox và button
        main_layout.addWidget(self.tab_widget)
        
        self.combobox.currentIndexChanged.connect(self.on_combobox_changed)
        self.market_config = load_market_data()

    def on_combobox_changed(self):
        selected_color = self.combobox.currentText().lower()  # Chuyển thành chữ thường để khớp với CSS
        self.circle_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {selected_color};
                border: 2px solid {selected_color};
                border-radius: 15px;
            }}
            QPushButton:hover {{
                background-color: #cfcfcf;
            }}
        """)

    def setup_frame_tab(self):
        frame_layout = QVBoxLayout()
        self.frame_tab.setLayout(frame_layout)

        container = QWidget()
        container_layout = QHBoxLayout()
        container.setLayout(container_layout)

        self.camera_label = QLabel("Camera Feed")
        self.camera_label.setFont(QFont("Arial", 10))
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")
        
        self.image_label = QLabel("Processed Image")
        self.image_label.setFont(QFont("Arial", 10))
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #f0f0f0; border: 1px solid #ccc;")

        container_layout.addWidget(self.camera_label)
        container_layout.addWidget(self.image_label)

        container_layout.setStretch(0, 1)
        container_layout.setStretch(1, 1)

        frame_layout.addWidget(container)

    def setup_general_tab(self):
        general_layout = QVBoxLayout()
        self.general_tab.setLayout(general_layout)

        self.config = load_config()
        self.input_fields = {}

        for section, generals in self.config.items():
            group_box = QGroupBox(section)
            form_layout = QFormLayout()
            group_box.setFont(QFont("Arial", 10))
            
            for key, value in generals.items():
                label = QLabel(f"{key}:")
                label.setFont(QFont("Arial", 10))
                label.setMinimumWidth(150)
                input_field = QLineEdit(str(value))
                input_field.setStyleSheet("min-height: 20px; padding: 5px;")
                input_field.setFont(QFont("Arial", 10))
                
                self.input_fields[f"{section}.{key}"] = input_field
                form_layout.addRow(label, input_field)
            
            group_box.setLayout(form_layout)
            general_layout.addWidget(group_box)

        save_button = QPushButton("SAVE")
        save_button.setFont(QFont("Arial", 13))
        save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; min-height: 20px;")
        save_button.clicked.connect(self.save_generals)
        save_button.setCursor(QCursor(Qt.PointingHandCursor))

        general_layout.addWidget(save_button)
        general_layout.addStretch()

    def save_generals(self):
        updated_config = {
            "SERIAL": {},
            "CAMERA": {},
            "SETTING": {}
        }
        
        for full_key, input_field in self.input_fields.items():
            section, key = full_key.split('.')
            default_value = self.config[section][key]
            if isinstance(default_value, int):
                updated_config[section][key] = int(input_field.text())
            elif isinstance(default_value, float):
                updated_config[section][key] = float(input_field.text())
            else:
                updated_config[section][key] = input_field.text()
        
        with open(PATH_CONFIG, 'w') as f:
            json.dump(updated_config, f, indent=4)
        print("generals saved")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.camera_label.setMinimumSize(self.width() // 3, self.height() // 3)
        self.image_label.setMinimumSize(self.width() // 3, self.height() // 3)