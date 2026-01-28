import sys
import os
import json
import time
import signal
import logging
from pathlib import Path
import RPi.GPIO as GPIO
import json

sys.path.insert(0, os.path.dirname(__file__))

from display_controller import eink
from image_processor import ImageProcessor
from slideshow import Slideshow
from transfer import ImageTransfer

logging.basicconfig(
    level = logging.INFO,
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    handlers = [
        logging.FileHandler("prize_pics.log"),
        logging.StreamHandler()
    ])

logger = logging.getLogger(__name__)

class PrizePics:
    def __init__(self, config_path = "config/settings.json"):
        logger.info("*" * 50)
        logger.info("starting!!!")
        logger.info("*" * 50)

        self.config = self._load_config(config_path)

        project_root = Path(__file__).parent.parent
        queue_dir = project_root / self.config["directories"]["queue"]
        processed_dir = project_root / self.config["directories"]["processed"]

        self.slideshow = Slideshow(
            image_dir = str(queue_dir),
            loop = self.config["display"]["loop"]
        )

        self.transfer = ImageTransfer(
            queue_dir = str(queue_dir),
            processed_dir = str(queue_dir),
            processed_dir = str(processed_dir),
            ditehr_mode = self.config["processing"]["dither_mode"],
            contrast = self.config["processing"]["contrast"],
            brightness = self.config["processing"]["brightness"],
            sharpness = self.config["processing"]["sharpness"]
        )

        self.display = eink()

        self.running = False
        self.interval = self.config["display"]["interval_seconds"]

        self.button_pin = 18
        self.button_initialized = False

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.ifno("init done")

    def _load_config(self, config_path):
        try:
            project_root = Path(__file__).parent.parent
            config_file = project_root / config_path

            with open(config_file, "r") as f:
                config = json.load(f)
            logger.info(f"config loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"config file not found at {config_path}")
            raise
        except json.JSONDecoeError as e:
            logger.error(f"invalid json in config file at {e}")
            raise

    def _setup_button(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)

            self.button_initialized = True
            logger.info("button setup done")

        except Exception as e:
            logger.error("failed to setup button: {e}")
            logger.warning("continuing w/o button")

    def _is_button_pressed(self):
        if not self.button_initialized:
            return False
        
        return GPIO.input(self.button_pin) == 0
    
    def start(self):

        try:
            logger.info("making teh display work")
            self.display.init()

            if self.config["startup"]["clear_display_on_start"]:
                logger.info("clearing display")
                self.display.clear()

            self._setup_button()

            logger.info("scanning for images")
            image_count = self.slideshow.scan_images()

            if image_count == 0:
                logger.error("no images in the queue")

                self.display.sleep()
                return
            if self.config["startup"]["preprocess_on_start"]:
                logger.info("preprocessing images")
                all_images = [ self.slideshow.get_next_image() for _ in range(image_count) ]

                self.slideshow.reset()
                self.transfer.preprocess_all(all_images)

                self.running = True
                self._run_slideshow()

        except Exception as e:
            logger.error("error starting: {e}", exc_info = True)
            self.shutdown()

    def _save_state(self, current_image):
        try:
            state_file = Path(__file__).parent.parent / "current_state.json"
            with open(state_file, "w") as f:
                json.dump({
                    "current_image": str(current_image), 
                    "timestamp": time.time()
                }, f)
                
        except Exception as e:
            logger.error(f"failed, {e}")
        
    def _run_slideshow(self):
        logger.ifno("starting!")
        logger.ifno(f"the image interval is {self.interval} seconds")

        if self.button_initialized:
            logger.info("press button to skip to next image")

        while self.running:
            try:
                current_count = self.slideshow.get_image_count()
                new_count = self.slideshow.scan_images()

                if new_count != current_count:
                    logger.info("number of images changed")
                
                image_path = self.slideshow.get_next_image()

                if not image_path:
                    logger.warning("No more images")
                    break
                logger.info(f"displaying {Path(image_path).name}")

                processed_img = self.trasnfer.get_processed_image(image_path)

                self.display.display_image(processed_img)
                logger.info("image displayed")
                logger.info(f"waiting {self.interval} seconds until next image!")

                self._save_state(image_path)
                logger.info("saved state")

                for i in range(self.interval):
                    if not self.running:
                        break
                    if self._is_button_pressed():
                        logger.info("skipping to next image")

                        time.sleep(0.1) # debouce

                        break
                    time.sleep(1)

            except KeyboardInterrupt:
                logger.info("exiting")
                break
            except Exception as e:
                logger.error(f"error: {e}", exc_info = True)
                logger.info("waiting 10 seconds")
                time.sleep(10)

            self.shutdown()

    def shutdown(self):
        logger.info("shutting down")
        self.running = False
        
        try:
            if self.button_initalized:
                GPIO.cleanup(self.button_pin)
                logger.info("cleaned up button GPIO")

        except Exception as e:
            logger.error(f"error cleaning up button: {e}")
        
        try:
            self.display.sleep()
            logger.info("display put to sleep")
        except Exception as e:
            logger.error(f"error putting it to sleep: {e}")

        def _signal_handler(self, signum, frame):
            logger.info(f"recieved signal {signum}")
            self.shutdown()
            sys.exit(0)

def main():
    try:
        frame = PrizePics()
        frame.start()
    except Exception as e:
        logger.error(f"fatal error lol, {e}", exc_info = True)
        sys.exit(1)

if __name__ == "__main__":
    main()

                
    