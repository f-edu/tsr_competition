import xml.etree.ElementTree as pars
import numpy as np

def iou(points, predicted_points):
    """IoU = Area of overlap / Area of union"""
    xA = max(points[0], predicted_points[0])
    yA = max(points[1], predicted_points[1])
    xB = min(points[2], predicted_points[2])
    yB = min(points[3], predicted_points[3])

    # x1, y1, xw1, yh1 = points
    # x2, y2, xw2, yh2 = predicted_points
    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # compute the area of both the prediction and ground-truth
    # rectangles

    boxAArea = (points[2] - points[0] + 1) * (points[3] - points[1] + 1)
    boxBArea = (predicted_points[2] - predicted_points[0] + 1) * (predicted_points[3] - predicted_points[1] + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou



e = pars.parse('data/test/annotations/xmls/201.xml')
root = e.getroot()

for object in root.findall('object'):
    name = object.find('name').text
    print(name)
    for box in object.findall('bndbox'):
        points = np.array([int(box.find('xmin').text),
                           int(box.find('ymin').text),
                           int(box.find('xmax').text),
                           int(box.find('ymax').text)])

        predicted_points = np.array([35,148,76,192])
        print (iou(points, predicted_points))


