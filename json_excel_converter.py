"""
JSON to Excel Converter for Vocabulary Builder
Converts vocabulary JSON files to Excel format and vice versa
"""
import json
import pandas as pd
import os
from datetime import datetime

class VocabularyConverter:
    def __init__(self):
        self.supported_formats = ['.json', '.xlsx', '.xls']
    
    def json_to_excel(self, json_file, excel_file=None):
        """
        Convert JSON vocabulary file to Excel format
        
        Args:
            json_file (str): Path to JSON file
            excel_file (str): Path to output Excel file (optional)
            
        Returns:
            str: Path to created Excel file
        """
        try:
            # Generate Excel filename if not provided
            if excel_file is None:
                base_name = os.path.splitext(json_file)[0]
                excel_file = f"{base_name}.xlsx"
            
            # Load JSON data
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert to flat structure for Excel
            rows = []
            for category, words in data.items():
                for word_entry in words:
                    # Handle expressions list - join with semicolon
                    expressions = word_entry.get('expressions', [])
                    expressions_str = '; '.join(expressions) if expressions else ''
                    
                    row = {
                        'Category': category,
                        'Word': word_entry.get('word', ''),
                        'Meaning': word_entry.get('meaning', ''),
                        'Phrase': word_entry.get('phrase', ''),
                        'Expressions': expressions_str,
                        'Media': word_entry.get('video', word_entry.get('media', ''))  # Handle both 'video' and 'media' fields
                    }
                    rows.append(row)
            
            # Create DataFrame
            df = pd.DataFrame(rows)
            
            # Save to Excel with formatting
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Vocabulary', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Vocabulary']
                for column in worksheet.columns:
                    max_length = 0
                    column = [cell for cell in column]
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            print(f"✅ Successfully converted {json_file} to {excel_file}")
            print(f"📊 Total words converted: {len(rows)}")
            print(f"📂 Categories: {list(data.keys())}")
            
            return excel_file
            
        except Exception as e:
            print(f"❌ Error converting JSON to Excel: {e}")
            return None
    
    def excel_to_json(self, excel_file, json_file=None):
        """
        Convert Excel vocabulary file to JSON format
        
        Args:
            excel_file (str): Path to Excel file
            json_file (str): Path to output JSON file (optional)
            
        Returns:
            str: Path to created JSON file
        """
        try:
            # Generate JSON filename if not provided
            if json_file is None:
                base_name = os.path.splitext(excel_file)[0]
                json_file = f"{base_name}.json"
            
            # Read Excel file
            df = pd.read_excel(excel_file, sheet_name='Vocabulary')
            
            # Convert to nested JSON structure
            data = {}
            
            for _, row in df.iterrows():
                category = row.get('Category', 'general').lower()
                
                # Parse expressions back to list
                expressions_str = row.get('Expressions', '')
                expressions = []
                if expressions_str and pd.notna(expressions_str):
                    expressions = [expr.strip() for expr in str(expressions_str).split(';') if expr.strip()]
                
                word_entry = {
                    'word': str(row.get('Word', '')),
                    'meaning': str(row.get('Meaning', '')),
                    'phrase': str(row.get('Phrase', '')),
                    'expressions': expressions,
                    'video': str(row.get('Media', '')) if pd.notna(row.get('Media')) else ''
                }
                
                # Initialize category if it doesn't exist
                if category not in data:
                    data[category] = []
                
                data[category].append(word_entry)
            
            # Save to JSON
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Successfully converted {excel_file} to {json_file}")
            print(f"📊 Total words converted: {len(df)}")
            print(f"📂 Categories: {list(data.keys())}")
            
            return json_file
            
        except Exception as e:
            print(f"❌ Error converting Excel to JSON: {e}")
            return None
    
    def convert_file(self, input_file, output_file=None):
        """
        Auto-detect format and convert accordingly
        
        Args:
            input_file (str): Path to input file
            output_file (str): Path to output file (optional)
            
        Returns:
            str: Path to converted file
        """
        input_ext = os.path.splitext(input_file)[1].lower()
        
        if input_ext == '.json':
            return self.json_to_excel(input_file, output_file)
        elif input_ext in ['.xlsx', '.xls']:
            return self.excel_to_json(input_file, output_file)
        else:
            print(f"❌ Unsupported file format: {input_ext}")
            print(f"📝 Supported formats: {self.supported_formats}")
            return None
    
    def batch_convert(self, directory, input_format, output_format):
        """
        Convert all files of a specific format in a directory
        
        Args:
            directory (str): Directory containing files
            input_format (str): Input format (.json, .xlsx, .xls)
            output_format (str): Output format (.json, .xlsx, .xls)
        """
        converted_files = []
        
        for filename in os.listdir(directory):
            if filename.lower().endswith(input_format):
                input_path = os.path.join(directory, filename)
                base_name = os.path.splitext(filename)[0]
                output_filename = f"{base_name}{output_format}"
                output_path = os.path.join(directory, output_filename)
                
                print(f"\n🔄 Converting {filename}...")
                result = self.convert_file(input_path, output_path)
                if result:
                    converted_files.append(result)
        
        print(f"\n✅ Batch conversion complete!")
        print(f"📁 Converted {len(converted_files)} files")
        return converted_files

def main():
    """Main function for interactive usage"""
    converter = VocabularyConverter()
    
    print("🔄 Vocabulary JSON-Excel Converter")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Convert JSON to Excel")
        print("2. Convert Excel to JSON") 
        print("3. Auto-detect and convert")
        print("4. Batch convert directory")
        print("5. Convert level1.json (quick test)")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-5): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        
        elif choice == '1':
            json_file = input("Enter JSON file path: ").strip()
            excel_file = input("Enter Excel output path (or press Enter for auto): ").strip()
            if not excel_file:
                excel_file = None
            converter.json_to_excel(json_file, excel_file)
        
        elif choice == '2':
            excel_file = input("Enter Excel file path: ").strip()
            json_file = input("Enter JSON output path (or press Enter for auto): ").strip()
            if not json_file:
                json_file = None
            converter.excel_to_json(excel_file, json_file)
        
        elif choice == '3':
            input_file = input("Enter file path: ").strip()
            output_file = input("Enter output path (or press Enter for auto): ").strip()
            if not output_file:
                output_file = None
            converter.convert_file(input_file, output_file)
        
        elif choice == '4':
            directory = input("Enter directory path: ").strip()
            input_format = input("Enter input format (.json, .xlsx, .xls): ").strip()
            output_format = input("Enter output format (.json, .xlsx, .xls): ").strip()
            converter.batch_convert(directory, input_format, output_format)
        
        elif choice == '5':
            # Quick test with level1.json
            level1_path = "level1.json"
            if os.path.exists(level1_path):
                converter.json_to_excel(level1_path)
            else:
                print(f"❌ {level1_path} not found in current directory")
        
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()