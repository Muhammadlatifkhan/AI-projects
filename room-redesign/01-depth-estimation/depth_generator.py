"""
MEMBER 1: Depth Map Generator
Takes room images and generates depth maps using MiDaS model
"""

import os
import torch
import cv2
import numpy as np
from PIL import Image

class DepthGenerator:
    def __init__(self):
        """Initialize the depth generator with MiDaS model"""
        print("🔄 Initializing Depth Generator...")
        print("   This will download the MiDaS model (first time only)...")
        
        # Load MiDaS model - using small version for CPU
        self.midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
        self.midas.eval()
        
        # Load transforms
        midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        self.transform = midas_transforms.small_transform
        
        print("✅ Depth Generator initialized")
        
    def generate_depth_map(self, image_path, output_path):
        """
        Generate depth map from an image
        """
        print(f"📸 Processing: {os.path.basename(image_path)}")
        
        # Load image using PIL
        img = Image.open(image_path).convert('RGB')
        img_np = np.array(img)
        
        # Apply transforms - this returns [1, 3, H, W]
        input_tensor = self.transform(img_np)
        
        # Remove any extra dimensions if present
        if input_tensor.dim() == 5:  # [1, 1, 3, H, W] -> [1, 3, H, W]
            input_tensor = input_tensor.squeeze(1)
        
        # Generate depth map
        with torch.no_grad():
            depth = self.midas(input_tensor)
            
            # Resize to original size
            depth = torch.nn.functional.interpolate(
                depth.unsqueeze(1),
                size=img_np.shape[:2],
                mode="bicubic",
                align_corners=False,
            ).squeeze()
        
        depth = depth.cpu().numpy()
        
        # Normalize to 0-255
        depth_min = depth.min()
        depth_max = depth.max()
        depth_norm = ((depth - depth_min) / (depth_max - depth_min) * 255).astype(np.uint8)
        
        # Save
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        Image.fromarray(depth_norm).save(output_path)
        print(f"💾 Saved: {os.path.basename(output_path)}")
        
        return depth_norm
    
    def process_folder(self, input_folder, output_folder):
        """Process all images in a folder"""
        
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Get all images
        images = [f for f in os.listdir(input_folder) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"\n📁 Found {len(images)} images to process")
        
        for i, img_file in enumerate(images, 1):
            input_path = os.path.join(input_folder, img_file)
            
            # Create output filename
            name = os.path.splitext(img_file)[0]
            output_path = os.path.join(output_folder, f"{name}_depth.png")
            
            print(f"\n[{i}/{len(images)}] Processing...")
            self.generate_depth_map(input_path, output_path)
        
        print(f"\n✅ Done! Depth maps saved in: {output_folder}")

def main():
    print("=" * 50)
    print("MEMBER 1: Depth Map Generator")
    print("=" * 50)
    
    # Paths
    input_folder = "../data/input_images"
    output_folder = "../data/depth_maps"
    
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"❌ Input folder not found: {input_folder}")
        return
    
    # Check if there are images
    images = [f for f in os.listdir(input_folder) 
             if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"📸 Found {len(images)} images in input folder")
    
    # Create generator
    generator = DepthGenerator()
    
    # Process all images
    generator.process_folder(input_folder, output_folder)
    
    # Check if output was created
    if os.path.exists(output_folder):
        output_files = os.listdir(output_folder)
        print(f"\n✅ Member 1 task completed! {len(output_files)} depth maps created")
    else:
        print("\n❌ No output files were created")

if __name__ == "__main__":
    main()