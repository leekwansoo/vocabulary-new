"""
Simple JSON to CSV/Excel Converter for Vocabulary Builder
Uses built-in csv module (no external dependencies)
"""
import json
import csv
import os

class SimpleVocabularyConverter:
    def json_to_csv(self, json_file, csv_file=None):
        """
        Convert JSON vocabulary file to CSV format
        
        Args:
            json_file (str): Path to JSON file
            csv_file (str): Path to output CSV file (optional)
            
        Returns:
            str: Path to created CSV file
        """
        try:
            # Generate CSV filename if not provided
            if csv_file is None:
                base_name = os.path.splitext(json_file)[0]
                csv_file = f"{base_name}.csv"
            
            # Load JSON data
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Prepare CSV data
            rows = []
            headers = ['Category', 'Word', 'Meaning', 'Phrase', 'Expressions', 'Media']
            
            for category, words in data.items():
                for word_entry in words:
                    # Handle expressions list - join with semicolon
                    expressions = word_entry.get('expressions', [])
                    expressions_str = '; '.join(expressions) if expressions else ''
                    
                    row = [
                        category,
                        word_entry.get('word', ''),
                        word_entry.get('meaning', ''),
                        word_entry.get('phrase', ''),
                        expressions_str,
                        word_entry.get('video', word_entry.get('media', ''))  # Handle both 'video' and 'media' fields
                    ]
                    rows.append(row)
            
            # Write to CSV
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            
            print(f"✅ Successfully converted {json_file} to {csv_file}")
            print(f"📊 Total words converted: {len(rows)}")
            print(f"📂 Categories: {list(data.keys())}")
            
            return csv_file
            
        except Exception as e:
            print(f"❌ Error converting JSON to CSV: {e}")
            return None
    
    def csv_to_json(self, csv_file, json_file=None):
        """
        Convert CSV vocabulary file to JSON format
        
        Args:
            csv_file (str): Path to CSV file
            json_file (str): Path to output JSON file (optional)
            
        Returns:
            str: Path to created JSON file
        """
        try:
            # Generate JSON filename if not provided
            if json_file is None:
                base_name = os.path.splitext(csv_file)[0]
                json_file = f"{base_name}_converted.json"
            
            # Read CSV file
            data = {}
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    category = row.get('Category', 'general').lower()
                    
                    # Parse expressions back to list
                    expressions_str = row.get('Expressions', '')
                    expressions = []
                    if expressions_str:
                        expressions = [expr.strip() for expr in expressions_str.split(';') if expr.strip()]
                    
                    word_entry = {
                        'word': row.get('Word', ''),
                        'meaning': row.get('Meaning', ''),
                        'phrase': row.get('Phrase', ''),
                        'expressions': expressions,
                        'video': row.get('Media', '')
                    }
                    
                    # Initialize category if it doesn't exist
                    if category not in data:
                        data[category] = []
                    
                    data[category].append(word_entry)
            
            # Save to JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully converted {csv_file} to {json_file}")
            print(f"📂 Categories: {list(data.keys())}")
            
            return json_file
            
        except Exception as e:
            print(f"❌ Error converting CSV to JSON: {e}")
            return None
    
    def show_preview(self, json_file, num_items=5):
        """
        Show a preview of the JSON file structure
        
        Args:
            json_file (str): Path to JSON file
            num_items (int): Number of items to preview per category
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n📋 Preview of {json_file}")
            print("=" * 50)
            
            total_words = 0
            for category, words in data.items():
                total_words += len(words)
                print(f"\n📂 Category: {category.upper()} ({len(words)} words)")
                print("-" * 30)
                
                # Show first few items
                for i, word in enumerate(words[:num_items]):
                    print(f"  {i+1}. {word.get('word', '')}")
                    print(f"     Meaning: {word.get('meaning', '')[:80]}{'...' if len(word.get('meaning', '')) > 80 else ''}")
                    print(f"     Media: {word.get('video', word.get('media', 'None'))}")
                    
                if len(words) > num_items:
                    print(f"     ... and {len(words) - num_items} more words")
            
            print(f"\n📊 Total: {total_words} words across {len(data)} categories")
            
        except Exception as e:
            print(f"❌ Error reading JSON file: {e}")

def main():
    """Test the converter with level1.json"""
    converter = SimpleVocabularyConverter()
    
    print("🔄 Simple Vocabulary JSON-CSV Converter")
    print("=" * 40)
    
    # Test with level1.json
    json_file = "level1.json"
    
    if os.path.exists(json_file):
        print(f"\n📋 Found {json_file}")
        
        # Show preview
        converter.show_preview(json_file, 3)
        
        # Convert to CSV
        print(f"\n🔄 Converting {json_file} to CSV...")
        csv_result = converter.json_to_csv(json_file)
        
        if csv_result:
            print(f"\n✅ Conversion complete!")
            print(f"📁 CSV file created: {csv_result}")
            print(f"\nYou can now open {csv_result} in Excel or any spreadsheet application.")
            
            # Ask if user wants to convert back to test
            test_back = input("\nWould you like to test converting back to JSON? (y/n): ").lower().strip()
            if test_back == 'y':
                test_json = converter.csv_to_json(csv_result, "level1_test.json")
                if test_json:
                    print(f"✅ Test conversion back to JSON complete: {test_json}")
    else:
        print(f"❌ {json_file} not found in current directory")
        
        # Show available JSON files
        json_files = [f for f in os.listdir('.') if f.endswith('.json')]
        if json_files:
            print(f"\n📁 Available JSON files:")
            for i, f in enumerate(json_files, 1):
                print(f"  {i}. {f}")
        
        # Allow manual selection
        manual_file = input("\nEnter JSON filename to convert: ").strip()
        if manual_file and os.path.exists(manual_file):
            converter.show_preview(manual_file, 3)
            converter.json_to_csv(manual_file)

if __name__ == "__main__":
    main()