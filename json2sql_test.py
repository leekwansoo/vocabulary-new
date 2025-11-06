import json
import sqlite3

# Load JSON data
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('words.db')
cursor = conn.cursor()

# Function to create table and insert data
def create_table_and_insert(category, entries):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {category} (
            word TEXT,
            meaning TEXT,
            phrase TEXT,
            expressions TEXT,
            video TEXT
        )
    ''')

    for entry in entries:
        word = entry.get("word", "")
        meaning = entry.get("meaning", "")
        phrase = entry.get("phrase", "")
        expressions = json.dumps(entry.get("expressions", []), ensure_ascii=False)
        video = entry.get("video", "")

        cursor.execute(f'''
            INSERT INTO {category} (word, meaning, phrase, expressions, video)
            VALUES (?, ?, ?, ?, ?)
        ''', (word, meaning, phrase, expressions, video))

# Loop through each category in JSON
for category, entries in data.items():
    create_table_and_insert(category, entries)

# Save and close
conn.commit()
conn.close()

# Full functionality for json2sql.py
import json
import sqlite3

# Load JSON data
with open('data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('words.db')
cursor = conn.cursor()

# Function to create table and insert data
def create_table_and_insert(category, entries):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {category} (
            word TEXT,
            meaning TEXT,
            phrase TEXT,
            expressions TEXT,
            video TEXT
        )
    ''')

    for entry in entries:
        word = entry.get("word", "")
        meaning = entry.get("meaning", "")
        phrase = entry.get("phrase", "")
        expressions = json.dumps(entry.get("expressions", []), ensure_ascii=False)
        video = entry.get("video", "")

        cursor.execute(f'''
            INSERT INTO {category} (word, meaning, phrase, expressions, video)
            VALUES (?, ?, ?, ?, ?)
        ''', (word, meaning, phrase, expressions, video))

# Loop through each category in JSON
for category, entries in data.items():
    create_table_and_insert(category, entries)

# Save and close
conn.commit()
conn.close()