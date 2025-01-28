from config import AUDIO_FILE_PATH, GRAMMAR_FILE_PATH
from audiohelper import combine_audio_files, create_silent_audio, duration_command
import os
import pickle
import random
from decimal import Decimal
from utils import send_email, generate_random_string, text_to_speech, translate_text
from aigenerator import with_turbo

familiar_bias_probs = {1: 1, 2: 2, 3: 3, 4: 7, 5: 17}
unfamiliar_bias_probs = {1: 27, 2: 14, 3: 11, 4: 8, 5: 1}

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

        lessons = generate_lessons(conn, data)
        total_time_lessons = sum(l[1] for l in lessons)

        data["length"] = str(float(data["length"]) - (total_time_lessons / 60))

        if data["familiarity_level"] == "Random":
            # basic_paths = random_path_gen(audio_files, data)
            # TODOLATER
            basic_paths = []
            # TODOLATER
        elif data["familiarity_level"] == "All":
            # basic_paths = gen_all(audio_files, data)
            basic_paths = []
        else:
            basic_paths = bias_gen(audio_files, data, data["familiarity_level"])

        # print("prior to phases")
        if int(data["percent"]) > 0:
            generated_phrase_paths = phrase_audio_gen(with_turbo(conn), data, conn)
        else:
            generated_phrase_paths = []
        final_audio = []
        
        all_paths = lessons + basic_paths + generated_phrase_paths
        # print(all_paths)

        curr_combo = []
        curr_time = 0
        total_time = 0
        for path in all_paths:
            curr_combo.append(path[0])
            curr_time += float(path[1])
            total_time += float(path[1])

            if curr_time > 740:
                final_path = f"{AUDIO_FILE_PATH}{generate_random_string(25)}random.mp3"
                combine_audio_files(final_path, curr_combo)
                final_audio.append(final_path)
                curr_combo = []
                curr_time = 0

        if len(curr_combo) > 0:
            final_path = f"{AUDIO_FILE_PATH}{generate_random_string(25)}random.mp3"
            combine_audio_files(final_path, curr_combo)
            final_audio.append(final_path)

        print(final_audio)
        # print("HERE 234234", final_audio)
        for i in range(len(final_audio)):
            send_email(data["email"], final_audio[i], i + 1, len(final_audio))
        
        # print(final_audio)
        # print(basic_paths[1])
        
        os.remove(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")     
        for path in final_audio:
            if os.path.exists(path):
                os.remove(path)
            else:
                print("SHOULD NOT HAVE MADE IT HERE 1")
        for path in basic_paths:
            if os.path.exists(path[0]):
                os.remove(path[0])
            else:
                print("SHOULD NOT HAVE MADE IT HERE 3")
        for path in generated_phrase_paths:
            if os.path.exists(path[0]):
                os.remove(path[0])
            else:
                print("SHOULD NOT HAVE MADE IT HERE 3")
        if os.path.exists(f"{AUDIO_FILE_PATH}set-generated-silence.mp3"):
            os.remove(f"{AUDIO_FILE_PATH}set-generated-silence.mp3")
        return total_time
    except Exception as e:
        print(f"Error: {str(e)}")

def random_path_gen(audio_files, data):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    basic_paths = []
    silence_basic_paths = []
    total_time = 0
    idx_greater_12 = [0]
    multiple = 12 * 60

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)) * Decimal((1 - int(data["percent_orig"]) * .01)) and len(audio_files) > 0:

        if total_time > multiple:
            idx_greater_12.append(len(basic_paths))
            multiple += 12 * 60

        word = random.choice(audio_files)

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")

        speedy_path = f"{AUDIO_FILE_PATH}{word['original_word'].replace('?', '_')}-{data['speed']}-{generate_random_string(20)}.mp3"

        create_silent_audio(speedy_path, gap_funcs[data['speed']](word['translated_duration']))
        basic_paths.append(speedy_path)
        silence_basic_paths.append(speedy_path)

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_path']}")
        basic_paths.append(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")

        total_time += Decimal(word["original_duration"])
        total_time += Decimal(str(gap_funcs[data['speed']](word['translated_duration'])))
        total_time += Decimal(word["translated_duration"])
        total_time += Decimal(data["gap"])

        index_of_random_dict = audio_files.index(word)
        audio_files.pop(index_of_random_dict)

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)) and len(audio_files) > 0:

        if total_time > multiple:
            idx_greater_12.append(len(basic_paths))
            multiple += 12 * 60

        word = random.choice(audio_files)

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_path']}")

        speedy_path = f"{AUDIO_FILE_PATH}{word['original_word'].replace('?', '_')}-{data['speed']}-{generate_random_string(20)}.mp3"
        create_silent_audio(speedy_path, gap_funcs[data['speed']](word['translated_duration']))
        basic_paths.append(speedy_path)
        silence_basic_paths.append(speedy_path)

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")
        basic_paths.append(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")

        total_time += Decimal(word["original_duration"])
        total_time += Decimal(str(gap_funcs[data['speed']](word['translated_duration'])))
        total_time += Decimal(word["translated_duration"])
        total_time += Decimal(data["gap"])

        index_of_random_dict = audio_files.index(word)
        audio_files.pop(index_of_random_dict)

    print(f"Final file length: {total_time}")
    return (basic_paths, silence_basic_paths, total_time, idx_greater_12)

def bias_gen(audio_files, data, bias):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    unfamiliar = [item for item in audio_files if item["familiarity"] < 5]
    familiar = [item for item in audio_files if item["familiarity"] == 5]

    if bias == "Unfamiliar":
        weights = [88, 12]
    else:
        weights = [20, 80]

    basic_paths = []
    total_time = 0
    temp = []

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)) * Decimal((1 - int(data["percent_orig"]) * .01)):
        # TODOLATER fix for groups that contain no elements
        group = random.choices([unfamiliar, familiar], weights=weights, k=1)[0]
        word = random.choice(group)

        temp = []

        temp.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")

        speedy_path = f"{AUDIO_FILE_PATH}{word['original_word'].replace('?', '_')}-{data['speed']}-{generate_random_string(20)}.mp3"
        silence_dur = gap_funcs[data['speed']](word['translated_duration'])
        create_silent_audio(speedy_path, silence_dur)
        temp.append(speedy_path)

        temp.append(f"{AUDIO_FILE_PATH}{word['original_path']}")
        temp.append(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")

        final_path = f"{AUDIO_FILE_PATH}{generate_random_string(25)}random.mp3"
        combine_audio_files(final_path, temp)

        os.remove(speedy_path)

        temp_total_time = 0
        temp_total_time += Decimal(word["original_duration"])
        temp_total_time += Decimal(str(silence_dur))
        temp_total_time += Decimal(word["translated_duration"])
        temp_total_time += Decimal(data["gap"])

        basic_paths.append((final_path, temp_total_time))
        total_time += temp_total_time

        # denom_list = [x for x in denom_list if x != word_idx]

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)):
        
        group = random.choices([unfamiliar, familiar], weights=weights, k=1)[0]
        word = random.choice(group)

        temp = []

        temp.append(f"{AUDIO_FILE_PATH}{word['original_path']}")

        speedy_path = f"{AUDIO_FILE_PATH}{word['original_word'].replace('?', '_')}-{data['speed']}-{generate_random_string(20)}.mp3"
        create_silent_audio(speedy_path, gap_funcs[data['speed']](word['translated_duration']))
        temp.append(speedy_path)

        temp.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")
        temp.append(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")

        final_path = f"{AUDIO_FILE_PATH}{generate_random_string(25)}random.mp3"
        combine_audio_files(final_path, temp)

        os.remove(speedy_path)

        temp_total_time = 0
        temp_total_time += Decimal(word["original_duration"])
        temp_total_time += Decimal(str(silence_dur))
        temp_total_time += Decimal(word["translated_duration"])
        temp_total_time += Decimal(data["gap"])

        basic_paths.append((final_path, temp_total_time))
        total_time += temp_total_time

        # denom_list = [x for x in denom_list if x != word_idx]

    print(f"Final file length: {total_time}")
    return basic_paths

def phrase_audio_gen(phrases, data, conn):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    random.shuffle(phrases)

    phrases_idx = 0
    generated_phrase_paths = []
    total_time = 0

    while total_time < Decimal(data["length"]) * 60 * Decimal(int(data["percent"]) * .01) and phrases_idx < len(phrases):

        if phrases_idx == len(phrases) - 1:
            phrases = with_turbo(conn)
            phrases_idx = 0

        translated_path = text_to_speech(phrases[phrases_idx])
        translated_duration = duration_command(f"{AUDIO_FILE_PATH}{translated_path}")
        temp = []

        temp.append(f"{AUDIO_FILE_PATH}{translated_path}")

        generated_silent_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
        create_silent_audio(generated_silent_path, gap_funcs["very_slow"](translated_duration))
        temp.append(generated_silent_path)

        original_word = translate_text(phrases[phrases_idx], target_language='en')
        original_path = text_to_speech(original_word, language="en")
        original_duration = duration_command(f"{AUDIO_FILE_PATH}{original_path}")

        temp.append(f"{AUDIO_FILE_PATH}{original_path}")
        temp.append(f"{AUDIO_FILE_PATH}set-generated-silence.mp3")

        # print(translated_duration, Decimal(gap_funcs["very_slow"](translated_duration)), original_duration, 5.0)
        temp_total_time = 0
        temp_total_time += translated_duration
        temp_total_time += float(str(gap_funcs["very_slow"](translated_duration)))
        temp_total_time += original_duration
        temp_total_time += 5.0

        final_path = f"{AUDIO_FILE_PATH}{generate_random_string(25)}random.mp3"
        combine_audio_files(final_path, temp)

        os.remove(generated_silent_path)

        generated_phrase_paths.append((final_path, temp_total_time))

        total_time += temp_total_time

        phrases_idx += 1

    print(f"Final file length: {total_time}")
    return (generated_phrase_paths)

def gen_all(audio_files, data):
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    basic_paths = []
    silence_basic_paths = []
    total_time = 0
    idx_greater_12 = [0]
    multiple = 12 * 60

    while len(audio_files) > 0:

        if total_time > multiple:
            idx_greater_12.append(len(basic_paths))
            multiple += 12 * 60

        word = random.choice(audio_files)

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['original_path']}")

        speedy_path = f"{AUDIO_FILE_PATH}{word['original_word'].replace('?', '_')}-{data['speed']}-{generate_random_string(20)}.mp3"
        create_silent_audio(speedy_path, gap_funcs[data['speed']](word['translated_duration']))
        basic_paths.append(speedy_path)
        silence_basic_paths.append(speedy_path)

        basic_paths.append(f"{AUDIO_FILE_PATH}{word['translated_path']}")
        basic_paths.append(f"{AUDIO_FILE_PATH}set-basic-silence.mp3")

        total_time += Decimal(word["original_duration"])
        total_time += Decimal(str(gap_funcs[data['speed']](word['translated_duration'])))
        total_time += Decimal(word["translated_duration"])
        total_time += Decimal(data["gap"])

        index_of_random_dict = audio_files.index(word)
        audio_files.pop(index_of_random_dict)

    print(f"Final file length: {total_time}")
    return (basic_paths, silence_basic_paths, total_time, idx_greater_12)

def generate_lessons(conn, data):
    print("generating lessons")
    lesson_paths = []
    if len(data["ltl"]) > 0:
        with conn.cursor() as cur:
            sql = f"SELECT * FROM db.lessons WHERE id IN ({', '.join(['%s'] * len(data["ltl"]))})"   
            cur.execute(sql, data["ltl"])
            lessons = cur.fetchall()
        
        for lesson in lessons:
            lesson_paths.append((f"{GRAMMAR_FILE_PATH}{lesson["path"]}", float(lesson["duration"])))

    print(lesson_paths)
    
    return lesson_paths
    
