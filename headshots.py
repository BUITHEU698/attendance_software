import cv2
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime  # Thêm import cho module datetime

# Hàm xử lý sự kiện khi nút chụp ảnh được nhấn
def take_snapshot():
    global frame
    dt_now = datetime.datetime.now()
    file_name = dt_now.strftime('%Y年%m月%d日%H時%M分%S秒') 
    path = './dataset/' + name_user + '/' + file_name + '.jpg'
    # Lưu ảnh
    cv2.imwrite(path, frame)
    print(path)

# Khởi tạo camera
camera = cv2.VideoCapture(0)
name_user = "theu"  # Tên thư mục ảnh

# Tạo cửa sổ OpenCV
cv2.namedWindow("Frame")

# Tạo cửa sổ Tkinter
root = tk.Tk()
root.title("Chụp ảnh")

# Tạo canvas để hiển thị hình ảnh từ camera
canvas = tk.Canvas(root, width=camera.get(cv2.CAP_PROP_FRAME_WIDTH), height=camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
canvas.pack()

# Tạo nút "Chụp ảnh"
snapshot_button = ttk.Button(root, text="Chụp ảnh", command=take_snapshot)
snapshot_button.pack(pady=10)

# Hàm cập nhật frame từ camera
def update_frame():
    ret, frame = camera.read()
    if ret:
        # Chuyển đổi frame thành định dạng hình ảnh Tkinter
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        
        # Hiển thị hình ảnh trên canvas
        canvas.img = img
        canvas.create_image(0, 0, anchor=tk.NW, image=img)
    
    # Lặp lại hàm sau một khoảng thời gian nhất định
    root.after(10, update_frame)

# Bắt đầu cập nhật frame
update_frame()

# Main loop của Tkinter
root.mainloop()

# Giải phóng camera và đóng cửa sổ
camera.release()
cv2.destroyAllWindows()
