import streamlit as st 
import random
import os
import json

DEFAULT_CATEGORIES = ["general", "science", "business", "literature", "travel", "history", "geography", "health"]
DEFAULT_VOCABULARY_FILE = "vocabulary.txt"
DIFFICULTY_LEVELS = {
    # General - Easy to Hard
    "efficient": "⭐",
    "authentic": "⭐",
    "versatile": "⭐⭐",
    "pragmatic": "⭐⭐",
    "resilient": "⭐⭐",
    "innovative": "⭐⭐",
    "profound": "⭐⭐",
    "coherent": "⭐⭐",
    "diligent": "⭐⭐",
    "benevolent": "⭐⭐⭐",
    "eloquent": "⭐⭐⭐",
    "meticulous": "⭐⭐⭐",
    "ubiquitous": "⭐⭐⭐",
    "ephemeral": "⭐⭐⭐",
    "ambiguous": "⭐⭐⭐",
    "tenacious": "⭐⭐⭐",
    "subtle": "⭐⭐⭐",
    "intricate": "⭐⭐⭐",
    "contemplative": "⭐⭐⭐",
    "serendipity": "⭐⭐⭐",
    
    # Science
    "gravity": "⭐",
    "molecule": "⭐",
    "ecosystem": "⭐⭐",
    "evolution": "⭐⭐",
    "catalyst": "⭐⭐",
    "enzyme": "⭐⭐",
    "neuron": "⭐⭐",
    "genome": "⭐⭐⭐",
    "hypothesis": "⭐⭐⭐",
    "photosynthesis": "⭐⭐⭐",
    "chromosome": "⭐⭐⭐",
    "quantum": "⭐⭐⭐",
    "biodiversity": "⭐⭐⭐",
    "metabolism": "⭐⭐⭐",
    "osmosis": "⭐⭐⭐",
    "mitosis": "⭐⭐⭐",
    "thermodynamics": "⭐⭐⭐",
    "isotope": "⭐⭐⭐",
    "radiation": "⭐⭐⭐",
    "symbiosis": "⭐⭐⭐",
}

def load_vocabulary_with_expressions(level):
    """Load vocabulary from JSON files with expressions included"""    
    # Map level to filename
    level_files = {
        1: "data/level1.json",
        2: "data/level2.json", 
        3: "data/level3.json"
    }
    filename = level_files.get(int(level))
    #filename = "data/level" + str(level) + ".json"
    if not filename or not os.path.exists(filename):
        return []
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Flatten all categories into a single list
        all_words = []
        for category, words in data.items():
            for word_entry in words:
                # Add category to each word entry
                word_entry['category'] = category
                all_words.append(word_entry)
        
        return all_words
    except (json.JSONDecodeError, FileNotFoundError):
        return []
    
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

def get_difficulty(word):
    """Get difficulty level for a word"""
    return DIFFICULTY_LEVELS.get(word.lower(), "⭐⭐")
    
st.subheader("🎯 Interactive Quiz Mode")
    
# Initialize session state for quiz
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0
if 'current_question' not in st.session_state:
    st.session_state.current_question = None

st.sidebar.markdown("### Quiz Settings")
# Category selection
selected_category = st.sidebar.radio("Select Category", ["All"] + DEFAULT_CATEGORIES, horizontal=True)
current_level = st.sidebar.radio("Select Level", ["1", "2", "3"], horizontal=True)
# Load words for quiz using sidebar selections with expressions

if st.button("🔄 Load Words for Quiz"):
    st.session_state.quiz_score = 0
    st.session_state.quiz_total = 0
    st.session_state.current_question = None
    all_words = load_vocabulary_with_expressions(current_level)
    print(current_level, all_words)
    quiz_words = filter_words_by_category(all_words, selected_category)
    print(quiz_words)
    st.session_state.quiz_words = quiz_words
else:
    quiz_words = st.session_state.get('quiz_words', [])

