import os
import time
import cv2
import numpy as np
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
import threading
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

latest_frame = None
stream_active = False
last_frame_time = 0
camera_password = os.environ.get('CAMERA_PASSWORD', 'your_default_password')

frame_lock = threading.Lock()

@app.route('/')
def index():
    return "Video Streaming Server is running"

@app.route('/stream')
def video_feed():
    if not stream_active:
        return "No active stream", 503
        
    def generate():
        global latest_frame
        while stream_active:
            with frame_lock:
                if latest_frame is not None:
                    # Encode frame as JPEG
                    _, buffer = cv2.imencode('.jpg', latest_frame)
                    frame_bytes = buffer.tobytes()
                    
                    # Yield the frame in the format expected by multipart/x-mixed-replace
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(0.033) 
            
    return Response(generate(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/frame')
def get_latest_frame():
    global latest_frame
    with frame_lock:
        if latest_frame is None or not stream_active:
            return "No frame available", 503
            
        _, buffer = cv2.imencode('.jpg', latest_frame)
        frame_bytes = buffer.tobytes()
    
    return Response(frame_bytes, mimetype='image/jpeg')

@app.route('/api/status')
def get_status():
    global stream_active, last_frame_time
    
    current_time = time.time()
    frame_age = current_time - last_frame_time if last_frame_time > 0 else None
    
    return jsonify({
        'stream_active': stream_active,
        'last_frame_time': last_frame_time,
        'frame_age_seconds': frame_age,
        'server_time': current_time
    })

@app.route('/api/upload_frame', methods=['POST'])
def upload_frame():
    global latest_frame, stream_active, last_frame_time
    
    if request.headers.get('X-Camera-Auth') != camera_password:
        logger.warning("Unauthorized upload attempt")
        return "Unauthorized", 401
    
    try:
        nparr = np.frombuffer(request.data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            logger.error("Failed to decode image")
            return "Invalid image data", 400
            
        with frame_lock:
            latest_frame = frame
            stream_active = True
            last_frame_time = time.time()
            
        return "Frame received", 200
        
    except Exception as e:
        logger.error(f"Error processing uploaded frame: {str(e)}")
        return f"Error: {str(e)}", 500

@app.route('/api/start_stream', methods=['POST'])
def start_stream():
    global stream_active
    
    if request.json.get('password') != camera_password:
        return "Unauthorized", 401
        
    stream_active = True
    return jsonify({"status": "Stream started"})

@app.route('/api/stop_stream', methods=['POST'])
def stop_stream():
    global stream_active
    
    if request.json.get('password') != camera_password:
        return "Unauthorized", 401
        
    stream_active = False
    return jsonify({"status": "Stream stopped"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)