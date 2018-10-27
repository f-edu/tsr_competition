import helpers
import cv2
import random
import numpy as np



def load_data():

    IMAGE_DIR_TEST = "data/test/"
    TEST_IMAGE_LIST = helpers.load_dataset(IMAGE_DIR_TEST)

    return TEST_IMAGE_LIST



def standardize_input(image):

    standard_im = np.copy(image)
    standard_im = cv2.cvtColor(standard_im, cv2.COLOR_BGR2HSV)
    standard_im = cv2.inRange(standard_im, (89, 124, 73), (255, 255, 255))
    standard_im = cv2.blur(standard_im, (5, 5))
    standard_im = cv2.erode(standard_im, None, iterations=2)
    standard_im = cv2.dilate(standard_im, None, iterations=4)
    standard_im = cv2.resize(standard_im, (64, 64))

    return standard_im



def one_hot_encode(label):

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


def standardize(image_list):

    standard_list = []

    for item in image_list:
        image = item[0]
        label = item[1]

        standardized_im = standardize_input(image)

        one_hot_label = one_hot_encode(label)

        # Append the image, and it's one hot encoded label to the full, processed list of image data
        standard_list.append((standardized_im, one_hot_label))

    return standard_list


def predict_label(rgb_image):

    a_unevenness = cv2.imread("data/standards/a_unevenness.jpg")
    a_unevenness = cv2.inRange(a_unevenness, (89, 91, 149), (255, 255, 255))
    a_unevenness = cv2.resize(a_unevenness, (64, 64))

    no_drive = cv2.imread("data/standards/no_drive.png")
    no_drive = cv2.inRange(no_drive, (89, 91, 149), (255, 255, 255))
    no_drive = cv2.resize(no_drive, (64, 64))

    no_entry = cv2.imread("data/standards/no_entry.jpg")
    no_entry = cv2.inRange(no_entry, (89, 91, 149), (255, 255, 255))
    no_entry = cv2.resize(no_entry, (64, 64))

    parking = cv2.imread("data/standards/parking.jpg")
    parking = cv2.inRange(parking, (0, 0, 0), (255, 0, 255))
    parking = cv2.resize(parking, (64, 64))

    pedistrain1 = cv2.imread("data/standards/pedistrain.jpg")
    pedistrain1 = cv2.inRange(pedistrain1, (89, 91, 149), (255, 255, 255))
    pedistrain1 = cv2.resize(pedistrain1, (64, 64))

    pedistrain2 = cv2.imread("data/standards/pedistrain.jpg")
    pedistrain2 = cv2.inRange(pedistrain2, (89, 91, 149), (255, 255, 255))
    pedistrain2 = cv2.resize(pedistrain2, (64, 64))

    road_works = cv2.imread("data/standards/road_works.jpg")
    road_works = cv2.inRange(road_works, (89, 91, 149), (255, 255, 255))
    road_works = cv2.resize(road_works, (64, 64))

    stop = cv2.imread("data/standards/stop.jpg")
    stop = cv2.inRange(stop, (89, 91, 149), (255, 255, 255))
    stop = cv2.resize(stop, (64, 64))

    way_out = cv2.imread("data/standards/way_out.jpg")
    way_out = cv2.inRange(way_out, (89, 91, 149), (255, 255, 255))
    way_out = cv2.resize(way_out, (64, 64))

    a_unevenness_val = 0
    no_drive_val = 0
    no_entry_val = 0
    none_val = 0
    parking_val = 0
    pedistrain_val = 0
    road_works_val = 0
    stop_val = 0
    way_out_val = 0
    for i in range(64):
        for j in range(64):
            if rgb_image[i][j] == a_unevenness[i][j]:
                a_unevenness_val += 1
            elif rgb_image[i][j] == no_drive[i][j]:
                no_drive_val += 1
            elif rgb_image[i][j] == no_entry[i][j]:
                no_entry_val += 1
            elif rgb_image[i][j] == parking[i][j]:
                parking_val += 1
            elif rgb_image[i][j] == pedistrain1[i][j]:
                pedistrain_val += 1
            elif rgb_image[i][j] == pedistrain2[i][j]:
                pedistrain_val += 1
            elif rgb_image[i][j] == road_works[i][j]:
                road_works_val += 1
            elif rgb_image[i][j] == stop[i][j]:
                stop_val += 1
            elif rgb_image[i][j] == way_out[i][j]:
                way_out_val += 1
            else:
                none_val += 1

    if a_unevenness_val > 3000:
        predicted_label = one_hot_encode("a_unevenness")
    elif no_drive_val > 3000:
        predicted_label = one_hot_encode("no_drive")
    elif no_entry_val > 3000:
        predicted_label = one_hot_encode("no_entry")
    elif parking_val > 3000:
        predicted_label = one_hot_encode("parking")
    elif pedistrain_val > 3000:
        predicted_label = one_hot_encode("pedistrain")
    elif road_works_val > 3000:
        predicted_label = one_hot_encode("road_works")
    elif stop_val > 3000:
        predicted_label = one_hot_encode("stop")
    elif way_out_val > 3000:
        predicted_label = one_hot_encode("way_out")
    else:
        predicted_label = one_hot_encode("none")




    return predicted_label


def get_misclassified_images(test_images):

    misclassified_images_labels = []

    for image in test_images:

        im = image[0]
        true_label = image[1]

        assert (len(true_label) == 8), "False len"


        predicted_label = predict_label(im)
        assert (len(predicted_label) == 8), "False len"


        if (predicted_label != true_label):
            misclassified_images_labels.append((im, predicted_label, true_label))

    return misclassified_images_labels


def main():

    TEST_IMAGE_LIST = load_data()
    STANDARDIZED_TEST_LIST = standardize(TEST_IMAGE_LIST)
    random.shuffle(STANDARDIZED_TEST_LIST)

    MISCLASSIFIED = get_misclassified_images(STANDARDIZED_TEST_LIST)


    total = len(STANDARDIZED_TEST_LIST)
    num_correct = total - len(MISCLASSIFIED)
    accuracy = num_correct / total

    print('acc: ' + str(accuracy))
    print("none_recognition = " + str(len(MISCLASSIFIED)) + ' from ' + str(total))


if __name__ == '__main__':
    main()
