# camera_service/app.py (Laptop Version)
from flask import Flask, Response, jsonify, request
import cv2
import numpy as np
import io

app = Flask(__name__)
camera = cv2.VideoCapture(0)  # Use 0 for the default webcam

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/image')
def image():
    success, frame = camera.read()
    if not success:
        return jsonify({"error": "Failed to capture image"}), 500
    ret, buffer = cv2.imencode('.jpg', frame)
    frame_bytes = buffer.tobytes()
    return Response(frame_bytes, mimetype='image/jpeg')

@app.route('/camera/config', methods=['POST'])
def config():
    import json
    try:
        data = json.loads(request.data)
        width = data.get("width", 640)
        height = data.get("height", 480)

        camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        return jsonify({"message": "Camera configuration updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)