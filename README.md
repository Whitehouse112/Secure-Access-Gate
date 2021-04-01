# Secure-Access-Gate
IoT project for a secure access gate system

## Requirements
- imutils
- keras
- numpy==1.18.4
- opencv-python==4.2.0.34
- Pillow
- pyserial
- pytesseract
- tensorflow

# Installation
In order to let the project work, users must:

+ ARDUINO
    - setup Arduino IDE for esp32 (https://mega.nz/folder/QFRXRKLA#6BQIcx_SrRIX9Igr5w6XsA/file/NdxTlY7R - page 1 to 4)
    - upload the Arduino.ino file to esp32-cam
    - connect E18-D80NK sensor to esp32-cam (blue=gnd, brown=5V, black=GPIO13)
    - connect lcd 7-segment 5161AS to esp32-cam (https://www.circuitbasics.com/arduino-7-segment-display-tutorial/ - E_segment=GPIO12, G_segment=GPIO2)
    - start esp32-cam and pair to pc with bluetooth (outgoing COM port must be annotated)

+ BRIDGE
    - install tesseract (https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe)
    - download the desired tesseract language (https://github.com/tesseract-ocr/tessdata) and put the .traineddata file into /Tesseract-OCR/tessdata installation folder
    - create a config.txt file in the root/Bridge/files project's folder (usage: "outgoing COM port, language". Es: "COM5,ita")

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
