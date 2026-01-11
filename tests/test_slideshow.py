import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from slideshow import Slideshow

def main():
    print("*" * 50)
    print("test slideshow")
    print("=" * 50)

    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    queue_dir = os.path.join(project_root, "images", "queue")

    slideshow = Slideshow (
        image_dir = queue_dir,
        loop = True
    )

    print("1. scanning iamges in queue")
    count = slideshow.scan_images()
    print(f"there are {count} images")

    if count == 0:
        print("no images, enter valid images")
        return

    print("3. resetting")
    slideshow.reset()
    img_path = slideshow.get_next_image()

    print(f"current position is {slideshow.get_current_index()} of {slideshow.get_image_count()}")

    print("*" * 50)
    print("test complete")
    print("*" * 50)

if __name__ == "__main__":
    main()

