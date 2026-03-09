# 🤖 AI Projects Portfolio

Welcome to my AI/ML projects repository! This contains projects completed during my internship.

## 📂 Projects

### 1. 🛍️ [Customer Support AI System](./customer-support-ai/)
An AI-powered system that processes customer messages and provides:
- **Message Classification**: Complaint, Refund/Return, Sales Inquiry, Delivery Question, Account/Technical Issue, General Query, Spam
- **Sentiment Analysis**: Positive, Neutral, Negative
- **Auto-reply Generation**: Professional responses
- **Tech Stack**: Python, Flask, Groq API, Transformers

### 2. 🔊 [Text-to-Speech (TTS) Voice Agent](./tts-agent/)

Multilingual TTS system that converts text from multiple sources:
- **Input Types**: Plain text, PDF, Word documents, Images (OCR)
- **Output Languages**: English and Urdu speech
- **Tech Stack**: Python, Flask, gTTS, pyttsx3, Tesseract OCR, PyPDF2
- **Multilingual TTS system for English and Urdu speech synthesis.

### 3. 🏠 [AI Room Redesign System](./room-redesign/)
Complete 5-member AI pipeline for interior design with **REAL generated samples**:
- **Member 1**: Depth map generation (MiDaS)
- **Member 2**: Object segmentation (DeepLabV3)
- **Member 3**: Prompt engineering (6 styles)
- **Member 4**: Image generation (Stable Diffusion + ControlNet)
- **Member 5**: Web interface (Flask)
- ✅ **See actual generated images** in the project README

## 🚀 Quick Start

Each project has its own setup instructions in its folder:

```bash
# Example: Run Customer Support AI
cd customer-support-ai
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
📊 Project Stats
done

Technologies: Python, Flask, PyTorch, Transformers, OpenCV, Groq API

Models Used: MiDaS, DeepLabV3, Stable Diffusion, LLaMA

### 4. 🎤 Urdu Offline Speech-to-Text System
A real-time, fully offline Urdu speech recognition system with a beautiful dark-themed GUI.

**Features:**
- 🎙️ Continuous microphone recording (never stops until you click Stop)
- 🔄 Real-time transcription with live partial results
- 🗣️ Urdu language support with proper RTL rendering
- ✅ Final results with timestamps in separate panel
- 📁 Automatic session logging to files
- 🎨 Beautiful dark theme with two-panel interface
- ⚡ Fast performance with 3-second audio chunks

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



👨‍💻 Author
Muhammad Latif - Computer Systems Engineer

📄 License
MIT License
