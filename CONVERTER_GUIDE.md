# Vocabulary Converter - User Guide

## 📋 Overview
I've created three vocabulary conversion utilities for your project:

## 🛠️ Available Converters

### 1. `simple_converter.py` (Basic, No Dependencies)
- **Features**: JSON ↔ CSV conversion
- **Dependencies**: None (uses built-in Python modules)
- **Best for**: Basic conversions, environments without pandas

### 2. `json_excel_converter.py` (Full-Featured)
- **Features**: JSON ↔ Excel with advanced formatting
- **Dependencies**: pandas, openpyxl
- **Best for**: Professional Excel output with auto-sized columns

### 3. `vocab_converter.py` (Comprehensive)
- **Features**: Auto-detects format, supports all conversions
- **Dependencies**: pandas, openpyxl (optional - falls back to CSV)
- **Best for**: Interactive use, batch processing

## 🚀 Usage Examples

### Quick Conversions
```bash
# Convert level1.json to Excel
python -c "from vocab_converter import VocabularyConverter; VocabularyConverter().json_to_excel('level1.json')"

# Convert all level files at once
python -c "from vocab_converter import VocabularyConverter; VocabularyConverter().batch_convert_levels()"

# Interactive mode
python vocab_converter.py
```

### File Formats Supported

#### Input JSON Structure
```json
{
  "category": [
    {
      "word": "Example",
      "meaning": "A sample or illustration",
      "phrase": "This is an example sentence.",
      "expressions": ["For example", "As an example"],
      "video": "media/example.mp4"
    }
  ]
}
```

#### Output CSV/Excel Structure
| Category | Word | Meaning | Phrase | Expressions | Media |
|----------|------|---------|--------|-------------|--------|
| general | Example | A sample... | This is... | For example; As an example | media/example.mp4 |

## ✅ Test Results

Successfully converted your vocabulary files:

### Level 1 (level1.json)
- **Words**: 241 total
- **Categories**: 8 (general, science, business, literature, travel, history, geography, health)
- **Output**: level1.csv, level1.xlsx

### Level 2 (level2.json)
- **Words**: 240 total
- **Categories**: 8
- **Output**: level2.csv, level2.xlsx

### Level 3 (level3.json)
- **Words**: 240 total
- **Categories**: 8
- **Output**: level3.csv, level3.xlsx

## 🔄 Conversion Features

### JSON → Excel/CSV
- ✅ Preserves all data fields
- ✅ Handles expressions arrays (joins with semicolons)
- ✅ Supports both 'video' and 'media' fields
- ✅ Auto-sized Excel columns
- ✅ UTF-8 encoding support (handles Korean filenames)

### Excel/CSV → JSON
- ✅ Recreates nested JSON structure
- ✅ Splits expressions back into arrays
- ✅ Groups by categories
- ✅ Validates data integrity

## 📊 Excel Features
- **Auto-sized columns** for better readability
- **Formatted headers** with proper column names
- **UTF-8 encoding** for international characters
- **Single worksheet** named "Vocabulary"

## 🔧 Technical Notes

### Dependencies Installation
```bash
pip install pandas openpyxl
```

### Error Handling
- File format auto-detection
- Graceful fallback to CSV if Excel libraries unavailable
- UTF-8 encoding for international characters
- Validation of data structure

## 📁 File Management
- **Auto-naming**: If no output filename specified, creates logical names
- **Backup-safe**: Never overwrites original JSON files
- **Batch processing**: Can convert multiple files at once

## 🎯 Use Cases

1. **Data Analysis**: Open vocabulary data in Excel for analysis
2. **Editing**: Bulk edit vocabulary in spreadsheet, convert back to JSON
3. **Sharing**: Send CSV/Excel files to non-technical users
4. **Backup**: Create readable backups of vocabulary data
5. **Import/Export**: Interface with other vocabulary management tools

## 🚨 Important Notes

- **Expressions field**: Multiple expressions are joined with semicolons (`;`)
- **Media paths**: Both `video` and `media` fields are supported
- **Category preservation**: Original category structure is maintained
- **Data validation**: Checks for required fields and proper structure

Your vocabulary conversion system is now ready for production use! 🎉