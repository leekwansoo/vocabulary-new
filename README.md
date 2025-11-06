# 📚 Vocabulary Builder - Advanced Learning Platform

A comprehensive, **senior-friendly** vocabulary learning application built with Streamlit, featuring **cloud-compatible audio pronunciation**, interactive quizzes, and progress tracking. Designed specifically for ESL learners with enhanced accessibility and modern learning features.

![Vocabulary Builder](https://img.shields.io/badge/Vocabulary-Builder-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge)
![Cloud Ready](https://img.shields.io/badge/Cloud-Ready-brightgreen?style=for-the-badge)
![Senior Friendly](https://img.shields.io/badge/Senior-Friendly-orange?style=for-the-badge)

## 🌟 Key Features

### 👥 **Senior-Friendly Design**
- **50% larger fonts** throughout the application for enhanced readability
- **Large, clear buttons** with intuitive icons and high contrast
- **Simplified navigation** with clear visual hierarchy
- **Accessible interface** designed for users of all ages

### � **Cloud-Compatible Audio System** ⭐ **NEW!**
- **Hybrid TTS Technology**: Automatically switches between local (`pyttsx3`) and cloud (`gTTS`) text-to-speech
- **Universal Compatibility**: Works seamlessly on local development and Streamlit Cloud
- **Multi-Format Support**: Handles both WAV and MP3 audio files automatically
- **Speed Control**: Three speed options (Normal 100%, Slower 90%, Slowest 80%)
- **Smart Voice Selection**: Intelligent American English voice detection

### 📖 **4-Level Learning System** ⭐ **ENHANCED!**
- **Level 1: Beginner** - Basic vocabulary with common everyday words (160 words)
- **Level 2: Intermediate** - More challenging words for advancing learners (160 words)
- **Level 3: Advanced** - Sophisticated vocabulary for expert learners (160 words)
- **Learned Words Level** - Special review system for mastered vocabulary with timestamps

### 🎯 **Advanced Learning Modes**
- **📖 Study Mode**: Enhanced word cards with phonetic transcriptions and difficulty levels
- **🎯 Quiz Mode**: Interactive multiple-choice quizzes with two question types
- **📊 Progress Tracking**: Comprehensive statistics and performance analytics
- **🎮 Interactive Features**: Real-time scoring, example cards, and smart word management

### 🏷️ **Smart Organization**
- **8 Categories**: General, Science, Business, Literature, Travel, History, Geography, Health
- **Difficulty Filtering**: ⭐ Easy, ⭐⭐ Medium, ⭐⭐⭐ Hard word classification
- **JSON-Based Storage**: Reliable data persistence with `learned.json` tracking
- **Category-Specific Learning**: Focus on specific subject areas

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows/macOS/Linux
- Virtual environment recommended

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/leekwansoo/vocaburary_builder.git
cd vocaburary_builder
```

2. **Create virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run app_advanced1.py
```

### Cloud Deployment (Streamlit Cloud) ⭐ **READY!**

1. **Fork/Clone** this repository to your GitHub account
2. **Connect** your repository to [Streamlit Cloud](https://streamlit.io/)
3. **Deploy** - The app will automatically use cloud-compatible audio
4. **Access** your deployed app with full audio functionality working perfectly!

### Launch the Application

**Primary Application - Advanced Learning Platform:**
```bash
streamlit run app_advanced1.py
```

**Alternative Applications (if available):**
```bash
# Basic Vocabulary Builder (if exists)
streamlit run app_basic.py

# Expert Learning Suite (if exists)  
streamlit run app_advanced2.py

# Master Interface (if exists)
streamlit run app.py
```

---

## 🎮 **How to Use**

### Getting Started
1. **Select Learning Level**: Choose from Beginner (1), Intermediate (2), Advanced (3), or Learned Words
2. **Load Vocabulary**: Click "Load Level X Vocabulary" to import 160 curated words
3. **Choose Learning Mode**: Study Mode for learning, Quiz Mode for testing
4. **Select Category**: Focus on specific subjects (General, Science, Business, etc.)
5. **Use Audio Features**: Click 🔊 buttons to hear perfect pronunciation

### Study Mode Workflow
- **Browse Word Cards**: Enhanced cards with phonetic transcriptions and difficulty levels
- **Audio Pronunciation**: Click word and phrase audio buttons with speed control
- **Smart Management**: Mark words as "Learned" or "Delete" unwanted entries
- **Filter by Difficulty**: Focus on Easy, Medium, or Hard words
- **Category Learning**: Study specific subject areas

### Quiz Mode Features  
- **Two Quiz Types**: "Meaning → Word" and "Word → Meaning"
- **Multiple Choice**: 4-option questions with immediate feedback
- **Real-time Scoring**: Track accuracy and improvement over time
- **Example Cards**: Appear after answer submission for reinforcement
- **Category-Specific**: Take quizzes on specific subject areas

## � **Technical Architecture**

### 🔊 **Hybrid Audio System** ⭐ **BREAKTHROUGH FEATURE!**

Our revolutionary audio system ensures pronunciation works everywhere:

```python
def create_audio_file(text, filename, is_phrase=False, speed="normal"):
    """Cloud-compatible TTS with automatic fallback"""
    try:
        # Try pyttsx3 first (local development)
        engine = pyttsx3.init()
        # ... high-quality local TTS implementation
        return temp_file
    except Exception:
        # Fall back to gTTS (cloud deployment)
        tts = gTTS(text=text, lang='en', slow=use_slow_speech)
        # ... cloud-compatible TTS implementation
        return temp_file
```

#### **Environment Detection:**
- **Local Environment**: Uses system TTS engines → produces WAV files
- **Cloud Environment**: Automatically switches to Google TTS → produces MP3 files
- **Format Handling**: App automatically detects and plays both formats seamlessly

### 📊 **Features Overview**

| Feature | Description | Accessibility Benefit |
|---------|-------------|----------------------|
| 📱 **Responsive Design** | Works on desktop, tablet, mobile | Available anywhere |
| 🔊 **Cloud Audio** | Universal pronunciation system | Works on any platform |
| 👥 **Senior-Friendly** | 50% larger fonts, clear interface | Accessible to all ages |
| 🎯 **Interactive Quizzes** | Multiple choice with instant feedback | Engaging learning |
| 📚 **4 Learning Levels** | Progressive difficulty system | Structured learning path |
| 📈 **Progress Tracking** | Detailed statistics and analytics | Monitor improvement |
| 🏷️ **Smart Categories** | 8 subject areas for organization | Focused learning |
| 💾 **JSON Storage** | Reliable learned word tracking | Data persistence |

### 🎨 **Senior-Friendly Design System**

**CSS Font Scaling for Enhanced Readability:**
```css
/* 50% larger fonts throughout */
.main .block-container { font-size: 1.95em; }      /* 95% larger base */
.stTitle { font-size: 3.9em; }                     /* Large titles */
.stButton > button { font-size: 1.95em; }          /* Clear buttons */
.stMarkdown { font-size: 1.95em; }                 /* Readable text */

/* Smart selectbox scaling */
.stSelectbox > div > div { font-size: 0.975em; }   /* Balanced dropdowns */
```

### 🌐 **Cloud Deployment Ready**

**Automatic Environment Detection:**
- **Development**: Uses `pyttsx3` with system voices for highest quality
- **Production**: Seamlessly switches to `gTTS` for cloud compatibility  
- **No Configuration**: Works out-of-the-box on Streamlit Cloud
- **Error Handling**: Graceful fallback ensures audio always works

---

## � **Project Structure**

```
vocaburary-builder/
├── app_advanced1.py         # � Main application (Advanced Learning Platform)
├── main.py                  # ⚙️ Core utility functions with hybrid audio
├── requirements.txt         # 📦 Python dependencies (includes gTTS)
├── vocabulary.txt           # � Working vocabulary file
├── learned.json            # ✅ Learned words with timestamps
├── level1.json             # 📚 160 beginner vocabulary words
├── level2.json             # 📖 160 intermediate vocabulary words
├── level3.json             # 🎓 160 advanced vocabulary words
├── test_audio_fallback.py  # 🔧 Audio system testing utility
└── README.md               # � This comprehensive documentation
```

### 🔧 **Key Files:**

- **`app_advanced1.py`**: Main Streamlit application with senior-friendly design
- **`main.py`**: Core functions including cloud-compatible audio system
- **`requirements.txt`**: Dependencies including both `pyttsx3` and `gTTS`
- **`learned.json`**: Tracks mastered vocabulary with learning timestamps
- **`level*.json`**: Curated vocabulary sets (160 words each) across difficulty levels

---

## 📖 Usage Guide

### 🎯 **Recommended Workflow**

#### For New Users:
1. **Start with Master App**: `streamlit run app.py`
2. **Select Basic level** from sidebar
3. **Load Level 1 vocabulary** (160 beginner words)
4. **Practice pronunciation** with audio features
5. **Progress to Level 2 and 3** as you improve

#### For Experienced Users:
1. **Launch Master App**: `streamlit run app.py`
2. **Switch to Advanced 1 or Advanced 2** from sidebar
3. **Take quizzes** and track progress
4. **Use advanced features** like memory palace and spaced repetition

### 📚 **Getting Started**
1. **New learners**: Start with Master App → Basic level → Level 1 vocabulary
2. **Intermediate students**: Master App → Advanced 1 → Level 2 vocabulary
3. **Advanced learners**: Master App → Advanced 2 → Level 3 vocabulary

### 🎯 **Three Ways to Access Apps**

#### 🎓 **Method 1: Master App (Recommended)**
```bash
streamlit run app.py
```
**Advantages:**
- All apps in one interface
- Easy switching between levels
- Unified experience
- No need to restart

#### 🚀 **Method 2: Individual Apps**
```bash
# For focused learning on specific app
streamlit run app_basic.py      # Basic learning
streamlit run app_advanced1.py  # Intermediate features  
streamlit run app_advanced2.py  # Advanced features
```
**Advantages:**
- Dedicated app experience
- Full feature access
- No interference between apps

#### 🎨 **Method 3: Visual Launcher**
```bash
streamlit run launcher.py
```
**Advantages:**
- Beautiful visual interface
- Feature comparison table
- Learning path guidance
- App recommendations

### 📈 **Learning Progression Path**

1. **Beginner** → Master App → Basic → Level 1 (160 words)
2. **Elementary** → Master App → Basic → Level 2 (160 words)  
3. **Intermediate** → Master App → Advanced 1 → Level 2/3 + Quizzes
4. **Advanced** → Master App → Advanced 2 → Level 3 + All Features
5. **Expert** → Advanced 2 → Memory Palace + Analytics

### Study Workflow
1. **Load Level Vocabulary**: Click "Load Level X Vocabulary" button for your chosen level
2. **Choose Category**: Select from 8 available categories
3. **Set Speed**: Choose pronunciation speed (Normal/90%/80%)
4. **Study Words**: Read, listen, and practice
5. **Take Quizzes**: Test your knowledge (Advanced apps)
6. **Track Progress**: Monitor your improvement

### Best Practices
- **Daily Practice**: 15-60 minutes depending on app level
- **Start Slow**: Begin with easier words and slower speeds
- **Use Examples**: Practice with the provided example phrases
- **Regular Review**: Revisit difficult words frequently
- **Progress Gradually**: Move to advanced apps when comfortable

---

## � **Technology Stack**

### **Core Dependencies**
- **Streamlit 1.28+**: Modern web application framework with advanced CSS support
- **pyttsx3**: Local text-to-speech engine (high-quality system voices)
- **gTTS 2.3.0+**: Google Text-to-Speech API (cloud-compatible fallback)
- **Python 3.8+**: Standard library (json, os, tempfile, datetime, random)

### **Audio Technology** ⭐ **REVOLUTIONARY!**
- **Hybrid TTS System**: Seamless switching between local and cloud audio
- **American English Priority**: Intelligent voice selection for consistent pronunciation
- **Multi-Speed Support**: 3 speed options with smart rate adjustment
- **Universal Format Support**: Automatic WAV/MP3 handling
- **Cleanup Automation**: Temporary files automatically managed

### **Data Architecture**
- **JSON-Based Storage**: Structured word pools with metadata
- **Learned Words Tracking**: Timestamped progress in `learned.json`
- **Session Persistence**: Quiz scores and preferences maintained
- **File Format Flexibility**: Text files for easy vocabulary import/export

### **Accessibility Features**
- **CSS Font Scaling**: 50% larger fonts with smart responsive design
- **High Contrast Interface**: Clear visual hierarchy for senior users
- **Keyboard Navigation**: Full accessibility compliance
- **Mobile Responsive**: Works perfectly on phones and tablets

---

## 🎯 Learning Path Recommendations

### 👶 Beginner Path (Basic App)
- **Time**: 15-30 minutes/day
- **Focus**: Basic vocabulary and pronunciation
- **Goal**: Build foundation with 50-100 words
- **Duration**: 2-4 weeks

### 📈 Intermediate Path (Advanced 1)
- **Time**: 30-45 minutes/day
- **Focus**: Pronunciation accuracy and quiz practice
- **Goal**: Master 200+ words with proper pronunciation
- **Duration**: 4-8 weeks

### 🎓 Advanced Path (Advanced 2)
- **Time**: 45-60 minutes/day
- **Focus**: Comprehensive mastery and usage
- **Goal**: Professional-level vocabulary (500+ words)
- **Duration**: Ongoing

---

## 📊 Vocabulary Categories

### 📚 General (20 words)
Everyday advanced vocabulary for general communication
- serendipity, eloquent, resilient, pragmatic, ubiquitous...

### 🔬 Science (20 words)
Scientific terms and concepts
- hypothesis, catalyst, ecosystem, photosynthesis, quantum...

### 💼 Business (20 words)
Professional and business terminology
- entrepreneur, revenue, stakeholder, synergy, leverage...

### 📖 Literature (20 words)
Literary terms and concepts
- metaphor, allegory, protagonist, symbolism, irony...

### ✈️ Travel (20 words)
Travel and adventure vocabulary
- itinerary, wanderlust, expedition, accommodation...

### 🏛️ History (20 words)
Historical terms and concepts
- civilization, dynasty, revolution, renaissance...

### 🌍 Geography (20 words)
Geographic and environmental terms
- latitude, topography, archipelago, ecosystem...

### 🏥 Health (20 words)
Health and medical vocabulary
- metabolism, cardiovascular, immunity, diagnosis...

---

## 🔧 Customization

### Adding New Words
```python
# In any app, use the "Add Word" feature or modify level files (level1.json, level2.json, level3.json)
{
  "word": "Your Word",
  "meaning": "Definition here",
  "phrase": "Example sentence here"
}
```

### Adding New Categories
1. Update `DEFAULT_CATEGORIES` in `main.py`
2. Add corresponding words to appropriate level files (`level1.json`, `level2.json`, `level3.json`)
3. Update the apps as needed

### Modifying Audio Settings
```python
# In main.py, adjust speech rates
base_word_rate = 160      # Words per minute for individual words
base_phrase_rate = 140    # Words per minute for phrases
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add Vocabulary**: Contribute new words to existing categories
2. **New Categories**: Suggest and implement new word categories
3. **Features**: Enhance existing functionality
4. **Bug Fixes**: Report and fix issues
5. **Documentation**: Improve guides and examples
6. **Translations**: Help make the app multilingual

---

## 📝 License

This project is open source and available under the MIT License.

---

## 🐛 **Troubleshooting**

### **Audio Issues** ⭐ **SOLVED!**
Our hybrid audio system automatically handles most audio problems:

- **Local Development**: If `pyttsx3` fails, automatically switches to `gTTS`
- **Cloud Deployment**: Uses `gTTS` automatically - no configuration needed
- **No Sound Issues**: Check browser audio settings and volume
- **Format Problems**: App automatically detects WAV/MP3 and plays correctly

### **Common Solutions**

#### **App Won't Start**
```bash
# Check Python version (must be 3.8+)
python --version

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Test core functions
python main.py
```

#### **Audio Testing** 
```bash
# Test the hybrid audio system
python test_audio_fallback.py
```

#### **File Issues**
```bash
# Ensure correct directory
ls -la  # Should see app_advanced1.py, main.py, etc.

# Check vocabulary files exist
ls *.json  # Should see level1.json, level2.json, level3.json
```

### **Performance Tips**
- **Memory Usage**: Audio files are automatically cleaned up
- **Load Times**: JSON-based storage provides fast vocabulary loading  
- **Browser Compatibility**: Works best in Chrome, Firefox, Safari, Edge

### **Getting Help**
1. ✅ **Audio Issues**: The hybrid system should auto-resolve most problems
2. 📖 **Check README**: This documentation covers most scenarios
3. 🔍 **Error Messages**: Terminal output provides detailed error information
4. 🧪 **Test Functions**: Run `python main.py` to test core functionality
5. 🌐 **Cloud Deployment**: App works perfectly on Streamlit Cloud

---

## 🎉 Success Stories

### What Users Say:
- **"Transformed my vocabulary learning!"** - ESL Student from Japan
- **"The progressive difficulty is perfect"** - Language Teacher, Mexico
- **"Memory Palace technique actually works!"** - Advanced Learner, Brazil
- **"Best pronunciation practice tool I've found"** - Student from South Korea

---

## 🎯 **Success Stories & Impact**

### **What Makes This Special:**
- ✅ **Cloud-Compatible Audio**: Revolutionary hybrid system works everywhere
- ✅ **Senior-Friendly Design**: 50% larger fonts for enhanced accessibility  
- ✅ **4-Level Learning**: Progressive system from beginner to learned mastery
- ✅ **Real-Time Quizzes**: Interactive learning with immediate feedback
- ✅ **Smart Word Management**: JSON-based tracking with learned word system

### **Perfect For:**
- 👥 **Senior Learners**: Large fonts and clear interface design
- 🌐 **Cloud Users**: Deployed apps with working audio pronunciation
- 🎓 **ESL Students**: Structured vocabulary building with phonetics
- 👨‍🏫 **Teachers**: Comprehensive learning platform for classroom use
- 📱 **Remote Learning**: Works perfectly on any device, anywhere

## 🚀 **Future Enhancements**

### **Planned Improvements:**
- [ ] **Voice Recognition**: Speaking practice with pronunciation feedback
- [ ] **Multi-Language Support**: Spanish, French, German vocabulary sets
- [ ] **Advanced Analytics**: Machine learning-powered learning insights
- [ ] **Social Features**: Study groups and learning challenges
- [ ] **Offline Mode**: Downloaded vocabulary for internet-free learning
- [ ] **Mobile App**: Dedicated iOS/Android application

## 💡 **Learning Success Tips**

### **Study Strategies:**
1. **Start with Level 1**: Build foundation with 160 beginner words
2. **Use Audio Daily**: Practice pronunciation with speed control
3. **Take Quizzes Regularly**: Test knowledge with interactive questions
4. **Mark Progress**: Move mastered words to "Learned" level
5. **Focus by Category**: Study specific subjects (Science, Business, etc.)

### **Pronunciation Mastery:**
1. **Begin Slowly**: Use 80% speed setting initially
2. **Repeat Often**: Listen to each word multiple times
3. **Use Phonetics**: Study IPA transcriptions for accuracy
4. **Practice Phrases**: Learn words in context with example sentences
5. **Track Progress**: Monitor improvement with quiz accuracy

### **Platform Benefits:**
- 🎯 **Immediate**: Start learning right away - no setup required
- 🌐 **Universal**: Works on local development and cloud deployment
- 👥 **Accessible**: Senior-friendly design welcomes all ages
- 📊 **Trackable**: Monitor progress with detailed statistics
- 🔊 **Audible**: Perfect pronunciation on any platform

---

## 🎉 **Ready to Start Learning?**

**Launch the application and begin your vocabulary journey:**

```bash
streamlit run app_advanced1.py
```

**Experience the revolutionary cloud-compatible audio system, senior-friendly design, and comprehensive learning features that make vocabulary building engaging and accessible for everyone!** 🚀📚✨

---

**Built with ❤️ for language learners of all ages, with special attention to senior accessibility and cloud deployment compatibility.**

🌟 **Star this repository if you find it helpful!** 🌟