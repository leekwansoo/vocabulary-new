"""
Main utility functions for vocabulary builder applications
Contains reusable functions that can be used across different apps
"""

import sqlite3
import io
import tempfile
import os
import json
from main import DEFAULT_CATEGORIES

db1 = "level1_words.db"
db2 = "level2_words.db"
db3 = "level3_words.db"

db_file = db1
conn1 = sqlite3.connect(db1)
cursor1 = conn1.cursor()
def load_word_pools_from_db(level=1):
    """
    Load word pools from a level-specific SQL database
    
    Args:
        level (int): Difficulty level (1, 2, or 3)
        
    Returns:
        dict: Dictionary containing word pools for each category
    """
    if level == 1:
        db_file = db1
    elif level == 2:
        db_file = db2
    elif level == 3:
        db_file = db3
    else:
        print("Error: Invalid difficulty level")
        return {}

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    word_pools = {}
    for category in DEFAULT_CATEGORIES:
        try:
            cursor.execute(f"SELECT word, meaning, phrase, expressions, media FROM {category}")
            rows = cursor.fetchall()
            word_pools[category] = []
            for row in rows:
                word_entry = {
                    "word": row[0],
                    "meaning": row[1],
                    "phrase": row[2],
                    "expressions": json.loads(row[3]) if row[3] else [],
                    "media": row[4]
                }
                word_pools[category].append(word_entry)
        except sqlite3.OperationalError:
            print(f"Warning: Table '{category}' does not exist in {db_file}")
            continue

    conn.close()
    return word_pools

word_pools = load_word_pools_from_db(level=1)
print(word_pools)