# Tests Readme

This is just documentation for all the tests so that you can troubleshoot as needed

for running thise, make sure you're on the test directory


## test_display.py

### What it Does
This tests the basic e-ink functionality. This is more lightweight than the defult epd test, which is why I wrote it. 

### What it Tests

This tests initialization, clearing, drawing, and sleep

Make sure that you have the dependencies installed beforehand. There is documentation for that under firmware_instructions.md

### Running It

```
sudo python3 test_display.py
```

### Expected output

<img width="633" height="576" alt="Screenshot 2026-01-05 at 3 23 52 PM" src="https://github.com/user-attachments/assets/b06bf7da-ed32-4f1a-969a-63acabb75550" />

## test_button.py

## What it Does
This tests the functionality of the button. Its an easy way to test if you soldered everything correctly. 

### What it tests
This tests the button. 

### Running it

```
sudo python3 test_button.py
```


### Expected Output

<img width="379" height="204" alt="Screenshot 2026-01-05 at 4 58 10 PM" src="https://github.com/user-attachments/assets/4879593d-c91b-4fdc-9ec9-42ed38131942" />

## test_display_controller.py

### What it Does
This tests if the class is properly wrapping the e-ink. 

### What it tests
This tests the wrapper class, which makes interacting with the e-ink easier. 

### Running it

```
sudo python3 test_display_controller.py
```

### Expected Output

this on the e-ink:

<img width="633" height="576" alt="Screenshot 2026-01-05 at 3 23 52 PM" src="https://github.com/user-attachments/assets/b06bf7da-ed32-4f1a-969a-63acabb75550" />


this on the terminal:


