from PIL import Image, ImageDraw, ImageFont
import os

def hex_to_rgb(hex_color):
    """Convert hex color string to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def create_style_image(room_name, style, output_path):
    # Create a gradient background
    img = Image.new('RGB', (512, 512), color='white')
    draw = ImageDraw.Draw(img)
    
    # Define colors for different styles
    style_colors = {
        'modern': ('#2c3e50', '#3498db'),        # Dark blue to light blue
        'minimal': ('#ecf0f1', '#bdc3c7'),       # Light gray to darker gray
        'luxury': ('#8e44ad', '#c39bd3'),         # Purple to light purple
        'bohemian': ('#e67e22', '#f39c12'),       # Orange to yellow
        'industrial': ('#7f8c8d', '#95a5a6'),      # Gray to light gray
        'scandinavian': ('#3498db', '#85c1e2')     # Blue to light blue
    }
    
    # Get colors for this style
    color1_hex, color2_hex = style_colors.get(style, ('#333333', '#666666'))
    color1_rgb = hex_to_rgb(color1_hex)
    color2_rgb = hex_to_rgb(color2_hex)
    
    # Create vertical gradient
    for y in range(512):
        r = int(color1_rgb[0] * (512 - y) / 512 + color2_rgb[0] * y / 512)
        g = int(color1_rgb[1] * (512 - y) / 512 + color2_rgb[1] * y / 512)
        b = int(color1_rgb[2] * (512 - y) / 512 + color2_rgb[2] * y / 512)
        draw.line([(0, y), (511, y)], fill=(r, g, b))
    
    # Add text
    try:
        # Try to use a nice font if available
        font = ImageFont.truetype("arial.ttf", 40)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw room name
    draw.text((256, 200), room_name.replace('_', ' ').title(), 
              fill='white', anchor='mm', font=font)
    
    # Draw style name
    draw.text((256, 280), style.title(), 
              fill='white', anchor='mm', font=font)
    
    # Draw "AI Redesigned" text
    draw.text((256, 350), "AI Redesigned", 
              fill='white', anchor='mm', font=font_small)
    
    # Draw border
    draw.rectangle([0, 0, 511, 511], outline='white', width=3)
    
    # Save image
    img.save(output_path)
    print(f"✅ Created: {os.path.basename(output_path)}")

def main():
    rooms = ['cozy_bedroom', 'dining_room', 'spacious_office']
    styles = ['modern', 'minimal', 'luxury', 'bohemian', 'industrial', 'scandinavian']
    
    output_dir = 'data/outputs/images'
    os.makedirs(output_dir, exist_ok=True)
    
    for room in rooms:
        for style in styles:
            output_path = os.path.join(output_dir, f'{room}_{style}.png')
            create_style_image(room, style, output_path)
    
    print(f"\n✅ Created {len(rooms) * len(styles)} beautiful placeholder images!")

if __name__ == '__main__':
    main()