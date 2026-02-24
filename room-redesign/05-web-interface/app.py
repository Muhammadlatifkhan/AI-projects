"""
MEMBER 5: UI/Web Interface
Flask web app to display original and redesigned rooms
"""

import os
import json
from flask import Flask, render_template, send_file, jsonify
from PIL import Image
import base64
from io import BytesIO

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_IMAGES_DIR = os.path.join(BASE_DIR, "data", "input_images")
OUTPUT_IMAGES_DIR = os.path.join(BASE_DIR, "data", "outputs", "images")
REAL_SAMPLES_DIR = os.path.join(OUTPUT_IMAGES_DIR, "real_samples")  # Added this!

# Styles available
STYLES = ['modern', 'minimal', 'luxury', 'bohemian', 'industrial', 'scandinavian']

@app.route('/')
def index():
    """Home page - show all original images"""
    images = []
    
    # Look for original images in input_images
    if os.path.exists(INPUT_IMAGES_DIR):
        for img_file in os.listdir(INPUT_IMAGES_DIR):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                name = os.path.splitext(img_file)[0]
                images.append({
                    'filename': img_file,
                    'name': name
                })
    
    # If no input images, show real_samples originals
    if not images and os.path.exists(REAL_SAMPLES_DIR):
        # Look for original_room.jpg in real_samples
        if os.path.exists(os.path.join(REAL_SAMPLES_DIR, 'original_room.jpg')):
            images.append({
                'filename': 'real_samples/original_room.jpg',
                'name': 'Original Room'
            })
    
    return render_template('index.html', images=images, styles=STYLES)

@app.route('/image/<path:filename>')
@app.route('/image/<path:filename>')
def get_image(filename):
    """Serve images with debug info"""
    print(f"Requesting image: {filename}")
    
    # Try real_samples first
    img_path = os.path.join(REAL_SAMPLES_DIR, filename.replace('real_samples/', ''))
    print(f"Trying real_samples path: {img_path}")
    print(f"Exists: {os.path.exists(img_path)}")
    
    if os.path.exists(img_path):
        return send_file(img_path)
    
    # Try input images
    img_path = os.path.join(INPUT_IMAGES_DIR, filename)
    print(f"Trying input path: {img_path}")
    print(f"Exists: {os.path.exists(img_path)}")
    
    if os.path.exists(img_path):
        return send_file(img_path)
    
    print(f"IMAGE NOT FOUND: {filename}")
    return "Image not found", 404
@app.route('/room/<room_name>')
def view_room(room_name):
    """View a specific room with all styles"""
    styles_data = []
    
    for style in STYLES:
        # Try different possible filenames
        possible_filenames = [
            f"{room_name}_{style}.jpg",
            f"{room_name}_{style}.png",
            f"room_{style}.jpg",
            f"{style}.jpg"
        ]
        
        found = False
        for filename in possible_filenames:
            # Check in real_samples first
            img_path = os.path.join(REAL_SAMPLES_DIR, filename)
            if os.path.exists(img_path):
                styles_data.append({
                    'style': style.capitalize(),
                    'filename': f"real_samples/{filename}"
                })
                found = True
                break
            
            # Then check output images
            img_path = os.path.join(OUTPUT_IMAGES_DIR, filename)
            if os.path.exists(img_path):
                styles_data.append({
                    'style': style.capitalize(),
                    'filename': filename
                })
                found = True
                break
        
        if not found:
            # Use placeholder if no image found
            styles_data.append({
                'style': style.capitalize(),
                'filename': None
            })
    
    return render_template('room.html', room_name=room_name, styles=styles_data)
@app.route('/compare/<image_name>/<style>')
def compare(image_name, style):
    """Compare original image with redesigned version"""
    
    # Clean image name (remove extension)
    base_name = image_name.replace('.jpg', '').replace('.png', '').replace('.jpeg', '')
    
    # Original image path
    original_path = f"/image/{image_name}"
    
    # Find redesigned image
    redesigned_path = None
    
    # Try real_samples first (for your AI images)
    possible_filenames = [
        f"room_{style}.jpg",
        f"{base_name}_{style}.jpg",
        f"{style}.jpg"
    ]
    
    for filename in possible_filenames:
        test_path = os.path.join(REAL_SAMPLES_DIR, filename)
        if os.path.exists(test_path):
            redesigned_path = f"/image/real_samples/{filename}"
            break
    
    # If not found, try output images
    if not redesigned_path:
        for filename in possible_filenames:
            test_path = os.path.join(OUTPUT_IMAGES_DIR, filename)
            if os.path.exists(test_path):
                redesigned_path = f"/image/{filename}"
                break
    
    # If still not found, use placeholder
    if not redesigned_path:
        redesigned_path = f"https://via.placeholder.com/512x512?text={style}"
    
    return render_template('compare.html',
                         original_image=original_path,
                         redesigned_image=redesigned_path,
                         style=style.capitalize(),
                         room_name=base_name)

@app.route('/api/images')
def get_all_images():
    """API endpoint to get all images info"""
    images_data = {
        'original': [],
        'styles': {},
        'real_samples': []
    }
    
    # Get real_samples images
    if os.path.exists(REAL_SAMPLES_DIR):
        for img_file in os.listdir(REAL_SAMPLES_DIR):
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                images_data['real_samples'].append({
                    'filename': f"real_samples/{img_file}",
                    'name': os.path.splitext(img_file)[0]
                })
    
    return jsonify(images_data)

if __name__ == '__main__':
    # Print debug info
    print(f"Looking for images in:")
    print(f"  Input: {INPUT_IMAGES_DIR}")
    print(f"  Output: {OUTPUT_IMAGES_DIR}")
    print(f"  Real Samples: {REAL_SAMPLES_DIR}")
    print(f"\nReal samples exist: {os.path.exists(REAL_SAMPLES_DIR)}")
    if os.path.exists(REAL_SAMPLES_DIR):
        print(f"Files in real_samples: {os.listdir(REAL_SAMPLES_DIR)}")
    
    app.run(debug=True, port=5000)