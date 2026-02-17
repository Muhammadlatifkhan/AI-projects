"""
MEMBER 3: Prompt Engineer
Generates redesign prompts for each room image
"""

import os
import json
import random

class PromptGenerator:
    def __init__(self):
        """Initialize with prompt templates"""
        print("🔄 Initializing Prompt Generator...")
        
        # Define style categories
        self.styles = {
            "modern": {
                "name": "Modern",
                "keywords": ["minimalist", "clean lines", "contemporary", "sleek", "glass", "steel"],
                "description": "Modern interior with clean lines, minimalist furniture, and contemporary design"
            },
            "minimal": {
                "name": "Minimal",
                "keywords": ["simple", "uncluttered", "neutral colors", "functional", "airy"],
                "description": "Minimalist space with simple forms, neutral palette, and uncluttered surfaces"
            },
            "luxury": {
                "name": "Luxury",
                "keywords": ["elegant", "sophisticated", "high-end", "rich textures", "velvet", "marble"],
                "description": "Luxurious interior with elegant furnishings, rich textures, and sophisticated details"
            },
            "bohemian": {
                "name": "Bohemian",
                "keywords": ["eclectic", "colorful", "patterned", "plants", "natural materials", "cozy"],
                "description": "Bohemian style with eclectic patterns, plants, natural materials, and cozy atmosphere"
            },
            "industrial": {
                "name": "Industrial",
                "keywords": ["raw", "brick", "metal", "exposed pipes", "concrete", "loft"],
                "description": "Industrial design with raw materials, exposed elements, and urban aesthetic"
            },
            "scandinavian": {
                "name": "Scandinavian",
                "keywords": ["light wood", "white", "functional", "hygge", "natural light", "simple"],
                "description": "Scandinavian interior with light woods, white walls, and cozy functional design"
            }
        }
        
        # Room type specific prompts
        self.room_templates = {
            "bedroom": [
                "Transform this bedroom into a {style} retreat with {keywords}",
                "Redesign this bedroom with {style} aesthetic featuring {keywords}",
                "Create a serene {style} bedroom with {keywords}"
            ],
            "living": [
                "Convert this living room to {style} style with {keywords}",
                "Redesign this living space with {style} elements including {keywords}",
                "Create an inviting {style} living room featuring {keywords}"
            ],
            "kitchen": [
                "Transform this kitchen with {style} design featuring {keywords}",
                "Redesign this kitchen using {style} elements including {keywords}",
                "Create a functional {style} kitchen with {keywords}"
            ],
            "dining": [
                "Redesign this dining room with {style} aesthetic featuring {keywords}",
                "Transform this dining space into a {style} area with {keywords}",
                "Create an elegant {style} dining room featuring {keywords}"
            ],
            "office": [
                "Convert this office to {style} workspace with {keywords}",
                "Redesign this office using {style} elements including {keywords}",
                "Create a productive {style} home office with {keywords}"
            ]
        }
        
        # Negative prompts (things to avoid)
        self.negative_prompts = [
            "cluttered",
            "messy",
            "dark",
            "outdated",
            "low quality",
            "blurry",
            "ugly",
            "poorly lit"
        ]
        
        print(f"✅ Prompt Generator initialized with {len(self.styles)} styles")
    
    def detect_room_type(self, filename):
        """Detect room type from filename"""
        filename = filename.lower()
        if "bedroom" in filename:
            return "bedroom"
        elif "living" in filename:
            return "living"
        elif "kitchen" in filename:
            return "kitchen"
        elif "dining" in filename:
            return "dining"
        elif "office" in filename:
            return "office"
        else:
            return "living"  # default
    
    def generate_prompts_for_image(self, image_name):
        """Generate all style prompts for a single image"""
        
        room_type = self.detect_room_type(image_name)
        prompts = {}
        
        for style_key, style_data in self.styles.items():
            # Select random keywords
            keywords = random.sample(style_data["keywords"], min(3, len(style_data["keywords"])))
            keywords_str = ", ".join(keywords)
            
            # Select template
            templates = self.room_templates.get(room_type, self.room_templates["living"])
            template = random.choice(templates)
            
            # Generate positive prompt
            positive = template.format(
                style=style_data["name"],
                keywords=keywords_str
            )
            
            # Add specific details based on style
            if style_key == "modern":
                positive += ", contemporary furniture, clean geometric shapes"
            elif style_key == "minimal":
                positive += ", sparse decoration, functional pieces"
            elif style_key == "luxury":
                positive += ", premium finishes, designer furniture"
            elif style_key == "bohemian":
                positive += ", layered textiles, indoor plants, global accents"
            elif style_key == "industrial":
                positive += ", exposed brick, metal fixtures, urban vibe"
            elif style_key == "scandinavian":
                positive += ", light wood floors, cozy textiles, simple elegance"
            
            # Generate negative prompt
            negative = ", ".join(random.sample(self.negative_prompts, min(3, len(self.negative_prompts))))
            
            prompts[style_key] = {
                "style": style_data["name"],
                "positive": positive,
                "negative": negative,
                "description": style_data["description"]
            }
        
        return prompts
    
    def process_images(self, input_folder, output_file):
        """Generate prompts for all images"""
        
        print(f"\n📁 Processing images from: {input_folder}")
        
        # Get all images
        if not os.path.exists(input_folder):
            print(f"❌ Input folder not found: {input_folder}")
            return
        
        images = [f for f in os.listdir(input_folder) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"Found {len(images)} images")
        
        all_prompts = {}
        
        for img_file in images:
            print(f"\n📸 Generating prompts for: {img_file}")
            room_type = self.detect_room_type(img_file)
            print(f"   Detected room type: {room_type}")
            
            prompts = self.generate_prompts_for_image(img_file)
            all_prompts[img_file] = prompts
            
            # Show sample prompt
            sample_style = list(prompts.keys())[0]
            print(f"   Sample ({prompts[sample_style]['style']}):")
            print(f"     + {prompts[sample_style]['positive'][:80]}...")
            print(f"     - {prompts[sample_style]['negative']}")
        
        # Save to JSON file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(all_prompts, f, indent=2)
        
        print(f"\n✅ Prompts saved to: {output_file}")
        return all_prompts
    
    def create_style_summary(self, prompts, output_folder):
        """Create a readable summary of all prompts"""
        
        summary_file = os.path.join(output_folder, "prompt_summary.txt")
        
        with open(summary_file, 'w') as f:
            f.write("PROMPT GENERATION SUMMARY\n")
            f.write("=" * 60 + "\n\n")
            
            for img_name, styles in prompts.items():
                f.write(f"📸 {img_name}\n")
                f.write("-" * 40 + "\n")
                
                for style_key, prompt_data in styles.items():
                    f.write(f"\n{style_key.upper()} STYLE:\n")
                    f.write(f"  Description: {prompt_data['description']}\n")
                    f.write(f"  Positive: {prompt_data['positive']}\n")
                    f.write(f"  Negative: {prompt_data['negative']}\n")
                
                f.write("\n" + "=" * 60 + "\n\n")
        
        print(f"📄 Summary saved to: {summary_file}")

def main():
    print("=" * 50)
    print("MEMBER 3: Prompt Engineer")
    print("=" * 50)
    
    # Paths
    input_folder = "../data/input_images"
    output_folder = "../data/prompts"
    output_file = os.path.join(output_folder, "prompts.json")
    
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"❌ Input folder not found: {input_folder}")
        return
    
    # Create generator
    generator = PromptGenerator()
    
    # Generate prompts
    prompts = generator.process_images(input_folder, output_file)
    
    # Create summary
    if prompts:
        generator.create_style_summary(prompts, output_folder)
    
    print("\n✅ Member 3 task completed!")
    print("\n📋 Available styles for each image:")
    if prompts:
        for img in prompts.keys():
            styles = list(prompts[img].keys())
            print(f"  {img}: {', '.join(styles)}")

if __name__ == "__main__":
    main()