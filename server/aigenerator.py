from config import OPEN_AI_KEY
from openai import OpenAI 

def with_turbo(conn):
    try:
        with conn.cursor() as cursor:
            sql = "SELECT translated_word FROM db.words WHERE familiarity = 5"
            cursor.execute(sql)
            all = cursor.fetchall()
            words = []
            for dict in all:
                words.append(dict["translated_word"])
            print(words)
    except Exception as e:
        print(str(e))
        # return jsonify({"message": f"Error: {str(e)}"})
    return "this technically counts as a phrase"