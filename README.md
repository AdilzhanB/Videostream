# Videostream - Oil Spill Detection Video Streaming Server

A Flask-based video streaming server designed for real-time oil spill detection and monitoring. This application receives video frames from external cameras, processes them for oil spill detection, and provides a live video stream with alerting capabilities.

## 🎯 Overview

The Videostream server is part of an oil spill monitoring system that:
- Receives video frames from external camera sources
- Detects oil spill events in real-time
- Provides live video streaming capabilities
- Maintains a history of oil spill detection events
- Stores detection frames for analysis

## 🚀 Features

### Core Functionality
- **Real-time Video Streaming**: Live video feed accessible via web browser
- **Oil Spill Detection**: Automated detection with alerting system
- **Frame Storage**: Automatic saving of frames when oil spills are detected
- **Detection History**: Complete log of all oil spill events with timestamps
- **RESTful API**: Comprehensive API for integration with other systems

### Security
- Password-protected frame uploads
- Authentication for stream control
- Secure API endpoints

### Monitoring & Status
- Stream health monitoring
- Real-time status reporting
- Detection event tracking

## 📋 Requirements

- Python 3.7+
- OpenCV for image processing
- Flask for web server functionality
- NumPy for numerical operations

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AdilzhanB/Videostream.git
   cd Videostream
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export CAMERA_PASSWORD="your_secure_password"
   export PORT=5000  # Optional, defaults to 5000
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CAMERA_PASSWORD` | Password for camera authentication | `your_default_password` |
| `PORT` | Server port | `5000` |

### Directory Structure
```
Videostream/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── oil_spill_frames/     # Auto-created directory for detection frames
```

## 📡 API Documentation

### Video Streaming Endpoints

#### `GET /`
Health check endpoint
- **Response**: "Video Streaming Server is running"

#### `GET /stream`
Live video stream
- **Response**: Multipart MJPEG stream
- **Status**: 503 if no active stream

#### `GET /api/frame`
Get latest frame as JPEG
- **Response**: JPEG image data
- **Status**: 503 if no frame available

### Data Endpoints

#### `GET /api/status`
Get server and stream status
```json
{
  "stream_active": true,
  "last_frame_time": 1687534800.123,
  "frame_age_seconds": 2.5,
  "server_time": 1687534802.623,
  "oil_spill_detected": false,
  "oil_spill_events": 3
}
```

#### `GET /api/oil_spill_events`
Get complete history of oil spill detection events
```json
[
  {
    "timestamp": "20230623_143022",
    "datetime": "2023-06-23T14:30:22.123456",
    "frame_path": "oil_spill_frames/oil_spill_20230623_143022.jpg"
  }
]
```

#### `GET /api/detection_summary`
Get oil spill detection summary
```json
{
  "current_status": "Normal: No oil spill detected",
  "total_events": 3,
  "last_detection": "2023-06-23T14:30:22.123456"
}
```

### Control Endpoints

#### `POST /api/upload_frame`
Upload video frame from camera
- **Headers**: 
  - `X-Camera-Auth`: Camera password
  - `X-Oil-Spill-Detected`: "true" if oil spill detected
- **Body**: Raw JPEG image data
- **Response**: "Frame received" (200) or error

#### `POST /api/start_stream`
Start video streaming
```json
{
  "password": "your_camera_password"
}
```

#### `POST /api/stop_stream`
Stop video streaming
```json
{
  "password": "your_camera_password"
}
```

## 🔍 Usage Examples

### Viewing the Live Stream
Navigate to `http://localhost:5000/stream` in your web browser to view the live video feed.

### Uploading Frames (Camera Integration)
```python
import requests

# Upload frame with oil spill detection
with open('frame.jpg', 'rb') as f:
    response = requests.post(
        'http://localhost:5000/api/upload_frame',
        data=f.read(),
        headers={
            'X-Camera-Auth': 'your_password',
            'X-Oil-Spill-Detected': 'true',
            'Content-Type': 'image/jpeg'
        }
    )
```

### Checking Detection Status
```python
import requests

response = requests.get('http://localhost:5000/api/status')
status = response.json()
print(f"Oil spill detected: {status['oil_spill_detected']}")
```

## 🚨 Oil Spill Detection Workflow

1. **Frame Reception**: Camera uploads frames via `/api/upload_frame`
2. **Detection Processing**: External system processes frame and sets detection header
3. **Alert Triggering**: When oil spill detected:
   - Frame is saved to `oil_spill_frames/` directory
   - Event is logged with timestamp
   - Detection status is updated
4. **Notification**: Additional alerting can be added (email, SMS, etc.)

## 🔄 Integration with Camera Systems

The server is designed to work with external camera systems that:
1. Capture video frames
2. Process frames for oil spill detection (using ML/AI models)
3. Upload frames to this server with detection results

## 📊 Monitoring and Alerts

### Frame Storage
- Detected oil spill frames are automatically saved
- Files named with timestamp: `oil_spill_YYYYMMDD_HHMMSS.jpg`
- Stored in `oil_spill_frames/` directory

### Event Logging
- All detection events are logged with full timestamps
- Historical data available via API
- Frame paths included for evidence retrieval

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production with Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🔧 Troubleshooting

### Common Issues

1. **No stream available (503)**
   - Ensure frames are being uploaded
   - Check camera authentication
   - Verify stream is started

2. **Unauthorized upload (401)**
   - Check `CAMERA_PASSWORD` environment variable
   - Verify `X-Camera-Auth` header in requests

3. **Invalid image data (400)**
   - Ensure frames are valid JPEG format
   - Check image encoding before upload

## 🛡️ Security Considerations

- Use strong passwords for camera authentication
- Consider HTTPS in production environments
- Implement rate limiting for upload endpoints
- Monitor for unauthorized access attempts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source. Please add an appropriate license file.

## 📞 Support

For issues and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above

---

**Note**: This server is designed to work as part of a larger oil spill monitoring system. Ensure proper integration with camera systems and detection algorithms for full functionality.
