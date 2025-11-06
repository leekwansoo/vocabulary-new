import sqlite3
import json

DB_NAME = 'words.db'

def connect():
    return sqlite3.connect(DB_NAME)

def create_table(category):
    with connect() as conn:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {category} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT,
                meaning TEXT,
                phrase TEXT,
                expressions TEXT,
                video TEXT
            )
        ''')

def add_word(category):
    create_table(category)
    word = input("Enter word: ")
    meaning = input("Enter meaning: ")
    phrase = input("Enter phrase: ")
    expressions = input("Enter expressions (comma-separated): ").split(',')
    video = input("Enter video path (optional): ")

    with connect() as conn:
        conn.execute(f'''
            INSERT INTO {category} (word, meaning, phrase, expressions, video)
            VALUES (?, ?, ?, ?, ?)
        ''', (word, meaning, phrase, json.dumps(expressions, ensure_ascii=False), video))
    print(f"✅ Added '{word}' to category '{category}'.")

def view_words(category):
    with connect() as conn:
        cursor = conn.execute(f'SELECT * FROM {category}')
        rows = cursor.fetchall()
        for row in rows:
            print(f"\n🆔 ID: {row[0]}")
            print(f"📘 Word: {row[1]}")
            print(f"📖 Meaning: {row[2]}")
            print(f"💬 Phrase: {row[3]}")
            print(f"🗣️ Expressions: {json.loads(row[4])}")
            print(f"🎥 Video: {row[5]}")

def update_word(category):
    word_id = input("Enter ID of word to update: ")
    word = input("New word: ")
    meaning = input("New meaning: ")
    phrase = input("New phrase: ")
    expressions = input("New expressions (comma-separated): ").split(',')
    video = input("New video path (optional): ")

    with connect() as conn:
        conn.execute(f'''
            UPDATE {category}
            SET word = ?, meaning = ?, phrase = ?, expressions = ?, video = ?
            WHERE id = ?
        ''', (word, meaning, phrase, json.dumps(expressions, ensure_ascii=False), video, word_id))
    print(f"✏️ Updated word ID {word_id} in category '{category}'.")

def delete_word(category):
    word_id = input("Enter ID of word to delete: ")
    with connect() as conn:
        conn.execute(f'DELETE FROM {category} WHERE id = ?', (word_id,))
    print(f"🗑️ Deleted word ID {word_id} from category '{category}'.")

def main():
    print("📚 Word Manager CLI")
    while True:
        print("\nChoose an option:")
        print("1. Add word")
        print("2. View words")
        print("3. Update word")
        print("4. Delete word")
        print("5. Exit")

        choice = input("Enter choice (1-5): ")
        if choice == '5':
            print("👋 Goodbye!")
            break

        category = input("Enter category (e.g., general, science, business): ")

        if choice == '1':
            add_word(category)
        elif choice == '2':
            view_words(category)
        elif choice == '3':
            update_word(category)
        elif choice == '4':
            delete_word(category)
        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()