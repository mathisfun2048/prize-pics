import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from image_processor import ImageProcessor
from PIL import Image, ImageDraw

def create_test_image():
    img = Image.new("RGB", (800, 600), "white")
    draw = ImageDraw.Draw(img) 
    
    for i in range(256):
        gray = i
        draw.rectangle([(i*3, 0), (i*3+3, 200)], fill=(gray, gray, gray))
    draw.text((50, 250), "testing!", fill = "black")
    draw.elipse([(50, 300), (250, 500)], fill = "gray")
    draw.rectangle([(300, 300), (500, 500)], fill = "darkgray")

    test_img_path = os.path.join(os.path.dirname(__file__), "..", "images", "test_gradient.png")
    os.makedirs(os.path.dirname(test_img_path), exist_ok=True) # makes sure output directory exists before saving
    img.save(test_img_path)
    return test_img_path


def main():
    print("*" * 50)
    print("testing image processor")
    print("*" * 50)


    processor = ImageProcessor()

    print("1. creating test image")
    test_img = create_test_image()
    print("test image created")

    dither_modes = ["floyd-steinberg", "atkinson", "ordered", "threshold"]

    for mode in dither_modes:
        print(f"2. Testing {mode}")
        try:
            processed = processor.process_image(test_img, dither_mode = mode, contrast = 1.3, brightness = 1.1, sharpness = 1.2)

            output_path = os.path.join(os.path.dirname(__file__), '..', 'images', f'processed_{mode}.png')
            processed.save(output_path)
            print(f"saved: {output_path}")
        except Exception as e:
            print(f"failed: {e}")

    print("*" * 50)
    print("test succesful. trasnfromed images in teh /images directory")
    print("*" * 50)

if __name__ == "__main__":
    main()