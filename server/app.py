from flask import Flask, jsonify, send_from_directory, request, render_template
from flask_cors import CORS
import pymysql
from config import AUDIO_FILE_PATH
import os
from audiohelper import convert_webm_to_mp3, duration_command
from utils import change_file_extension
from podgenerator import generate_pod

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
    try:
        with conn.cursor() as cur:
            sql = "SELECT * FROM db.words"
            cur.execute(sql)
            audio_files = cur.fetchall()
        conn.commit()
        return jsonify(audio_files)
    except Exception as e:
        return jsonify([{"message": f"Error: {str(e)}"}])

@app.route('/addentry', methods=["POST"])
def add_entry():

    data = request.get_json()
    print(data)

    mp3_polish_file = change_file_extension(data["polish_path"], 'mp3')
    convert_webm_to_mp3(f"{AUDIO_FILE_PATH}{data['polish_path']}", f"{AUDIO_FILE_PATH}{mp3_polish_file}")
    polish_duration = duration_command(f"{AUDIO_FILE_PATH}{mp3_polish_file}")
    os.remove(f"{AUDIO_FILE_PATH}{data['polish_path']}")

    mp3_english_file = change_file_extension(data["english_path"], 'mp3')
    convert_webm_to_mp3(f"{AUDIO_FILE_PATH}{data['english_path']}", f"{AUDIO_FILE_PATH}{mp3_english_file}")
    english_duration = duration_command(f"{AUDIO_FILE_PATH}{mp3_english_file}")
    os.remove(f"{AUDIO_FILE_PATH}{data['english_path']}")

    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO db.words (word, polish_path, polish_length, familiarity, english_path, english_length) VALUES (%s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (data["word"], mp3_polish_file, polish_duration, data["familiarity"], mp3_english_file, english_duration))
        conn.commit()
        return jsonify({"message": "Data should be inserted successfully at this point"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/removeentry', methods=["POST"])
def remove_entry():

    data = request.get_json()
    print(data)
    
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM db.words WHERE polish_path = %s"
            cur.execute(sql, (data["polish_path"]))
        conn.commit()
        os.remove(f"{AUDIO_FILE_PATH}{data['polish_path']}")
        os.remove(f"{AUDIO_FILE_PATH}{data['english_path']}")
        return jsonify({"message": "Data should be deleted successfully at this point"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/generatepodcast', methods=["POST"])
def generate_podcast():

    data = request.get_json()
    print(data)
    
    try:
        generate_pod(conn, data)
        return jsonify({"message": "Podcast is generated"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/updatefamlevel', methods=["POST"])
def update_fam_level():

    data = request.get_json()
    print(data)

    try:
        with conn.cursor() as cursor:
            update_query = f"UPDATE db.words SET familiarity = %s WHERE id = %s"
            cursor.execute(update_query, (data["familiarity"], data["id"]))
            conn.commit()
        return jsonify({"message": "Value is updated"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})
    
if __name__ == '__main__':
    app.run()
