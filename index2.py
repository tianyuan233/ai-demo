import subprocess
from flask import Flask, Response,render_template,send_from_directory

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/stream')
def start_stream():
    # 定义 FFmpeg 命令
    ffmpeg_command = [
      'ffmpeg',
      '-fflags', 'nobuffer',
      '-rtsp_transport', 'tcp',
      '-i', 'rtsp://localhost/live',
      '-vsync', '0',
      '-copyts',
      '-vcodec', 'copy',
      '-movflags', 'frag_keyframe+empty_moov',
      '-an',
      '-hls_flags', 'delete_segments+append_list',
      '-f', 'hls',
      '-hls_time', '1',
      '-hls_list_size', '3',
      '-hls_segment_type', 'mpegts',
      '-hls_segment_filename', './static/stream/%d.ts',
      './static/stream/index.m3u8'
    ]
    # 启动 FFmpeg 进程
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 返回视频流响应 /static/stream/index.m3u8
    return app.send_static_file('stream/index.m3u8')

if __name__ == '__main__':
    app.run()
