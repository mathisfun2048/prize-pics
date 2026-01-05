import RPi.GPIO as GPIO
import time

BUTTON_GPIO = 18

def main():
    print("*" * 50)
    print("test button")
    print("*" * 50)

    GPIO.setwarnings(False) # dispables warning messages
    GPIO.setmode(GPIO.BCM) # sets numbring mode to broadcom; uses gpio nums instead of physical pin
    GPIO.setup(BUTTON_GPIO, GPIO.IN, pull_up_down = GPIO.PUD_UP) # sets button as input, enables pull up resistor
    '''
    our button is connected from gpio 18 -> ground

    if we enable a pull up resistor, our pin reads high by defult
    when we press the button, the current flows from high to ground, so teh pin reads low
    '''

    print(f"\n testing on gpio {BUTTON_GPIO}")
    print("button connects to ground when pressed")
    

    try:
        press_count = 0
        while True:
            if GPIO.input(BUTTON_GPIO) == 0:
                press_count += 1
                print(f"Button pressed, count: {press_count}")
                time.sleep(0.3) #this is for debounce
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("*" * 50)
        print(f"test complete. total presses: {press_count}")
        print("*" * 50)

    finally:
        GPIO.cleanup(BUTTON_GPIO)

if __name__ == "__main__":
    main()