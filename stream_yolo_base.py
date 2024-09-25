import cv2
import os
from ultralytics import YOLO
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from collections import Counter
from flask import Flask, Response, render_template

app = Flask(__name__)

os.environ["OPENCV_VIDEOIO_MSMF_ENABLE_HW_TRANSFORMS"] = "0"

# Load the YOLO model
model = YOLO("trained_model8n.pt")

class_counts = {}

# Firebase configuration
cred = credentials.Certificate('private_key.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://iot-smart-city-e86cd-default-rtdb.firebaseio.com'
})

# Reference to the Realtime Database
ref = db.reference('camera')

# Initialize video capture from the camera (0 for the default camera)
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)  # Change to 0 for the default camera
assert cap.isOpened(), "Error opening camera"

# Get camera properties
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))

def generate_frames():
    while cap.isOpened():
        success, im0 = cap.read()
        if not success:
            print("Camera frame is empty or video processing has been successfully completed.")
            break

        # Track objects using the YOLO model
        tracks = model(source=im0, conf=0.7, device=0)
        object_counts = tracks[0].boxes.cls.cpu().numpy()

        # Count the object number of each class
        object_counts = Counter(object_counts)
        class_counts['tree'] = True if object_counts[0] >= 1 else False
        class_counts['car'] = object_counts[1]
        class_counts['rock'] = True if object_counts[2] >= 1 else False

        # Update Firebase with object counts
        ref.set(class_counts)

        # Render results on the frame
        im0 = tracks[0].plot()  # Get the annotated frame

        # Display the resulting frame
        #cv2.imshow('Webcam Object Detection', annotated_frame)

        ret, buffer = cv2.imencode('.jpg', im0)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt detected. Releasing camera and closing windows.")
    finally:
        # Release the camera and close OpenCV windows
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
