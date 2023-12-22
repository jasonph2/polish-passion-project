from config import AUDIO_FILE_PATH
from audiohelper import combine_audio_files, create_silent_audio
import os
import pickle
import random
from decimal import Decimal
from utils import send_email

familiar_bias_probs = {1: 1, 2: 2, 3: 3, 4: 7, 5: 17}
unfamiliar_bias_probs = {1: 17, 2: 7, 3: 3, 4: 2, 5: 1}

def generate_pod(conn, data):
    try:
        if (data["length"] == ""):
            raise RuntimeError("pod unable to be generated")
        
        create_silent_audio(f"{AUDIO_FILE_PATH}set-silence.mp3", data["gap"])

        audio_files = []
        with conn.cursor() as cur:
            sql = "SELECT * FROM db.words"
            cur.execute(sql)
            audio_files = cur.fetchall()

        print(audio_files)

        if data["familiarity_level"] == "random":
            paths = random_path_gen(audio_files, data)
        else:
            paths = bias_gen(audio_files, data, data["familiarity_level"])

        combine_audio_files(f"{AUDIO_FILE_PATH}testcombination.mp3", paths[0])

        send_email(data["email"], f"{AUDIO_FILE_PATH}testcombination.mp3")
        
        os.remove(f"{AUDIO_FILE_PATH}set-silence.mp3")
        for path in paths[1]:
            os.remove(path)

    except Exception as e:
        print(f"Error: {str(e)}")

def random_path_gen(audio_files, data):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    paths = []
    silence_paths = []
    total_time = 0

    while total_time < Decimal(data["length"]) * 60:

        word = random.choice(audio_files)

        paths.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")

        create_silent_audio(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3", gap_funcs[data['speed']](word['translated_duration']))
        paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")
        silence_paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")

        paths.append(f"{AUDIO_FILE_PATH}{word['original_path']}")
        paths.append(f"{AUDIO_FILE_PATH}set-silence.mp3")

        total_time += word["original_duration"]
        total_time += Decimal(str(gap_funcs[data['speed']](word['translated_duration'])))
        total_time += word["translated_duration"]
        total_time += Decimal(data["gap"])

        index_of_random_dict = audio_files.index(word)
        audio_files.pop(index_of_random_dict)

    print(f"Final file length: {total_time}")
    return (paths, silence_paths)

def bias_gen(audio_files, data, bias):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    denom_list = []
    for i in range(len(audio_files)):
        idx = 0
        if bias == "familiar":
            while idx < familiar_bias_probs[audio_files[i]["familiarity"]]:
                denom_list.append(i)
                idx += 1
        elif bias == "unfamiliar":
            while idx < unfamiliar_bias_probs[audio_files[i]["familiarity"]]:
                denom_list.append(i)
                idx += 1

    print(denom_list)
    paths = []
    silence_paths = []
    total_time = 0

    while total_time < Decimal(data["length"]) * 60:

        random_int = random.randint(0, len(denom_list) - 1)
        word_idx = denom_list[random_int]
        word = audio_files[word_idx]
        print(word["familiarity"])

        paths.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")

        create_silent_audio(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3", gap_funcs[data['speed']](word['translated_duration']))
        paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")
        silence_paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")

        paths.append(f"{AUDIO_FILE_PATH}{word['original_path']}")
        paths.append(f"{AUDIO_FILE_PATH}set-silence.mp3")

        total_time += word["original_duration"]
        total_time += Decimal(str(gap_funcs[data['speed']](word['translated_duration'])))
        total_time += word["translated_duration"]
        total_time += Decimal(data["gap"])

        denom_list = [x for x in denom_list if x != word_idx]

    print(f"Final file length: {total_time}")
    return (paths, silence_paths)