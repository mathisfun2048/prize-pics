import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from transfer import ImageTransfer
from slideshow import Slideshow

def main():
    print("*" * 50)
    print("testing trasnfer FINAL FUNCTION YAY")
    print("*" * 50)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    queue_dir = os.path.join(project_root, "images", "queue")
    processed_dir = os.path.join(project_root, "images", "processed")

    slideshow = Slideshow(image_dir = queue_dir)
    transfer = ImageTransfer(queue_dir = queue_dir, processed_dir = processed_dir)

    print("1. scanning images")
    count = slideshow.scan_images()
    print(f"found {count} images")

    if count == 0:
        print("no images found :(")
        return
    
    print("2. processing first image")
    img_path = slideshow.get_next_image()
    
    processed = transfer.get_processed_image(img_path)
    
    print("3. processing same image using cache")
    processed2 = transfer.get_processed_image(img_path)

    print(f"4. cache location at {processed_dir}")
    cache_files = os.listdir(processed_dir)
    

    print("5. test cache clearning?")
    response = input("> ").strip().lower()
    if response == "y":
        cleared = transfer.clear_cache()
    
    print("*" * 50)
    print("transfer test done :p")
    print("*" * 50)

if __name__ == "__main__":
    main()

