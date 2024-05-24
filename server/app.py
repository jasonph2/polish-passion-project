from flask import Flask, jsonify, send_from_directory, request, render_template
from flask_cors import CORS
import pymysql
from config import AUDIO_FILE_PATH, USER_EMAIL
import os
from audiohelper import duration_command
from utils import translate_text, text_to_speech, is_single_word, find_frequency
from podgenerator import generate_pod
from datetime import date, datetime
from aigenerator import with_turbo
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


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

@app.route('/audiolist')
def get_audio_list():
    try:
        with conn.cursor() as cur:
            sql = "SELECT * FROM db.words ORDER BY id DESC"
            cur.execute(sql)
            audio_files = cur.fetchall()
        conn.commit()
        return jsonify(audio_files)
    except Exception as e:
        return jsonify([{"message": f"Error: {str(e)}"}])

# @app.route('/addentry', methods=["POST"])
# def add_entry():

#     data = request.get_json()
#     print(data)

#     mp3_polish_file = change_file_extension(data["polish_path"], 'mp3')
#     convert_webm_to_mp3(f"{AUDIO_FILE_PATH}{data['polish_path']}", f"{AUDIO_FILE_PATH}{mp3_polish_file}")
#     polish_duration = duration_command(f"{AUDIO_FILE_PATH}{mp3_polish_file}")
#     os.remove(f"{AUDIO_FILE_PATH}{data['polish_path']}")

#     mp3_english_file = change_file_extension(data["english_path"], 'mp3')
#     convert_webm_to_mp3(f"{AUDIO_FILE_PATH}{data['english_path']}", f"{AUDIO_FILE_PATH}{mp3_english_file}")
#     english_duration = duration_command(f"{AUDIO_FILE_PATH}{mp3_english_file}")
#     os.remove(f"{AUDIO_FILE_PATH}{data['english_path']}")

#     try:
#         with conn.cursor() as cur:
#             sql = "INSERT INTO db.words (original_word, original_path, original_duration, translated_word, translated_path, translated_duration, familiarity) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#             cur.execute(sql, (data["word"], mp3_english_file, english_duration, data["translated_word"], mp3_polish_file, polish_duration, data["familiarity"]))
#         conn.commit()
#         return jsonify({"message": "Data should be inserted successfully at this point"})
#     except Exception as e:
#         return jsonify({"message": f"Error: {str(e)}"})

