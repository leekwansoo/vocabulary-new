"""
Complete Vocabulary Converter
Supports JSON ↔ Excel ↔ CSV conversions
"""
import os
import pandas as pd
import json
import csv

from datetime import datetime

# Try to import advanced Excel support
EXCEL_SUPPORT = True
print("📊 Excel support enabled (pandas available)")

class VocabularyConverter:
    def __init__(self):
        self.supported_formats = ['.json', '.csv']
        if EXCEL_SUPPORT:
            self.supported_formats.extend(['.xlsx', '.xls'])
    
    def json_to_csv(self, json_file, csv_file=None):
        """Convert JSON to CSV (always available)"""
        if csv_file is None:
            base_name = os.path.splitext(json_file)[0]
            csv_file = f"{base_name}.csv"
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            rows = []
            headers = ['Category', 'Word', 'Meaning', 'Phrase', 'Expressions', 'Media']
            
            for category, words in data.items():
                for word_entry in words:
                    expressions = word_entry.get('expressions', [])
                    expressions_str = '; '.join(expressions) if expressions else ''
                    
                    row = [
                        category,
                        word_entry.get('word', ''),
                        word_entry.get('meaning', ''),
                        word_entry.get('phrase', ''),
                        expressions_str,
                        word_entry.get('video', word_entry.get('media', ''))
                    ]
                    rows.append(row)
            
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            
            print(f"✅ JSON → CSV: {json_file} → {csv_file}")
            print(f"📊 Converted {len(rows)} words")
            return csv_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def csv_to_json(self, csv_file, json_file=None):
        """Convert CSV to JSON (always available)"""
        if json_file is None:
            base_name = os.path.splitext(csv_file)[0]
            json_file = f"{base_name}_from_csv.json"
        
        try:
            data = {}
            
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                for row in reader:
                    category = row.get('Category', 'general').lower()
                    expressions_str = row.get('Expressions', '')
                    expressions = [expr.strip() for expr in expressions_str.split(';') if expr.strip()] if expressions_str else []
                    
                    word_entry = {
                        'word': row.get('Word', ''),
                        'meaning': row.get('Meaning', ''),
                        'phrase': row.get('Phrase', ''),
                        'expressions': expressions,
                        'video': row.get('Media', '')
                    }
                    
                    if category not in data:
                        data[category] = []
                    data[category].append(word_entry)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ CSV → JSON: {csv_file} → {json_file}")
            return json_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def json_to_excel(self, json_file, excel_file=None):
        """Convert JSON to Excel (requires pandas)"""
        if not EXCEL_SUPPORT:
            print("❌ Excel support not available. Use CSV format instead.")
            return self.json_to_csv(json_file, csv_file=excel_file.replace('.xlsx', '.csv') if excel_file else None)
        
        if excel_file is None:
            base_name = os.path.splitext(json_file)[0]
            excel_file = f"{base_name}.xlsx"
        
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            rows = []
            for category, words in data.items():
                for word_entry in words:
                    expressions = word_entry.get('expressions', [])
                    expressions_str = '; '.join(expressions) if expressions else ''
                    
                    row = {
                        'Category': category,
                        'Word': word_entry.get('word', ''),
                        'Meaning': word_entry.get('meaning', ''),
                        'Phrase': word_entry.get('phrase', ''),
                        'Expressions': expressions_str,
                        'Media': word_entry.get('video', word_entry.get('media', ''))
                    }
                    rows.append(row)
            
            df = pd.DataFrame(rows)
            
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
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            print(f"✅ JSON → Excel: {json_file} → {excel_file}")
            print(f"📊 Converted {len(rows)} words")
            return excel_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def excel_to_json(self, excel_file, json_file=None):
        """Convert Excel to JSON (requires pandas)"""
        if not EXCEL_SUPPORT:
            print("❌ Excel support not available. Convert to CSV first.")
            return None
        
        if json_file is None:
            base_name = os.path.splitext(excel_file)[0]
            json_file = f"{base_name}_from_excel.json"
        
        try:
            df = pd.read_excel(excel_file, sheet_name='Vocabulary')
            
            data = {}
            for _, row in df.iterrows():
                category = row.get('Category', 'general').lower()
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
                
                if category not in data:
                    data[category] = []
                data[category].append(word_entry)
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Excel → JSON: {excel_file} → {json_file}")
            return json_file
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def convert_auto(self, input_file, output_format=None):
        """Auto-detect input format and convert"""
        input_ext = os.path.splitext(input_file)[1].lower()
        base_name = os.path.splitext(input_file)[0]
        
        if output_format is None:
            # Default conversions
            if input_ext == '.json':
                output_format = '.xlsx' if EXCEL_SUPPORT else '.csv'
            elif input_ext in ['.xlsx', '.xls']:
                output_format = '.json'
            elif input_ext == '.csv':
                output_format = '.json'
            else:
                print(f"❌ Unsupported format: {input_ext}")
                return None
        
        output_file = f"{base_name}{output_format}"
        
        # Perform conversion
        if input_ext == '.json' and output_format == '.csv':
            return self.json_to_csv(input_file, output_file)
        elif input_ext == '.json' and output_format in ['.xlsx', '.xls']:
            return self.json_to_excel(input_file, output_file)
        elif input_ext == '.csv' and output_format == '.json':
            return self.csv_to_json(input_file, output_file)
        elif input_ext in ['.xlsx', '.xls'] and output_format == '.json':
            return self.excel_to_json(input_file, output_file)
        else:
            print(f"❌ Conversion {input_ext} → {output_format} not supported")
            return None
    
    def batch_convert_levels(self):
        """Convert all level files in current directory"""
        level_files = ['level1.json', 'level2.json', 'level3.json']
        converted = []
        
        for level_file in level_files:
            if os.path.exists(level_file):
                print(f"\n🔄 Processing {level_file}...")
                
                # Convert to both CSV and Excel (if available)
                csv_result = self.json_to_csv(level_file)
                if csv_result:
                    converted.append(csv_result)
                
                if EXCEL_SUPPORT:
                    excel_result = self.json_to_excel(level_file)
                    if excel_result:
                        converted.append(excel_result)
            else:
                print(f"⚠️ {level_file} not found")
        
        return converted

