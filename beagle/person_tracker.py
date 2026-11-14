import cv2
from ultralytics import YOLO

stream_url = "http://192.168.66.1:9527/videostream.cgi?loginuse=admin&loginpas=admin" #video address found through Chrome
model = YOLO("yolo11n.pt") #contains the pretrained models learning weights
cam = cv2.VideoCapture(stream_url) #video stream

if not cam.isOpened(): #if cannot connect to camera then show this message
    raise RuntimeError("Camera stream could not be opened :(")
reference_histogram = None #initially no reference shirt is saved 
try:
    while True:
        success, frame = cam.read() #returns if the frames are read or not
        current_histogram = None #prevents the program from comparing an old shirt image when no person is detected
        if not success:
            print("Could not read camera frame :(")#If the stream stops supplying images, exit the loop
            break
        results = model.track( 
            source = frame, #frame to analyze
            persist = True, #Retain tracking state between consecutive frames
            tracker = "bytetrack.yaml", #Use ByteTrack and its configuration
            classes = [0], #Keep only the pretrained model’s person class
            imgsz=416, #Use a smaller inference image size
            conf=0.5, #Filter detections using a confidence threshold of 0.5
            verbose = False #Suppress routine prediction output
        )
        boxed_frame = results[0].plot() #contains the result for this frame and creates an annotated image
        boxes = results[0].boxes #gets the boxes for the person detected (numerical detection information)
        if boxes is not None and len(boxes) >0: #Only calculate a shirt region when a person box exists
            largest_box = max(boxes, key = lambda box: float(box.xywh[0][2] * box.xywh[0][3])) #This is a temporary selection rule. It may switch to another person if their box becomes larger.
            x1, y1, x2, y2 = map(int, largest_box.xyxy[0].tolist()) #calculate the shirt rectangle
            box_width = x2 - x1
            box_height = y2 - y1
            shirt_x1 = x1 + int(0.15 * box_width)
            shirt_x2 = x1 + int(0.85 * box_width)
            shirt_y1 = y1 + int(0.25 * box_height)
            shirt_y2 = y1 + int(0.65 * box_height)
            frame_height, frame_width = frame.shape[:2]
            shirt_x1 = max(0, shirt_x1)
            shirt_y1 = max(0, shirt_y1)
            shirt_x2 = min(frame_width, shirt_x2)
            shirt_y2 = min(frame_height, shirt_y2)
            if shirt_x2 > shirt_x1 and shirt_y2 > shirt_y1: 
                shirt_crop = frame[shirt_y1:shirt_y2, shirt_x1:shirt_x2] #crop the original frame, so drawn yellow lines do not contaminate the color measurements
                hsv_shirt = cv2.cvtColor(shirt_crop, cv2.COLOR_BGR2HSV) #converts OpenCVs BGR colors into HSV
                current_histogram = cv2.calcHist( #This builds a 30 × 32 table counting combinations of hue and saturation
                    [hsv_shirt],
                    [0, 1],
                    None,
                    [30, 32],
                    [0, 180, 0, 256]
                )
                cv2.normalize( #Normalization makes the bin values sum to approximately 1, allowing different-sized crops to be compared
                    current_histogram,
                    current_histogram,
                    alpha=1,
                    beta=0,
                    norm_type=cv2.NORM_L1
                )


                cv2.rectangle(
                    boxed_frame,
                    (shirt_x1, shirt_y1),
                    (shirt_x2, shirt_y2),
                    (0, 255, 255),  # Yellow in OpenCV's BGR format.
                    2
                )
        if current_histogram is None:
            status = "No shirt region available"

        elif reference_histogram is None:
            status = "Press s to save target shirt"

        else:
            distance = cv2.compareHist(
                reference_histogram,
                current_histogram,
                cv2.HISTCMP_BHATTACHARYYA
            )
            '''OpenCV’s Bhattacharyya comparison returns a distance: smaller means more similar distributions.
              We subtract it from 1 to make the displayed score increase with similarity.'''
            similarity = 1.0 - distance
            status = f"Shirt similarity: {similarity:.2f}"
        cv2.putText(
        boxed_frame,
        status,
        (10, 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2   
    )
        cv2.imshow("Person tracking", boxed_frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):
            if current_histogram is not None:
                reference_histogram = current_histogram.copy()
                print("Target shirt colors saved.", flush=True)
            else:
                print("Cannot save: no shirt region available.", flush=True)

        elif key == ord("r"):
            reference_histogram = None
            print("Reference cleared.", flush=True)

        elif key == ord("q"):
            break   
        ''' s: saves current_histogram.copy() as an independent reference.
            r: clears the reference.
            q: exits the loop.
            flush=True makes printed messages appear promptly in Terminal.
        '''
finally:
    cam.release()
    cv2.destroyAllWindows()
