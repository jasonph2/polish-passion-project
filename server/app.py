from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from moviepy.editor import VideoFileClip
from config import AUDIO_FILE_PATH
import os

app = Flask(__name__)
CORS(app)

@app.after_request
def add_cors_headers(response):
    response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    return response

@app.route('/test', methods=['GET'])
def hello_world():
    data = jsonify({"message": "Hello Poland"})
    return data

@app.route('/audio/<filename>')
def serve_audio(filename):
    return send_from_directory(AUDIO_FILE_PATH, filename)

@app.route('/audio-list')
def get_audio_list():
    audio_files = [f for f in os.listdir(AUDIO_FILE_PATH) if f.endswith('.webm')]
    return jsonify(audio_files)

@app.route('/addentry', methods=["POST"])
def add_entry(file_name):
    webm_file = f"{AUDIO_FILE_PATH}{file_name}.webm"
    mp3_file = f"{AUDIO_FILE_PATH}{file_name}.mp3"
    try:
        old_file = VideoFileClip(webm_file)
        audio_clip = old_file.audio
        audio_clip.write_audiofile(mp3_file)

        audio_clip.close()
        old_file.close()
        return jsonify({"status": "Success"})
    except Exception as e:
        return jsonify({"status": f"failure {Exception}"})

if __name__ == '__main__':
    app.run()
