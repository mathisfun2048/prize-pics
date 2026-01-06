import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))

from waveshare_epd import epd4in2_V2
from PIL import Image
import logging

logging.basicConfig(level=logging.INFO) # configs logging and sets minimum severity -> will hide debug
logger = logging.getLogger(__name__) # creates logging object and allows identify which file raised the logger

class eink:
    def __init__(self): #constructor for the wrapper class
        self.epd = None #initializes empty instance variable
        self.width = 400
        self.height = 300
        self.initialized = False
        logger.info("controller created")
    
    def init(self):
        try:
            if not self.EPD:
                self.epd = epd4in2_V2.EPD()
            
            logger.info("initalizing")
            self.epd.init()
            self.initialized = True
            logger.info("initialized e-paper")

        except Exception as e:
            logger.error(f"failed: {e}")
            raise

    def clear(self):
        try:
            if not self.initialized:
                logger.warning("display not initalized. initilizing now")
                self.init()
             
            logger.info("clearning")
            self.epd.Clear()
            logger.info("cleared")

        except Exception as e:
            logger.error(f"failed: {e}")
            raise

    def display_image(self, pil_image):
        try:
            if not self.initialized:
                logger.warning("display not initalized. initilizing now")
                self.init()
            
            if pil_image.size != (self.width, self.height):
                logger.warning(f"image size {pil_image.size} is not the display size, {self.width} x {self.height}. images should be resized")

                raise ValueError(f"image must be {self.width} x {self.height}, not {pil_image.size}")
            
            if pil_image.mode != "1":
                logger.warning(f"converting image from {pil_image.mode} to 1 bit")
                pil_image = pil_image.convert("1")

            
            logger.info("sending image")

            buffer = self.epd.getbuffer(pil_image)

            self.epd.display(buffer)
            logger.info("image displayed")

        except Exception as e:
            logger.error(f"failed: {e}")
            raise
            
    def sleep(self):

        try:
            if self.epd and self.initialized:
                logger.info("going to sleep")
                self.epd.sleep()
                self.initialized = False
                logger.info("now asleep")

            else:
                logger.warning("display not initialized, cannot put to sleep")
        except Exception as e:
            logger.error("failsed: {e}")
            raise

    def __del__(self):
        try:
            if self.initialized:
                logger.info("activating destructor")
                self.sleep
            if self.epd:
                epd4in2_V2.epdconfig.module_exit(cleanup=True)
                logger.info("destruction done")
        except Exception as e:
            logger.error(f"failed: {e}")