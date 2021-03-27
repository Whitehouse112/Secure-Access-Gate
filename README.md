# Secure-Access-Gate
IoT project for a secure access gate system

## Requirements
- Pillow
- pyserial
- numpy==1.18.4
- opencv-python==4.2.0.34
- matplotlib
- scikit-image==0.17.2
- scikit-learn==0.23.1

## Directories structure
+ root/
    + Arduino/   
        - Arduino.ino
        - camera_pins.h
    + Backend
    + Bridge
        + files/
            - config.txt
            - model.sav
        - Bridge.py
        - Detection.py
        - main.py
        - Prediction.py
        - Segmentation.py
        - Training.py
    + train
    - .gitignore
    - README.md
