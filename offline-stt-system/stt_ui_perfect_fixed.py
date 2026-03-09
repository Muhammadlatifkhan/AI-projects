"""
Perfect Urdu STT UI - FIXED VERSION
Based on working minimal UI
"""
import arabic_reshaper
from bidi.algorithm import get_display
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
from datetime import datetime
from phase2_final_engine_working import WorkingUrduSTTEngine

class PerfectUrduSTTUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎤 Urdu Speech-to-Text System")
        self.root.geometry("1200x700")
        
        # Colors
        self.colors = {
            'bg': '#1e1e2e',
            'fg': '#cdd6f4',
            'accent': '#89b4fa',
            'success': '#a6e3a1',
            'error': '#f38ba8',
            'card': '#313244'
        }
        
        self.root.configure(bg=self.colors['bg'])
        
        self.engine = None
        self.is_recording = False
        self.final_results = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main = tk.Frame(self.root, bg=self.colors['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title = tk.Label(main, text="🎤 Urdu Speech-to-Text System",
                        font=('Segoe UI', 24, 'bold'),
                        bg=self.colors['bg'],
                        fg=self.colors['accent'])
        title.pack(pady=(0, 20))
        
        # Model Selection Card
        model_card = tk.Frame(main, bg=self.colors['card'])
        model_card.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(model_card, text="🤖 Model Selection",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['accent']).pack(anchor=tk.W, padx=15, pady=10)
        
        # Model options
        model_frame = tk.Frame(model_card, bg=self.colors['card'])
        model_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.model_var = tk.StringVar(value="tiny")
        
        models = [
            ("🚀 Tiny (Fastest)", "tiny"),
            ("⚡ Base (Balanced)", "base"),
            ("🎯 Small (Best Accuracy)", "small")
        ]
        
        for i, (text, value) in enumerate(models):
            rb = tk.Radiobutton(model_frame, text=text, value=value,
                               variable=self.model_var,
                               bg=self.colors['card'],
                               fg=self.colors['fg'],
                               selectcolor=self.colors['bg'])
            rb.pack(side=tk.LEFT, padx=(0 if i==0 else 20, 0))
        
        # Initialize button
        self.init_btn = tk.Button(model_frame, text="🚀 Initialize Engine",
                                  command=self.init_engine,
                                  bg=self.colors['accent'],
                                  fg='black',
                                  font=('Segoe UI', 11, 'bold'),
                                  padx=20, pady=5,
                                  relief='flat',
                                  cursor='hand2')
        self.init_btn.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Recording Controls Card
        control_card = tk.Frame(main, bg=self.colors['card'])
        control_card.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(control_card, text="🎤 Recording Controls",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['accent']).pack(anchor=tk.W, padx=15, pady=10)
        
        # Buttons
        button_frame = tk.Frame(control_card, bg=self.colors['card'])
        button_frame.pack(fill=tk.X, padx=15, pady=15)
        
        self.record_btn = tk.Button(button_frame, text="🔴 Start Recording",
                                    command=self.start_recording,
                                    bg=self.colors['success'],
                                    fg='black',
                                    font=('Segoe UI', 11, 'bold'),
                                    padx=25, pady=10,
                                    relief='flat',
                                    state=tk.DISABLED,
                                    cursor='hand2')
        self.record_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_btn = tk.Button(button_frame, text="⏹️ Stop",
                                  command=self.stop_recording,
                                  bg=self.colors['error'],
                                  fg='black',
                                  font=('Segoe UI', 11, 'bold'),
                                  padx=35, pady=10,
                                  relief='flat',
                                  state=tk.DISABLED,
                                  cursor='hand2')
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Output Area
        output_frame = tk.Frame(main, bg=self.colors['bg'])
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        # Live Output (Left)
        live_frame = tk.Frame(output_frame, bg=self.colors['card'])
        live_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        tk.Label(live_frame, text="🔄 Live Output",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['accent']).pack(anchor=tk.W, padx=10, pady=10)
        
        self.live_text = scrolledtext.ScrolledText(live_frame,
                                                   font=('Consolas', 11),
                                                   bg='#2b2b3b',
                                                   fg='#89dceb',
                                                   height=15)
        self.live_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Final Results (Right)
        final_frame = tk.Frame(output_frame, bg=self.colors['card'])
        final_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        tk.Label(final_frame, text="✅ Final Results",
                font=('Segoe UI', 12, 'bold'),
                bg=self.colors['card'],
                fg=self.colors['accent']).pack(anchor=tk.W, padx=10, pady=10)
        
        self.final_text = scrolledtext.ScrolledText(final_frame,
                                                    font=('Consolas', 11),
                                                    bg='#1a1a2a',
                                                    fg=self.colors['success'],
                                                    height=15)
        self.final_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Status Bar
        status_bar = tk.Frame(main, bg=self.colors['card'], height=30)
        status_bar.pack(fill=tk.X, pady=(10, 0))
        status_bar.pack_propagate(False)
        
        self.status_label = tk.Label(status_bar, text="● Ready",
                                     font=('Segoe UI', 10),
                                     bg=self.colors['card'],
                                     fg=self.colors['fg'])
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        self.stats_label = tk.Label(status_bar, text="📊 Results: 0",
                                    font=('Segoe UI', 10),
                                    bg=self.colors['card'],
                                    fg=self.colors['success'])
        self.stats_label.pack(side=tk.RIGHT, padx=10)
        
    def log_live(self, text):
        """Add text to live output"""
        self.live_text.insert(tk.END, text + '\n')
        self.live_text.see(tk.END)
        
    def add_to_final(self, text):
        """Add text to final results with proper RTL display"""
        try:
            # Check if text contains Urdu/Arabic characters
            if any('\u0600' <= c <= '\u06FF' for c in text):
                # Reshape and reorder for proper display
                reshaped_text = arabic_reshaper.reshape(text)
                bidi_text = get_display(reshaped_text)
                display_text = bidi_text
                # Force right alignment for Urdu text
                self.final_text.tag_configure('urdu', justify='right')
                tag = 'urdu'
            else:
                display_text = text
                self.final_text.tag_configure('latin', justify='left')
                tag = 'latin'
        except Exception as e:
            # If reshaping fails, try simple RTL marker
            display_text = f"\u202B{text}\u202C"
            tag = 'rtl'
            self.final_text.tag_configure('rtl', justify='right')
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.final_text.insert(tk.END, f"[{timestamp}] ", ('timestamp',))
        self.final_text.insert(tk.END, f"{display_text}\n", (tag,))
        self.final_text.see(tk.END)
        self.final_results.append(text)
        self.stats_label.config(text=f"📊 Results: {len(self.final_results)}")
        
        # Configure timestamp tag
        self.final_text.tag_configure('timestamp', justify='left', foreground='#89b4fa')

    def init_engine(self):
        def init():
            self.log_live("Initializing engine...")
            self.engine = WorkingUrduSTTEngine(
                model_size=self.model_var.get(),
                language="ur"
            )
            self.engine.initialize()
            self.engine.load_model()
            self.root.after(0, self.init_done)
        
        self.init_btn.config(state=tk.DISABLED)
        threading.Thread(target=init, daemon=True).start()
    
    def init_done(self):
        self.log_live("✅ Engine ready")
        self.record_btn.config(state=tk.NORMAL)
        self.status_label.config(text="● Ready", fg=self.colors['success'])
    
    def start_recording(self):
        self.is_recording = True
        self.record_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status_label.config(text="● Recording...", fg=self.colors['error'])
        
        self.log_live("\n" + "="*50)
        self.log_live("STARTED RECORDING")
        self.log_live("="*50)
        
        # Clear previous transcriptions in engine for new session
        if self.engine:
            self.engine.transcriptions = []
        
        def record():
            self.engine.start_streaming()
        
        threading.Thread(target=record, daemon=True).start()
        
        # Start checking for results
        self.check_results()
    
    def check_results(self):
        """Check for new transcriptions"""
        if self.is_recording and self.engine:
            # Check if there are new transcriptions
            if hasattr(self.engine, 'transcriptions') and self.engine.transcriptions:
                current_count = len(self.engine.transcriptions)
                if current_count > len(self.final_results):
                    # Add all new transcriptions
                    for i in range(len(self.final_results), current_count):
                        text = self.engine.transcriptions[i]['text']
                        # Check if not already added
                        if text not in self.final_results:
                            self.add_to_final(text)
            
            # Check again in 1 second
            self.root.after(1000, self.check_results)

    def stop_recording(self):
        self.engine.stop_streaming()
        self.is_recording = False
        
        self.stop_btn.config(state=tk.DISABLED)
        self.record_btn.config(state=tk.NORMAL)
        self.status_label.config(text="● Stopped", fg=self.colors['fg'])
        
        self.log_live("\n" + "="*50)
        self.log_live("STOPPED RECORDING")
        self.log_live("="*50)
        
        # Show any remaining transcriptions
        if self.engine and self.engine.transcriptions:
            self.log_live(f"\n📊 Total: {len(self.engine.transcriptions)} transcriptions")
            
            # Get existing final texts for comparison
            existing_texts = [r for r in self.final_results]  # self.final_results is list of strings
            
            for t in self.engine.transcriptions:
                if t['text'] not in existing_texts:
                    self.add_to_final(t['text'])


if __name__ == "__main__":
    root = tk.Tk()
    app = PerfectUrduSTTUI(root)
    
    # Center window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()