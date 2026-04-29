# 🤖 AI Projects Portfolio

Welcome to my AI/ML projects repository! This contains projects completed during my internship.

## 📂 Projects

### 1. 🛍️ Customer Support AI System
An AI-powered system that processes customer messages and provides:
- **Message Classification**: Complaint, Refund/Return, Sales Inquiry, Delivery Question, Account/Technical Issue, General Query, Spam
- **Sentiment Analysis**: Positive, Neutral, Negative
- **Auto-reply Generation**: Professional responses
- **Tech Stack**: Python, Flask, Groq API, Transformers

### 2. 🔊 Text-to-Speech (TTS) Voice Agent
Multilingual TTS system that converts text from multiple sources:
- **Input Types**: Plain text, PDF, Word documents, Images (OCR)
- **Output Languages**: English and Urdu speech
- **Tech Stack**: Python, Flask, gTTS, pyttsx3, Tesseract OCR, PyPDF2

### 3. 🏠 AI Room Redesign System
Complete 5-member AI pipeline for interior design with REAL generated samples:
- **01-depth-estimation**: Depth map generation (MiDaS)
- **02-segmentation**: Object segmentation (DeepLabV3)
- **03-prompt-engineering**: Prompt engineering (6 styles)
- **04-image-generation**: Image generation (Stable Diffusion + ControlNet)
- **05-web-interface**: Flask web interface
- **✅ REAL RESULTS**: 14 images + 3 videos in `/data/outputs/`

### 4. 🎤 Urdu Offline Speech-to-Text System
A real-time, fully offline Urdu speech recognition system with beautiful dark-themed GUI.

**Features:**
- 🎙️ **Continuous Recording**: Never stops until you click Stop
- 🔄 **Real-time Transcription**: Live partial results while speaking
- 🗣️ **Urdu Language Support**: Proper RTL rendering
- ✅ **Two-Panel Interface**: Live output + Final results with timestamps
- 📁 **Session Logging**: Automatic saving to log files
- ⚡ **Fast Performance**: 3-second audio chunks with 50% overlap

**Tech Stack:** OpenAI Whisper, Python, Tkinter, PyAudio, static-ffmpeg

**Location:** [`/offline-stt-system/`](./offline-stt-system/)

**Quick Start:**
```bash
cd offline-stt-system
pip install -r requirements.txt
python stt_ui_perfect_fixed.py

Screenshot Preview:
┌─────────────────────────────────────┐
│  🎤 Urdu Speech-to-Text System      │
├──────────────┬──────────────────────┤
│ Live Output  │ Final Results        │
│ 🔄 ...       │ [12:30] آپ کا نام    │
│              │ [12:31] آپ سکول جاتے │
└──────────────┴──────────────────────┘

Sample Output:
[15:33:11] اب کہا سے آرہی ہے
[15:33:18] اب کا ب آئے ہیں
[15:33:25] آپ کا نام کیا
[15:33:52] آپ قاب آئے ہیں
[15:33:59] آپ سکول جاتے ہیں

👨‍💻 Author
Muhammad Latif - Computer Systems Engineer

📄 License
MIT License

## 5. AI Room Transformation System 🏠✨

**Description:**  
45-60 second vertical AI video showing a dirty room transforming into a clean modern room. Maintains consistent camera angle, layout, and lighting throughout to achieve realistic footage without AI glitches.

**Tech Stack:** Bing Image Creator, Pika, CapCut

**Key Features:**
- Anchor frame method for layout consistency
- Progressive 4-stage video clips (dirty → slightly clean → half clean → fully clean)
- Smooth dissolve transitions and background music
- Realistic dust fading and cleaning progression

**Files:** Anchor images, 4 video clips, final MP4, prompts used, workflow summary
