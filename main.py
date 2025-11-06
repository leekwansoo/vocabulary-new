"""
Main utility functions for vocabulary builder applications
Contains reusable functions that can be used across different apps
"""

import pyttsx3
from gtts import gTTS
import io
import tempfile
import os
import json


def load_word_pools(level=1):
    """
    Load word pools from a level-specific JSON file
    
    Args:
        level (int): Difficulty level (1, 2, or 3)
        
    Returns:
        dict: Dictionary containing word pools for each category
    """
    json_file = f"level{level}.json"
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {json_file} not found")
        # Fallback to word_pools.json if level file doesn't exist
        try:
            with open("word_pools.json", 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: No vocabulary files found")
            return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_file}")
        return {}


def create_audio_file(text, filename, is_phrase=False, speed="normal"):
    """
    Create audio file for text-to-speech with American English voice (cloud-compatible)
    
    Args:
        text (str): Text to convert to speech
        filename (str): Name for the temporary audio file
        is_phrase (bool): Whether the text is a phrase (affects speech rate)
        speed (str): Speed setting - "normal", "0.9", or "0.8"
        
    Returns:
        str or None: Path to the created audio file, or None if failed
    """
    # Try pyttsx3 first (for local development)
    try:
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        
        # Try to find an American English voice
        american_voice = None
        for voice in voices:
            # Look for American English voices (common identifiers)
            if voice.id and any(identifier in voice.id.lower() for identifier in ['david', 'mark', 'zira', 'hazel', 'us', 'american', 'en-us']):
                american_voice = voice.id
                break
            # Fallback: look for any English voice
            elif voice.id and 'en' in voice.id.lower():
                american_voice = voice.id
        
        # Set the American English voice if found
        if american_voice:
            engine.setProperty('voice', american_voice)
        
        # Base speech rates
        base_word_rate = 160
        base_phrase_rate = 140
        
        # Apply speed multiplier
        speed_multipliers = {
            "normal": 1.0,
            "0.9": 0.9,
            "0.8": 0.8
        }
        
        multiplier = speed_multipliers.get(speed, 1.0)
        
        # Adjust settings for phrases vs single words with speed options
        if is_phrase:
            final_rate = int(base_phrase_rate * multiplier)
        else:
            final_rate = int(base_word_rate * multiplier)
        
        engine.setProperty('rate', final_rate)
        engine.setProperty('volume', 0.9)
        
        # Create temporary file path
        temp_file = os.path.join(tempfile.gettempdir(), f"{filename}.wav")
        engine.save_to_file(text, temp_file)
        engine.runAndWait()
        return temp_file
        
    except Exception as e:
        print(f"pyttsx3 failed ({e}), trying gTTS for cloud compatibility...")
        
        # Fall back to gTTS (for cloud deployment)
        try:
            # Adjust speed for gTTS (it only has slow/normal)
            use_slow_speech = speed in ["0.9", "0.8"] or is_phrase
            
            # Create TTS object
            tts = gTTS(text=text, lang='en', slow=use_slow_speech)
            
            # Create temporary file path (MP3 format for gTTS)
            temp_file = os.path.join(tempfile.gettempdir(), f"{filename}.mp3")
            tts.save(temp_file)
            
            print(f"Created audio file using gTTS: {temp_file}")
            return temp_file
            
        except Exception as e2:
            print(f"All TTS methods failed: pyttsx3({e}), gTTS({e2})")
            return None


def load_vocabulary_from_file(file_path):
    """
    Load vocabulary words from a text file
    
    Args:
        file_path (str): Path to the vocabulary file
        
    Returns:
        list: List of dictionaries containing word data
    """
    word_list = []
    try:
        with open(file_path, "r", encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split(" | ")
                    if len(parts) >= 4:
                        word_details = {
                            "word": parts[0],
                            "meaning": parts[1],
                            "phrase": parts[2],
                            "category": parts[3]
                        }
                        word_list.append(word_details)
    except FileNotFoundError:
        print(f"Error: {file_path} not found")
    except Exception as e:
        print(f"Error loading vocabulary: {e}")
    
    return word_list


def save_word_pools_to_file(word_pools, file_path):
    """
    Save word pools to vocabulary file
    
    Args:
        word_pools (dict): Dictionary containing word pools
        file_path (str): Path to save the vocabulary file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(file_path, "w", encoding='utf-8') as f:
            for category, words in word_pools.items():
                for word_data in words:
                    f.write(f"{word_data['word']} | {word_data['meaning']} | {word_data['phrase']} | {category}\n")
        return True
    except Exception as e:
        print(f"Error saving word pools: {e}")
        return False


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
    Get statistics about words in each category
    
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
    Validate word entry data
    
    Args:
        word (str): The vocabulary word
        meaning (str): The word's meaning
        phrase (str): Example phrase (optional)
        category (str): Word category
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if not word or not word.strip():
        return False, "Word cannot be empty"
    
    if not meaning or not meaning.strip():
        return False, "Meaning cannot be empty"
    
    if len(word.strip()) > 100:
        return False, "Word is too long (max 100 characters)"
    
    if len(meaning.strip()) > 500:
        return False, "Meaning is too long (max 500 characters)"
    
    if phrase and len(phrase.strip()) > 500:
        return False, "Phrase is too long (max 500 characters)"
    
    return True, ""


def cleanup_audio_file(file_path):
    """
    Clean up temporary audio file
    
    Args:
        file_path (str): Path to the audio file to delete
    """
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        print(f"Warning: Could not delete temporary file {file_path}: {e}")


# Constants
DEFAULT_CATEGORIES = ["General", "Science", "Business", "Literature", "Travel", "History", "Geography", "Health"]
DEFAULT_VOCABULARY_FILE = "vocabulary.txt"
DEFAULT_WORD_POOLS_FILE = "word_pools.json"
DIFFICULTY_LEVELS = [1, 2, 3]
LEVEL_DESCRIPTIONS = {
    1: "Beginner - Basic vocabulary with common everyday words",
    2: "Intermediate - More challenging words for advancing learners", 
    3: "Advanced - Sophisticated vocabulary for expert learners"
}
SPEED_OPTIONS = ["normal", "0.9", "0.8"]
SPEED_LABELS = {
    "normal": "Normal (100%)",
    "0.9": "Slower (90%)",
    "0.8": "Slowest (80%)"
}


if __name__ == "__main__":
    # Test functions when running main.py directly
    print("Testing vocabulary builder functions...")
    
    # Test loading word pools for each level
    for level in DIFFICULTY_LEVELS:
        pools = load_word_pools(level)
        if pools:
            print(f"Level {level} - Loaded {len(pools)} categories")
            for category, words in pools.items():
                print(f"  {category.title()}: {len(words)} words")
        print()
    
    # Test audio creation
    print("\nTesting audio creation...")
    try:
        audio_file = create_audio_file("Hello world", "test", is_phrase=True)
        if audio_file:
            print(f"Audio file created: {audio_file}")
            cleanup_audio_file(audio_file)
            print("Audio file cleaned up")
        else:
            print("Audio creation failed")
    except Exception as e:
        print(f"Audio test skipped (dependency not installed): {e}")