import streamlit as st 
from video_play import play_video
import json
import random
import os
from vocab_converter import VocabularyConverter
converter = VocabularyConverter()

st.title("Vocabulary Video Player")
# Upload JSON file
uploaded_file = st.sidebar.file_uploader("Upload JSON file", type=["json", "xlsx", "csv"])

# Initialize variables
url_data = []
media_list = []

if uploaded_file:
    file_name = uploaded_file.name
    st.sidebar.write(f"Uploaded file: {file_name}")
    file_type = file_name.split('.')[-1].lower()
    
    # Load data based on file type
    if file_type == 'json':
        data_json = uploaded_file.read()
        data_json = json.loads(data_json)
        url_data = data_json.get("general", [])
    else:
        if file_type == 'xlsx':
            # Save uploaded file temporarily
            temp_excel_path = f"temp_{file_name}"
            with open(temp_excel_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Convert Excel to JSON
            json_file_path = converter.excel_to_json(temp_excel_path)
            
            if json_file_path and os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data_json = json.load(f)
                    url_data = data_json.get("general", [])
                
                # Clean up temporary files
                os.remove(temp_excel_path)
                os.remove(json_file_path)
            else:
                st.error("Failed to convert Excel file")
                
        elif file_type == 'csv':
            # Save uploaded file temporarily
            temp_csv_path = f"temp_{file_name}"
            with open(temp_csv_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Convert CSV to JSON
            json_file_path = converter.csv_to_json(temp_csv_path)
            
            if json_file_path and os.path.exists(json_file_path):
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    data_json = json.load(f)
                    url_data = data_json.get("general", [])
                
                # Clean up temporary files
                os.remove(temp_csv_path)
                os.remove(json_file_path)
            else:
                st.error("Failed to convert CSV file")
    
    # Extract URL data from the loaded JSON
    # print(url_data)
    # url_data = data_json.get("general", [])
    #print(url_data)
    # if "media" is in the row of url_data, get the video link and play the video
    for row in url_data:
        # print(row)
        media = row.get("video", "") or row.get("media", "")
        # print(media)
        if media:
            #if str(media).startswith(("http://", "https://")):
            video_url = media
            row_word = row.get("word", "")
            #print(video_url, row_word)
            media_list.append(video_url)
    
    if media_list:
        st.sidebar.json(media_list)


url_path = st.text_input("Enter video URL or path:")
if url_path:
    play_video(url_path)

