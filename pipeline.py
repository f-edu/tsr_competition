import helpers
def load_data():
    # IMAGE_DIR_TRAINING = "data/training/"
    IMAGE_DIR_TEST = "data/test/"
    # IMAGE_DIR_VALIDATION = "data/val/"

    # IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TRAINING)

    TEST_IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TEST)

    # VALIDATION_IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_VALIDATION)
    # print(TEST_IMAGE_LIST)
    TEST_OBJECTS_LIST = helpers.load_objects(TEST_IMAGE_LIST)
    return TEST_OBJECTS_LIST


load_data()

def one_hot_encode(label):
    """ Функция осуществляет перекодировку текстового входного сигнала
     в массив элементов, соответствующий выходному сигналу

     Входные параметры: текстовая метка (прим.  pedistrain)

     Выходные параметры: метка ввиде массива
     """
    one_hot_encoded = []
    if label == "none":
        one_hot_encoded = [0, 0, 0, 0, 0, 0, 0, 0]
    elif label == "pedistrain":
        one_hot_encoded = [1, 0, 0, 0, 0, 0, 0, 0]
    elif label == "no_drive":
        one_hot_encoded = [0, 1, 0, 0, 0, 0, 0, 0]
    elif label == "stop":
        one_hot_encoded = [0, 0, 1, 0, 0, 0, 0, 0]
    elif label == "way_out":
        one_hot_encoded = [0, 0, 0, 1, 0, 0, 0, 0]
    elif label == "no_entry":
        one_hot_encoded = [0, 0, 0, 0, 1, 0, 0, 0]
    elif label == "road_works":
        one_hot_encoded = [0, 0, 0, 0, 0, 1, 0, 0]
    elif label == "parking":
        one_hot_encoded = [0, 0, 0, 0, 0, 0, 1, 0]
    elif label == "a_unevenness":
        one_hot_encoded = [0, 0, 0, 0, 0, 0, 0, 1]

    return one_hot_encoded

def predict(frame):
    label = "pedistrain"
    predicted_label = one_hot_encode(label)


    predicted_label = [['way_out', [24, 144, 65, 188]], ['no_entry', [192, 141, 249, 209]], ['way_out', [140, 144, 175, 188]], ['no_drive', [256, 142, 310, 212]]]

    return predicted_label

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

def check_prediction(test_image_label, predict_image_label):
    # print(len(test_image_label))
    for obj in test_image_label:
        for p_obj in predict_image_label:
            if p_obj[0] == obj[0]:
                print (obj[1],p_obj[1])

                iou_res = iou(obj[1], p_obj[1])

                print(iou_res)






if __name__ == '__main__':

    TEST_OBJECTS_LIST = load_data()

    test_image = TEST_OBJECTS_LIST[5][0]
    test_image_label = TEST_OBJECTS_LIST[5][2]

    predict_image_label = predict(test_image)


    check_prediction(test_image_label, predict_image_label)

    # print(predict_image_label[0][0],test_image_label[0][0])
    #
    # print("Реальный класс изображения: {} Предсказанный класс изображения {}".format(test_image_label, predict_image_label))