@app.route('/removeentry', methods=["POST"])
def remove_entry():

    data = request.get_json()
    print(data)
    
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM db.words WHERE translated_path = %s"
            cur.execute(sql, (data["translated_path"]))
        conn.commit()
        os.remove(f"{AUDIO_FILE_PATH}{data['translated_path']}")
        os.remove(f"{AUDIO_FILE_PATH}{data['original_path']}")
        return jsonify({"message": "Data should be deleted successfully at this point"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/generatepodcast', methods=["POST"])
def generate_podcast():

    data = request.get_json()
    data["email"] = USER_EMAIL
    print(data)
    
    try:
        pod_time = generate_pod(conn, data)
        with conn.cursor() as cur:
            sql = "INSERT INTO db.podcasts (date, duration, generated_percentage, familiarity, listened) VALUES (%s, %s, %s, %s, %s)"
            cur.execute(sql, (datetime.now(), pod_time, data["percent"], data["familiarity_level"], 0))
        conn.commit()
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

@app.route('/getaudio', methods=["POST"])
def get_audio():

    data = request.get_json()

    translated_word = translate_text(data["word"])
    path = text_to_speech(translated_word)

    return jsonify({"path": path})

@app.route('/removeaudio', methods=["POST"])
def remove_audio():

    data = request.get_json()

    os.remove(f"{AUDIO_FILE_PATH}{data['path']}")

    return jsonify({"message": "Audio is removed"})

@app.route('/submitword', methods=["POST"])
def submit_word():

    data = request.get_json()
    print(data)

    original_word = data["word"]
    original_path = text_to_speech(original_word, "en")
    original_duration = duration_command(f"{AUDIO_FILE_PATH}{original_path}")
    translated_word = translate_text(data["word"])
    translated_path = data["path"]
    translated_duration = duration_command(f"{AUDIO_FILE_PATH}{translated_path}")

    frequency = -1
    if is_single_word(translated_word):
        frequency = find_frequency(translated_word)


    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO db.words (original_word, original_path, original_duration, translated_word, translated_path, translated_duration, familiarity, date, frequency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (original_word, original_path, original_duration, translated_word, translated_path, translated_duration, data["familiarity"], date.today(), frequency))
        conn.commit()
        return jsonify({"message": "Data should be inserted successfully at this point"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/generatephrase', methods=["POST"])
def generate_phrase():

    phrase = with_turbo(conn)

    return jsonify({"message": phrase})

@app.route('/podcastlist')
def get_podcast_list():
    try:
        with conn.cursor() as cur:
            sql = "SELECT * FROM db.podcasts ORDER BY id DESC"
            cur.execute(sql)
            podcasts = cur.fetchall()
        conn.commit()
        return jsonify(podcasts)
    except Exception as e:
        return jsonify([{"message": f"Error: {str(e)}"}])
    
@app.route('/removepodcastentry', methods=["POST"])
def remove_podcast_entry():

    data = request.get_json()
    print(data)
    
    try:
        with conn.cursor() as cur:
            sql = "DELETE FROM db.podcasts WHERE id = %s"
            cur.execute(sql, (data["id"]))
        conn.commit()
        return jsonify({"message": "Data should be deleted successfully at this point"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

@app.route('/updatelistenedstatus', methods=["POST"])
def update_listened_status():

    data = request.get_json()
    print(data)

    try:
        with conn.cursor() as cursor:
            update_query = f"UPDATE db.podcasts SET listened = %s WHERE id = %s"
            cursor.execute(update_query, (data["listened"], data["id"]))
            conn.commit()
        return jsonify({"message": "Value is updated"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})
    
@app.route('/submitmanualword', methods=["POST"])
def submit_manual_word():

    data = request.get_json()
    print(data)

    original_word = data["original_word"]
    original_path = text_to_speech(original_word, "en")
    original_duration = duration_command(f"{AUDIO_FILE_PATH}{original_path}")
    translated_word = data["translated_word"]
    translated_path = text_to_speech(translated_word, "pl")
    translated_duration = duration_command(f"{AUDIO_FILE_PATH}{translated_path}")

    frequency = -1
    if is_single_word(translated_word):
        frequency = find_frequency(translated_word)

    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO db.words (original_word, original_path, original_duration, translated_word, translated_path, translated_duration, familiarity, date, frequency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (original_word, original_path, original_duration, translated_word, translated_path, translated_duration, data["familiarity"], date.today(), frequency))
        conn.commit()
        return jsonify({"message": "Data should be inserted successfully at this point"})
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})
    
@app.route('/getfreqwords', methods=["POST"])
def get_freq_words():
    data = request.get_json()
    print(data)
    
    existing_freqss = []
    try:
        with conn.cursor() as cur:
                sql = "SELECT frequency FROM db.words ORDER BY frequency"
                cur.execute(sql)
                existing_freqss = cur.fetchall()
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"})

    existing_freqs = [row["frequency"] for row in existing_freqss if row["frequency"] != -1]
    print(existing_freqs)
    new_words = []
    with open("Polish-Frequencies.csv", encoding='utf-8') as f:
        csv_idx = 0
        ex_idx = 1
        while len(new_words) < int(data["freq"]):
            line = f.readline()
            csv_idx += 1
            if csv_idx not in existing_freqs:
                print("HERE 1")
                new_words.append((line.strip(), csv_idx, ""))
            else:
                print("HERE 2")
                ex_idx += 1
    
    service = webdriver.ChromeService(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    base = "https://dictionary.cambridge.org/us/dictionary/polish-english/"

    urls = [base + word[0] for word in new_words]

    print(urls)

    xpath = '/html/body/div[2]/div/div[1]/div[2]/article/div[2]/div[1]/span/div/div[4]/div/div[1]/div[2]/div/div[3]/span/a/span'
    original_words = []
    try:
        idx = 0
        for url in urls:
            driver.get(url)
            try:
                element = driver.find_element("xpath", xpath)
                print(f"Element Text from {url}:", element.text)
                original_words.append(element.text)
            except Exception as e:
                original_words.append(translate_text(new_words[idx][0], "en"))
                print(f"An error occurred on {url}: {e}")
            idx += 1
    except Exception as e:
        print(f"An overall error occurred: {e}")

    # Close the browser
    driver.quit()
    print(len(original_words))
    print(original_words)
    idx = 0
    for translated_word in new_words:

        original_word = original_words[idx]
        print(original_word)
        original_path = text_to_speech(original_word, "en")
        original_duration = duration_command(f"{AUDIO_FILE_PATH}{original_path}")
        translated_path = text_to_speech(translated_word[0], "pl")
        translated_duration = duration_command(f"{AUDIO_FILE_PATH}{translated_path}")

        try:
            with conn.cursor() as cur:
                sql = "INSERT INTO db.words (original_word, original_path, original_duration, translated_word, translated_path, translated_duration, familiarity, date, frequency) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                cur.execute(sql, (original_word, original_path, original_duration, translated_word[0], translated_path, translated_duration, 1, date.today(), translated_word[1]))
            conn.commit()
        except Exception as e:
            return jsonify({"message": f"Error: {str(e)}"})

        idx += 1
    return jsonify({"message": new_words})

if __name__ == '__main__':
    app.run()
