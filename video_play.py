# ...existing code...
import os
import sys
import subprocess
import webbrowser
import json
from pathlib import Path
import streamlit as st 
from gtts import gTTS
import pyttsx3
import random 
random_num = random.randint(1, 100)
from utils.main import DIFFICULTY_LEVELS
# ...existing code...

# Try to use user's videoplay helper if present
try:
    from videoplay import play_video as external_play_video
except Exception:
    external_play_video = None
def get_difficulty(word):
    """Get difficulty level for a word (robust to unexpected DIFFICULTY_LEVELS types)."""
    try:
        # If word is not a string, return default
        if not isinstance(word, str):
            return "⭐⭐"
        key = word.lower().strip()
        # If DIFFICULTY_LEVELS is a dict-like object
        if hasattr(DIFFICULTY_LEVELS, "get"):
            return DIFFICULTY_LEVELS.get(key, "⭐⭐")
        # If DIFFICULTY_LEVELS is a list of dicts try to find an entry
        if isinstance(DIFFICULTY_LEVELS, (list, tuple)):
            for item in DIFFICULTY_LEVELS:
                if isinstance(item, dict):
                    if item.get("word", "").lower() == key:
                        return item.get("difficulty", "⭐⭐")
        # Unknown structure -> default
        return "⭐⭐"
    except Exception:
        return "⭐⭐"

def display_photo(path):
    """Display local image file or image from URL in Streamlit."""
    try:
        # If it's a local path
        if not str(path).startswith(("http://", "https://")):
            p = Path(path)
            if not p.is_absolute():
                p = (Path(__file__).parent / p).resolve()
                print(f"Resolved image path: {p}")
            if p.exists():
                st.image(str(p))
            else:
                st.error(f"Image file not found: {p}")
        else:
            # It's a URL
            st.image(path)
    except Exception as e:
        st.error(f"Failed to display image: {e}")
        
def play_video(path_or_url):
    """Open local file in external player or open a URL in the browser.
    Prefers the external helper if provided (videoplay.play_video)."""
    try:
        # If it's a local path
        if not str(path_or_url).startswith(("http://", "https://")):
            p = Path(path_or_url)
            if not p.is_absolute():
                p = (Path(__file__).parent / p).resolve()
            if p.exists():
                if external_play_video:
                    try:
                        external_play_video(str(p))
                        return
                    except Exception:
                        pass
                # Fallback to platform open
                if sys.platform.startswith("win"):
                    os.startfile(str(p))
                elif sys.platform.startswith("darwin"):
                    subprocess.Popen(["open", str(p)])
                else:
                    subprocess.Popen(["xdg-open", str(p)])
                return
            else:
                # Not found as a file; treat as URL below
                path_or_url = str(path_or_url)
        # It's a URL or local file was not found — open in browser
        webbrowser.open_new_tab(path_or_url)
    except Exception as e:
        st.error(f"Failed to open video: {e}")

def _drive_direct_link(url: str) -> str | None:
    """Try to convert common Google Drive share URLs to a direct-download link Streamlit can play."""
    import re
    # /d/FILEID/...
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    # id=FILEID
    m = re.search(r"id=([a-zA-Z0-9_-]+)", url)
    if m:
        return f"https://drive.google.com/uc?export=download&id={m.group(1)}"
    return None

def _drive_embed_link(url: str) -> str | None:
    """Convert Google Drive share URLs to embeddable iframe link."""
    import re
    # /d/FILEID/...
    m = re.search(r"/d/([a-zA-Z0-9_-]+)", url)
    if m:
        return f"https://drive.google.com/file/d/{m.group(1)}/preview"
    # id=FILEID
    m = re.search(r"id=([a-zA-Z0-9_-]+)", url)
    if m:
        return f"https://drive.google.com/file/d/{m.group(1)}/preview"
    return None

