import Bridge
import Detection
import Segmentation
import Prediction

def main():

    ser = Bridge.setup()

    while (True):
        img = Bridge.loop(ser)
        if (img != None):
            possible_plates = Detection.detection(img)
            if (len(possible_plates) != 0):
                chars, x_chars = Segmentation.segmentation(possible_plates)
                if (len(possible_plates) != 0):
                    model = Prediction.setup()
                    plate = Prediction.prediction(model, chars, x_chars)

if __name__ == '__main__':
    main()