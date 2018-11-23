import cv2
# 导包
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

# 处理黑白画面 用1.3大小的框 框的线条粗细是5个像素


def detect(gray, frame):
    # 识别人脸的方法
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y: y+h, x:x+w]  # 灰色的相片一口气处理完
        roi_color = frame[y: y+h, x:x+w]

    return frame  # 把处理玩的整个相片 回传回去


# 开启摄像头

video_capture = cv2.VideoCapture(0)
while True:
    _, frame = video_capture.read()  # 读取摄像头采集到的画面
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 把画面转成黑白  在 opencv中处理颜色的顺序是蓝绿红
    canvas = detect(gray, frame)  # 把结果展示出来
    cv2.imshow('Video', canvas)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # 如果在键盘上输入q的话就停下来
        break


video_capture.release()
cv2.destroyAllWindows()
