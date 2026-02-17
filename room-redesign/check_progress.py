import os
import time

def check_progress():
    images_folder = "data/outputs/images"
    
    while True:
        if os.path.exists(images_folder):
            images = os.listdir(images_folder)
            print(f"\r📸 Images generated: {len(images)}/18", end="")
        
        time.sleep(5)

if __name__ == "__main__":
    check_progress()