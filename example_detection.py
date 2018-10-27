import cv2
import numpy as np
from shapedetector import ShapeDetector
from imutils.object_detection import non_max_suppression
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import cv2
from itertools import groupby

def detector(img, model):

    sign_dict = {0: 'a_unevenness',
                 1: 'no_drive',
                 2: 'no_entry',
                 3: 'none',
                 4: 'parking',
                 5: 'pedistrain',
                 6: 'road_works',
                 7: 'stop',
                 8: 'way_out'}

    img_rgb = img.copy()
    img_rgb = img_rgb[100:,:]

    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    res = img_rgb.copy()
    gray = img[100:,:]
    mser = cv2.MSER_create()

    regions, _ = mser.detectRegions(gray)

    hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]

    boxes = []

    for contour in hulls:

        (x, y, w, h) = cv2.boundingRect(contour)
        # pick = non_max_suppression(hulls, probs=None, overlapThresh=0.65)
        ar = w / float(h)
        # a square will have an aspect ratio that is approximately
        # equal to one, otherwise, the shape is a rectangle
        if ar >= 0.5 and ar <= 1.5:
            print("square")
            rect = cv2.minAreaRect(contour)
            box = np.int0(cv2.boxPoints(rect))
            roiImg = img_rgb[y:y + h, x:x + w]

            roiImg = cv2.resize(roiImg, (32, 32))

            x_img = image.img_to_array(roiImg)
            x_img = np.expand_dims(x_img, axis=0)
            x_img /= 255.
            classes = model.predict_classes(x_img)
            classes_arr = model.predict(x_img)
            print(classes)
            print(classes_arr)
            # [] recognition

            if classes[0] != 3:
                cv2.imshow('roi', roiImg)

                boxes.append([sign_dict[classes[0]],[x,y,x+w,y+h]])


                cv2.drawContours(res, [box], -1, (0, 255, 0), 1)
                #
                # cv2.imshow('res',res)
                # cv2.waitKey(0)

    # cv2.imshow('vis', vis)
    # cv2.waitKey(0)
    new_boxes = [el for el, _ in groupby(boxes)]  # группировка одинаковых элементов
    return new_boxes

if __name__ == '__main__':

    # load the model we saved
    model = load_model('tsr1.h5')

    img = cv2.imread('1002.jpg')
    boxes = detector(img, model)
    print(boxes)
