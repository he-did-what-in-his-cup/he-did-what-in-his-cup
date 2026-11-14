import cv2
stream_url = "http://192.168.66.1:9527/videostream.cgi?loginuse=admin&loginpas=admin"
cam = cv2.VideoCapture(stream_url)
if not cam.isOpened():
    raise RuntimeError("Camera stream could not be opened :(")
try:
    while True:
        success, frame = cam.read()
        if not success:
            print("Frame could not be read :(")
            break
        cv2.imshow("Beagle Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
finally:
    cam.release()
    cv2.destroyAllWindows()


