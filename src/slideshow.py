import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class Slideshow:

    def __init__ (self, image_dir = "images/queue", loop = True):
        self.image_dir = Path(image_dir)
        self.loop = loop
        self.image_list = []
        self.current_index = 0

        logger.info(f"slideshow initilaizied, directory = {image_dir}")

    def scan_images(self):
        valid_extensions = {".jpg", ".jpeg", ".png", ".heic"}

        if not self.image_dir.exists():
            logger.warning(f"image directory at {self.image_dir} does not exist")
            self.image_dir.mkdir(parents = True, exist_ok = True) #creates directory if not there, but if it is there we don't crash the program 
            return 0

        self.image_list = [
            f for f in self.image_dir.iterdir()
            if f.is_file() and f.suffix.lower() in valid_extensions
        ]

        self.image_list.sort()

        logger.info(f"scanned {len(self.image_list)} images from {self.image_dir}")

        return len(self.image_list)
    

    def get_next_image(self):

        if not self.image_list:
            self.scan_images()

        if not self.image_list:
            logger.warning("no images in queue")
            return None
        
        image_path = str(self.image_list[self.current_index])

        self.current_index += 1

        if self.current_index >= len(self.image_list):
            if self.loop:
                logger.info("looping back to start")
                self.current_index = 0
            else:
                logger.info("done with images!")
                return None
        
        return image_path
    
    def reset(self):
        self.current_index = 0
        logger.info("slideshow reset")

    def get_image_count(self):
        return len(self.image_list)
    
    def get_current_index(self):
        return self.current_index