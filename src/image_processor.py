from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import logging
import os

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self, width = 400, height = 300):
        
        self.width = width
        self.height = height
        logger.info(f"initializing image processor for {self.width} x {self.height} display")

    def process_image(self, image_path, dither_mode = "atkinson", contrast = 1.2, brightness = 1.0, sharpness = 1.0):
        '''
        different modes:
        floyd-steinberg -> smooth
        atkinson -> retro mac
        ordered -> pattern
        threshold -> no dithering
        '''

        try:
            logger.info(f"started processing image at {image_path}")

            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found at {image_path}")

            img = Image.open(image_path)
            logger.info(f"image loaded: {img.size}, mode:{img.mode}")

            if img.mode not in ("RGB", "L"):
                logger.info(f"converting img to rgb")
                img = img.convert("RGB")
            
            if img.width != 400 and img.height != 300:
                img = self.resize_maintain_aspect(img) # implment this function later lol
                logger.info(f"resized image") 

            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
                logger.info("applied contrast adjustment")
            
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
                logger.info("applied brightness adjustment")

            if sharpness != 1.0:
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(sharpness)
                logger.info("applied sharpness adjustment")

            img = img.convert("L")

            img = self.apply_dither(img, dither_mode) # implement this function later lol
            logger.info("applied dithering")

            logger.info("finished processing")
            return img
        except Exception as e:
            logger.error(f"Failed: {e}")
            raise

    def resize_maintain_aspect(self, img):
        img_ratio = img.width / img.height
        target_ratio = self.width / self.height
        
        if img_ratio > target_ratio: # this means taht the width is larger
            new_width = self.width
            new_height = int(self.width / img_ratio)
        else:
            new_height = self.height
            new_width = int(self.height * img_ratio)

        img = img.resize((new_width, new_height), Image.LANCZOS) #LANCZOS is a resampling algorihtm that reduces pixilation
        

        canvas = Image.new("RGB", (self.width, self.height), "white")
        offset_x = (self.width - new_width) // 2 # the 2 backslashes are for floor divison
        offset_y = (self.height - new_height) // 2
        canvas.paste(img, (offset_x, offset_y))

        return canvas
        
    def apply_dither(self, img, dither_mode):
        if dither_mode == "floyd-steinberg":
            return img.convert("1", dither=Image.FLOYDSTEINBERG)
        elif dither_mode == "atkinson": #do this later tspmo
            return self.atkinson_dither(img)
        elif dither_mode == "ordered":
            return img.convert("1", dither=Image.ORDERED)
        elif dither_mode == "threshold":
            return img.convert("1", dither=Image.NONE)
        
        else:
            logger.warning(f"{dither_mode} is unknown, using floyd-steinberg")
            return img.convert("1", dither=Image.FLOYDSTEINBERG)
    
    def atkinson_dither(self, img):
        img_array = np.array(img, dtype=float) # converts pil object to numpy array bc we are going to be doing some matrix math!
        height, width = img_array.shape # getting teh array dimensions (should be 300 x 400)

        """
        okay I should probably do an explination of what atkinson ditherign is
        like other dithering algorihtms, it attempts to show greyscale with only black and whtie

        algorithm in a nutshel:
        for every pixel:
            1. is this pixel closer to black or white
            2. what is the error of teh pixel and black or white
            3. spread teh error to nearby pixles
        
        so if we have a pixel x, the errror is spread in this matrix:

        [x    , 0.125, 0.125]
        [0.125, 0.125, 0.125]
        [0,   , 0.125, 0    ]
        """

        for y in range(height - 2):
            for x in range(1, width-2):
                old_pixel = img_array[y, x]
                new_pixel = 155 if old_pixel > 128 else 0
                img_array[y, x] = new_pixel # this chunk of code does the "closer to white or black" step

                error = (old_pixel - new_pixel) / 8 # finds the error we're spreading out

                if x+1 < width:
                    img_array[y, x+1] += error
                if x+2 < width:
                    img_array[y, x+2] += error
                if y+1 < height:
                    if x-1 > 0:
                        img_array[y+1, x-1] += error
                    img_array[y+1, x] += error
                    if x+1 < width:
                        img_array[y+1, x+1] += error
                if y+2 < height:
                    img_array[y+2, x] += error
                
            img_array = np.clip(img_array, 0, 255).astype("uint8")
            return Image.fromarray(img_array).convert("1")