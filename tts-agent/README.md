# 🔊 TTS Voice Agent - Text to Speech System

## 📋 Overview
A comprehensive Text-to-Speech system that converts text from multiple sources into natural-sounding speech in **English** and **Urdu**.

## ✨ Features

### Input Types Supported:
- 📝 **Plain Text** - Direct text input
- 📄 **PDF Documents** - Extract and read text from PDFs
- 📃 **Word Documents** - Support for .docx files
- 🖼️ **Images** - OCR text extraction from images
- 📄 **Text Files** - Direct .txt file support

### Output:
- 🔊 **English Speech** - Using Google TTS and offline engine
- 🎙️ **Urdu Speech** - Using Google TTS with Urdu language support
- 💻 **Offline Mode** - English TTS without internet

## 🛠️ Technologies Used
- **Backend**: Python, Flask
- **TTS Engines**: gTTS (online), pyttsx3 (offline)
- **OCR**: Tesseract OCR, OpenCV, PIL
- **Document Processing**: PyPDF2, python-docx
- **Frontend**: HTML5, CSS3, JavaScript

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Muhammadlatifkhan/AI-projects.git
   cd AI-projects/tts-agent

2.Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

3.Install dependencies
pip install -r requirements.txt

4.Install Tesseract OCR

Download from: https://github.com/UB-Mannheim/tesseract/wiki

Install with "Additional language data"

Default path: C:\Program Files\Tesseract-OCR\

5.Run the application
python app.py

6.Open browser
Navigate to: http://localhost:5001

📁 Project Structure
tts-agent/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Web interface
├── static/                # CSS, JS files
├── uploads/               # Temporary uploaded files
└── outputs/               # Generated audio files

🎯 Usage Examples

Plain Text:
	1.Select "Plain Text Input"
	2.Choose language (English/Urdu)
	3.Type or paste text
	4.Click "Convert to Speech"

PDF/Word/Image:
	1.Select "File Upload"
	2.Choose language
	3.Upload file
	4.Click "Process File"

Offline TTS:
	1.Use "Offline TTS" section
	2.Enter English text
	3.Click "Convert Offline"

🌟 Key Features Implemented
	✅ Text cleaning to remove special characters (_ * • etc.)
	✅ Smooth sentence flow (no word-by-word pauses)
	✅ Urdu language support
	✅ OCR text extraction from images
	✅ PDF and Word document parsing
	✅ Online and offline TTS options
	✅ Modern web interface

📊 Performance
	Response Time: 1-3 seconds (online), instant (offline)
	Supported Languages: 2 (English, Urdu)
	File Size Limit: 16MB
	Text Limit: 3000 characters (gTTS limit)

👨‍💻 Author
Muhammad Latif - Computer Systems Engineer

📄 License
MIT License

## **STEP 3: Also update the main README to mention TTS**

```powershell
cd ..
notepad README.md