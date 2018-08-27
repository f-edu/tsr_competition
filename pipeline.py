import helpers
import cv2

def load_data():
    """Загрзка данных тренироваочные, валидационные, тестовые"""

    try:
        IMAGE_DIR_TRAIN = "data/training"
        TRAIN_IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TRAIN)
        TRAIN_OBJECTS_LIST = helpers.load_objects(TRAIN_IMAGE_LIST, IMAGE_DIR_TRAIN)
    except Exception:
        TRAIN_OBJECTS_LIST = []

    try:
        IMAGE_DIR_TEST = "data/test"
        TEST_IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TEST)
        TEST_OBJECTS_LIST = helpers.load_objects(TEST_IMAGE_LIST, IMAGE_DIR_TEST)
    except Exception:
        TEST_OBJECTS_LIST = []

    try:
        IMAGE_DIR_VAL = "data/val"
        VAL_IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_VAL)
        VAL_OBJECTS_LIST = helpers.load_objects(VAL_IMAGE_LIST, IMAGE_DIR_VAL)
    except Exception:
        VAL_OBJECTS_LIST = []

    return TRAIN_OBJECTS_LIST, TEST_OBJECTS_LIST, VAL_OBJECTS_LIST


def predict(frame):
    """Детектирование дорожных знаков на изображении:
    Для каждого изображения формируется массив, состоящий из наименования дорожного знака
    и координат углов знака (xmin,ymin, xmax, ymax) - координаты левого верхнего угла и
    правого нижнего угла знака
    """
    predicted_label = [['a_unevenness', [129, 153, 194, 225]], ['no_entry', [448, 159, 554, 305]]]
    # predicted_label = [['a_unevenness', [129, 153, 194, 225]], ['no_entry', [448, 159, 554, 305]], ['no_entry', [192, 141, 249, 209]]]
    # predicted_label = [['way_out', [24, 144, 65, 188]], ['no_entry', [192, 141, 249, 209]], ['way_out', [140, 144, 175, 188]], ['no_drive', [256, 142, 310, 212]]]

    return predicted_label

def iou(points, predicted_points):
    """IoU = Area of overlap / Area of union
    Площадь пересечеения 2 знаков / общая площадь 2 знаков
    Значение выше 0.5 считаестя удачным детектированием знака
    """
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
    """ Проверка детектирования на изображении.
        Двойной проход по изображениям знака, обеспечивающий сравнение каждого существующего
        знака со всеми предсказанными по очереди и оперделяющий знак при наличии совпадения.
        Также при отсутствии совпадения определяющий что данный знак отсутствует и формирующй
        массив ложных совпадений
    """
    true_predicted = []
    false_predicted = []

    for obj in test_image_label:
        for p_obj in predict_image_label:
            if p_obj[0] == obj[0]:
                iou_res = iou(obj[1], p_obj[1])

                if iou_res > 0.5:
                    true_predicted.append(p_obj)
                else:
                    false_predicted.append(p_obj)

    if len(true_predicted) >= len(test_image_label):
        predicted_count = len(test_image_label)
    else:
        predicted_count = len(true_predicted)

    local_acc = predicted_count/len(test_image_label)

    false_positive = len(false_predicted)/len(test_image_label)

    return local_acc, false_positive


def get_misclassified_images(test_images):
    """ Проверка массива изображений на совпадение
    Результат: среднее точности и среднееточности срабатывания"""
    local_acc_summ = 0.
    false_positive_summ = 0.
    count = 0.

    for frame in test_images:

        count += 1
        test_image_label = frame[2]
        predict_image_label = predict(frame[0])
        local_acc, local_acc_false_positive = check_prediction(test_image_label, predict_image_label)
        # cv2.imshow("fr", frame[0])
        # cv2.waitKey(0)
        local_acc_summ += local_acc
        false_positive_summ += local_acc_false_positive

    print(local_acc_summ/count, false_positive_summ/count)
    return (local_acc_summ/count, false_positive_summ/count)



if __name__ == '__main__':
    # Загрузка данных
    TRAIN_OBJECTS_LIST, TEST_OBJECTS_LIST, VAL_OBJECTS_LIST = load_data()

    # [1] Пример для 1 изображения
    # test_image = TEST_OBJECTS_LIST[3][0]
    # test_image_label = TEST_OBJECTS_LIST[3][2]
    # cv2.imshow("test",test_image)
    # cv2.waitKey(0)
    # predict_image_label = predict(test_image)
    # local_acc, local_acc_false_positive = check_prediction(test_image_label, predict_image_label)

    # [2] Проверка группы изображений
    MISCLASSIFIED = get_misclassified_images(TEST_OBJECTS_LIST)
    print("Точность: {}, Ложное предсказание (false positive): {}".format(MISCLASSIFIED[0], MISCLASSIFIED[1]))
