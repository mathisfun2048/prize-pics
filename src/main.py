import sys
import os
import json
import time
import signal
import logging
from pathlib import Path
import RPi.GPIO as GPIO


sys.path.insert(0, os.path.dirname(__file__))

from display_controller import eink
from image_processor import ImageProcessor
from slideshow import Slideshow
from transfer import ImageTransfer

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime_s - %(name)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler("prize-pics.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class prize_pics:

    def __init__(self, config_path = "config/settings.json"):
        logger.info("*" * 50)
        logger.info("prize pics starting")
        logger.ifno("*" * 50)

        self.config = self._load_config(config_path)
        project_root = Path(__file__).parent.parent

        queue_dir = project_root / self.config["directories"]["queue"]
        processed_dir = project_root / self.config["directories"]["processed"]

        self.slideshow = Slideshow(
            image_dir = str(queue_dir)
            loop = self.config["display"]["loop"]
        )

        self.transfer = ImageTransfer(
            queue_dir = str(queue_dir),
            processed_dir = str(processed_dir),
            dither_mode = self.config["processing"]["dither_mode"],
            contrast = self.config["processing"]["contrast"],
            brightness = self.config["processing"]["brightness"],
            sharpness = self.config["processing"]["sharpness"]
        )

        self.display = eink()

        self.running = False
        self.interval = self.config["display"]["interval_seconds"]

        self.button_gpio = 18
        self.button_initialized = False

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        logger.info("initialized")


    def _load_config(self, config_path):
        
        try:
            project_root = Path(__file__).parent.parent
            config_file = project_root / config_path

            with open(config_file, "r") as f:
                config = json.load(f)
            logger.info("config loaded")
            return config
        except FileNotFoundError:
            logger.error("config file not found")
            raise
        except json.JSONDecoderError as e:
            logger.error(f"failed decoding json: {e}")
            raise

    def _setup_button(self):
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
            self.button_initialized = True
            logger.info("button setup done")
        except Exception as e:
            logger.error("failed: {e}")
            logger.warning("we'll continue bu tbutton won't work")

    def _is_button_pressed(self):
        if not self.button_initialized:
            return False
        
        return GPIO.input(self.button_pin) == 0
    
    def start(self):
        try:
            logger.info("trying to start")
            self.display.init()

            if self.config["startup"]["clear_display_on_start"]:
                self.display.clear()

            self._setup_button()

            image_count = self.slideshow.scan_images()

            if image_count == 0:
                logger.error("no images in queue")
                self.display.sleep()
                return
            
            if self.config["startup"]["preprocess_on_start"]:
                all_images = [
                    self.slideshow.get_next_image()
                    for _ in range(image_count)
                ]

                self.slideshow.reset()
                self.transfer.preprocess_all(all_images)

            self.running = True
            self._run_slideshow()

        except Exception as e:
            logger.error(f"failed: {e}", exc_info = True)
            self.shutdown()


    def _save_state(self, current_image):
        try:
            state_file = Path(__file__).parent.parent / "current_state.json"
            with open(state_file, "w") as f:
                json.dump({
                    "curreont_image": str(current_image),
                    "timestamp": time.time()
                }, f)
        except Exception as e:
            logger.error(f"failed: {e}")
    
    def _run_slideshow(self):
