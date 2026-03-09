"""
Working Urdu STT Engine - Captures All Transcriptions
"""

# FFmpeg fix
try:
    import static_ffmpeg
    static_ffmpeg.add_paths()
except:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "static-ffmpeg"])
    import static_ffmpeg
    static_ffmpeg.add_paths()

import whisper
import time
import os
import pyaudio
import wave
import threading
import numpy as np
from datetime import datetime

class WorkingUrduSTTEngine:
    def __init__(self, model_size="tiny", language="ur"):
        self.model_size = model_size
        self.language = language
        self.model = None
        self.is_recording = False
        self.recording_thread = None
        self.transcriptions = []  # All transcriptions
        self.last_transcription_time = 0
        
        # Session
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def initialize(self):
        """Initialize engine"""
        print("✅ Engine initialized")
        return True
    
    def load_model(self):
        """Load Whisper model"""
        print(f"Loading Whisper {self.model_size}...")
        start = time.time()
        self.model = whisper.load_model(self.model_size)
        load_time = time.time() - start
        print(f"✅ Model loaded in {load_time:.2f}s")
        return True
    
    def start_streaming(self):
        """Start continuous recording"""
        if self.is_recording:
            print("⚠️ Already recording")
            return
        
        print("🎤 Starting recording...")
        self.is_recording = True
        self.transcriptions = []  # Clear previous transcriptions
        self.last_transcription_time = 0
        self.recording_thread = threading.Thread(target=self._record_loop)
        self.recording_thread.daemon = True
        self.recording_thread.start()
        print("🎤 Recording thread started")
        return True
    
    def _record_loop(self):
        """Main recording loop"""
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 1024
        RECORD_SECONDS = 3
        
        p = pyaudio.PyAudio()
        
        while self.is_recording:
            try:
                frames = []
                stream = p.open(
                    format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK
                )
                
                # Record for RECORD_SECONDS
                for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                    if not self.is_recording:
                        break
                    data = stream.read(CHUNK, exception_on_overflow=False)
                    frames.append(data)
                
                stream.stop_stream()
                stream.close()
                
                if not self.is_recording or len(frames) == 0:
                    continue
                
                # Process the recorded audio
                self._process_audio(frames, p.get_sample_size(FORMAT), FORMAT, CHANNELS, RATE)
                
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(0.1)
        
        p.terminate()
        print("🛑 Recording stopped")
    
    def _has_audio(self, frames, sample_width):
        """Check if audio has actual sound"""
        audio_data = np.frombuffer(b''.join(frames), dtype=np.int16)
        rms = np.sqrt(np.mean(audio_data.astype(np.float32)**2))
        return rms > 300  # Lower threshold to catch quieter speech
    
    def _process_audio(self, frames, sample_width, format, channels, rate):
        """Process recorded audio"""
        temp_file = f"temp_{int(time.time())}.wav"
        
        try:
            # Check if there's actual audio
            if not self._has_audio(frames, sample_width):
                return
            
            # Save to WAV file
            wf = wave.open(temp_file, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(sample_width)
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))
            wf.close()
            
            # Transcribe
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 1000:
                result = self.model.transcribe(temp_file, language=self.language)
                text = result['text'].strip()
                
                # Only add if it's not empty and has some meaningful content
                if text and len(text) > 1:
                    # Check if it's different from the last transcription
                    current_time = time.time()
                    
                    # Always add if it's been more than 2 seconds since last transcription
                    # or if it's significantly different
                    time_diff = current_time - self.last_transcription_time
                    
                    if (time_diff > 2.0 or 
                        not self.transcriptions or 
                        text != self.transcriptions[-1]['text']):
                        
                        self.transcriptions.append({
                            "timestamp": datetime.now().isoformat(),
                            "text": text
                        })
                        self.last_transcription_time = current_time
                        print(f"✅ {text}")
                    else:
                        # Just show in console but don't add duplicate
                        print(f"🔄 (duplicate skipped) {text}")
            
        except Exception as e:
            print(f"⚠️ Transcription error: {e}")
        
        finally:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except:
                pass
    
    def stop_streaming(self):
        """Stop recording"""
        print("⏹️ Stopping recording...")
        self.is_recording = False
        
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join(timeout=2.0)
        
        print(f"📊 Total transcriptions: {len(self.transcriptions)}")
        for i, t in enumerate(self.transcriptions, 1):
            print(f"  {i}. {t['text']}")
        
        return True
    
    def get_statistics(self):
        return {"total": len(self.transcriptions)}