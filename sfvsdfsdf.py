from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
from datetime import datetime
import imutils
import pickle
import time
import cv2
import os

# Khởi tạo 'currentname' để chỉ kích hoạt khi có một người mới được nhận diện.
currentname = "unknown"
# Xác định khuôn mặt từ tệp encodings.pickle mô hình được tạo từ train_model.py
encodingsP = "encodings.pickle"
# Sử dụng tệp xml này
# https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_default.xml
cascade = "haarcascade_frontalface_default.xml"

# Nạp khuôn mặt đã biết và các mã hóa cùng với Haar cascade của OpenCV
# cho việc phát hiện khuôn mặt
print("[INFO] Đang nạp mã hóa + bộ phát hiện khuôn mặt...")
data = pickle.loads(open(encodingsP, "rb").read())
detector = cv2.CascadeClassifier(cascade)

# Khởi tạo luồng video và cho phép cảm biến camera làm nóng lên
print("[INFO] Bắt đầu luồng video...")
vs = VideoStream(src=0).start()
#vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

# Bắt đầu bộ đếm FPS
fps = FPS().start()

# Lặp qua các khung từ luồng video
while True:
    # Chụp khung từ luồng video và thay đổi kích thước nó thành 500px (để tăng tốc xử lý)
    frame = vs.read()
    frame = imutils.resize(frame, width=500)

    # Chuyển đổi khung đầu vào từ BGR sang grayscale (để phát hiện khuôn mặt) và từ BGR sang RGB (để nhận diện khuôn mặt)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt trong khung màu xám
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    # OpenCV trả về tọa độ hộp giới hạn theo thứ tự (x, y, w, h)
    # nhưng chúng ta cần chúng theo thứ tự (top, right, bottom, left), vì vậy chúng ta cần phải thay đổi chúng một chút
    boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

    # Tính toán mã hóa khuôn mặt cho mỗi hộp giới hạn khuôn mặt
    encodings = face_recognition.face_encodings(rgb, boxes)
    names = []

    # Lặp qua mã hóa khuôn mặt
    for encoding in encodings:
        # Cố gắng so sánh mỗi khuôn mặt trong khung hình với các mã hóa đã biết của chúng ta
        matches = face_recognition.compare_faces(data["encodings"], encoding)
        name = "Unknown"  # Nếu khuôn mặt không được nhận diện, in Unknown

        # Kiểm tra xem chúng ta có phát hiện một sự khớp nào đó không
        if True in matches:
            # Tìm các chỉ số của tất cả các khuôn mặt đã khớp sau đó khởi tạo
            # một từ điển để đếm tổng số lần mỗi khuôn mặt đã được nhận diện
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            counts = {}

            # Lặp qua các chỉ số đã khớp và duy trì một đếm cho
            # mỗi khu
            # Lặp qua các chỉ số đã khớp và duy trì một đếm cho
            # mỗi khuôn mặt đã được nhận diện
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

            # Xác định khuôn mặt được nhận diện có số phiếu lớn nhất
            # (lưu ý: trong trường hợp có thể có một sự cố giống nhau, Python
            # sẽ chọn mục đầu tiên trong từ điển)
            name = max(counts, key=counts.get)

            # Nếu có người nào đó trong tập dữ liệu của bạn được nhận diện, in tên của họ trên màn hình
            if currentname != name:
                currentname = name
                # Đặt đường dẫn của thư mục lưu trữ hình ảnh đã nhận diện
                output_dir = f'photo/{currentname}'

                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                current_time = datetime.now().strftime("%Y%m%d%H%M%S")
                img_name = f"{output_dir}{name}_{current_time}.png"
                cv2.imwrite(img_name, frame[top:bottom, left:right])

                print(currentname)

        # Cập nhật danh sách tên
        names.append(name)

    # Lặp qua các khuôn mặt được nhận diện
    for ((top, right, bottom, left), name) in zip(boxes, names):
        # Vẽ tên của khuôn mặt dự đoán lên hình ảnh - màu sắc là BGR
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        y = top - 15 if top - 15 > 15 else top + 15
        cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    # Hiển thị hình ảnh lên màn hình
    cv2.imshow("Đang chạy nhận diện khuôn mặt", frame)
    key = cv2.waitKey(1) & 0xFF

    # Thoát khi phím 'q' được nhấn
    if key == ord("q"):
        break

    # Cập nhật bộ đếm FPS
    fps.update()

# Dừng bộ đếm và hiển thị thông tin FPS
fps.stop()
print("[INFO] Thời gian trôi qua: {:.2f}".format(fps.elapsed()))
print("[INFO] FPS xấp xỉ: {:.2f}".format(fps.fps()))



# Dọn dẹp
cv2.destroyAllWindows()
vs.stop()