def _detect_media_type(path_or_url: str) -> str:
    """Detect if the media is an image, video, or unknown type."""
    # Common extensions
    image_exts = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff', '.tif'}
    video_exts = {'.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.mpg', '.mpeg'}
    audio_exts = {'.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'}
    
    # Get extension from path/URL
    ext = Path(path_or_url).suffix.lower()
    
    # Check query parameters for URLs (e.g., ?format=mp4)
    if '?' in str(path_or_url):
        import re
        format_match = re.search(r'[?&]format=([^&]+)', str(path_or_url))
        if format_match:
            ext = f".{format_match.group(1).lower()}"
    
    if ext in image_exts:
        return 'image'
    elif ext in video_exts:
        return 'video'
    elif ext in audio_exts:
        return 'audio'
    else:
        # Default to video for unknown types with URLs
        if str(path_or_url).startswith(('http://', 'https://')):
            return 'video'  # Assume video for online content
        return 'unknown'

def create_word_widget(entry: dict, editable_expressions=True, current_level=None):
    """Render the word card (meaning, expressions, phrase) and show video if provided.
    Handles local files, direct URLs, and attempts to convert Google Drive links.
    Also supplies an 'Open in external player' button that calls play_video()."""
    st.markdown("---")
    difficulty = get_difficulty(entry['word'])
    st.markdown(f"### 📚 {entry['word']} {difficulty}")
    
    # Larger font for Meaning with balanced styling
    st.markdown(f"<div class='balanced-meaning'><strong>Meaning:</strong> {entry.get('meaning','')}</div>", unsafe_allow_html=True)
    
    # Handle expressions display - either editable or read-only
    if editable_expressions and current_level != "learned":
        # Get current expressions as default text - limit to 5 and format properly
        current_expressions = entry.get('expressions', [])[:5]  # Limit to 5 expressions
        # Smaller font for expressions label with compact styling and count
        current_count = len(current_expressions) if current_expressions else 0
        st.markdown(f"<div class='balanced-expressions'><strong>✏️ Expressions ({current_count}/5):</strong></div>", unsafe_allow_html=True)
        # Format with proper comma separation and line breaks for better readability
        if current_expressions:
            default_text = ",\n".join(current_expressions)
        else:
            default_text = ""
        
        # Calculate height based on number of expressions (auto-adjust)
        num_expressions = len(current_expressions) if current_expressions else 1
        # Base height + additional height per expression (minimum 2 lines, maximum 6 lines for 5 expressions)
        calculated_height = max(140, min(140, 40 + (num_expressions * 20)))
        
        # Custom CSS for auto-adjusting text area
        st.markdown(f"""
        <style>
        div[data-testid="stTextArea"] textarea {{
            font-size: 1.4em !important;
            line-height: 1.4 !important;
            padding: 8px 12px !important;
            min-height: 60px !important;
            height: {calculated_height}px !important;
            resize: vertical !important;
        }}
        </style>
        """, unsafe_allow_html=True)
        
        # Text area for expressions input with auto-calculated height
        random_num = random.randint(1, 100)
        expressions_input = st.text_area(
            "Enter expressions separated by commas (max 5):", 
            value=default_text,
            key=f"expr_widget_{entry['word']}_{random_num}",
            height=calculated_height,
            label_visibility="collapsed",
            help="Enter up to 5 expressions, separated by commas. Use line breaks for better readability."
        )
        
        # Auto-save functionality with session state
        if f"prev_expr_{entry['word']}" not in st.session_state:
            st.session_state[f"prev_expr_{entry['word']}"] = default_text
        
        # Parse expressions for processing (but don't auto-save yet)
        if expressions_input.strip():
            # Handle both comma and line break separation
            # First split by line breaks, then by commas
            all_expressions = []
            for line in expressions_input.split('\n'):
                line_expressions = [expr.strip() for expr in line.split(',') if expr.strip()]
                all_expressions.extend(line_expressions)
            
            # Limit to 5 expressions and clean up
            new_expressions = [expr for expr in all_expressions if expr][:5]
            
            # Show warning if more than 5 expressions were entered
            if len(all_expressions) > 5:
                st.warning(f"⚠️ Only first 5 expressions will be saved (entered {len(all_expressions)})", icon="📝")
        else:
            new_expressions = []
        
        # Debug info (you can remove this later)
        with st.expander("🔍 Debug Info", expanded=False):
            st.write(f"**Current expressions:** {entry.get('expressions', [])}")
            st.write(f"**Input text:** '{expressions_input}'")
            st.write(f"**Parsed new expressions:** {new_expressions}")
            st.write(f"**Text area has content:** {bool(expressions_input.strip())}")
        
        # Save Expressions Button - always visible for manual saving
        st.markdown("<div style='margin: 8px 0;'></div>", unsafe_allow_html=True)
        
        # Check if expressions are different from saved ones (for styling)
        current_expressions_text = ",\n".join(entry.get('expressions', []))
        expressions_changed = expressions_input.strip() != current_expressions_text
        
        # Button styling based on whether there are changes
        button_type = "primary" if expressions_changed else "secondary"
        button_text = f"💾 Save Expressions ({len(new_expressions)}/5)" + (" *" if expressions_changed else "")
        random_num = random.randint(1, 100)
        if st.button(button_text, key=f"save_expr_{entry['word']}_{random_num}", type=button_type):
                # Update the entry
                entry['expressions'] = new_expressions
                
                # Save to JSON file
                import json
                import os
                level_files = {
                    1: "level1.json",
                    2: "level2.json", 
                    3: "level3.json"
                }
                
                if current_level and current_level in level_files:
                    filename = level_files[current_level]
                    if os.path.exists(filename):
                        try:
                            with open(filename, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                            
                            # Find and update the word in the appropriate category
                            category = entry.get('category', '').lower()
                            if category in data:
                                for i, word_entry in enumerate(data[category]):
                                    if word_entry['word'] == entry['word']:
                                        data[category][i]['expressions'] = new_expressions
                                        break
                            
                            # Save back to file
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2)
                            
                            # Show success message
                            st.success(f"✅ {len(new_expressions)} expressions saved successfully!", icon="💾")
                            st.rerun()  # Refresh to show updated data
                        except Exception as e:
                            st.error(f"❌ Error saving expressions: {e}")
    else:
        # Read-only expressions display with balanced styling (max 5)
        expressions = entry.get('expressions', [])[:5]  # Limit to 5 expressions for display
        if expressions:
            st.markdown("<div class='balanced-expressions'><strong>Expressions:</strong></div>", unsafe_allow_html=True)
            for expr in expressions:
                st.markdown(f"<div class='balanced-expressions'>• {expr}</div>", unsafe_allow_html=True)
    
    # Add small spacing between expressions and phrase
    st.markdown("<div style='margin: 4px 0;'></div>", unsafe_allow_html=True)
    
    # Larger font for Phrase with balanced styling
    st.markdown(f"<div class='balanced-phrase'><strong>Phrase:</strong> {entry.get('phrase','')}</div>", unsafe_allow_html=True)
    
    media_path = entry.get('media')
    if media_path:
        # Detect media type automatically
        media_type = _detect_media_type(media_path)
        
        st.markdown("**Media:**")
        proj_root = Path(__file__).parent
        is_url = str(media_path).startswith(("http://", "https://"))
        
        # Handle based on media type
        if media_type == 'image':
            # Image handling
            if not is_url:
                # Local image
                img_path = Path(media_path)
                if not img_path.is_absolute():
                    img_path = (proj_root / img_path).resolve()
                if img_path.exists():
                    st.image(str(img_path), use_container_width=True)
                else:
                    st.warning(f"Image file not found: {img_path}")
            else:
                # URL image
                try:
                    st.image(media_path, use_container_width=True)
                except Exception as e:
                    st.error(f"Cannot load image: {e}")
                    st.markdown(f"[🖼️ Open image link]({media_path})")
        
        elif media_type == 'video':
            # Video handling
            if not is_url:
                # Local video file
                vp = Path(media_path)
                if not vp.is_absolute():
                    vp = (proj_root / vp).resolve()
                if vp.exists():
                    try:
                        st.video(str(vp))
                    except Exception:
                        try:
                            with open(vp, "rb") as vf:
                                st.video(vf.read())
                        except Exception as e:
                            st.error(f"Cannot play local video: {e}")
                    # Provide external open button
                    random_num = random.randint(1, 100)
                    if st.button("Open in external player", key=f"open_ext_{entry['word']}_{random_num}"):
                        play_video(str(vp))
                else:
                    st.warning(f"Video file not found: {vp}")
                    st.write(str(vp))
            else:
                # URL video handling
                if "drive.google.com" in str(media_path):
                    # Google Drive video
                    embed_link = _drive_embed_link(media_path)
                    direct = _drive_direct_link(media_path)
                    
                    if embed_link:
                        st.info("🎥 Google Drive Video")
                        try:
                            st.markdown(
                                f'<iframe src="{embed_link}" width="100%" height="400" frameborder="0" allowfullscreen></iframe>',
                                unsafe_allow_html=True
                            )
                        except Exception as e:
                            st.warning(f"⚠️ Cannot embed video: {str(e)[:50]}")
                        
                        st.markdown(f"[📺 Open in browser]({media_path})")
                        random_num = random.randint(1, 100)
                        if st.button("🎬 Open in external player", key=f"open_ext_{entry['word']}_{random_num}"):
                            if direct:
                                play_video(direct)
                            else:
                                play_video(media_path)
                        else:
                            # Not a single-file share (maybe folder) — provide link + external open
                            st.markdown(f"[Open Google Drive link]({media_path})")
                            random_num = random.randint(1, 100)
                            if st.button("Open in external player", key=f"open_ext_{entry['word']}_{random_num}"):
                                play_video(media_path)
                    else:
                        # Generic URL video: try to let Streamlit play it
                        random_num = random.randint(1, 100)
                        try:
                            st.video(media_path)
                        except Exception as e:
                            st.warning(f"⚠️ Cannot embed video from URL")
                            st.markdown(f"[📺 Open video link]({media_path})")
                            if st.button("🎬 Open in external player", key=f"open_ext_{entry['word']}_{random_num}"):
                                play_video(media_path)
        
        elif media_type == 'audio':
            # Audio handling
            if not is_url:
                # Local audio file
                audio_path = Path(media_path)
                if not audio_path.is_absolute():
                    audio_path = (proj_root / audio_path).resolve()
                if audio_path.exists():
                    st.audio(str(audio_path))
                else:
                    st.warning(f"Audio file not found: {audio_path}")
            else:
                # URL audio
                try:
                    st.audio(media_path)
                except Exception as e:
                    st.error(f"Cannot load audio: {e}")
                    st.markdown(f"[� Open audio link]({media_path})")
        
        else:
            # Unknown media type - try to determine by content
            st.info(f"📎 Media file detected (type: {media_type})")
            if not is_url:
                # Local file with unknown type
                unknown_path = Path(media_path)
                if not unknown_path.is_absolute():
                    unknown_path = (proj_root / unknown_path).resolve()
                if unknown_path.exists():
                    st.markdown(f"**File:** `{unknown_path.name}`")
                    # Try as image first, then video
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("📷 Try as Image", key=f"img_{entry['word']}"):
                            try:
                                st.image(str(unknown_path), use_container_width=True)
                            except Exception as e:
                                st.error(f"Cannot display as image: {e}")
                    with col2:
                        if st.button("🎬 Try as Video", key=f"vid_{entry['word']}"):
                            try:
                                st.video(str(unknown_path))
                            except Exception as e:
                                st.error(f"Cannot play as video: {e}")
                else:
                    st.warning(f"File not found: {unknown_path}")
            else:
                # URL with unknown type
                st.markdown(f"[🔗 Open media link]({media_path})")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📷 Try as Image", key=f"img_{entry['word']}"):
                        try:
                            st.image(media_path, use_container_width=True)
                        except Exception as e:
                            st.error(f"Cannot display as image: {e}")
                with col2:
                    if st.button("🎬 Try as Video", key=f"vid_{entry['word']}"):
                        try:
                            st.video(media_path)
                        except Exception as e:
                            st.error(f"Cannot play as video: {e}")
        
        st.markdown("---")

# ...existing code...
# Ensure the left column uses create_word_widget(entry) (if not already)
