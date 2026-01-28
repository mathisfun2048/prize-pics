# src/main.py

import sys
import os
import json
import time
import signal
import logging
from pathlib import Path
import RPi.GPIO as GPIO
import json

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from display_controller import EInkDisplay
from image_processor import ImageProcessor
from slideshow import Slideshow
from transfer import ImageTransfer

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('picture_frame.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class PictureFrame:
    """
    Main picture frame application
    Coordinates all components to display a slideshow on e-ink
    """
    
    def __init__(self, config_path='config/settings.json'):
        """
        Initialize the picture frame
        
        Args:
            config_path: Path to configuration file
        """
        logger.info("=" * 60)
        logger.info("E-Ink Picture Frame Starting")
        logger.info("=" * 60)
        
        # Load configuration
        self.config = self._load_config(config_path)
        
        # Get project root
        project_root = Path(__file__).parent.parent
        
        # Initialize components
        queue_dir = project_root / self.config['directories']['queue']
        processed_dir = project_root / self.config['directories']['processed']
        
        self.slideshow = Slideshow(
            image_dir=str(queue_dir),
            loop=self.config['display']['loop']
        )
        
        self.transfer = ImageTransfer(
            queue_dir=str(queue_dir),
            processed_dir=str(processed_dir),
            dither_mode=self.config['processing']['dither_mode'],
            contrast=self.config['processing']['contrast'],
            brightness=self.config['processing']['brightness'],
            sharpness=self.config['processing']['sharpness']
        )
        
        self.display = EInkDisplay()
        
        self.running = False
        self.interval = self.config['display']['interval_seconds']
        
        # Button setup (GPIO 18, physical pin 12)
        self.button_pin = 18
        self.button_initialized = False
        
        # Setup signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("Picture frame initialized")
    
    def _load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            # Get absolute path relative to project root
            project_root = Path(__file__).parent.parent
            config_file = project_root / config_path
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            logger.info(f"Configuration loaded from {config_path}")
            return config
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            raise
    
    def _setup_button(self):
        """Simple button setup with polling"""
        try:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            self.button_initialized = True
            logger.info(f"Button setup complete on GPIO {self.button_pin}")
        except Exception as e:
            logger.error(f"Failed to setup button: {e}")
            logger.warning("Continuing without button functionality")
    
    def _is_button_pressed(self):
        """Check if button is currently pressed"""
        if not self.button_initialized:
            return False
        # Button connects to ground, so pressed = LOW (0)
        return GPIO.input(self.button_pin) == 0
    
    def start(self):
        """Start the picture frame slideshow"""
        try:
            # Initialize display
            logger.info("Initializing display...")
            self.display.init()
            
            if self.config['startup']['clear_display_on_start']:
                logger.info("Clearing display...")
                self.display.clear()
            
            # Setup button
            self._setup_button()
            
            # Scan for images
            logger.info("Scanning for images...")
            image_count = self.slideshow.scan_images()
            logger.info(f"Found {image_count} images in queue")
            
            if image_count == 0:
                logger.error("No images found in queue. Add images and restart.")
                self.display.sleep()
                return
            
            # Optional: Preprocess all images on startup
            if self.config['startup']['preprocess_on_start']:
                logger.info("Preprocessing all images...")
                all_images = [
                    self.slideshow.get_next_image() 
                    for _ in range(image_count)
                ]
                self.slideshow.reset()
                self.transfer.preprocess_all(all_images)
            
            # Start slideshow loop
            self.running = True
            self._run_slideshow()
            
        except Exception as e:
            logger.error(f"Error starting picture frame: {e}", exc_info=True)
            self.shutdown()
    
    def _save_state(self, current_image):
        """Save current state for web UI"""
        try:
            state_file = Path(__file__).parent.parent / 'current_state.json'
            with open(state_file, 'w') as f:
                json.dump({
                    'current_image': str(current_image),
                    'timestamp': time.time()
                }, f)
        except Exception as e:
            logger.error(f"Failed to save state: {e}")



    def _run_slideshow(self):
        """Main slideshow loop"""
        logger.info("Starting slideshow loop")
        logger.info(f"Image interval: {self.interval} seconds")
        if self.button_initialized:
            logger.info(f"Press button on GPIO {self.button_pin} to skip to next image")
        
        while self.running:
            try:
                # Rescan for new images every loop iteration
                current_count = self.slideshow.get_image_count()
                new_count = self.slideshow.scan_images()
                if new_count != current_count:
                    logger.info(f"Found {new_count - current_count} new images!")
        
                # Get next image
                image_path = self.slideshow.get_next_image()
                
                if not image_path:
                    logger.warning("No more images, stopping")
                    break
                
                logger.info(f"Displaying: {Path(image_path).name}")
                
                # Process image
                processed_img = self.transfer.get_processed_image(image_path)
                
                # Display on e-ink
                self.display.display_image(processed_img)
                logger.info(f"Image {self.slideshow.get_current_index()}/{self.slideshow.get_image_count()} displayed")
                logger.info(f"Waiting {self.interval} seconds until next image...")
                
                # Save current state for web UI
                self._save_state(image_path)
                logger.info(f"Image {self.slideshow.get_current_index()}/{self.slideshow.get_image_count()} displayed")
                


                # Wait for interval, checking button every second
                for i in range(self.interval):
                    if not self.running:
                        break
                    
                    # Check if button is pressed
                    if self._is_button_pressed():
                        logger.info("Button pressed - skipping to next image!")
                        time.sleep(0.3)  # Simple debounce - wait for release
                        break
                    
                    time.sleep(1)
                
            except KeyboardInterrupt:
                logger.info("Keyboard interrupt received")
                break
            except Exception as e:
                logger.error(f"Error in slideshow loop: {e}", exc_info=True)
                logger.info("Waiting 10 seconds before retry...")
                time.sleep(10)
        
        self.shutdown()
    
    def shutdown(self):
        """Clean shutdown of picture frame"""
        logger.info("Shutting down picture frame...")
        self.running = False
        
        try:
            if self.button_initialized:
                GPIO.cleanup(self.button_pin)
                logger.info("Button GPIO cleaned up")
        except Exception as e:
            logger.error(f"Error cleaning up button: {e}")
        
        try:
            self.display.sleep()
            logger.info("Display put to sleep")
        except Exception as e:
            logger.error(f"Error during display shutdown: {e}")
        
        logger.info("=" * 60)
        logger.info("Picture frame stopped")
        logger.info("=" * 60)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}")
        self.shutdown()
        sys.exit(0)


def main():
    """Entry point for picture frame application"""
    try:
        frame = PictureFrame()
        frame.start()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()