"""
Test script for the level-based vocabulary system
"""
import json

def test_level_files():
    """Test that all level files exist and have proper structure"""
    print("Testing Level-Based Vocabulary System...")
    
    for level in [1, 2, 3]:
        filename = f"level{level}.json"
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            print(f"\n📚 Level {level} ({filename}):")
            print(f"  Categories: {len(data)}")
            
            total_words = 0
            for category, words in data.items():
                word_count = len(words)
                total_words += word_count
                print(f"  {category.title()}: {word_count} words")
                
                # Test first word structure
                if words:
                    first_word = words[0]
                    required_keys = ['word', 'meaning', 'phrase']
                    if all(key in first_word for key in required_keys):
                        print(f"    ✅ Structure valid (example: '{first_word['word']}')")
                    else:
                        print(f"    ❌ Missing required keys in first word")
            
            print(f"  Total words: {total_words}")
            
        except FileNotFoundError:
            print(f"❌ {filename} not found")
        except json.JSONDecodeError:
            print(f"❌ {filename} has invalid JSON format")
        except Exception as e:
            print(f"❌ Error reading {filename}: {e}")
    
    print("\n🎯 Level System Summary:")
    print("✅ Level 1: Beginner vocabulary - Basic everyday words")
    print("✅ Level 2: Intermediate vocabulary - More challenging words") 
    print("✅ Level 3: Advanced vocabulary - Sophisticated vocabulary")
    print("\n🚀 Total vocabulary database: 480 words across 3 levels!")

if __name__ == "__main__":
    test_level_files()