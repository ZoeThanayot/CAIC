import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
from google.colab.patches import cv2_imshow  # สำหรับแสดงภาพใน Colab


# เปิดใช้งานกล้อง
cap = cv2.VideoCapture(0)

def scan_barcode():
    while True:
        frame=cv2.imread('/content/LINE_ALBUM_DATA_241014_2.jpg')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # ถอดรหัสบาร์โค้ดจากภาพขาวดำ
        decoded_objects = decode(gray)
        for obj in decoded_objects:
            # แสดงประเภทและข้อมูลที่อ่านได้จากบาร์โค้ด
            barcode_type = obj.type
            barcode_data = obj.data.decode('utf-8')
            print(f'ประเภทบาร์โค้ด: {barcode_type}')
            print(f'ข้อมูลที่ได้จากบาร์โค้ด: {barcode_data}')

            # วาดกรอบรอบบาร์โค้ดในภาพ
            points = obj.polygon
            if len(points) == 4:
                # แปลงพิกัดของจุดให้เป็นรูปแบบที่เหมาะสมสำหรับการวาดกรอบ
                pts = np.array([[point.x, point.y] for point in points], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

            # ใส่ข้อมูลบาร์โค้ดในภาพ
            x, y, w, h = obj.rect
            cv2.putText(frame, barcode_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # แสดงภาพพร้อมกรอบและข้อมูลบาร์โค้ด
        cv2_imshow(gray)
        cv2_imshow(frame)
        break
    # ปิดการใช้งานกล้องและหน้าต่าง
    cap.release()
    return None

# เรียกใช้งานฟังก์ชันสแกนบาร์โค้ด
scan_barcode()
