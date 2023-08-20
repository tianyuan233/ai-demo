from flask import Flask, Response, render_template
import cv2

app = Flask(__name__)

# RTSP URL for your camera
rtsp_url = 'rtsp://localhost/live'

def generate():
    cap = cv2.VideoCapture(rtsp_url)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 编码为MP4格式
        ret, buffer = cv2.imencode('.png', frame)
        if not ret:
            break
        
        # 将帧作为字节流传输
        yield (b'--frame\r\n'
               b'Content-Type: video/mp4\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
