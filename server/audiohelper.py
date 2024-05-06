import subprocess

def convert_webm_to_mp3(input_file, output_file):
    ffmeg_path = r'C:\Users\Jason\Polish-Passion-Project\ffmpeg-2023-12-14-git-5256b2fbe6-essentials_build\bin\ffmpeg.exe'
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

    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful: {input_file} -> {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def duration_command(file_path):
    ffprobe_path = r'C:\Users\Jason\polish-passion-project\ffmpeg\bin\ffprobe.exe'
    command = [
        ffprobe_path,
        '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]

    try:
        result = subprocess.check_output(command, text=True)
        duration = float(result.strip())
        print(f"Duration of {file_path}: {duration} seconds")
        return duration
    except subprocess.CalledProcessError as e:
        print(f"Error during ffprobe: {e}")
        return None
    
def combine_audio_files(output_path, input_files):
    ffmpeg_path = r'C:\Users\Jason\polish-passion-project\ffmpeg\bin\ffprobe.exe'

    audio_codec = 'mp3'
    sample_rate = '44100'
    bit_rate = '192k'

    command = [
        ffmpeg_path,
        '-i', f'concat:{("|".join(input_files))}',
        '-c:a', audio_codec,
        '-b:a', bit_rate,
        '-ar', sample_rate,
        output_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Audio files combined successfully. Output saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg: {e}")

def create_silent_audio(output_path, duration):
    ffmpeg_path = r'C:\Users\Jason\polish-passion-project\ffmpeg\bin\ffprobe.exe'

    silence_command = [
        ffmpeg_path,
        '-f', 'lavfi',
        '-t', str(duration),
        '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        '-c:a', 'libmp3lame',
        '-y',
        output_path
    ]


    try:
        subprocess.run(silence_command, check=True)
        print(f"Silent audio generated successfully.")

    except subprocess.CalledProcessError as e:
        print(f"Error during silence generation: {e}")
