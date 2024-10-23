import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
# เปิดไฟล์ภาพที่อัปโหลด
image_path = "/content/LINE_ALBUM_DATA_241014_15.jpg"
image = Image.open(image_path)

# แปลงเป็นภาพสำหรับ OpenCV
opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# แสดงภาพ (ถ้าจำเป็น)
# cv2_imshow(opencv_image)  # ใช้ใน Colab เพื่อแสดงภาพ

# อ่านบาร์โค้ดจากภาพ
decoded_objects = decode(opencv_image)
for obj in decoded_objects:
    print(f'ประเภทบาร์โค้ด: {obj.type}')
    print(f'ข้อมูลที่ได้จากบาร์โค้ด: {obj.data.decode("utf-8")}')
