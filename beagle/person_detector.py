import cv2
from ultralytics import YOLO
stream_url = "http://192.168.66.1:9527/videostream.cgi?loginuse=admin&loginpas=admin"
model = YOLO("yolo11n.pt")
cam = cv2.VideoCapture(stream_url)
if not cam.isOpened():
    raise RuntimeError("Camera stream could not be opened :(")
try:
    while True:
        success, frame = cam.read()
        if not success:
            print("Could not read camera frame :(")
            break
        results = model.predict( 
            source = frame,
            classes = [0],
            conf=0.5,
            verbose = False
        )
        boxed_frame = results[0].plot()
        cv2.imshow("Person detection", boxed_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cam.release()
    cv2.destroyAllWindows()