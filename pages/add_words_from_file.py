import streamlit as st
import os
import json
import random
import csv
from pathlib import Path

from utils.main import DEFAULT_CATEGORIES
from utils.main import DIFFICULTY_LEVELS
from utils.json_manager import load_json, save_json, add_words_to_json

st.title("➕ Add New Word from file")

st.sidebar.markdown("📝 **Select File to Add Words from:**")
uploaded_file = st.sidebar.file_uploader("Upload a file", type=["xlsx", "csv", "json"])
if uploaded_file:
    file_name = uploaded_file.name
    st.sidebar.write(f"Uploaded file: {file_name}")
    file_type = file_name.split('.')[-1].lower()
    
    # Save uploaded file temporarily
    temp_file_path = f"temp_{file_name}"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        # Print uploaded file content for debugging: show text for json/csv/txt,
        # otherwise show a binary preview and size.
        try:
            if file_type in ("json", "csv", "txt"):
                content = uploaded_file.getvalue().decode("utf-8", errors="replace")
                print(content)
            else:
                buf = uploaded_file.getbuffer()
                print(f"Uploaded binary file: {len(buf)} bytes. Preview (first 200 bytes): {buf.tobytes()[:200]!r}")
        except Exception as e:
            print("Error printing uploaded file content:", e)
    
    # Load data based on file type
    if file_type == 'json':
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            data_json = json.load(f)
            print(data_json.keys())
    else:
        from vocab_converter import VocabularyConverter
        converter = VocabularyConverter()
        
        if file_type == 'xlsx':
            json_file_path = converter.excel_to_json(temp_file_path)
            
        elif file_type == 'csv':
            json_file_path = converter.csv_to_json(temp_file_path)
            # Debugging: log returned path and file existence
            try:
                print("converter.csv_to_json returned:", json_file_path)
                if json_file_path:
                    abs_json_path = os.path.abspath(json_file_path)
                    print("abs path:", abs_json_path)
                    print("exists:", os.path.exists(abs_json_path))
                    if os.path.exists(abs_json_path):
                        with open(abs_json_path, 'r', encoding='utf-8') as jf:
                            preview = jf.read(1000)
                            print("converted JSON preview:", preview)
                else:
                    print("csv_to_json returned None")
            except Exception as _e:
                print("Error while inspecting converted JSON:", _e)

            # Fallback: if converter didn't produce a JSON file, try parsing CSV here
            if not json_file_path or not os.path.exists(json_file_path):
                try:
                    fallback_json = f"{os.path.splitext(temp_file_path)[0]}_from_csv.json"
                    data_fallback = {}
                    with open(temp_file_path, 'r', encoding='utf-8') as cf:
                        rdr = csv.DictReader(cf)
                        for row in rdr:
                            category = row.get('Category', 'general') or 'general'
                            category = category.lower()
                            expressions_str = row.get('Expressions', '') or ''
                            expressions = [expr.strip() for expr in expressions_str.split(';') if expr.strip()]
                            word_entry = {
                                'word': row.get('Word', '') or '',
                                'meaning': row.get('Meaning', '') or '',
                                'phrase': row.get('Phrase', '') or '',
                                'expressions': expressions,
                                'video': row.get('Media', '') or ''
                            }
                            data_fallback.setdefault(category, []).append(word_entry)

                    with open(fallback_json, 'w', encoding='utf-8') as jf:
                        json.dump(data_fallback, jf, ensure_ascii=False, indent=2)

                    json_file_path = fallback_json
                    print("Fallback CSV→JSON wrote:", json_file_path)
                except Exception as e:
                    print("Fallback CSV→JSON failed:", e)
            
        else:
            st.error("Unsupported file type.")
            words_data = []
            json_file_path = None
        
        if json_file_path and os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data_json = json.load(f)
            # Clean up converted temporary file
            print(json_file_path)
            os.remove(json_file_path)
        else:
            st.error("Failed to convert file")
            data_json = None
    
    # Clean up temporary upload file
    os.remove(temp_file_path)

    # If we have loaded JSON data, import words preserving categories
    if data_json:
        try:
            if isinstance(data_json, dict):
                total = sum(len(v) for v in data_json.values())
                for category, words in data_json.items():
                    for word_entry in words:
                        add_words_to_json(word_entry, json_file="level1.json", category=category)
                st.success(f"Successfully added {total} words across {len(data_json)} categories to the vocabulary storage.")
            elif isinstance(data_json, list):
                for word_entry in data_json:
                    add_words_to_json(word_entry, json_file="level1.json", category="general")
                st.success(f"Successfully added {len(data_json)} words to the vocabulary storage.")
            else:
                st.warning("Uploaded JSON has unexpected format.")
        except Exception as e:
            print("Error adding words to storage:", e)
            st.error("Failed to add words to vocabulary storage.")
    else:
        st.warning("No words found in the uploaded file.")