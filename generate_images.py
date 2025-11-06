import json
import os
import requests
import time
from PIL import Image
import io

def generate_images_with_dalle(api_key=None, max_images=None):
    """
    Generate images using OpenAI's DALL-E API
    
    Args:
        api_key (str): Your OpenAI API key
        max_images (int): Maximum number of images to generate (None for all)
    """
    
    if not api_key:
        print("Error: OpenAI API key is required!")
        print("Get your API key from: https://platform.openai.com/api-keys")
        print("Then run: python generate_images.py --api-key YOUR_KEY")
        return
    
    # Load the prompts
    with open('image_generation_prompts.json', 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    
    if max_images:
        prompts = prompts[:max_images]
    
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    success_count = 0
    error_count = 0
    
    for i, prompt_data in enumerate(prompts, 1):
        try:
            print(f"Generating image {i}/{len(prompts)}: {prompt_data['word']}")
            
            # Prepare the request
            data = {
                "model": "dall-e-3",
                "prompt": prompt_data['prompt'],
                "n": 1,
                "size": "1024x1024",
                "quality": "standard",
                "response_format": "url"
            }
            
            # Make the API request
            response = requests.post(
                'https://api.openai.com/v1/images/generations',
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                
                # Download the image
                img_response = requests.get(image_url, timeout=30)
                if img_response.status_code == 200:
                    # Ensure directory exists
                    os.makedirs(os.path.dirname(prompt_data['media_path']), exist_ok=True)
                    
                    # Save the image
                    with open(prompt_data['media_path'], 'wb') as f:
                        f.write(img_response.content)
                    
                    success_count += 1
                    print(f"✓ Saved: {prompt_data['media_path']}")
                else:
                    print(f"✗ Failed to download image for {prompt_data['word']}")
                    error_count += 1
            else:
                print(f"✗ API error for {prompt_data['word']}: {response.status_code}")
                print(f"Response: {response.text}")
                error_count += 1
            
            # Rate limiting - wait between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"✗ Error generating image for {prompt_data['word']}: {str(e)}")
            error_count += 1
            continue
    
    print(f"\nGeneration complete!")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Total: {len(prompts)}")

def generate_placeholder_images():
    """
    Generate placeholder images for testing (colored rectangles with text)
    """
    print("Generating placeholder images...")
    
    with open('image_generation_prompts.json', 'r', encoding='utf-8') as f:
        prompts = json.load(f)
    
    # Create placeholder images
    from PIL import Image, ImageDraw, ImageFont
    
    for prompt_data in prompts:
        try:
            # Create a colored background
            colors = {
                'general': (70, 130, 180),     # Steel Blue
                'science': (34, 139, 34),      # Forest Green
                'business': (178, 34, 34),     # Fire Brick
                'literature': (128, 0, 128),   # Purple
                'travel': (255, 140, 0),       # Dark Orange
                'history': (139, 69, 19),      # Saddle Brown
                'geography': (0, 128, 128),    # Teal
                'health': (220, 20, 60)        # Crimson
            }
            
            color = colors.get(prompt_data['category'], (128, 128, 128))
            
            # Create image
            img = Image.new('RGB', (800, 600), color)
            draw = ImageDraw.Draw(img)
            
            # Try to use a default font
            try:
                font = ImageFont.truetype("arial.ttf", 40)
                small_font = ImageFont.truetype("arial.ttf", 20)
            except:
                font = ImageFont.load_default()
                small_font = ImageFont.load_default()
            
            # Add text
            word = prompt_data['word']
            category = prompt_data['category'].upper()
            
            # Draw category
            draw.text((50, 50), category, fill='white', font=small_font)
            
            # Draw word (centered)
            bbox = draw.textbbox((0, 0), word, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (800 - text_width) // 2
            y = (600 - text_height) // 2
            draw.text((x, y), word, fill='white', font=font)
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(prompt_data['media_path']), exist_ok=True)
            
            # Save image
            img.save(prompt_data['media_path'], 'JPEG', quality=85)
            
        except Exception as e:
            print(f"Error creating placeholder for {prompt_data['word']}: {str(e)}")
    
    print(f"Generated {len(prompts)} placeholder images")

def update_original_word_pools():
    """
    Update the original word_pools.json with media fields
    """
    print("Updating original word_pools.json...")
    
    # Read the updated version
    with open('word_pools_with_media.json', 'r', encoding='utf-8') as f:
        updated_data = json.load(f)
    
    # Save it as the original
    with open('word_pools.json', 'w', encoding='utf-8') as f:
        json.dump(updated_data, f, indent=2, ensure_ascii=False)
    
    print("✓ Updated word_pools.json with media fields")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate vocabulary learning images')
    parser.add_argument('--api-key', help='OpenAI API key for DALL-E')
    parser.add_argument('--max-images', type=int, help='Maximum number of images to generate')
    parser.add_argument('--placeholder', action='store_true', help='Generate placeholder images instead')
    parser.add_argument('--update-json', action='store_true', help='Update original word_pools.json')
    
    args = parser.parse_args()
    
    if args.update_json:
        update_original_word_pools()
    elif args.placeholder:
        generate_placeholder_images()
    else:
        generate_images_with_dalle(args.api_key, args.max_images)
    
    print("\nUsage examples:")
    print("1. Generate placeholder images: python generate_images.py --placeholder")
    print("2. Generate real images: python generate_images.py --api-key YOUR_OPENAI_KEY")
    print("3. Generate first 10 images: python generate_images.py --api-key YOUR_KEY --max-images 10")
    print("4. Update word_pools.json: python generate_images.py --update-json")