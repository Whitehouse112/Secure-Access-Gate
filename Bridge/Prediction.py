import cv2
import imutils
import pytesseract
import numpy as np
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def prediction(img):

    # Apro il file di configurazione e leggo il parametro [PORTA]
    filename = f"{dir_path}\\files\\config.txt"
    file = open(filename, 'r')
    lang= file.readline().split(',')[1]
    file.close()

    img = cv2.resize(img, (600,400) )
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Applico il filtro bilaterale per rimuovere il rumore ed i dettagli dell'immagine
    gray = cv2.bilateralFilter(gray, 13, 15, 15) 

    # Calcolo gli edge ed i contorni
    edged = cv2.Canny(gray, 30, 200) 
    contours = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]

    possible_plates = []
    plate = []
    # Salvo solo i rettangoli
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        
        if len(approx) == 4:
            possible_plates.append(approx)
            #cv2.drawContours(img, [approx], -1, (0, 0, 255), 3)

    if len(possible_plates) != 0:
        bottom = 400
        
        # Prendo in considerazione solo il rettangolo più in basso nell'immagine
        for i, plate in enumerate(possible_plates):
            if (min(possible_plates[i][:,:,1] < bottom)):
                bottom = min(possible_plates[i][:,:,1])
                plate = possible_plates[i]
        
        # Disegno i contorni sull'immagine
        cv2.drawContours(img, [plate], -1, (0, 0, 255), 3)
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[plate],0,255,-1,)
        new_image = cv2.bitwise_and(img,img,mask=mask)

        # Estraggo solo l'immagine della targa
        (x, y) = np.where(mask == 255)
        (topx, topy) = (np.min(x), np.min(y))
        (bottomx, bottomy) = (np.max(x), np.max(y))
        Cropped = gray[topx:bottomx+1, topy:bottomy+1]

        # Riconoscimento del testo tramite tesseract
        text = pytesseract.image_to_string(Cropped, lang=lang, config='--psm 7')      

        cv2.imshow('Cropped',Cropped)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return checkText(text)
    else:
        return None


def checkText(text):

    tmp = ""
    
    text = text.split('\n')[0]
    for character in text:
        if character.isalnum():
            plate += character
    if len(plate) == 7:
        return plate
    else:
        return None