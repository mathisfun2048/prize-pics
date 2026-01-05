# Tests Readme

This is just documentation for all the tests so that you can troubleshoot as needed

## test_display.py

### What it Does
This tests the basic e-ink functionality. This is more lightweight than the defult epd test, which is why I wrote it. 

### What it Tests

This tests initialization, clearing, drawing, and sleep

Make sure that you have the dependencies installed beforehand. There is documentation for that under firmware_instructions.md

### Running It

on terminal, go to the test directory

then run

```
sudo python3 test_display.py
```

we need sudo bc of gpio permissions

### Expected output

<img width="633" height="576" alt="Screenshot 2026-01-05 at 3 23 52 PM" src="https://github.com/user-attachments/assets/b06bf7da-ed32-4f1a-969a-63acabb75550" />
