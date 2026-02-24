"""
Task 4: Video Generation (Day 10)
Creates professional video showcasing redesigned rooms
"""

import cv2
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

class VideoGenerator:
    def __init__(self, images_folder, output_folder):
        self.images_folder = images_folder
        self.output_folder = output_folder
        os.makedirs(output_folder, exist_ok=True)
        
    def create_fade_transition(self, img1, img2, steps=30):
        """Create fade transition between two images"""
        frames = []
        for i in range(steps + 1):
            alpha = i / steps
            blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
            frames.append(blended)
        return frames
    
    def add_text_overlay(self, img, text, position=(50, 50)):
        """Add text to image"""
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img_pil)
        
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        draw.text(position, text, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0,0,0))
        return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    def create_main_video(self):
        """Create video showing all styles with transitions"""
        print("="*60)
        print("TASK 4: Generating Main Showcase Video")
        print("="*60)
        
        styles = [
            ("original", "Original Room"),
            ("modern", "Modern Style"),
            ("minimal", "Minimal Style"),
            ("luxury", "Luxury Style"),
            ("bohemian", "Bohemian Style"),
            ("industrial", "Industrial Style"),
            ("scandinavian", "Scandinavian Style"),
            ("original", "Back to Original")
        ]
        
        # Video settings
        fps = 30
        frame_size = (1024, 768)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = os.path.join(self.output_folder, "room_redesign_showcase.mp4")
        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
        
        # Load all images
        images = []
        for style, _ in styles:
            if style == "original":
                path = os.path.join(self.images_folder, "original_room.jpg")
            else:
                path = os.path.join(self.images_folder, f"room_{style}.jpg")
            
            if os.path.exists(path):
                img = cv2.imread(path)
                img = cv2.resize(img, frame_size)
                images.append(img)
                print(f"✅ Loaded: {style}")
            else:
                print(f"❌ Missing: {path}")
                return
        
        # Create video with transitions
        for i in range(len(images) - 1):
            current_img = images[i]
            next_img = images[i + 1]
            style_name = styles[i][1]
            
            # Show current image with text (2 seconds)
            for _ in range(fps * 2):
                frame = self.add_text_overlay(current_img.copy(), style_name)
                out.write(frame)
            
            # Fade transition (1 second)
            transition_frames = self.create_fade_transition(current_img, next_img, fps)
            for frame in transition_frames:
                out.write(frame)
        
        # Show final image
        for _ in range(fps * 2):
            frame = self.add_text_overlay(images[-1].copy(), "Complete!")
            out.write(frame)
        
        out.release()
        print(f"\n✅ Video saved: {output_path}")
        return output_path
    
    def create_comparison_video(self):
        """Create side-by-side comparison video"""
        print("\n" + "="*60)
        print("Generating Comparison Video")
        print("="*60)
        
        styles = ['modern', 'minimal', 'luxury', 'bohemian', 'industrial', 'scandinavian']
        
        # Load original
        original_path = os.path.join(self.images_folder, "original_room.jpg")
        if not os.path.exists(original_path):
            print(f"❌ Original image not found")
            return
        
        original = cv2.imread(original_path)
        original = cv2.resize(original, (512, 512))
        
        # Video settings
        fps = 30
        frame_size = (1024, 512)  # Side by side
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = os.path.join(self.output_folder, "before_after_comparison.mp4")
        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
        
        for style in styles:
            style_path = os.path.join(self.images_folder, f"room_{style}.jpg")
            if not os.path.exists(style_path):
                print(f"❌ Missing: {style_path}")
                continue
            
            generated = cv2.imread(style_path)
            generated = cv2.resize(generated, (512, 512))
            
            # Create side-by-side
            comparison = np.hstack((original, generated))
            
            # Add labels
            comparison = self.add_text_overlay(comparison, f"Original vs {style.capitalize()}", (50, 50))
            
            # Show for 3 seconds
            for _ in range(fps * 3):
                out.write(comparison)
            
            print(f"✅ Added: {style}")
        
        out.release()
        print(f"\n✅ Comparison video saved: {output_path}")
        return output_path
    
    def create_slideshow_video(self):
        """Create simple slideshow (no transitions)"""
        print("\n" + "="*60)
        print("Generating Slideshow Video")
        print("="*60)
        
        styles = ['original', 'modern', 'minimal', 'luxury', 'bohemian', 'industrial', 'scandinavian']
        style_names = ['Original', 'Modern', 'Minimal', 'Luxury', 'Bohemian', 'Industrial', 'Scandinavian']
        
        fps = 1  # 1 second per image
        frame_size = (512, 512)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_path = os.path.join(self.output_folder, "style_slideshow.mp4")
        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)
        
        for style, name in zip(styles, style_names):
            if style == 'original':
                path = os.path.join(self.images_folder, "original_room.jpg")
            else:
                path = os.path.join(self.images_folder, f"room_{style}.jpg")
            
            if os.path.exists(path):
                img = cv2.imread(path)
                img = cv2.resize(img, frame_size)
                img = self.add_text_overlay(img, name)
                out.write(img)
                print(f"✅ Added: {name}")
        
        out.release()
        print(f"\n✅ Slideshow saved: {output_path}")
        return output_path

def main():
    print("="*60)
    print("🎬 TASK 4: VIDEO GENERATION (DAY 10)")
    print("="*60)
    
    # Use your real_samples folder
    images_folder = "data/outputs/images/real_samples"
    videos_folder = "data/outputs/videos"
    
    # Check if images exist
    if not os.path.exists(images_folder):
        print(f"❌ Images folder not found: {images_folder}")
        print("\nPlease run the Colab notebook first to generate images.")
        return
    
    # Create video generator
    generator = VideoGenerator(images_folder, videos_folder)
    
    # Generate all videos
    print("\n📹 Generating videos...\n")
    
    main_video = generator.create_main_video()
    comparison_video = generator.create_comparison_video()
    slideshow = generator.create_slideshow_video()
    
    # Final summary
    print("\n" + "="*60)
    print("✅ TASK 4 COMPLETE!")
    print("="*60)
    print(f"\n📁 Videos saved in: {videos_folder}")
    print("\n📹 Files created:")
    print(f"   1. room_redesign_showcase.mp4 - Main video with transitions")
    print(f"   2. before_after_comparison.mp4 - Side-by-side comparison")
    print(f"   3. style_slideshow.mp4 - Simple slideshow")
    print("\n🎯 These videos fulfill Day 10 requirements!")

if __name__ == "__main__":
    main()