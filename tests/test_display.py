import sys # imports python's system module allows us to access paths
import os # imports os module, allows us to move files accross paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

'''
this line does quite a bit:
__file__ is the location of this script
.. means go up one directory
lib means access lib folder
insert(0, ...) means that this is the first place python looks for imports

These together makes importing the waveshare library easier
'''

from waveshare_epd import epd4in2_V2 # imports e-ink lib
from PIL import Image, ImageDraw
import time

def main() :
    print("*" * 50)
    print("hello world! starting the test")
    print("*" * 50)

    epd = epd4in2_V2.EPD() # creates a display object

    try: # we're going to make a try catch block so that control c can stop this

        print("1. initializing display") 
        epd.init() # initializes e-ink

        print("2. clearnign display")
        epd.Clear() # clears display
        time.sleep(1) # mild sleep to allow clear to occur

        print("3. test >:)")
        image = Image.new("1", (400, 300), 255) # creates pillow image: 1 menas black and white, the tuple sets dimensions, and 255 makes the background white
        draw = ImageDraw.Draw(image) # creates drawing object
        draw.text((10, 10), "hello world!", fill=0) # the first tuple is the start xy cord, the string is the text, and the fill is color with 0 meaning black
        draw.text((10, 40), "prize pics", fill = 0)
        draw.text((10, 70), "cool", fill = 0)
        draw.rectangle((10, 100, 100, 150), outline = 0, width = 3) # the 4-tuple is the corners: first is the top left, second is the bottom left
        draw.ellipse((120, 100, 170, 390), outline = 0, width = 5)
        draw.line((10, 170, 390, 290), fill = 0, width = 6)

        print("4. displaying image")
        epd.display(epd.getbuffer(image)) # converts image object to a byte buffer

        print("5. display will be here for 5 whole seconds")
        time.sleep(5)

        print("6. putting display to sleep")
        epd.sleep()

        print("*" * 50)
        print("done!")
        print("*" * 50)

    except KeyboardInterrupt:
        print(" \n keyboard inturrupt")
        epd.sleep()

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        epd4in2_V2.epdconfig.module_exit(cleanup=True)
    
if __name__ == "__main__":
    main()
