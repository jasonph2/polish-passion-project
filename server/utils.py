import os
import smtplib
from config import EMAIL_USERNAME, EMAIL_PASSWORD
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.audio import MIMEAudio
from email import encoders

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