if quiz_words:
    # Quiz type selection
    quiz_type = st.sidebar.radio("Quiz Type", ["Meaning → Word", "Word → Meaning"])
    
    # Display current quiz settings
    st.info(f"📚 **Category:** {selected_category} | 🎯 **Quiz Type:** {quiz_type}")

    if quiz_words and len(quiz_words) >= 4:
        # Score display
        if st.session_state.quiz_total > 0:
            accuracy = (st.session_state.quiz_score / st.session_state.quiz_total) * 100
            st.metric("Quiz Accuracy", f"{accuracy:.1f}%", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}")
        
        # Generate new question button
        if st.button("🎲 New Question") or st.session_state.current_question is None:
            correct_word = random.choice(quiz_words)
            options = generate_quiz_question(quiz_words, correct_word)
            st.session_state.current_question = {
                'correct': correct_word,
                'options': options,
                'answered': False
            }
            
        # Display current question
        if st.session_state.current_question:
            question = st.session_state.current_question
            correct_word = question['correct']
            
            if quiz_type == "Meaning → Word":
                st.markdown(f'<h3 style="font-size: 2.4em;">What word has this meaning?</h3>', unsafe_allow_html=True)
                st.markdown(f'<div style="background-color: #d1ecf1; padding: 15px; border-radius: 10px; border-left: 5px solid #0c5460; font-size: 1.95em;"><strong>Meaning:</strong> {correct_word["meaning"]}</div>', unsafe_allow_html=True)
                
                # Multiple choice options
                option_labels = [opt['word'] for opt in question['options']]
            else:  # Word → Meaning
                st.markdown(f'<h3 style="font-size: 2.4em;">What is the meaning of: <strong>{correct_word["word"]}</strong></h3>', unsafe_allow_html=True)
                
                # Multiple choice options
                option_labels = [opt['meaning'] for opt in question['options']]
            
            # Radio button for answer selection
            if not question['answered']:
                st.markdown('<p style="font-size: 1.95em; font-weight: bold; margin-top: 20px;">Choose your answer:</p>', unsafe_allow_html=True)
                selected_answer = st.radio(
                    "Answer Selection",
                    option_labels,
                    key="quiz_answer",
                    label_visibility="hidden"
                )
                
                if st.button("✅ Submit Answer"):
                    # Check if answer is correct
                    if quiz_type == "Meaning → Word":
                        is_correct = selected_answer == correct_word['word']
                    else:
                        is_correct = selected_answer == correct_word['meaning']
                    
                    # Update score
                    st.session_state.quiz_total += 1
                    if is_correct:
                        st.session_state.quiz_score += 1
                        st.success("🎉 Correct! Well done!")
                    else:
                        st.error(f"❌ Incorrect. The correct answer was: **{correct_word['word'] if quiz_type == 'Meaning → Word' else correct_word['meaning']}**")
                    
                    # Mark as answered
                    st.session_state.current_question['answered'] = True
                    
                    # Show word details with new structure
                    difficulty = get_difficulty(correct_word['word'])
                    
                    # Simple quiz result card
                    st.success("Word Details:")
                    
                    with st.container():
                        # Simple border for quiz result
                        st.markdown("---")
                        
                        # Word title with emoji
                        st.markdown(f"### 📚 {correct_word['word']} {difficulty}")
                        
                        # Meaning
                        st.markdown(f"**Meaning:** {correct_word['meaning']}")
                        
                        # Expressions if available
                        expressions = correct_word.get('expressions', [])
                        if expressions:
                            st.markdown("**Simple Expressions:**")
                            for expr in expressions:
                                st.markdown(f"• {expr}")
                        
                        # Example phrase
                        if correct_word['phrase']:
                            st.markdown(f"**💡 Example:** {correct_word['phrase']}")
                        
                        # Display media if exists (image or video)
                        media_path = correct_word.get('media')
                        if media_path and os.path.exists(media_path):
                            file_extension = os.path.splitext(media_path)[1].lower()
                            
                            if file_extension in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm']:
                                st.markdown("**🎥 Video Reference:**")
                                try:
                                    st.video(media_path)
                                except Exception as e:
                                    st.error(f"Error loading video: {str(e)}")
                            elif file_extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg']:
                                st.markdown("**📷 Visual Reference:**")
                                try:
                                    st.image(media_path, caption=f"Visual for: {correct_word['phrase']}", use_column_width=True)
                                except Exception as e:
                                    st.error(f"Error loading image: {str(e)}")
                            else:
                                st.warning(f"Unsupported media format: {file_extension}")
                        
                        # Bottom border
                        st.markdown("---")
    else:
        st.warning("Need at least 4 words in the selected category to run quiz mode. Please load sample vocabulary first.")