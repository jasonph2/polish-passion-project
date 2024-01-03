from config import OPEN_AI_KEY
from openai import OpenAI 
import string
import random
import ast

def with_turbo(conn):
    try:
        with conn.cursor() as cursor:

            # get all the words the user is familiar with
            sql = "SELECT translated_word FROM db.words WHERE familiarity = 5"
            cursor.execute(sql)
            all = cursor.fetchall()

            translator = str.maketrans('', '', string.punctuation)
            individual_words = [word.translate(translator) for sentence in all for word in sentence['translated_word'].split()]
            individual_words = list(filter(lambda x: x.strip() != '', individual_words))
            random.shuffle(individual_words)
            individual_words = set(individual_words)
            print(individual_words)

            # make an OpenAI request
            client = OpenAI(api_key=OPEN_AI_KEY)
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You will be given a list of words or phrases in an arbitrary language. Use these words and only these words to formulate sentences, phrases, or questions in this language. Do not give the English translations. Only use the words given. Give your message content as a Python list"},
                    {"role": "user", "content": str(individual_words)}
                ]
            )
            # print(completion.choices[0].message.content)
            generated_content = completion.choices[0].message.content
            print(generated_content)
            # new_translated_list = generated_content.split("\n")
            # new_translated_list = list(filter(lambda x: x != '', new_translated_list))
            # print(new_translated_list)
            return ast.literal_eval(generated_content)
        
    except Exception as e:
        print({"message": f"Error: {str(e)}"})
