import os
from pathlib import Path
import logging
import hashlib
from PIL import Image

try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
    HEIC_SUPPORTED = True
except ImportError:
    HEIC_SUPPORTED = False
    logging.warning("heif not installed, heif not supported")

from image_processor import ImageProcessor

logger = logging.getLogger(__name__)

class ImageTransfer:
    def __init__(self, queue_dir = "images/queue", processed_dir = "images/processed", dither_mode = "atkinson", contrast = 1.2, brightness = 1.0, sharpness = 1.0):

        self.queue_dir = Path(queue_dir)
        self.processed_dir = Path(processed_dir)
        self.processor = ImageProcessor()
        self.dither_mode = dither_mode
        self.contrast = contrast
        self.brightness = brightness
        self.sharpness = sharpness


        self.processed_dir.mkdir(parents = True, exist_ok = True)

        logger.info("image transfer initialized!")


    def get_processed_image(self, source_path):
        
        cache_filename = self._get_cache_filename(source_path)
        cache_path = self.processed_dir / cache_filename

        if cache_path.exists():
            source_mtime = source_path.stat().st_mtime
            cache_mtime = cache_path.stat().st_mtime

            if cache_mtime >= source_mtime:
                logger.info("using cached processed iamge")
                return Image.open(cache_path)
            else:
                logger.info("cached outdated, reproducing")
        else:
            logger.info("processing new image")
        
        processed_img = self.processor.process_image(
            str(source_path),
            dither_mode = self.dither_mode,
            contrast = self.contrast,
            brightness = self.brightness,
            sharpness = self.sharpness
        )

        processed_img.save(cache_path)
        logger.info("cached processed image)")

        return processed_img
    
    def _get_cache_filename(self, source_path):
        
        source_name = source_path.name
        name_hash = hashlib.md5(source_name.encode()).hexdigest()[:8]

        cache_name = f"{source_path.stem}_{name_hash}.png"

        return cache_name
    
    
    def clear_cache(self):
        count = 0
        for cache_file in self.processed_dir.glob("*.png"):
            cache_file.unlink()
            count += 1
        
        logger.info("cleared cache")
        return count
    
    def preprocess_all(self, image_paths): #I want everything processed so that it is easeir haha
        logger.info("preprocessing :p")

        for i, img_path in enumerate(image_paths):
            try:
                self.get_processed_image(img_path)
            except Exception as e:
                logger.error(f"failed: {e}")
        
        logger.info("finished processing")
