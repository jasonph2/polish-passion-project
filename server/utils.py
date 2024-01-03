import os
import smtplib
from config import EMAIL_USERNAME, EMAIL_PASSWORD, AUDIO_FILE_PATH
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email import encoders
import random
from googletrans import Translator
from gtts import gTTS

def change_file_extension(file_path, new_extension):
    directory, filename_with_extension = os.path.split(file_path)
    filename, _ = os.path.splitext(filename_with_extension)

    new_file_path = os.path.join(directory, f"{filename}.{new_extension}")

    return new_file_path

def send_email(recipient_email, mp3_file_path):

    message = MIMEMultipart()
    message['From'] = EMAIL_USERNAME
    message['To'] = recipient_email
    message['Subject'] = 'Check out this MP3 file!'

    with open(mp3_file_path, 'rb') as mp3_file:
        mp3_attachment = MIMEAudio(mp3_file.read(), 'mp3')
        mp3_attachment.add_header('Content-Disposition', f'attachment; filename="{mp3_file_path}"')
        message.attach(mp3_attachment)

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

        server.sendmail(EMAIL_USERNAME, recipient_email, message.as_string())

    print("Email sent successfully!")

def translate_text(text, target_language='pl'):
    translator = Translator()
    
    translated_text = translator.translate(text, dest=target_language)

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
