import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src")) # tells where to find display_controller

from display_controller import eink
from PIL import Image, ImageDraw
import time

def main():
    print("*" * 50)
    print("testing display controller >:)")
    print("*" * 50)

    display = eink()

    try:
        print("1. init display")
        display.init()

        print("2. clear")
        display.clear()
        time.sleep(2) # mild sleep to see if clearing works

        print("3. create test")
        img = Image.new('1', (400, 300), 255)
        draw = ImageDraw.Draw(img)

        draw.text((10, 10), "hello world!", fill=0) # the first tuple is the start xy cord, the string is the text, and the fill is color with 0 meaning black
        draw.text((10, 40), "prize pics", fill = 0)
        draw.text((10, 70), "*" * 380 , fill = 0)
        draw.rectangle((10, 100, 100, 290), outline = 0, width = 3) # the 4-tuple is the corners: first is the top left, second is the bottom left
        draw.ellipse((120, 100, 390, 290), outline = 0, width = 5)
        draw.line((10, 170, 390, 290), fill = 0, width = 6)


        print("4. display test")

        display.display_image(img)
        time.sleep(5) #time to make sure it draws

        print("5. sleep")
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


        