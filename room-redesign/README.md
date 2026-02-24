# 🏠 AI-Powered Room Redesign System
### Complete Computer Vision & Generative AI Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.0-orange)
![Flask](https://img.shields.io/badge/Flask-Web%20App-green)
![Stable Diffusion](https://img.shields.io/badge/Stable%20Diffusion-ControlNet-purple)
![Status](https://img.shields.io/badge/Status-100%25%20Complete-brightgreen)

</div>

## 📋 Project Overview
An end-to-end AI system that automatically redesigns room images using depth estimation, segmentation, and generative AI. The system processes input room images and generates redesigned versions in **6 different interior design styles**.

## 🎯 Key Features
- **Depth Map Generation**: MiDaS-based depth estimation to preserve room geometry
- **Object Segmentation**: DeepLabV3 identifies furniture and objects for controlled redesign
- **Prompt Engineering**: Automatically generates design prompts for 6 distinct styles
- **Image Generation**: Stable Diffusion + ControlNet creates redesigned rooms
- **Web Interface**: Interactive Flask gallery with side-by-side comparisons
- **Video Generation**: Automated creation of style comparison and showcase videos

## 🎨 Available Design Styles
| Style | Description |
|-------|-------------|
| **Modern** | Clean lines, contemporary furniture, neutral palette |
| **Minimal** | "Less is more" - simple forms, clutter-free |
| **Luxury** | Elegant finishes, rich textures, sophisticated details |
| **Bohemian** | Eclectic, colorful, layered patterns and textures |
| **Industrial** | Raw elements, exposed materials, urban aesthetic |
| **Scandinavian** | Light, functional, cozy with natural elements |

## 🎬 Demo Videos

### Complete System Showcase
[![Room Redesign Demo](https://img.shields.io/badge/Watch-Video%20Showcase-red)](data/outputs/videos/room_redesign_showcase.mp4)
*Click the badge above to view the full system demonstration*

### Style Comparison Video
[![Style Comparison](https://img.shields.io/badge/Watch-Style%20Comparison-blue)](data/outputs/videos/style_comparison.mp4)
*See all 6 styles animated side-by-side*

### Image Slideshow
[![Slideshow](https://img.shields.io/badge/Watch-Image%20Slideshow-green)](data/outputs/videos/redesign_slideshow.mp4)
*Browse through all generated designs*

## 📁 Project Structure
room-redesign/
├── 01-depth-estimation/ # MiDaS depth map generation
├── 02-segmentation/ # DeepLabV3 object segmentation
├── 03-prompt-engineering/ # Style prompts (6 designs)
├── 04-image-generation/ # Stable Diffusion + ControlNet
├── 05-web-interface/ # Flask web application
├── data/
│ ├── inputs/ # Original room images (3 rooms)
│ └── outputs/
│ ├── images/
│ │ └── real_samples/ # 14 final images
│ └── videos/ # 3 demo videos
├── models/ # Downloaded AI models
├── utils/ # Helper functions
├── temp/ # Temporary processing files
├── venv/ # Python virtual environment
├── check_progress.py # Progress verification
├── create_style_placeholders.py
├── download_images.py
├── task4_video_generator.py # Video creation script
└── README.md

## 🎨 REAL AI-Generated Samples

Here are actual images generated using the **Stable Diffusion + ControlNet** pipeline with real room inputs:

### Original vs Redesigned Comparison

| Original Room | Depth Map | Modern Redesign |
|---------------|-----------|-----------------|
| ![Original](data/outputs/images/real_samples/original_room.jpg) | ![Depth Map](data/outputs/images/real_samples/depth_map.png) | ![Modern](data/outputs/images/real_samples/room_modern.jpg) |

### All 6 Design Styles (Generated from Same Room)

| Modern | Minimal | Luxury |
|--------|---------|--------|
| ![Modern](data/outputs/images/real_samples/room_modern.jpg) | ![Minimal](data/outputs/images/real_samples/room_minimal.jpg) | ![Luxury](data/outputs/images/real_samples/room_luxury.jpg) |

| Bohemian | Industrial | Scandinavian |
|----------|------------|--------------|
| ![Bohemian](data/outputs/images/real_samples/room_bohemian.jpg) | ![Industrial](data/outputs/images/real_samples/room_industrial.jpg) | ![Scandinavian](data/outputs/images/real_samples/room_scandinavian.jpg) |

### Additional Room Examples

**Room 2 - All Styles**
![Room 2 All Styles](data/outputs/images/real_samples/room2_comparison_grid.jpg)

**Room 3 - All Styles**
![Room 3 All Styles](data/outputs/images/real_samples/room3_comparison_grid.jpg)

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Language** | Python 3.11 | Core programming |
| **Deep Learning** | PyTorch, Transformers, Diffusers | AI model inference |
| **Depth Estimation** | MiDaS | Room geometry understanding |
| **Segmentation** | DeepLabV3 (ResNet101) | Object identification |
| **Image Generation** | Stable Diffusion + ControlNet | AI redesign |
| **Web Framework** | Flask | User interface |
| **Image Processing** | OpenCV, PIL | Image manipulation |
| **Video Processing** | OpenCV VideoWriter | Demo video creation |
| **Data Handling** | NumPy, Matplotlib | Arrays and visualization |

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.11 or higher
- Git
- 8GB+ RAM (16GB recommended)
- Internet connection for model downloads

### Installation Steps

1. **Clone the Repository**
```bash
git clone https://github.com/Muhammadlatifkhan/AI-projects.git
cd AI-projects/room-redesign

2.Create Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate

3.Install Dependencies
pip install -r requirements.txt

4.Run the Web Interface
cd 05-web-interface
python app.py

5.Access the Application
Open your browser and navigate to: http://localhost:5000

💡 How It Works
1.Upload a room image through the web interface

2.System Processes:

Generates depth map (01-depth-estimation)

Creates segmentation masks (02-segmentation)

Builds style prompts (03-prompt-engineering)

Produces 6 redesigned images (04-image-generation)

3.View Results in the interactive gallery (05-web-interface)

📊 Output Statistics

Metric	Count
Original Rooms Processed	3
Redesigned Images Generated	18 (3 rooms × 6 styles)
Demo Videos Created	3
Total Output Files	14 images + 3 videos
🏆 Key Achievements
✅ End-to-end pipeline from input to redesigned output

✅ 6 distinct design styles (exceeded requirement of 3)

✅ Real room images tested, not just ideal cases

✅ Video demonstrations for portfolio

✅ Clean modular architecture (5 independent components)

✅ Interactive web interface for easy use

🔮 Future Improvements
Video input support (process room walkthrough videos)

Object-specific editing (change only selected furniture)

Mobile-responsive web design

Batch processing for multiple rooms

More design styles (Art Deco, Mid-century, etc.)

👨‍💻 Author
Muhammad Latif
Computer Systems Engineer | AI Developer

GitHub: @Muhammadlatifkhan

LinkedIn: Muhammad Latif

Portfolio: AI Projects

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

🙏 Acknowledgments
MiDaS team for depth estimation models

DeepLabV3 for segmentation capabilities

Stable Diffusion and ControlNet communities

Open-source AI/ML community

<div align="center"> **⭐ Don't forget to star the repository if you found it useful! ⭐** </div> ```