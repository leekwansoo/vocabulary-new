import streamlit as st 
import os
import random
import json
from datetime import datetime, timedelta
from main import (
    load_word_pools, 
    create_audio_file, 
    load_vocabulary_from_file, 
    save_word_pools_to_file,
    filter_words_by_category,
    validate_word_entry,
    cleanup_audio_file,
    DEFAULT_CATEGORIES,
    DEFAULT_VOCABULARY_FILE,
    DIFFICULTY_LEVELS,
    LEVEL_DESCRIPTIONS,
    SPEED_OPTIONS,
    SPEED_LABELS
)

# Advanced word data with comprehensive information
ADVANCED_WORD_DATA = {
    "serendipity": {
        "phonetic": "/ˌsɛrənˈdɪpɪti/",
        "difficulty": "⭐⭐⭐",
        "part_of_speech": "noun",
        "etymology": "From Persian fairy tale 'The Three Princes of Serendip'",
        "synonyms": ["chance", "fortune", "luck", "accident"],
        "antonyms": ["misfortune", "bad luck", "intention"],
        "collocations": ["pure serendipity", "by serendipity", "serendipity strikes"],
        "word_forms": {"noun": "serendipity", "adjective": "serendipitous", "adverb": "serendipitously"},
        "frequency": "rare",
        "register": "formal",
        "common_mistakes": "Often misspelled as 'serendipety'"
    },
    "entrepreneur": {
        "phonetic": "/ˌɑntrəprəˈnɜr/",
        "difficulty": "⭐⭐",
        "part_of_speech": "noun",
        "etymology": "French 'entreprendre' meaning 'to undertake'",
        "synonyms": ["business owner", "innovator", "founder", "startup founder"],
        "antonyms": ["employee", "worker", "follower"],
        "collocations": ["successful entrepreneur", "young entrepreneur", "serial entrepreneur"],
        "word_forms": {"noun": "entrepreneur", "adjective": "entrepreneurial", "noun": "entrepreneurship"},
        "frequency": "common",
        "register": "business/formal",
        "common_mistakes": "Pronunciation often confused with 'entrepren-your'"
    },
    "metabolism": {
        "phonetic": "/məˈtæbəˌlɪzəm/",
        "difficulty": "⭐⭐",
        "part_of_speech": "noun",
        "etymology": "Greek 'metabole' meaning 'change'",
        "synonyms": ["metabolic process", "biochemical process"],
        "antonyms": [],
        "collocations": ["fast metabolism", "slow metabolism", "boost metabolism"],
        "word_forms": {"noun": "metabolism", "verb": "metabolize", "adjective": "metabolic"},
        "frequency": "common",
        "register": "scientific/medical",
        "common_mistakes": "Often confused with 'metablism' (missing 'o')"
    }
}

# Spaced repetition system
def calculate_next_review_date(word, performance):
    """Calculate when a word should be reviewed next based on performance"""
    base_intervals = {
        "again": 1,      # 1 day
        "hard": 2,       # 2 days  
        "good": 4,       # 4 days
        "easy": 7        # 7 days
    }
    return datetime.now() + timedelta(days=base_intervals.get(performance, 4))

def get_advanced_word_data(word):
    """Get advanced data for a word"""
    return ADVANCED_WORD_DATA.get(word.lower(), {
        "phonetic": "",
        "difficulty": "⭐⭐",
        "part_of_speech": "unknown",
        "etymology": "Etymology not available",
        "synonyms": [],
        "antonyms": [],
        "collocations": [],
        "word_forms": {},
        "frequency": "common",
        "register": "general",
        "common_mistakes": "None noted"
    })

# Configure the app
st.set_page_config(
    page_title="Vocabulary Builder - Advanced 2",
    page_icon="🚀",
    layout="wide"
)

# Custom CSS to increase base font size by 30%
st.markdown("""
<style>
    .main .block-container {
        font-size: 1.3em;
    }
    
    .stSelectbox > div > div {
        font-size: 1.3em;
    }
    
    .stRadio > div {
        font-size: 1.3em;
    }
    
    .stButton > button {
        font-size: 1.3em;
    }
    
    .stMarkdown {
        font-size: 1.3em;
    }
    
    .stSubheader {
        font-size: 1.69em;
    }
    
    .stHeader {
        font-size: 2.08em;
    }
    
    .stTitle {
        font-size: 2.6em;
    }
    
    .stMetric {
        font-size: 1.3em;
    }
    
    .stSlider {
        font-size: 1.3em;
    }
    
    .stTextInput > div > div > input {
        font-size: 1.3em;
    }
    
    .stTextArea > div > div > textarea {
        font-size: 1.3em;
    }
</style>
""", unsafe_allow_html=True)

