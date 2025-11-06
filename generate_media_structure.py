import json
import os
import re

def sanitize_filename(text):
    """Convert text to a safe filename"""
    # Remove or replace unsafe characters
    safe_text = re.sub(r'[<>:"/\\|?*]', '', text)
    safe_text = re.sub(r'[^\w\s-]', '', safe_text)
    safe_text = re.sub(r'[-\s]+', '_', safe_text)
    return safe_text.strip('_').lower()

def update_word_pools_with_media():
    """Update word_pools.json to include media fields"""
    
    # Read the current word_pools.json
    with open('word_pools.json', 'r', encoding='utf-8') as f:
        word_pools = json.load(f)
    
    # Create media directory if it doesn't exist
    media_dir = 'media'
    if not os.path.exists(media_dir):
        os.makedirs(media_dir)
    
    # Create subdirectories for each category
    for category in word_pools.keys():
        category_dir = os.path.join(media_dir, category)
        if not os.path.exists(category_dir):
            os.makedirs(category_dir)
    
    # Update each word entry with media field
    for category, words in word_pools.items():
        for word_entry in words:
            word = word_entry['word']
            phrase = word_entry['phrase']
            
            # Generate filename based on word and phrase
            filename = f"{sanitize_filename(word)}_{sanitize_filename(phrase[:50])}.jpg"
            media_path = f"media/{category}/{filename}"
            
            # Add media field
            word_entry['media'] = media_path
            
            print(f"Added media field for {word}: {media_path}")
    
    # Save updated word_pools.json
    with open('word_pools_with_media.json', 'w', encoding='utf-8') as f:
        json.dump(word_pools, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated word_pools saved as 'word_pools_with_media.json'")
    print(f"Created media directory structure in '{media_dir}'")
    
    return word_pools

def generate_image_generation_prompts():
    """Generate prompts for AI image generation"""
    
    with open('word_pools.json', 'r', encoding='utf-8') as f:
        word_pools = json.load(f)
    
    prompts = []
    
    for category, words in word_pools.items():
        for word_entry in words:
            word = word_entry['word']
            phrase = word_entry['phrase']
            meaning = word_entry['meaning']
            
            # Create a descriptive prompt for image generation
            prompt = f"Create a visual representation of: '{phrase}'. The image should illustrate the word '{word}' which means '{meaning}'. Style: clean, educational, suitable for vocabulary learning. Avoid text in the image."
            
            filename = f"{sanitize_filename(word)}_{sanitize_filename(phrase[:50])}.jpg"
            
            prompts.append({
                'category': category,
                'word': word,
                'phrase': phrase,
                'meaning': meaning,
                'filename': filename,
                'prompt': prompt,
                'media_path': f"media/{category}/{filename}"
            })
    
    # Save prompts to a file
    with open('image_generation_prompts.json', 'w', encoding='utf-8') as f:
        json.dump(prompts, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(prompts)} image generation prompts")
    print("Saved to 'image_generation_prompts.json'")
    
    return prompts

if __name__ == "__main__":
    print("Updating word pools with media structure...")
    word_pools = update_word_pools_with_media()
    
    print("\nGenerating image generation prompts...")
    prompts = generate_image_generation_prompts()
    
    print(f"\nTotal words processed: {sum(len(words) for words in word_pools.values())}")
    print("\nNext steps:")
    print("1. Use the prompts in 'image_generation_prompts.json' with an AI image generator")
    print("2. Save generated images to the corresponding media paths")
    print("3. Replace 'word_pools.json' with 'word_pools_with_media.json'")