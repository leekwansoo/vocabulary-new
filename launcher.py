import streamlit as st
import subprocess
import sys
import os

# Configure the launcher
st.set_page_config(
    page_title="Vocabulary Builder Suite",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em;
        font-weight: bold;
        margin-bottom: 20px;
    }
    
    .app-card {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        transition: transform 0.3s ease;
    }
    
    .app-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    
    .level-badge {
        display: inline-block;
        padding: 5px 15px;
        border-radius: 20px;
        color: white;
        font-weight: bold;
        margin-bottom: 10px;
    }
    
    .basic { background-color: #4CAF50; }
    .advanced1 { background-color: #FF9800; }
    .advanced2 { background-color: #9C27B0; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🎓 Vocabulary Builder Suite</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; font-size: 1.2em; color: #666;">Choose your learning level and start building your English vocabulary!</p>', unsafe_allow_html=True)

st.markdown("---")

# App selection cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="app-card">
        <div class="level-badge basic">BASIC</div>
        <h3>📚 Basic Vocabulary Builder</h3>
        <p><strong>Perfect for beginners!</strong></p>
        <ul>
            <li>Simple, clean interface</li>
            <li>Add and view vocabulary words</li>
            <li>Audio pronunciation (3 speeds)</li>
            <li>8 categories with 160 words per level</li>
            <li>3 difficulty levels (Beginner/Intermediate/Advanced)</li>
            <li>Level-based vocabulary progression</li>
            <li>Enhanced text visibility</li>
        </ul>
        <p><strong>Best for:</strong> New English learners, simple vocabulary practice</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Basic App", key="basic", use_container_width=True):
        st.info("💡 Run this command in your terminal:")
        st.code("streamlit run app.py", language="bash")

with col2:
    st.markdown("""
    <div class="app-card">
        <div class="level-badge advanced1">ADVANCED 1</div>
        <h3>🎯 Advanced Learning</h3>
        <p><strong>For intermediate learners!</strong></p>
        <ul>
            <li>Phonetic transcription (IPA)</li>
            <li>3 vocabulary levels + word difficulty ratings</li>
            <li>Interactive quiz system</li>
            <li>Progress tracking</li>
            <li>Enhanced study modes</li>
            <li>Level-based difficulty filtering</li>
        </ul>
        <p><strong>Best for:</strong> ESL students, pronunciation focus, quiz practice</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎯 Launch Advanced 1", key="advanced1", use_container_width=True):
        st.info("💡 Run this command in your terminal:")
        st.code("streamlit run app_advanced1.py", language="bash")

with col3:
    st.markdown("""
    <div class="app-card">
        <div class="level-badge advanced2">ADVANCED 2</div>
        <h3>🚀 Expert Learning Suite</h3>
        <p><strong>For serious language learners!</strong></p>
        <ul>
            <li>AI-powered adaptive learning</li>
            <li>Memory Palace technique</li>
            <li>Spaced repetition system</li>
            <li>Writing practice with feedback</li>
            <li>Word explorer & relationships</li>
            <li>Multi-level vocabulary progression</li>
            <li>Comprehensive analytics</li>
        </ul>
        <p><strong>Best for:</strong> Advanced students, comprehensive learning, language mastery</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Launch Advanced 2", key="advanced2", use_container_width=True):
        st.info("💡 Run this command in your terminal:")
        st.code("streamlit run app_advanced2.py", language="bash")

st.markdown("---")

# Feature comparison table
st.markdown("## 📊 Feature Comparison")

features_data = {
    "Feature": [
        "Basic Vocabulary Management",
        "Audio Pronunciation", 
        "Multiple Speed Options",
        "Category-based Learning",
        "Sample Word Database",
        "Phonetic Transcription (IPA)",
        "Word Difficulty Levels",
        "Interactive Quizzes",
        "Progress Tracking",
        "Memory Palace Technique",
        "Adaptive Learning AI",
        "Spaced Repetition",
        "Writing Practice",
        "Word Explorer",
        "Analytics Dashboard",
        "Favorites System",
        "Export Functionality"
    ],
    "Basic": [
        "✅", "✅", "✅", "✅", "✅ (160 words x3 levels)", 
        "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌", "❌"
    ],
    "Advanced 1": [
        "✅", "✅", "✅", "✅", "✅ (160 words x3 levels)",
        "✅", "✅", "✅", "✅", "❌", "❌", "❌", "❌", "❌", "✅", "❌", "❌"
    ],
    "Advanced 2": [
        "✅", "✅", "✅", "✅", "✅ (160 words x3 levels)",
        "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅", "✅"
    ]
}

st.table(features_data)

# Learning path recommendation
st.markdown("## 🎯 Recommended Learning Path")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    ### 👶 **Start Here: Basic**
    - New to English learning
    - Want simple vocabulary practice
    - Need basic pronunciation help
    - Prefer minimal features
    
    **Time commitment:** 15-30 min/day
    """)

with col2:
    st.markdown("""
    ### 📈 **Progress To: Advanced 1** 
    - Comfortable with basic vocabulary
    - Want to improve pronunciation
    - Ready for quiz challenges
    - Need difficulty-based learning
    
    **Time commitment:** 30-45 min/day
    """)

with col3:
    st.markdown("""
    ### 🎓 **Master With: Advanced 2**
    - Serious about language learning
    - Want comprehensive features
    - Enjoy analytical feedback
    - Aim for language mastery
    
    **Time commitment:** 45-60 min/day
    """)

# Tips and getting started
st.markdown("---")
st.markdown("## 💡 Getting Started Tips")

tips_col1, tips_col2 = st.columns(2)

with tips_col1:
    st.markdown("""
    ### 🚀 **Quick Start Guide:**
    1. Choose your appropriate level app
    2. Click "Load Sample Vocabulary" to get 160 words
    3. Select a category that interests you
    4. Start with pronunciation practice
    5. Progress to quizzes (Advanced apps)
    
    ### 📚 **Study Tips:**
    - Study 15-20 words per session
    - Focus on pronunciation first
    - Use example phrases in your own sentences
    - Review difficult words more frequently
    """)

with tips_col2:
    st.markdown("""
    ### 🎯 **Maximize Your Learning:**
    - Set daily study goals (10-30 minutes)
    - Use multiple speeds for pronunciation
    - Practice writing with new vocabulary
    - Track your progress regularly
    - Focus on words you find difficult
    
    ### 🌟 **Pro Tips:**
    - Start each session with review words
    - Use memory techniques (Advanced 2)
    - Create personal sentences with new words
    - Export your progress regularly
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-style: italic;">
    <p>🎓 Vocabulary Builder Suite - Empowering English Language Learners Worldwide</p>
    <p>Choose your path, start your journey, master the language! 🚀</p>
</div>
""", unsafe_allow_html=True)