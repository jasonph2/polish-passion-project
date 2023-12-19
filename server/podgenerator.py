from config import AUDIO_FILE_PATH
from audiohelper import combine_audio_files

def generate_pod(conn, data):
    try:
        if (data["length"] == ""):
            raise RuntimeError("pod unable to be generated")
        audio_files = []
        with conn.cursor() as cur:
            sql = "SELECT * FROM db.words"
            cur.execute(sql)
            audio_files = cur.fetchall()
        paths = []
        for word in audio_files:
            paths.append(f"{AUDIO_FILE_PATH}{word['polish_path']}")
            paths.append(f"{AUDIO_FILE_PATH}{word['english_path']}")
        combine_audio_files(f"{AUDIO_FILE_PATH}{'testcombination.mp3'}", paths)
    except Exception as e:
        print(f"Error: {str(e)}")