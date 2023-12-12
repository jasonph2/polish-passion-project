from flask import Flask, jsonify, send_from_directory, request, render_template
from flask_cors import CORS
from moviepy.editor import VideoFileClip
import pymysql
from config import AUDIO_FILE_PATH
import os

app = Flask(__name__)
CORS(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'db'

try:
    conn = pymysql.connect(host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor)
    print("connected successfully")
except Exception as e:
    print(f"Error connecting to MySQL: {str(e)}")

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

# @app.route('/addentry', methods=["POST"])
# def add_entry(file_name):
#     webm_file = f"{AUDIO_FILE_PATH}{file_name}.webm"
#     mp3_file = f"{AUDIO_FILE_PATH}{file_name}.mp3"
#     try:
#         old_file = VideoFileClip(webm_file)
#         audio_clip = old_file.audio
#         audio_clip.write_audiofile(mp3_file)

#         audio_clip.close()
#         old_file.close()
#         return jsonify({"status": "Success"})
#     except Exception as e:
#         return jsonify({"status": f"failure {Exception}"})

@app.route('/addentry', methods=["POST"])
def add_entry():
    word = "temp"
    path = "/this/is/path"
    rec_length = 10.4
    familiarity = 1

    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO db.words (word, path, rec_length, familiarity) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (word, path, rec_length, familiarity))
        conn.commit()
        print("here1")
        return "Data should be inserted successfully at this point"
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"
    finally:
        conn.close()


if __name__ == '__main__':
    app.run()
