from config import AUDIO_FILE_PATH
from audiohelper import combine_audio_files, create_silent_audio
import os
import pickle
from decimal import Decimal

def generate_pod(conn, data):
    try:
        if (data["length"] == ""):
            raise RuntimeError("pod unable to be generated")
        
        audio_files = []
        with conn.cursor() as cur:
            sql = "SELECT * FROM db.words"
            cur.execute(sql)
            audio_files = cur.fetchall()
        
        #switch to accept argument from front end later
        create_silent_audio(f"{AUDIO_FILE_PATH}set-silence.mp3", 2)
        with open('time_funcs.pkl', 'rb') as file:
            gap_funcs = pickle.load(file)

        paths = []
        silence_paths = []
        total_time = 0
        for word in audio_files:
            paths.append(f"{AUDIO_FILE_PATH}{word['polish_path']}")

            create_silent_audio(f"{AUDIO_FILE_PATH}{word['word']}-{data['speed']}.mp3", gap_funcs[data['speed']](word['polish_length']))
            paths.append(f"{AUDIO_FILE_PATH}{word['word']}-{data['speed']}.mp3")
            silence_paths.append(f"{AUDIO_FILE_PATH}{word['word']}-{data['speed']}.mp3")

            paths.append(f"{AUDIO_FILE_PATH}{word['english_path']}")
            paths.append(f"{AUDIO_FILE_PATH}set-silence.mp3")

            total_time += word["english_length"]
            total_time += Decimal(str(gap_funcs[data['speed']](word['polish_length'])))
            total_time += word["polish_length"]
            #change to accept argument from front end
            total_time += 2

        combine_audio_files(f"{AUDIO_FILE_PATH}testcombination.mp3", paths)
        print(f"Final file length: {total_time}")
        os.remove(f"{AUDIO_FILE_PATH}set-silence.mp3")
        for path in silence_paths:
            os.remove(path)
    except Exception as e:
        print(f"Error: {str(e)}")