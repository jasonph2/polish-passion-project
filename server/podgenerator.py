from config import AUDIO_FILE_PATH
from audiohelper import combine_audio_files, create_silent_audio, duration_command
import os
import pickle
import random
from decimal import Decimal
from utils import send_email, generate_random_string, text_to_speech, translate_text
from aigenerator import with_turbo

familiar_bias_probs = {1: 1, 2: 2, 3: 3, 4: 7, 5: 17}
unfamiliar_bias_probs = {1: 17, 2: 7, 3: 3, 4: 2, 5: 1}

def generate_pod(conn, data):
    try:
        if (data["length"] == ""):
            raise RuntimeError("pod unable to be generated")
        
        create_silent_audio(f"{AUDIO_FILE_PATH}set-basic-silence.mp3", data["gap"])
        create_silent_audio(f"{AUDIO_FILE_PATH}set-generated-silence.mp3", 5)

        audio_files = []
        with conn.cursor() as cur:
            sql = "SELECT * FROM db.words"
            cur.execute(sql)
            audio_files = cur.fetchall()


        if data["familiarity_level"] == "random":
            basic_paths = random_path_gen(audio_files, data)
        else:
            basic_paths = bias_gen(audio_files, data, data["familiarity_level"])

        generated_phrase_paths = phrase_audio_gen(with_turbo(conn), data)

        basic_audio = ""
        generated_phrase_audio = ""
        final_audio = ""
        if len(basic_paths[0]) > 0 and len(generated_phrase_paths[0]) > 0:
            basic_audio = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
            combine_audio_files(basic_audio, basic_paths[0])


            generated_phrase_audio = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
            combine_audio_files(generated_phrase_audio, generated_phrase_paths[0])


            final_audio = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
            combine_audio_files(final_audio, [basic_audio, generated_phrase_audio])

        elif len(basic_paths[0]) > 0:
            final_audio = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
            combine_audio_files(final_audio, basic_paths[0])

        elif len(generated_phrase_paths[0]) > 0:
            print("HERE123")
            print(generated_phrase_paths[0])
            final_audio = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
            combine_audio_files(final_audio, generated_phrase_paths[0])

        send_email(data["email"], final_audio)
        
        os.remove(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")
        if basic_audio != "":
            os.remove(basic_audio)
        if generated_phrase_audio != "":
            os.remove(generated_phrase_audio)
        os.remove(final_audio)
        for path in basic_paths[1]:
            os.remove(path)
        temp_set = set(generated_phrase_paths[0])
        for path in temp_set:
            os.remove(path)

    except Exception as e:
        print(f"Error: {str(e)}")

def random_path_gen(audio_files, data):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    basic_paths = []
    silence_basic_paths = []
    total_time = 0

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)):

        word = random.choice(audio_files)

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")

        create_silent_audio(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3", gap_funcs[data['speed']](word['translated_duration']))
        basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")
        silence_basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_path']}")
        basic_paths.append(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")

        total_time += word["original_duration"]
        total_time += Decimal(str(gap_funcs[data['speed']](word['translated_duration'])))
        total_time += word["translated_duration"]
        total_time += Decimal(data["gap"])

        index_of_random_dict = audio_files.index(word)
        audio_files.pop(index_of_random_dict)

    print(f"Final file length: {total_time}")
    return (basic_paths, silence_basic_paths)

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
    basic_paths = []
    silence_basic_paths = []
    total_time = 0

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)):

        random_int = random.randint(0, len(denom_list) - 1)
        word_idx = denom_list[random_int]
        word = audio_files[word_idx]
        print(word["familiarity"])

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")

        create_silent_audio(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3", gap_funcs[data['speed']](word['translated_duration']))
        basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")
        silence_basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_word']}-{data['speed']}.mp3")

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_path']}")
        basic_paths.append(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")

        total_time += word["original_duration"]
        total_time += Decimal(str(gap_funcs[data['speed']](word['translated_duration'])))
        total_time += word["translated_duration"]
        total_time += Decimal(data["gap"])

        denom_list = [x for x in denom_list if x != word_idx]

    print(f"Final file length: {total_time}")
    return (basic_paths, silence_basic_paths)

def phrase_audio_gen(phrases, data):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    random.shuffle(phrases)

    phrases_idx = 0
    generated_phrase_paths = []
    silence_paths = []
    total_time = 0

    while total_time < Decimal(data["length"]) * 60 * Decimal(int(data["percent"]) * .01) and phrases_idx < len(phrases):
        print("HERE1")
        translated_path = text_to_speech(phrases[phrases_idx])
        translated_duration = duration_command(f"{AUDIO_FILE_PATH}{translated_path}")
        print("HERE2")

        generated_phrase_paths.append(f"{AUDIO_FILE_PATH}{translated_path}")

        generated_silent_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
        create_silent_audio(generated_silent_path, gap_funcs["very_slow"](translated_duration))
        print(generated_silent_path)
        generated_phrase_paths.append(generated_silent_path)
        silence_paths.append(generated_silent_path)

        original_word = translate_text(phrases[phrases_idx], target_language='en')
        original_path = text_to_speech(original_word, language="en")
        original_duration = duration_command(f"{AUDIO_FILE_PATH}{original_path}")

        generated_phrase_paths.append(f"{AUDIO_FILE_PATH}{original_path}")
        generated_phrase_paths.append(f"{AUDIO_FILE_PATH}set-generated-silence.mp3")

        # print(translated_duration, Decimal(gap_funcs["very_slow"](translated_duration)), original_duration, 5.0)
        total_time += translated_duration
        total_time += float(str(gap_funcs["very_slow"](translated_duration)))
        total_time += original_duration
        total_time += 5.0

        phrases_idx += 1

    print(f"Final file length: {total_time}")
    return (generated_phrase_paths, silence_paths)