from ultralytics import YOLO
import cv2
import os

 
class main():
    def __init__(self, conf_threshold=0.1):
        # Khởi tạo mô hình YOLO với trọng số đã được huấn luyện
        self.model = YOLO(r'D:\NguyenCuong\1A\FT672\data\train2\weights\best.pt')
        self.conf_threshold = conf_threshold  # Ngưỡng độ tin cậy

    def process(self, img):
        # Thực hiện phát hiện đối tượng trên hình ảnh
        results = self.model(img, conf=self.conf_threshold)  # Chỉ sử dụng conf
        # Kiểm tra xem có kết quả không
        if results and results[0].boxes:
            boxes = results[0].boxes  # Lấy đối tượng boxes
            for box in boxes:
                # Lấy nhãn và độ tin cậy
                label_index = box.cls.item()  # Nhãn (class index)
                confidence = box.conf.item()  # Độ tin cậy
                label = results[0].names[label_index]  # Lấy tên nhãn từ chỉ số

                # Vẽ bounding box lên hình ảnh (nếu cần)
                img = results[0].plot()  # Trả về hình ảnh với các bounding box
                return label, img  # Trả về nhãn đầu tiên phát hiện được
        return None, img  # Trả về None nếu không có đối tượng nào được phát hiện


if __name__ == '__main__':
    process_image = main(conf_threshold=0.1)  # Khởi tạo với ngưỡng tùy chỉnh
    # Thư mục chứa hình ảnh
    path = r"D:\NguyenCuong\1A\FT672\img_2103\img\TEST\test"
    

    for entry in os.scandir(path):
        if entry.is_file():  # Kiểm tra xem entry có phải là file không
            print(f"Processing file: {entry.name}")
            frame = cv2.imread(entry.path)

            if frame is not None:
                data, img = process_image.process(frame)
                print(data)
                cv2.imshow("img",img)
                cv2.waitKey(0)