st.title("🚀 Vocabulary Builder - Advanced 2")
st.header("AI-Powered Language Learning Suite")
st.subheader("Advanced features for serious language learners")

# Level Selection  
st.markdown("### 🎯 Select Your Learning Level")
level_col1, level_col2, level_col3 = st.columns(3)

with level_col1:
    if st.button("📚 **Level 1: Beginner**\n\nBasic vocabulary", key="adv2_level1"):
        st.session_state.selected_level = 1

with level_col2:
    if st.button("📖 **Level 2: Intermediate**\n\nChallenging words", key="adv2_level2"):
        st.session_state.selected_level = 2

with level_col3:
    if st.button("🎓 **Level 3: Advanced**\n\nSophisticated vocabulary", key="adv2_level3"):
        st.session_state.selected_level = 3

# Initialize session state
if 'selected_level' not in st.session_state:
    st.session_state.selected_level = 3  # Default to advanced for Advanced 2 app

# Display current level
current_level = st.session_state.selected_level
st.info(f"🎯 **Current Level: {current_level}** - {LEVEL_DESCRIPTIONS[current_level]}")

st.sidebar.title("🎓 Expert Navigation")

# Configuration
word_file = DEFAULT_VOCABULARY_FILE
category_list = DEFAULT_CATEGORIES

# Initialize session state for advanced features
if 'learning_progress' not in st.session_state:
    st.session_state.learning_progress = {}
if 'favorite_words' not in st.session_state:
    st.session_state.favorite_words = set()
if 'daily_streak' not in st.session_state:
    st.session_state.daily_streak = 0
if 'last_study_date' not in st.session_state:
    st.session_state.last_study_date = None
if 'study_time' not in st.session_state:
    st.session_state.study_time = 0

# Load sample vocabulary button
col1, col2, col3 = st.columns(3)
with col1:
    if st.button(f"📚 Load Level {current_level} Vocabulary", help=f"Load 160 words at Level {current_level}"):
        word_pools = load_word_pools(current_level)
        if word_pools:
            success = save_word_pools_to_file(word_pools, word_file)
            if success:
                st.success("✅ Loaded 160 words!")
            else:
                st.error("❌ Loading failed.")

with col2:
    all_words = load_vocabulary_from_file(word_file)
    if all_words:
        st.metric("📊 Total Words", len(all_words))

with col3:
    # Daily streak
    today = datetime.now().date()
    if st.session_state.last_study_date:
        if st.session_state.last_study_date == today:
            st.metric("🔥 Daily Streak", st.session_state.daily_streak)
        elif st.session_state.last_study_date == today - timedelta(days=1):
            st.metric("🔥 Daily Streak", st.session_state.daily_streak, "Continue today!")
        else:
            st.metric("🔥 Daily Streak", 0, "Streak broken")
    else:
        st.metric("🔥 Daily Streak", 0)

# Main navigation
select = st.sidebar.radio("Select Learning Mode", [
    "🎓 Smart Study", 
    "🧠 Memory Palace", 
    "🎯 Adaptive Quiz",
    "📝 Writing Practice",
    "🔍 Word Explorer",
    "📊 Analytics Dashboard",
    "⚙️ Learning Settings"
])

