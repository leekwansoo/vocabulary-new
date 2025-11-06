# Image Generation Guide for Vocabulary Learning

This guide will help you generate images for your vocabulary learning app using AI image generation services.

## What We've Created

1. **Updated word_pools.json**: Now includes "media" field for each word entry
2. **Media directory structure**: Organized by category (general, science, business, etc.)
3. **160 placeholder images**: Colored rectangles with word names
4. **image_generation_prompts.json**: Contains optimized prompts for AI image generation

## Generated Files Structure

```
media/
├── general/
├── science/
├── business/
├── literature/
├── travel/
├── history/
├── geography/
└── health/
```

Each category contains .jpg files for every word's phrase.

## How to Generate Real Images

### Option 1: OpenAI DALL-E 3 (Recommended)

1. **Get API Key**: Visit https://platform.openai.com/api-keys
2. **Install Dependencies**:
   ```bash
   pip install requests pillow openai
   ```
3. **Generate Images**:
   ```bash
   # Generate all images (160 total - costs ~$160)
   python generate_images.py --api-key YOUR_OPENAI_KEY
   
   # Generate first 10 images for testing ($10)
   python generate_images.py --api-key YOUR_OPENAI_KEY --max-images 10
   ```

### Option 2: Free Alternatives

#### Stable Diffusion (Free, Local)
1. Install Stable Diffusion WebUI
2. Use the prompts from `image_generation_prompts.json`
3. Batch generate using the API

#### Microsoft Bing Image Creator (Free, Limited)
1. Visit https://www.bing.com/images/create
2. Use prompts from the JSON file
3. Download and rename images manually

#### Leonardo.AI (Free Tier Available)
1. Sign up at https://leonardo.ai
2. Use their API or web interface
3. 150 free generations per day

### Option 3: Batch Processing Script

Here's a simplified script for batch processing with any API:

```python
import json
import requests
import time

def batch_generate_images():
    with open('image_generation_prompts.json', 'r') as f:
        prompts = json.load(f)
    
    for prompt_data in prompts:
        print(f"Generate: {prompt_data['word']}")
        print(f"Prompt: {prompt_data['prompt']}")
        print(f"Save as: {prompt_data['media_path']}")
        print("-" * 50)
        
        # Add your image generation API call here
        # Example for different services:
        
        # For Stable Diffusion API:
        # response = requests.post('http://localhost:7860/api/v1/txt2img', ...)
        
        # For other APIs:
        # response = requests.post('API_ENDPOINT', headers=headers, json=data)
        
        # Save the generated image to prompt_data['media_path']

if __name__ == "__main__":
    batch_generate_images()
```

## Image Requirements

- **Format**: JPEG (.jpg)
- **Size**: 800x600 pixels or larger
- **Style**: Clean, educational, suitable for vocabulary learning
- **Content**: Visual representation of the phrase, not just the word
- **No Text**: Avoid including text in the images

## Sample Prompts

Here are some example prompts from our generated list:

1. **Serendipity**: "Create a visual representation of: 'It was pure serendipity that I met my best friend at the coffee shop.' The image should illustrate the word 'Serendipity' which means 'A pleasant surprise; finding something good without looking for it'. Style: clean, educational, suitable for vocabulary learning. Avoid text in the image."

2. **Photosynthesis**: "Create a visual representation of: 'Photosynthesis is essential for life on Earth.' The image should illustrate the word 'Photosynthesis' which means 'The process by which plants make food using sunlight'. Style: clean, educational, suitable for vocabulary learning. Avoid text in the image."

## Cost Analysis

### OpenAI DALL-E 3
- Price: ~$0.04 per image (1024x1024)
- Total cost for 160 images: ~$6.40
- High quality, consistent style

### Other Services
- Midjourney: ~$10/month for 200 images
- Leonardo.AI: Free tier (150/day), then paid
- Stable Diffusion: Free (requires local setup)

## Next Steps

1. Choose your image generation method
2. Generate a few test images to verify quality
3. Run the full batch generation
4. Update your vocabulary app to use the new media files
5. Test the app with the new images

## Troubleshooting

- **Images not loading**: Check file paths in word_pools.json
- **Poor quality**: Adjust prompts for better descriptions
- **Wrong style**: Add more specific style instructions to prompts
- **API errors**: Check rate limits and API key validity

## Integration with Your App

The updated word_pools.json now includes media paths. Update your app to display images:

```python
# Example usage in your app
import json

with open('word_pools.json', 'r') as f:
    word_pools = json.load(f)

for category, words in word_pools.items():
    for word_entry in words:
        word = word_entry['word']
        meaning = word_entry['meaning']
        phrase = word_entry['phrase']
        media_path = word_entry['media']  # New field!
        
        # Display image using media_path
        # display_image(media_path)
```

Happy vocabulary learning! 🎓✨