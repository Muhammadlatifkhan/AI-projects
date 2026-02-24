"""
MEMBER 2: Segmentation Mask Generator
Takes room images and generates individual object masks
"""

import os
import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

class MaskGenerator:
    def __init__(self):
        """Initialize the segmentation model"""
        print("🔄 Initializing Mask Generator...")
        print("   This will download the segmentation model (first time only)...")
        
        # Load a pre-trained segmentation model (DeepLabV3)
        self.model = torch.hub.load('pytorch/vision:v0.10.0', 'deeplabv3_resnet50', pretrained=True)
        self.model.eval()
        
        # ImageNet normalization
        from torchvision import transforms
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # COCO class labels (the model was trained on COCO dataset)
        self.classes = [
            '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
            'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign',
            'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
            'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
            'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite',
            'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
            'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana',
            'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
            'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table',
            'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock',
            'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
        ]
        
        # Room-relevant classes we care about
        self.room_classes = {
            57: 'chair',
            58: 'couch',
            59: 'potted plant',
            60: 'bed',
            61: 'dining table',
            62: 'toilet',
            63: 'tv',
            72: 'sink',
            73: 'refrigerator'
        }
        
        print(f"✅ Mask Generator initialized with {len(self.classes)} classes")
        
    def generate_masks(self, image_path, output_folder):
        """
        Generate individual masks for each object in the image
        """
        print(f"📸 Processing: {os.path.basename(image_path)}")
        
        # Load and prepare image
        img = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(img).unsqueeze(0)
        
        # Generate segmentation
        with torch.no_grad():
            output = self.model(img_tensor)['out'][0]
            predictions = output.argmax(0).cpu().numpy()
        
        # Create output folder for this image
        img_name = os.path.splitext(os.path.basename(image_path))[0]
        img_output_folder = os.path.join(output_folder, img_name)
        os.makedirs(img_output_folder, exist_ok=True)
        
        # Get unique object IDs found in the image
        unique_ids = np.unique(predictions)
        
        # Create individual masks for each object
        masks_created = []
        
        for obj_id in unique_ids:
            if obj_id == 0:  # Skip background
                continue
                
            class_name = self.classes[obj_id] if obj_id < len(self.classes) else 'unknown'
            
            # Create binary mask for this object
            mask = (predictions == obj_id).astype(np.uint8) * 255
            
            # Only save if mask has enough pixels (filter noise)
            if np.sum(mask) > 500:  # Minimum 500 white pixels
                mask_img = Image.fromarray(mask)
                mask_filename = f"{class_name}_mask_{obj_id}.png"
                mask_path = os.path.join(img_output_folder, mask_filename)
                mask_img.save(mask_path)
                masks_created.append(class_name)
                print(f"  ✅ Created mask: {class_name}")
        
        # Also create a combined color-coded segmentation map
        self.create_colored_segmentation(predictions, img_output_folder, img_name)
        
        print(f"  ✅ Total {len(masks_created)} masks created for {img_name}")
        return masks_created
    
    def create_colored_segmentation(self, predictions, output_folder, img_name):
        """
        Create a color-coded segmentation map for visualization
        """
        # Create a color map
        colors = [
            [0, 0, 0],       # 0: background (black)
            [255, 0, 0],     # 1: red
            [0, 255, 0],     # 2: green
            [0, 0, 255],     # 3: blue
            [255, 255, 0],   # 4: yellow
            [255, 0, 255],   # 5: magenta
            [0, 255, 255],   # 6: cyan
            [128, 0, 0],     # 7: dark red
            [0, 128, 0],     # 8: dark green
            [0, 0, 128],     # 9: dark blue
            [128, 128, 0],   # 10: olive
            [128, 0, 128],   # 11: purple
            [0, 128, 128],   # 12: teal
        ]
        
        # Create RGB image
        h, w = predictions.shape
        rgb_image = np.zeros((h, w, 3), dtype=np.uint8)
        
        # Get unique objects
        unique_ids = np.unique(predictions)
        
        for i, obj_id in enumerate(unique_ids):
            if obj_id == 0:  # Background black
                continue
            color_idx = (i % (len(colors) - 1)) + 1  # Skip index 0 (background)
            mask = (predictions == obj_id)
            rgb_image[mask] = colors[color_idx]
        
        # Save
        output_path = os.path.join(output_folder, f"{img_name}_segmentation_colored.png")
        Image.fromarray(rgb_image).save(output_path)
        print(f"  ✅ Created colored segmentation map")
    
    def process_folder(self, input_folder, output_folder):
        """
        Process all images in a folder
        """
        print(f"\n📁 Processing batch from: {input_folder}")
        
        # Create output folder
        os.makedirs(output_folder, exist_ok=True)
        
        # Get all images
        images = [f for f in os.listdir(input_folder) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        print(f"Found {len(images)} images to process")
        
        all_masks = {}
        
        for i, img_file in enumerate(images, 1):
            input_path = os.path.join(input_folder, img_file)
            
            print(f"\n[{i}/{len(images)}] Processing {img_file}...")
            
            try:
                masks = self.generate_masks(input_path, output_folder)
                all_masks[img_file] = masks
                print(f"✅ Completed")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Save mask summary
        summary_path = os.path.join(output_folder, "mask_summary.txt")
        with open(summary_path, 'w') as f:
            f.write("Mask Generation Summary\n")
            f.write("=" * 50 + "\n")
            for img, masks in all_masks.items():
                f.write(f"\n{img}: {len(masks)} masks\n")
                for mask in masks:
                    f.write(f"  - {mask}\n")
        
        print(f"\n✅ Batch processing complete!")
        print(f"📁 Masks saved in: {output_folder}")
        print(f"📄 Summary saved: {summary_path}")

def main():
    print("=" * 50)
    print("MEMBER 2: Segmentation Mask Generator")
    print("=" * 50)
    
    # Paths
    input_folder = "../data/input_images"
    output_folder = "../data/masks"
    
    # Check if input folder exists
    if not os.path.exists(input_folder):
        print(f"❌ Input folder not found: {input_folder}")
        return
    
    # Create generator
    generator = MaskGenerator()
    
    # Process all images
    generator.process_folder(input_folder, output_folder)
    
    print("\n✅ Member 2 task completed!")

if __name__ == "__main__":
    main()