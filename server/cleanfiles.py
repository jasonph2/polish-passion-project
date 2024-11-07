# cleans all files that are not in words

import os
import pymysql

conn = pymysql.connect(host='localhost',
    user='root',
    password='password',
    db='db',
    cursorclass=pymysql.cursors.DictCursor)
print("connected successfully")


path = "../audio/"

all_audio_files = os.listdir(path)

try:
    with conn.cursor() as cur:
        sql = "SELECT original_path, translated_path FROM db.words"
        cur.execute(sql)
        real_audio_files = cur.fetchall()
    conn.commit()
except Exception as e:
    print(e)

s = set()
for dic in real_audio_files:
    s.add(dic["original_path"])
    s.add(dic['translated_path'])
# print(s)

for file in all_audio_files:
    if os.path.isfile(os.path.join(path, file)):
        if file not in s:
            # os.remove(os.path.join(path, file))
            print(file)