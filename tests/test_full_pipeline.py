import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from display_controller import eink
from image_processor import ImageProcessor
import time
def main():
    print("*" * 50)
    print("lets see if the pipeline works")
    print("*"*50)

    image_path = os.path.join(os.path.dirme(__file__), "..", "images", "queue", "test.png")
    
    if not os.path.exists(image_path):
        print(f"error with test image with path {image_path}")
        return
    
    processor = ImageProcessor()
    display = eink()

    try:
        print("1. processing image")
        processed_image = processor.process_image(image_path, dither_mode = "atkinson", contrast = 1.3, brightness = 1.1, sharpness = 1.1)
        
        print("2. init display")
        display.init()
        display.clear()

        print("3. displaying image")
        display.display_image(processed_image)
        time.sleep(10)

        print("4. cleaning up")
        display.sleep()

        print("*" * 50)
        print("test successful")
        print("*" * 50)

    except Exception as e:
        print(f"failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if display.initialized:
            display.sleep()

if __name__ == "__main__":
    main()