def main():
    """Interactive main function"""
    converter = VocabularyConverter()
    
    print("🔄 Vocabulary Format Converter")
    print("=" * 40)
    print(f"📁 Supported formats: {', '.join(converter.supported_formats)}")
    
    while True:
        print(f"\nOptions:")
        print("1. Convert single file (auto-detect)")
        print("2. JSON → CSV")
        print("3. CSV → JSON")
        if EXCEL_SUPPORT:
            print("4. JSON → Excel")
            print("5. Excel → JSON")
        print("6. Convert all level files")
        print("7. Quick test with level1.json")
        print("0. Exit")
        
        choice = input(f"\nChoose option (0-{7 if EXCEL_SUPPORT else 6}): ").strip()
        
        if choice == '0':
            break
        elif choice == '1':
            file_path = input("Enter file path: ").strip()
            if os.path.exists(file_path):
                converter.convert_auto(file_path)
            else:
                print("❌ File not found")
        elif choice == '2':
            json_file = input("Enter JSON file path: ").strip()
            if os.path.exists(json_file):
                converter.json_to_csv(json_file)
            else:
                print("❌ File not found")
        elif choice == '3':
            csv_file = input("Enter CSV file path: ").strip()
            if os.path.exists(csv_file):
                converter.csv_to_json(csv_file)
            else:
                print("❌ File not found")
        elif choice == '4' and EXCEL_SUPPORT:
            json_file = input("Enter JSON file path: ").strip()
            if os.path.exists(json_file):
                converter.json_to_excel(json_file)
            else:
                print("❌ File not found")
        elif choice == '5' and EXCEL_SUPPORT:
            excel_file = input("Enter Excel file path: ").strip()
            if os.path.exists(excel_file):
                converter.excel_to_json(excel_file)
            else:
                print("❌ File not found")
        elif choice == '6':
            print("\n🔄 Converting all level files...")
            results = converter.batch_convert_levels()
            print(f"\n✅ Converted {len(results)} files")
        elif choice == '7':
            if os.path.exists('level1.json'):
                print("\n🧪 Testing with level1.json...")
                converter.convert_auto('level1.json')
            else:
                print("❌ level1.json not found")
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()
