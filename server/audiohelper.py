import subprocess
import os

def convert_webm_to_mp3(input_file, output_file):
    ffmeg_path = r'C:\Users\Jason\polish-passion-project\ffmpeg\bin\ffmpeg.exe'
    command = [
        ffmeg_path,
        '-i', input_file,
        '-vn',
        '-ar', '44100',
        '-ac', '2',
        '-ab', '192k',
        '-f', 'mp3',
        output_file
    ]

    devnull = open(os.devnull, 'w')

    try:
        subprocess.run(command, check=True, stdout=devnull, stderr=subprocess.STDOUT)
        print(f"Conversion successful: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
    finally:
        devnull.close()

def duration_command(file_path):
    ffprobe_path = r'C:\Users\Jason\polish-passion-project\ffmpeg\bin\ffprobe.exe'
    command = [
        ffprobe_path,
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]

    devnull = open(os.devnull, 'w')

    try:
        result = subprocess.check_output(command, text=True)
        duration = float(result.strip())
        # print(f"Duration of {file_path}: {duration} seconds")
        return duration
    except subprocess.CalledProcessError as e:
        print(f"Error during ffprobe: {e}")
        return None
    finally:
        devnull.close()
    
def combine_audio_files(output_path, input_files):
    ffmpeg_path = r'C:\Users\Jason\polish-passion-project\ffmpeg\bin\ffmpeg.exe'

    audio_codec = 'mp3'
    sample_rate = '44100'
    bit_rate = '192k'

    devnull = open(os.devnull, 'w')

    for file_path in input_files:
        if not os.path.isfile(file_path):
            print("WORD FOUND")
            print(file_path)

    command = [
        ffmpeg_path,
        '-i', f'concat:{("|".join(input_files))}',
        '-c:a', audio_codec,
        '-b:a', bit_rate,
        '-ar', sample_rate,
        output_path
    ]

    try:
        subprocess.run(command, check=True, stdout=devnull, stderr=subprocess.STDOUT)
        print(f"Audio files combined successfully. Output saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg: {e}")
    finally:
        devnull.close()

def create_silent_audio(output_path, duration):
    ffmpeg_path = r'C:\Users\Jason\polish-passion-project\ffmpeg\bin\ffmpeg.exe'

    silence_command = [
        ffmpeg_path,
        '-f', 'lavfi',
        '-t', str(duration),
        '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-c:a', 'libmp3lame',
        '-y',
        output_path
    ]

    devnull = open(os.devnull, 'w')

    try:
        subprocess.run(silence_command, check=True, stdout=devnull, stderr=subprocess.STDOUT)
        #print(f"Silent audio generated successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error during silence generation: {e}")
    finally:
        devnull.close()
