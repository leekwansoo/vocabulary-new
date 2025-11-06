import streamlit as st 
from utils.main import DEFAULT_CATEGORIES
from utils.main import DIFFICULTY_LEVELS
import json
import os

def add_word_to_json(word_entry):
    """
    Add a new word entry to the vocabulary storage.
    
    Args:
        word_entry (dict): Dictionary with word details
    """
    category = word_entry.get("category", "general")
    difficulty_level = word_entry.get("difficulty", 1)
    word = word_entry.get("word", "")
    meaning = word_entry.get("meaning", "")
    expressions = word_entry.get("expressions", [])
    phrase = word_entry.get("phrase", "")
    media = word_entry.get("media", "")
    new_word_entry = {
        "word": word,
        "meaning": meaning,
        "expressions": expressions,
        "phrase": phrase,
        "media": media,
    }
    if difficulty_level == 1:
        json_file = "level1.json"
    elif difficulty_level == 2:
        json_file = "level2.json"
    elif difficulty_level == 3:
        json_file = "level3.json"
    else:
        st.error("Invalid difficulty level.")
        return

    with open(json_file, 'r+', encoding='utf-8') as f:
        data = json.load(f)
        category = word_entry.get("category", "general")
        if category not in data:
            data[category] = []

        data[category].append(new_word_entry)
        
        # Write the updated data back to the JSON file
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.truncate()

st.title("➕ Add New Word")

st.sidebar.markdown("📝 **Add New Word:**")
st.sidebar.subheader("Enter the details of the new word below:")
category = st.sidebar.radio("Word Category:", DEFAULT_CATEGORIES, key="word_category_radio", horizontal =True).lower()
difficulty_level = st.sidebar.radio("Difficulty Level:", DIFFICULTY_LEVELS, key="word_difficulty_select", horizontal=True)
# Upload File for media (optional)
media_file = st.sidebar.file_uploader("Upload Media File (optional):", type=["mp4", "jpg", "wav"])
if media_file:
    media_path = os.path.join("media", media_file.name)
    with open(media_path, "wb") as f:
        f.write(media_file.getbuffer())
    st.sidebar.success(f"Uploaded file saved to {media_path}")
media = f"media/{media_file.name}" if media_file else ""
print(media)

word = st.text_input("Word")
meaning = st.text_input("Meaning")
expressions = st.text_area("Expressions (one per line)", height=100).split("\n")
phrase = st.text_input("Example Phrase (optional)")

if st.button("➕ Add Word", key="add_word_button"):
    # Add the new word to the vocabulary
    word_entry = {
        "word": word,
        "meaning": meaning,
        "expressions": [expr.strip() for expr in expressions if expr.strip()],
        "phrase": phrase,
        "media": media,
        "category": category,
        "difficulty": difficulty_level
    }
    add_word_to_json(word_entry)
    st.success(f"✅ Word '{word}' added to category '{category}' at level {difficulty_level}_!.json")