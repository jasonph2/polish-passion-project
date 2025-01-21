from config import AUDIO_FILE_PATH
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


        if data["familiarity_level"] == "Random":
            basic_paths = random_path_gen(audio_files, data)
        elif data["familiarity_level"] == "All":
            basic_paths = gen_all(audio_files, data)
        else:
            basic_paths = bias_gen(audio_files, data, data["familiarity_level"])

        # print("prior to phases")
        if int(data["percent"]) > 0:
            generated_phrase_paths = phrase_audio_gen(with_turbo(conn), data, conn)
        else:
            generated_phrase_paths = ([], [], 0, [])
        final_audio = []
        if len(basic_paths[0]) > 0 and len(generated_phrase_paths[0]) > 0:
            for i in range(len(basic_paths[3])):
                if i == len(basic_paths[3]) - 1:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, basic_paths[0][basic_paths[3][i]:])
                    final_audio.append(temp_path)
                else:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, basic_paths[0][basic_paths[3][i]: basic_paths[3][i + 1]])
                    final_audio.append(temp_path)

            for i in range(len(generated_phrase_paths[3])):
                if i == len(generated_phrase_paths[3]) - 1:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, generated_phrase_paths[0][generated_phrase_paths[3][i]:])
                    final_audio.append(temp_path)
                else:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, generated_phrase_paths[0][generated_phrase_paths[3][i]: generated_phrase_paths[3][i + 1]])
                    final_audio.append(temp_path)

            if len(final_audio) == 2 and Decimal(basic_paths[2]) + Decimal(generated_phrase_paths[2]) < 780:
                final_audio_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                combine_audio_files(final_audio_path, final_audio)
                final_audio = [final_audio_path]

        elif len(basic_paths[0]) > 0:
            for i in range(len(basic_paths[3])):
                if i == len(basic_paths[3]) - 1:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, basic_paths[0][basic_paths[3][i]:])
                    final_audio.append(temp_path)
                else:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, basic_paths[0][basic_paths[3][i]: basic_paths[3][i + 1]])
                    final_audio.append(temp_path)

        elif len(generated_phrase_paths[0]) > 0:
            for i in range(len(generated_phrase_paths[3])):
                if i == len(generated_phrase_paths[3]) - 1:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, generated_phrase_paths[0][generated_phrase_paths[3][i]:])
                    final_audio.append(temp_path)
                else:
                    temp_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
                    combine_audio_files(temp_path, generated_phrase_paths[0][generated_phrase_paths[3][i]: generated_phrase_paths[3][i + 1]])
                    final_audio.append(temp_path)

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
        for path in basic_paths[1]:
            if os.path.exists(path):
                os.remove(path)
            else:
                print("SHOULD NOT HAVE MADE IT HERE 2")
        temp_set = set(generated_phrase_paths[0])
        for path in temp_set:
            if os.path.exists(path):
                os.remove(path)
            else:
                print("SHOULD NOT HAVE MADE IT HERE 3")
        if os.path.exists(f"{AUDIO_FILE_PATH}set-generated-silence.mp3"):
            os.remove(f"{AUDIO_FILE_PATH}set-generated-silence.mp3")
        return Decimal(basic_paths[2]) + Decimal(generated_phrase_paths[2])
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

    denom_list = []
    for i in range(len(audio_files)):
        idx = 0
        if bias == "Familiar":
            while idx < familiar_bias_probs[audio_files[i]["familiarity"]]:
                denom_list.append(i)
                idx += 1
        elif bias == "Unfamiliar":
            while idx < unfamiliar_bias_probs[audio_files[i]["familiarity"]]:
                denom_list.append(i)
                idx += 1

    basic_paths = []
    silence_basic_paths = []
    total_time = 0
    idx_greater_12 = [0]
    multiple = 12 * 60

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)) * Decimal((1 - int(data["percent_orig"]) * .01)) and len(denom_list) > 0:

        if total_time > multiple:
            idx_greater_12.append(len(basic_paths))
            multiple += 12 * 60

        random_int = random.randint(0, len(denom_list) - 1)
        word_idx = denom_list[random_int]
        word = audio_files[word_idx]

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

        # denom_list = [x for x in denom_list if x != word_idx]

    while total_time < Decimal(data["length"]) * 60 * Decimal((1 - int(data["percent"]) * .01)) and len(denom_list) > 0:

        if total_time > multiple:
            idx_greater_12.append(len(basic_paths))
            multiple += 12 * 60

        random_int = random.randint(0, len(denom_list) - 1)
        word_idx = denom_list[random_int]
        word = audio_files[word_idx]

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

        # denom_list = [x for x in denom_list if x != word_idx]

    print(f"Final file length: {total_time}")
    return (basic_paths, silence_basic_paths, total_time, idx_greater_12)

def phrase_audio_gen(phrases, data, conn):
    print("HERE HERE")
    with open('time_funcs.pkl', 'rb') as file:
        gap_funcs = pickle.load(file)

    random.shuffle(phrases)

    phrases_idx = 0
    generated_phrase_paths = []
    silence_paths = []
    total_time = 0
    idx_greater_12 = [0]
    multiple = 12 * 60

    while total_time < Decimal(data["length"]) * 60 * Decimal(int(data["percent"]) * .01) and phrases_idx < len(phrases):

        if phrases_idx == len(phrases) - 1:
            print("HEREE 2")
            phrases = with_turbo(conn)
            print("HEREE 3")
            phrases_idx = 0

        if total_time > multiple:
            idx_greater_12.append(len(generated_phrase_paths))
            multiple += 12 * 60

        translated_path = text_to_speech(phrases[phrases_idx])
        translated_duration = duration_command(f"{AUDIO_FILE_PATH}{translated_path}")

        generated_phrase_paths.append(f"{AUDIO_FILE_PATH}{translated_path}")

        generated_silent_path = f"{AUDIO_FILE_PATH}{generate_random_string(20)}.mp3"
        create_silent_audio(generated_silent_path, gap_funcs["very_slow"](translated_duration))
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
    return (generated_phrase_paths, silence_paths, total_time, idx_greater_12)

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