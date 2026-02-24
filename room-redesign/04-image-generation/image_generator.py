"""
MEMBER 4: Image & Video Generator
Uses Stable Diffusion + ControlNet to generate redesigned rooms
"""

import os
import json
import torch
import numpy as np
from PIL import Image
import cv2
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
from diffusers.utils import load_image
import time

class ImageGenerator:
    def __init__(self):
        """Initialize Stable Diffusion with ControlNet"""
        print("🔄 Initializing Image Generator...")
        print("   This will download models (first time only, may take a while)...")
        
        # Check if we have CUDA (GPU) or fallback to CPU
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"   Using device: {self.device}")
        
        try:
            # Load ControlNet models (smaller versions for CPU)
            print("   Loading ControlNet models...")
            
            # For depth control
            self.controlnet_depth = ControlNetModel.from_pretrained(
                "lllyasviel/sd-controlnet-depth", 
                torch_dtype=torch.float32
            )
            
            # For segmentation control
            self.controlnet_seg = ControlNetModel.from_pretrained(
                "lllyasviel/sd-controlnet-seg", 
                torch_dtype=torch.float32
            )
            
            # Load Stable Diffusion pipeline with both ControlNets
            print("   Loading Stable Diffusion (this may take 2-3 minutes)...")
            self.pipe = StableDiffusionControlNetPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5",
                controlnet=[self.controlnet_depth, self.controlnet_seg],
                torch_dtype=torch.float32,
                safety_checker=None  # Disable safety checker for speed
            )
            
            # Move to CPU (since we're on CPU)
            self.pipe = self.pipe.to(self.device)
            
            # Enable memory optimizations
            self.pipe.enable_attention_slicing()
            
            print("✅ Image Generator initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            print("   Will use simplified mode for testing")
            self.pipe = None
    
    def prepare_control_images(self, depth_map_path, masks_folder):
        """
        Prepare control images for ControlNet
        """
        # Load depth map
        if os.path.exists(depth_map_path):
            depth_image = Image.open(depth_map_path).convert('RGB')
        else:
            # Create blank image if depth map not found
            depth_image = Image.new('RGB', (512, 512), color='gray')
        
        # Create segmentation map from masks
        seg_image = self.create_segmentation_map(masks_folder)
        
        return depth_image, seg_image
    
    def create_segmentation_map(self, masks_folder):
        """
        Combine individual masks into a single segmentation map
        """
        # Define colors for different object types (RGB)
        color_map = {
            'chair': (255, 0, 0),      # Red
            'couch': (0, 255, 0),       # Green
            'bed': (0, 0, 255),          # Blue
            'dining table': (255, 255, 0),  # Yellow
            'tv': (255, 0, 255),         # Magenta
            'potted plant': (0, 255, 255),  # Cyan
            'refrigerator': (128, 0, 0),  # Dark red
            'sink': (0, 128, 0),         # Dark green
            'train': (0, 0, 128),         # Dark blue
            'boat': (128, 128, 0),        # Olive
            'fire hydrant': (128, 0, 128), # Purple
            'bird': (0, 128, 128),        # Teal
        }
        
        # Create blank segmentation map
        seg_map = Image.new('RGB', (512, 512), color='black')
        
        if not os.path.exists(masks_folder):
            return seg_map
        
        # Get all mask files
        mask_files = [f for f in os.listdir(masks_folder) if f.endswith('.png') and 'segmentation' not in f]
        
        for mask_file in mask_files:
            try:
                # Determine object type from filename
                obj_type = mask_file.split('_mask')[0]
                color = color_map.get(obj_type, (255, 255, 255))  # Default white
                
                # Load mask
                mask_path = os.path.join(masks_folder, mask_file)
                mask = Image.open(mask_path).convert('L')
                
                # Convert mask to numpy for processing
                mask_np = np.array(mask)
                
                # Create colored mask
                colored_mask = np.zeros((512, 512, 3), dtype=np.uint8)
                for i in range(3):
                    colored_mask[:,:,i] = mask_np * color[i] // 255
                
                # Combine with existing segmentation map
                seg_np = np.array(seg_map)
                mask_bool = mask_np > 128
                seg_np[mask_bool] = colored_mask[mask_bool]
                seg_map = Image.fromarray(seg_np)
                
            except Exception as e:
                print(f"   Warning: Could not process {mask_file}: {e}")
        
        return seg_map
    
    def generate_image(self, prompt, negative_prompt, depth_image, seg_image, 
                      output_path, num_inference_steps=25, guidance_scale=7.5):
        """
        Generate a redesigned image using ControlNet
        """
        print(f"   Generating image with {num_inference_steps} steps...")
        
        if self.pipe is None:
            print("   Model not loaded - creating placeholder image")
            # Create a simple placeholder
            img = Image.new('RGB', (512, 512), color='gray')
            img.save(output_path)
            return img
        
        try:
            # Resize control images to 512x512
            depth_image = depth_image.resize((512, 512))
            seg_image = seg_image.resize((512, 512))
            
            # Generate image
            with torch.no_grad():
                result = self.pipe(
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    image=[depth_image, seg_image],
                    num_inference_steps=num_inference_steps,
                    guidance_scale=guidance_scale,
                    height=512,
                    width=512
                ).images[0]
            
            # Save result
            result.save(output_path)
            print(f"   ✅ Image saved")
            return result
            
        except Exception as e:
            print(f"   ❌ Generation failed: {e}")
            # Create fallback image
            img = Image.new('RGB', (512, 512), color='lightgray')
            img.save(output_path)
            return img
    
    def process_all_styles(self, image_name, prompts, depth_folder, masks_folder, output_folder):
        """
        Generate images for all styles for a given input image
        """
        print(f"\n📸 Processing: {image_name}")
        
        # Get base name without extension
        base_name = os.path.splitext(image_name)[0]
        
        # Prepare control images
        depth_path = os.path.join(depth_folder, f"{base_name}_depth.png")
        masks_path = os.path.join(masks_folder, base_name)
        
        depth_image, seg_image = self.prepare_control_images(depth_path, masks_path)
        
        # Generate for each style
        generated_images = []
        
        for style, style_data in prompts.items():
            print(f"\n   🎨 Style: {style_data['style']}")
            
            # Create output filename
            output_filename = f"{base_name}_{style}.png"
            output_path = os.path.join(output_folder, output_filename)
            
            # Generate image
            start_time = time.time()
            self.generate_image(
                prompt=style_data['positive'],
                negative_prompt=style_data['negative'],
                depth_image=depth_image,
                seg_image=seg_image,
                output_path=output_path,
                num_inference_steps=20  # Lower steps for CPU speed
            )
            elapsed = time.time() - start_time
            print(f"   ⏱️  Time: {elapsed:.1f} seconds")
            
            generated_images.append(output_path)
        
        return generated_images
    
    def process_all_images(self, prompts_file, depth_folder, masks_folder, output_folder):
        """
        Process all images with all styles
        """
        print("\n" + "="*60)
        print("Starting batch image generation...")
        print("="*60)
        
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Load prompts
        with open(prompts_file, 'r') as f:
            all_prompts = json.load(f)
        
        print(f"📁 Found {len(all_prompts)} images to process")
        
        # Process each image
        all_results = {}
        
        for image_name, prompts in all_prompts.items():
            results = self.process_all_styles(
                image_name, prompts, depth_folder, masks_folder, output_folder
            )
            all_results[image_name] = results
        
        # Save summary
        summary_file = os.path.join(output_folder, "generation_summary.txt")
        with open(summary_file, 'w') as f:
            f.write("IMAGE GENERATION SUMMARY\n")
            f.write("="*60 + "\n")
            for image_name, results in all_results.items():
                f.write(f"\n{image_name}:\n")
                for result in results:
                    f.write(f"  - {os.path.basename(result)}\n")
        
        print(f"\n✅ All images generated!")
        print(f"📁 Output folder: {output_folder}")
        print(f"📄 Summary: {summary_file}")

def main():
    print("="*50)
    print("MEMBER 4: Image & Video Generator")
    print("="*50)
    
    # Paths
    prompts_file = "../data/prompts/prompts.json"
    depth_folder = "../data/depth_maps"
    masks_folder = "../data/masks"
    output_folder = "../data/outputs/images"
    
    # Check if required files exist
    if not os.path.exists(prompts_file):
        print(f"❌ Prompts file not found: {prompts_file}")
        return
    
    # Create generator
    generator = ImageGenerator()
    
    # Process all images
    generator.process_all_images(prompts_file, depth_folder, masks_folder, output_folder)
    
    print("\n✅ Member 4 image generation completed!")
    print("➡️  Next: Run video_generator.py to create videos")

if __name__ == "__main__":
    main()