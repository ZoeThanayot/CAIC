import cv2

# เปิดการใช้งานกล้อง
cap = cv2.VideoCapture(0)

# ตรวจสอบว่ากล้องเปิดสำเร็จหรือไม่
if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

# อ่านภาพจากกล้อง
ret, frame = cap.read()

# ตรวจสอบว่าการอ่านภาพสำเร็จหรือไม่
if ret:
    # บันทึกภาพที่ถ่ายเป็นไฟล์
    cv2.imwrite('photo.jpg', frame)
    print("ถ่ายภาพสำเร็จและบันทึกเป็น photo.jpg")
else:
    print("ไม่สามารถถ่ายภาพได้")

# ปิดการใช้งานกล้อง
cap.release()