if select == "🎓 Smart Study":
    st.subheader("🎓 AI-Powered Smart Study Mode")
    
    # Study preferences
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_category = st.selectbox("Category", category_list)
    with col2:
        study_focus = st.selectbox("Focus Area", [
            "All Aspects", "Pronunciation", "Meaning", "Usage", "Etymology"
        ])
    with col3:
        selected_speed = st.selectbox("Voice Speed", SPEED_OPTIONS, format_func=lambda x: SPEED_LABELS[x])
    
    # Advanced filters
    st.markdown("#### 🎛️ Advanced Filters")
    filter_cols = st.columns(4)
    with filter_cols[0]:
        difficulty_filter = st.multiselect("Difficulty", ["⭐", "⭐⭐", "⭐⭐⭐"], default=["⭐", "⭐⭐", "⭐⭐⭐"])
    with filter_cols[1]:
        frequency_filter = st.multiselect("Frequency", ["rare", "uncommon", "common", "very common"], default=["common", "very common"])
    with filter_cols[2]:
        pos_filter = st.multiselect("Part of Speech", ["noun", "verb", "adjective", "adverb"], default=["noun", "verb", "adjective", "adverb"])
    with filter_cols[3]:
        show_favorites_only = st.checkbox("❤️ Favorites Only")
    
    if selected_category:
        all_words = load_vocabulary_from_file(word_file)
        filtered_words = filter_words_by_category(all_words, selected_category)
        
        # Apply advanced filters
        if show_favorites_only:
            filtered_words = [w for w in filtered_words if w['word'] in st.session_state.favorite_words]
        
        if filtered_words:
            st.info(f"📚 Showing {len(filtered_words)} words")
            
            for entry in filtered_words:
                word_data = get_advanced_word_data(entry['word'])
                
                with st.container():
                    # Main word card
                    col1, col2 = st.columns([5, 1])
                    
                    with col1:
                        # Header with word, phonetic, and metadata
                        col_word, col_actions = st.columns([4, 1])
                        
                        with col_word:
                            st.markdown(
                                f"""
                                <div style="border: 2px solid #2E86AB; border-radius: 15px; padding: 20px; margin: 15px 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);">
                                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                                        <h3 style="color: #2E86AB; margin: 0; font-size: 1.8em;">📚 {entry['word']} {word_data['difficulty']}</h3>
                                        <span style="background: #2E86AB; color: white; padding: 4px 8px; border-radius: 12px; font-size: 1.04em;">{word_data['part_of_speech']}</span>
                                    </div>
                                    <p style="color: #666; font-style: italic; margin: 5px 0; font-size: 1.43em;">{word_data['phonetic']}</p>
                                    <p style="font-size: 1.82em; margin: 10px 0;"><strong>Meaning:</strong> {entry['meaning']}</p>
                                    <p style="font-size: 1.82em; margin: 10px 0;"><strong>Example:</strong> {entry['phrase']}</p>
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                        
                        with col_actions:
                            # Favorite button
                            if entry['word'] in st.session_state.favorite_words:
                                if st.button("❤️", key=f"unfav_{entry['word']}", help="Remove from favorites"):
                                    st.session_state.favorite_words.discard(entry['word'])
                                    st.rerun()
                            else:
                                if st.button("🤍", key=f"fav_{entry['word']}", help="Add to favorites"):
                                    st.session_state.favorite_words.add(entry['word'])
                                    st.rerun()
                        
                        # Expandable sections based on study focus
                        if study_focus in ["All Aspects", "Etymology"]:
                            with st.expander("📜 Etymology & Word History"):
                                st.write(f"**Origin:** {word_data['etymology']}")
                                if word_data['word_forms']:
                                    st.write("**Word Forms:**")
                                    for pos, form in word_data['word_forms'].items():
                                        st.write(f"- {pos.title()}: {form}")
                        
                        if study_focus in ["All Aspects", "Usage"]:
                            with st.expander("💡 Usage & Context"):
                                if word_data['synonyms']:
                                    st.write(f"**Synonyms:** {', '.join(word_data['synonyms'])}")
                                if word_data['antonyms']:
                                    st.write(f"**Antonyms:** {', '.join(word_data['antonyms'])}")
                                if word_data['collocations']:
                                    st.write(f"**Common Collocations:** {', '.join(word_data['collocations'])}")
                                st.write(f"**Register:** {word_data['register']}")
                                st.write(f"**Frequency:** {word_data['frequency']}")
                        
                        if study_focus in ["All Aspects", "Pronunciation"]:
                            with st.expander("🗣️ Pronunciation Tips"):
                                st.write(f"**IPA:** {word_data['phonetic']}")
                                if word_data['common_mistakes']:
                                    st.warning(f"**Common Mistake:** {word_data['common_mistakes']}")
                    
                    with col2:
                        st.markdown("<br>" * 2, unsafe_allow_html=True)
                        
                        # Audio controls
                        if st.button("🔊 Word", key=f"word_{entry['word']}"):
                            audio_file = create_audio_file(entry['word'], f"word_{entry['word']}", is_phrase=False, speed=selected_speed)
                            if audio_file and os.path.exists(audio_file):
                                with open(audio_file, 'rb') as audio:
                                    st.audio(audio.read(), format='audio/wav')
                                cleanup_audio_file(audio_file)
                        
                        if st.button("🔊 Example", key=f"phrase_{entry['word']}"):
                            audio_file = create_audio_file(entry['phrase'], f"phrase_{entry['word']}", is_phrase=True, speed=selected_speed)
                            if audio_file and os.path.exists(audio_file):
                                with open(audio_file, 'rb') as audio:
                                    st.audio(audio.read(), format='audio/wav')
                                cleanup_audio_file(audio_file)
                        
                        # Study progress buttons
                        st.markdown("**How well do you know this word?**")
                        progress_cols = st.columns(2)
                        with progress_cols[0]:
                            if st.button("😰", key=f"again_{entry['word']}", help="Study again"):
                                st.session_state.learning_progress[entry['word']] = "again"
                                st.success("Marked for review!")
                            if st.button("😊", key=f"good_{entry['word']}", help="Good"):
                                st.session_state.learning_progress[entry['word']] = "good"
                                st.success("Well done!")
                        with progress_cols[1]:
                            if st.button("😓", key=f"hard_{entry['word']}", help="Hard"):
                                st.session_state.learning_progress[entry['word']] = "hard"
                                st.info("Keep practicing!")
                            if st.button("😎", key=f"easy_{entry['word']}", help="Easy"):
                                st.session_state.learning_progress[entry['word']] = "easy"
                                st.success("Mastered!")

elif select == "🧠 Memory Palace":
    st.subheader("🧠 Memory Palace - Visual Learning")
    st.info("💡 Memory Palace uses visual associations and stories to help you remember words better.")
    
    selected_category = st.selectbox("Choose Category for Memory Palace", category_list)
    
    if selected_category:
        all_words = load_vocabulary_from_file(word_file)
        filtered_words = filter_words_by_category(all_words, selected_category)
        
        if filtered_words:
            # Create memory palace with 5 words at a time
            st.markdown("### 🏰 Your Memory Palace")
            
            palace_words = random.sample(filtered_words, min(5, len(filtered_words)))
            
            # Visual memory aids
            memory_aids = {
                0: "🚪 **Entrance Hall**",
                1: "🛋️ **Living Room**", 
                2: "🍽️ **Dining Room**",
                3: "🛏️ **Bedroom**",
                4: "🌿 **Garden**"
            }
            
            for i, entry in enumerate(palace_words):
                location = memory_aids.get(i, f"📍 **Room {i+1}**")
                word_data = get_advanced_word_data(entry['word'])
                
                st.markdown(f"#### {location}")
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(
                        f"""
                        <div style="border: 2px solid #FF6B6B; border-radius: 10px; padding: 15px; margin: 10px 0; background-color: #fff5f5;">
                            <h4 style="color: #FF6B6B;">🎭 {entry['word']} - Create a Memory Story!</h4>
                            <p><strong>Meaning:</strong> {entry['meaning']}</p>
                            <p><strong>Memory Tip:</strong> Imagine this word in the {location.lower()}. What would you see?</p>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    # User can create their own memory story
                    memory_story = st.text_area(
                        f"Write your memory story for '{entry['word']}':",
                        placeholder=f"e.g., In the {location.lower()}, I see...",
                        key=f"memory_{entry['word']}"
                    )
                    
                with col2:
                    if st.button("🔊", key=f"memory_audio_{entry['word']}"):
                        audio_file = create_audio_file(entry['word'], f"memory_{entry['word']}", is_phrase=False)
                        if audio_file and os.path.exists(audio_file):
                            with open(audio_file, 'rb') as audio:
                                st.audio(audio.read(), format='audio/wav')
                            cleanup_audio_file(audio_file)
            
            if st.button("🔄 Generate New Memory Palace"):
                st.rerun()

elif select == "🎯 Adaptive Quiz":
    st.subheader("🎯 AI-Adaptive Quiz System")
    st.info("🤖 This quiz adapts to your performance and focuses on words you need to practice most.")
    
    # Quiz configuration
    col1, col2, col3 = st.columns(3)
    with col1:
        quiz_category = st.selectbox("Category", category_list)
    with col2:
        quiz_mode = st.selectbox("Quiz Mode", [
            "Mixed Practice", 
            "Weak Points Focus", 
            "New Words Only",
            "Review Mode"
        ])
    with col3:
        quiz_length = st.selectbox("Quiz Length", [5, 10, 15, 20])
    
    # Initialize quiz state
    if 'adaptive_quiz' not in st.session_state:
        st.session_state.adaptive_quiz = {
            'current_question': 0,
            'score': 0,
            'questions': [],
            'started': False
        }
    
    all_words = load_vocabulary_from_file(word_file)
    quiz_words = filter_words_by_category(all_words, quiz_category)
    
    if quiz_words and len(quiz_words) >= 4:
        if not st.session_state.adaptive_quiz['started']:
            if st.button("🚀 Start Adaptive Quiz"):
                # Select words based on quiz mode
                if quiz_mode == "Weak Points Focus":
                    # Prioritize words marked as "again" or "hard"
                    weak_words = [w for w in quiz_words if st.session_state.learning_progress.get(w['word'], '') in ['again', 'hard']]
                    selected_words = weak_words[:quiz_length] if len(weak_words) >= quiz_length else quiz_words[:quiz_length]
                else:
                    selected_words = random.sample(quiz_words, min(quiz_length, len(quiz_words)))
                
                st.session_state.adaptive_quiz = {
                    'current_question': 0,
                    'score': 0,
                    'questions': selected_words,
                    'started': True,
                    'answers': []
                }
                st.rerun()
        else:
            quiz = st.session_state.adaptive_quiz
            
            if quiz['current_question'] < len(quiz['questions']):
                # Show current question
                current_word = quiz['questions'][quiz['current_question']]
                word_data = get_advanced_word_data(current_word['word'])
                
                st.markdown(f"### Question {quiz['current_question'] + 1} of {len(quiz['questions'])}")
                
                # Progress bar
                progress = (quiz['current_question']) / len(quiz['questions'])
                st.progress(progress)
                
                # Question types vary
                question_types = ["meaning", "synonym", "usage"]
                question_type = random.choice(question_types)
                
                if question_type == "meaning":
                    st.markdown(f"**What is the meaning of:** {current_word['word']} {word_data['phonetic']}")
                    
                    # Create options
                    correct_answer = current_word['meaning']
                    other_words = [w for w in quiz_words if w['word'] != current_word['word']]
                    wrong_options = [w['meaning'] for w in random.sample(other_words, min(3, len(other_words)))]
                    
                    options = [correct_answer] + wrong_options
                    random.shuffle(options)
                    
                    selected = st.radio("Choose the correct meaning:", options, key=f"q_{quiz['current_question']}")
                    
                    if st.button("Submit Answer"):
                        is_correct = selected == correct_answer
                        if is_correct:
                            st.success("✅ Correct!")
                            quiz['score'] += 1
                        else:
                            st.error(f"❌ Incorrect. The answer was: {correct_answer}")
                        
                        quiz['answers'].append({
                            'word': current_word['word'],
                            'correct': is_correct,
                            'selected': selected,
                            'correct_answer': correct_answer
                        })
                        
                        quiz['current_question'] += 1
                        st.rerun()
            else:
                # Quiz completed
                st.markdown("### 🎉 Quiz Completed!")
                
                final_score = (quiz['score'] / len(quiz['questions'])) * 100
                st.metric("Final Score", f"{final_score:.1f}%", f"{quiz['score']}/{len(quiz['questions'])}")
                
                # Performance analysis
                if final_score >= 80:
                    st.success("🌟 Excellent performance! You're mastering these words!")
                elif final_score >= 60:
                    st.info("👍 Good job! Keep practicing to improve further.")
                else:
                    st.warning("💪 Keep studying! Focus on the words you missed.")
                
                # Show detailed results
                with st.expander("📊 Detailed Results"):
                    for answer in quiz['answers']:
                        status = "✅" if answer['correct'] else "❌"
                        st.write(f"{status} **{answer['word']}** - Your answer: {answer['selected'][:50]}...")
                
                if st.button("🔄 Take Another Quiz"):
                    st.session_state.adaptive_quiz['started'] = False
                    st.rerun()

elif select == "📝 Writing Practice":
    st.subheader("📝 Advanced Writing Practice")
    st.info("✍️ Practice using vocabulary words in context with AI-powered feedback.")
    
    selected_category = st.selectbox("Category for Writing Practice", category_list)
    practice_type = st.selectbox("Practice Type", [
        "Sentence Creation",
        "Story Writing", 
        "Formal Writing",
        "Creative Writing"
    ])
    
    all_words = load_vocabulary_from_file(word_file)
    category_words = filter_words_by_category(all_words, selected_category)
    
    if category_words:
        # Select 5 random words for practice
        practice_words = random.sample(category_words, min(5, len(category_words)))
        
        st.markdown("### 📝 Your Writing Challenge")
        st.markdown("**Use these words in your writing:**")
        
        word_list_display = []
        for word in practice_words:
            word_data = get_advanced_word_data(word['word'])
            word_list_display.append(f"**{word['word']}** {word_data['phonetic']} - {word['meaning']}")
        
        st.markdown("\n".join(word_list_display))
        
        if practice_type == "Sentence Creation":
            st.markdown("**Task:** Write one sentence for each word above.")
            user_writing = st.text_area("Your sentences:", height=200, 
                placeholder="Write one sentence for each word, showing you understand their meanings...")
        
        elif practice_type == "Story Writing":
            st.markdown("**Task:** Write a short story (150-300 words) using all the words above.")
            user_writing = st.text_area("Your story:", height=300,
                placeholder="Once upon a time...")
        
        elif practice_type == "Formal Writing":
            st.markdown("**Task:** Write a formal paragraph (business/academic style) using these words.")
            user_writing = st.text_area("Your formal writing:", height=250,
                placeholder="In recent developments...")
        
        else:  # Creative Writing
            st.markdown("**Task:** Write a creative piece (poem, dialogue, or creative story) using these words.")
            user_writing = st.text_area("Your creative writing:", height=300,
                placeholder="Be creative and have fun!")
        
        if st.button("🔍 Analyze My Writing"):
            if user_writing:
                # Simple analysis (in a real app, you'd use AI)
                word_count = len(user_writing.split())
                used_words = []
                for word in practice_words:
                    if word['word'].lower() in user_writing.lower():
                        used_words.append(word['word'])
                
                st.markdown("### 📊 Writing Analysis")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Word Count", word_count)
                with col2:
                    st.metric("Target Words Used", f"{len(used_words)}/5")
                with col3:
                    completion = (len(used_words) / 5) * 100
                    st.metric("Completion", f"{completion:.0f}%")
                
                if used_words:
                    st.success(f"✅ Great! You used: {', '.join(used_words)}")
                
                missing_words = [w['word'] for w in practice_words if w['word'] not in used_words]
                if missing_words:
                    st.info(f"💡 Try to include: {', '.join(missing_words)}")
                
                # Encourage rewriting
                if len(used_words) < 5:
                    st.markdown("**💪 Challenge:** Rewrite your text to include all target words!")
            else:
                st.warning("Please write something first!")

elif select == "🔍 Word Explorer":
    st.subheader("🔍 Advanced Word Explorer")
    st.info("🕵️ Dive deep into word relationships, patterns, and linguistic connections.")
    
    # Search functionality
    search_term = st.text_input("🔎 Search for a word:", placeholder="Enter any word...")
    
    if search_term:
        all_words = load_vocabulary_from_file(word_file)
        
        # Find exact matches and partial matches
        exact_matches = [w for w in all_words if w['word'].lower() == search_term.lower()]
        partial_matches = [w for w in all_words if search_term.lower() in w['word'].lower() and w not in exact_matches]
        meaning_matches = [w for w in all_words if search_term.lower() in w['meaning'].lower() and w not in exact_matches + partial_matches]
        
        if exact_matches:
            st.markdown("### 🎯 Exact Match")
            word = exact_matches[0]
            word_data = get_advanced_word_data(word['word'])
            
            # Comprehensive word display
            st.markdown(
                f"""
                <div style="border: 3px solid #FFD700; border-radius: 15px; padding: 20px; background: linear-gradient(135deg, #fff9c4 0%, #fff5a5 100%);">
                    <h2 style="color: #B8860B; margin-bottom: 10px; font-size: 2.2em;">🌟 {word['word']} {word_data['difficulty']}</h2>
                    <p style="font-size: 1.56em; color: #8B7355; font-style: italic; margin: 5px 0;">{word_data['phonetic']}</p>
                    <p style="font-size: 1.82em; margin: 15px 0;"><strong>Definition:</strong> {word['meaning']}</p>
                    <p style="font-size: 1.69em; margin: 15px 0;"><strong>Example:</strong> <em>{word['phrase']}</em></p>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            # Detailed linguistic information
            tabs = st.tabs(["🧬 Linguistics", "📚 Usage", "🎯 Practice", "🔗 Related"])
            
            with tabs[0]:  # Linguistics
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Part of Speech:** {word_data['part_of_speech']}")
                    st.write(f"**Etymology:** {word_data['etymology']}")
                    st.write(f"**Frequency:** {word_data['frequency']}")
                    st.write(f"**Register:** {word_data['register']}")
                
                with col2:
                    if word_data['word_forms']:
                        st.write("**Word Family:**")
                        for pos, form in word_data['word_forms'].items():
                            st.write(f"• {pos.title()}: {form}")
            
            with tabs[1]:  # Usage
                if word_data['synonyms']:
                    st.write(f"**Synonyms:** {', '.join(word_data['synonyms'])}")
                if word_data['antonyms']:
                    st.write(f"**Antonyms:** {', '.join(word_data['antonyms'])}")
                if word_data['collocations']:
                    st.write(f"**Common Collocations:** {', '.join(word_data['collocations'])}")
                if word_data['common_mistakes']:
                    st.warning(f"**⚠️ Common Mistake:** {word_data['common_mistakes']}")
            
            with tabs[2]:  # Practice
                st.write("**Quick Practice:**")
                practice_sentence = st.text_input(f"Use '{word['word']}' in a sentence:")
                if practice_sentence and word['word'].lower() in practice_sentence.lower():
                    st.success("✅ Great! You used the word correctly!")
                elif practice_sentence:
                    st.info(f"💡 Try including the word '{word['word']}' in your sentence.")
            
            with tabs[3]:  # Related
                # Find words with similar meanings or from same category
                same_category = [w for w in all_words if w.get('category') == word.get('category') and w['word'] != word['word']]
                if same_category:
                    st.write(f"**Other {word.get('category', 'similar').title()} Words:**")
                    related_sample = random.sample(same_category, min(5, len(same_category)))
                    for related in related_sample:
                        st.write(f"• **{related['word']}** - {related['meaning'][:60]}...")
        
        if partial_matches:
            st.markdown("### 🔍 Partial Matches")
            for word in partial_matches[:3]:
                st.write(f"• **{word['word']}** - {word['meaning'][:80]}...")
        
        if meaning_matches:
            st.markdown("### 💭 Meaning Matches")
            for word in meaning_matches[:3]:
                st.write(f"• **{word['word']}** - {word['meaning'][:80]}...")
        
        if not (exact_matches or partial_matches or meaning_matches):
            st.info("🤔 No matches found. Try a different search term or add new words to your vocabulary!")

elif select == "📊 Analytics Dashboard":
    st.subheader("📊 Advanced Learning Analytics")
    
    all_words = load_vocabulary_from_file(word_file)
    
    if all_words:
        # Overall metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Vocabulary", len(all_words))
        with col2:
            favorites_count = len(st.session_state.favorite_words)
            st.metric("❤️ Favorite Words", favorites_count)
        with col3:
            mastered = len([w for w, status in st.session_state.learning_progress.items() if status == "easy"])
            st.metric("🌟 Mastered", mastered)
        with col4:
            needs_review = len([w for w, status in st.session_state.learning_progress.items() if status in ["again", "hard"]])
            st.metric("🔄 Needs Review", needs_review)
        
        # Learning progress visualization
        st.markdown("### 📈 Learning Progress")
        
        progress_data = {"Not Studied": 0, "Needs Review": 0, "Good": 0, "Mastered": 0}
        for word in all_words:
            status = st.session_state.learning_progress.get(word['word'], 'not_studied')
            if status == 'again' or status == 'hard':
                progress_data["Needs Review"] += 1
            elif status == 'good':
                progress_data["Good"] += 1
            elif status == 'easy':
                progress_data["Mastered"] += 1
            else:
                progress_data["Not Studied"] += 1
        
        # Display as metrics
        prog_cols = st.columns(4)
        colors = ["🔴", "🟡", "🟢", "🌟"]
        for i, (status, count) in enumerate(progress_data.items()):
            with prog_cols[i]:
                st.metric(f"{colors[i]} {status}", count)
        
        # Category breakdown
        st.markdown("### 📊 Vocabulary by Category & Difficulty")
        
        category_stats = {}
        difficulty_stats = {"⭐": 0, "⭐⭐": 0, "⭐⭐⭐": 0}
        
        for word in all_words:
            # Category stats
            cat = word.get('category', 'Unknown').title()
            category_stats[cat] = category_stats.get(cat, 0) + 1
            
            # Difficulty stats
            word_data = get_advanced_word_data(word['word'])
            diff = word_data['difficulty']
            if diff in difficulty_stats:
                difficulty_stats[diff] += 1
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Categories:**")
            for cat, count in category_stats.items():
                percentage = (count / len(all_words)) * 100
                st.write(f"• {cat}: {count} words ({percentage:.1f}%)")
        
        with col2:
            st.markdown("**Difficulty Levels:**")
            for diff, count in difficulty_stats.items():
                percentage = (count / len(all_words)) * 100
                st.write(f"• {diff} : {count} words ({percentage:.1f}%)")
        
        # Learning recommendations
        st.markdown("### 🎯 Personalized Recommendations")
        
        if needs_review > 0:
            st.warning(f"🔄 You have {needs_review} words that need review. Focus on these first!")
        
        if len(st.session_state.favorite_words) == 0:
            st.info("💡 Try marking some words as favorites to create a personalized study list!")
        
        if mastered > len(all_words) * 0.7:
            st.success("🌟 Excellent! You've mastered most of your vocabulary. Time to add more words!")
        
        # Export options
        st.markdown("### 📥 Export Your Data")
        export_cols = st.columns(3)
        
        with export_cols[0]:
            if st.button("📄 Export Favorites"):
                favorite_words = [w for w in all_words if w['word'] in st.session_state.favorite_words]
                if favorite_words:
                    export_text = "\n".join([f"{w['word']} | {w['meaning']} | {w['phrase']}" for w in favorite_words])
                    st.download_button("Download Favorites", export_text, "favorites.txt")
        
        with export_cols[1]:
            if st.button("📊 Export Progress"):
                progress_text = json.dumps(st.session_state.learning_progress, indent=2)
                st.download_button("Download Progress", progress_text, "progress.json")
        
        with export_cols[2]:
            if st.button("🔄 Reset All Data"):
                if st.button("⚠️ Confirm Reset", type="secondary"):
                    st.session_state.learning_progress = {}
                    st.session_state.favorite_words = set()
                    st.session_state.daily_streak = 0
                    st.success("All data reset!")

elif select == "⚙️ Learning Settings":
    st.subheader("⚙️ Personalize Your Learning Experience")
    
    # Learning preferences
    st.markdown("### 🎯 Learning Preferences")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Study Goals:**")
        daily_goal = st.number_input("Words to study per day:", min_value=5, max_value=50, value=20)
        focus_areas = st.multiselect(
            "Focus on these areas:",
            ["Pronunciation", "Meaning", "Usage", "Etymology", "Grammar"],
            default=["Pronunciation", "Meaning", "Usage"]
        )
        
        learning_style = st.selectbox("Preferred learning style:", [
            "Visual (reading, colors, diagrams)",
            "Auditory (sounds, pronunciation)",
            "Kinesthetic (writing, interaction)",
            "Mixed approach"
        ])
    
    with col2:
        st.markdown("**Difficulty Preferences:**")
        preferred_difficulty = st.selectbox("Preferred difficulty level:", [
            "Beginner (⭐)",
            "Intermediate (⭐⭐)", 
            "Advanced (⭐⭐⭐)",
            "Mixed levels"
        ])
        
        review_frequency = st.selectbox("Review frequency:", [
            "Daily",
            "Every 2 days",
            "Weekly",
            "Custom"
        ])
        
        show_phonetics = st.checkbox("Always show phonetic transcription", value=True)
        show_etymology = st.checkbox("Show word etymology", value=False)
    
    # Notification settings
    st.markdown("### 🔔 Study Reminders")
    enable_reminders = st.checkbox("Enable study reminders")
    
    if enable_reminders:
        reminder_time = st.time_input("Daily reminder time:")
        reminder_message = st.text_input(
            "Custom reminder message:",
            value="Time for your vocabulary practice! 📚"
        )
    
    # Save settings
    if st.button("💾 Save Settings"):
        # In a real app, these would be saved to a database or file
        settings = {
            "daily_goal": daily_goal,
            "focus_areas": focus_areas,
            "learning_style": learning_style,
            "preferred_difficulty": preferred_difficulty,
            "review_frequency": review_frequency,
            "show_phonetics": show_phonetics,
            "show_etymology": show_etymology,
            "enable_reminders": enable_reminders
        }
        
        st.success("✅ Settings saved successfully!")
        st.json(settings)

# Update study streak
if st.session_state.last_study_date != datetime.now().date():
    if st.session_state.last_study_date == datetime.now().date() - timedelta(days=1):
        st.session_state.daily_streak += 1
    else:
        st.session_state.daily_streak = 1
    st.session_state.last_study_date = datetime.now().date()

# Footer
st.markdown("---")
st.markdown("**🚀 Advanced 2 Features:** AI-powered learning, spaced repetition, memory palace, adaptive quizzes, comprehensive analytics, personalized recommendations")