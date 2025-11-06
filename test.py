import json
import os
import random

from main import DEFAULT_CATEGORIES
category_list = DEFAULT_CATEGORIES

def filter_words_by_category(word_list, category):
    """
    Filter words by category
    
    Args:
        word_list (list): List of word dictionaries
        category (str): Category to filter by
        
    Returns:
        list: Filtered list of words matching the category
    """
    return [word for word in word_list if word.get('category', '').lower() == category.lower()]
def get_category_statistics(word_list):
    """
    Get statistics for each category in the word list
    
    Args:
        word_list (list): List of word dictionaries
    Returns:
        dict: Dictionary with category names as keys and word counts as values
    """
    category_stats = {}
    for word in word_list:
        category = word.get('category', 'Unknown').lower()
        category_stats[category] = category_stats.get(category, 0) + 1
    return category_stats

def validate_word_entry(word, meaning, phrase="", category="general"):
    """
    Validate a word entry
    
    Args:
        word (str): Word to validate
        meaning (str): Meaning of the word
        phrase (str, optional): Example phrase using the word
        category (str, optional): Category of the word

    Returns:
        tuple: (is_valid (bool), error_message (str))
    """
    if not word or not meaning:
        return False, "Word and meaning are required."

    if category not in DEFAULT_CATEGORIES:
        return False, f"Invalid category. Choose from: {DEFAULT_CATEGORIES}"

    return True, """
        word (str): Word to validate
        meaning (str): Meaning of the word
        phrase (str, optional): Example phrase using the word
        category (str, optional): Category of the word
    """

def load_file(file_path):
    """Load JSON file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def generate_quiz_question(words, correct_word):
    """Generate a multiple choice quiz question"""
    options = [correct_word]
    other_words = [w for w in words if w['word'] != correct_word['word']]
    
    # Add 3 random wrong options
    wrong_options = random.sample(other_words, min(3, len(other_words)))
    for word in wrong_options:
        options.append(word)
    
    random.shuffle(options)
    return options

# Load the JSON file
def load_json_file(file_path):
    """Load JSON file and return its content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


# Access the "general" key
    general_data = data.get("general", [])
    print(general_data)
    # Print or process each entry
    for entry in general_data:
        word = entry.get("word")
        meaning = entry.get("meaning")
        phrase = entry.get("phrase")
        expressions = entry.get("expressions", [])
        video = entry.get("video")

        print(f"Word: {word}")
        print(f"Meaning: {meaning}")
        print(f"Phrase: {phrase}")
        print(f"Expressions: {', '.join(expressions)}")
        print(f"Video: {video}")
        print("-" * 40)
    

#