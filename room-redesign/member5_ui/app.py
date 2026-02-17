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
PROMPTS_FILE = os.path.join(BASE_DIR, "data", "prompts", "prompts.json")

# Load prompts
with open(PROMPTS_FILE, 'r') as f:
    prompts = json.load(f)

# Available styles
styles = ['modern', 'minimal', 'luxury', 'bohemian', 'industrial', 'scandinavian']

@app.route('/')
def index():
    """Home page - show all images"""
    images = []
    for img_file in os.listdir(INPUT_IMAGES_DIR):
        if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            name = os.path.splitext(img_file)[0]
            images.append({
                'name': name,
                'filename': img_file,
                'styles': styles
            })
    return render_template('index.html', images=images, styles=styles)

@app.route('/image/<path:filename>')
def get_image(filename):
    """Serve images"""
    # Try input images first
    img_path = os.path.join(INPUT_IMAGES_DIR, filename)
    if os.path.exists(img_path):
        return send_file(img_path)
    
    # Try output images
    img_path = os.path.join(OUTPUT_IMAGES_DIR, filename)
    if os.path.exists(img_path):
        return send_file(img_path)
    
    return "Image not found", 404

@app.route('/prompts/<image_name>')
def get_prompts(image_name):
    """Get prompts for an image"""
    # Find the original filename
    for f in os.listdir(INPUT_IMAGES_DIR):
        if f.startswith(image_name):
            if f in prompts:
                return jsonify(prompts[f])
    return jsonify({})

@app.route('/compare/<image_name>/<style>')
def compare(image_name, style):
    """Show original and redesigned side by side"""
    original = None
    redesigned = None
    
    # Find original
    for f in os.listdir(INPUT_IMAGES_DIR):
        if f.startswith(image_name):
            original = f
            break
    
    # Find redesigned
    redesigned = f"{image_name}_{style}.png"
    
    return render_template('compare.html', 
                         original=original, 
                         redesigned=redesigned,
                         image_name=image_name,
                         style=style)

if __name__ == '__main__':
    app.run(debug=True, port=5000)