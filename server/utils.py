import os
import smtplib
from config import EMAIL_USERNAME, EMAIL_PASSWORD, AUDIO_FILE_PATH, TUTOR_EMAIL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email import encoders
import random
from googletrans import Translator
from gtts import gTTS
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import date, datetime
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from collections import defaultdict

# changes the file extension and returns a new string
def change_file_extension(file_path, new_extension):
    directory, filename_with_extension = os.path.split(file_path)
    filename, _ = os.path.splitext(filename_with_extension)

    new_file_path = os.path.join(directory, f"{filename}.{new_extension}")

    return new_file_path

def send_email(recipient_email, mp3_file_path, audio_file_num, audio_file_total_num):

    message = MIMEMultipart()
    message['From'] = EMAIL_USERNAME
    message['To'] = recipient_email
    if audio_file_total_num > 1:
        message['Subject'] = f"MP3 file {audio_file_num} out of {audio_file_total_num}"
    else:
        message['Subject'] = "Here is your MP3 file!"

    with open(mp3_file_path, 'rb') as mp3_file:
        mp3_attachment = MIMEAudio(mp3_file.read(), 'mp3')
        mp3_attachment.add_header('Content-Disposition', f'attachment; filename="{mp3_file_path}"')
        print("Inside email send", mp3_file_path)
        message.attach(mp3_attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        server.sendmail(EMAIL_USERNAME, recipient_email, message.as_string())

    print("Email sent successfully!")

def translate_text(text, target_language='pl'):
    translator = Translator()
    translated_text = ""
    try:
        translated_text = translator.translate(text, dest=target_language)
    except Exception as e:
        print(e)
    return translated_text.text

def text_to_speech(desired_text, language='pl'):

    tts = gTTS(text=desired_text, lang=language, slow=False)

    desired_text = desired_text.replace('?', '')
    path = f"{desired_text.replace(' ', '_')}-{generate_random_string(15)}.mp3"
    tts.save(f"{AUDIO_FILE_PATH}{path}")
    return path

def generate_random_string(length):
    characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    result = ''

    for _ in range(length):
        random_index = random.randint(0, len(characters) - 1)
        result += characters[random_index]

    return result

def is_single_word(s):
    return not any(c.isspace() for c in s)

def find_frequency(word):
    encodings = ['utf-8', 'latin-1', 'cp1250']  # Add more encodings as needed
    for encoding in encodings:
        try:
            with open("Polish-Frequencies.csv", encoding=encoding) as f:
                idx = 0
                for line in f:
                    idx += 1
                    if word.lower() == line.strip():
                        return idx
                #print(encoding)
            return -1
        except UnicodeDecodeError:
            continue
    return -1

def send_all_email(words):

    word_list = [item['translated_word'] for item in words]

    original_list = "\t".join(word_list)
    
    sorted_list = "\t".join(sorted(word_list))
    
    body = f"Original List:\n{original_list}\n\nAlphabetically Sorted List:\n{sorted_list}"

    message = MIMEMultipart()
    message['From'] = EMAIL_USERNAME
    message['To'] = TUTOR_EMAIL
    message['Subject'] = "List of all Polish words"

    message.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        server.sendmail(EMAIL_USERNAME, TUTOR_EMAIL, message.as_string())

def get_listen_monthly(data):
    all_dates = [datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S.%f') for entry in data]
    start_date = min(all_dates).replace(day=1)
    end_date = max(all_dates).replace(day=2)

    current_date = start_date
    listening_data = {}

    while current_date <= end_date:
        listening_data[current_date.strftime('%m-%Y')] = 0
        next_month = current_date.month % 12 + 1
        year = current_date.year + (current_date.month // 12)
        current_date = current_date.replace(year=year, month=next_month)
    
    for entry in data:
        mmyyyy = datetime.strptime(entry['date'], '%Y-%m-%d %H:%M:%S.%f')
        key = mmyyyy.strftime('%m-%Y')
        listening_data[key] += float(entry['duration']) * int(entry['listened'])
    
    for key in listening_data:
        listening_data[key] /= 3600

    print(listening_data)
    
    months = list(listening_data.keys())
    totals = list(listening_data.values())

    fig, ax = plt.subplots(figsize=(10, 6))  
    
    bars = ax.bar(months, totals, color='skyblue')
    for bar, total in zip(bars, totals):
        hours = int(total)
        minutes = int((total - hours) * 60)
        label = f"{hours}h {minutes}m"
        ax.text(
            bar.get_x() + bar.get_width() / 2,  
            bar.get_height() + 0.1,  
            label,
            ha='center',  
            va='bottom',
            fontsize=10,
            color='black'
        )
    ax.axhline(y=10, color='red', linestyle='--', linewidth=1.5, label='10-Hour Threshold')
    ax.set_title('Total Listening Time Per Month', fontsize=16)
    ax.set_xlabel('Month-Year', fontsize=12)
    ax.set_ylabel('Total Listening Time (hours)', fontsize=12)
    ax.set_xticklabels(months, rotation=45)
    ax.legend()
    fig.tight_layout()

    img = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)
    plt.close(fig)
    img.seek(0)
    return img

def get_learned_data(data):
    dates = [item['known'] for item in data]
    dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates]

    dates.sort()

    cumulative_frequency = list(range(1, len(dates) + 1))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(dates, cumulative_frequency, linestyle="-", color="blue", linewidth=2)

    ax.set_title("Cumulative Frequency of Dates")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Frequency")
    ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter("%m-%Y"))
    fig.autofmt_xdate() 

    ax.text(0.95, 0.05, f"Total Words Learned: {len(dates)}", transform=ax.transAxes,
         ha="right", va="bottom", fontsize=12, color="black", bbox=dict(facecolor="white", alpha=0.7))

    fig.tight_layout()

    img = BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(img)
    plt.close(fig) 
    img.seek(0)
    return img