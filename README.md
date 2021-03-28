# Secure-Access-Gate
IoT project for a secure access gate system

## Requirements
- imutils
- numpy==1.18.4
- opencv-python==4.2.0.34
- Pillow
- pyserial
- pytesseract

# Installation
In order to let the project works, users must:

+ ARDUINO
    - upload the Arduino.ino file to esp32-cam
    - connect E18-D80NK sensor to esp32-cam (blue=gnd, brown=5V, black=GPIO13)
    - start esp32-cam and pair to pc with bluetooth (outgoing COM port must be annoteted)
+ BRIDGE
    - install tesseract (https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe)
    - download the desired tesseract language (https://github.com/tesseract-ocr/tessdata) and put the .traineddata file into /Tesseract-OCR/tessdata installation folder
    - create a config.txt file in the root/Bridge/files project's folder (usage: "outgoing COM port, language". Es: "COM4,ita")

## Directories structure
+ root/
    + Arduino/   
        - Arduino.ino
        - camera_pins.h
    + Backend
    + Bridge
        + files/
            - config.txt
        - Bridge.py
        - main.py
        - Prediction.py
    - .gitignore
    - README.md