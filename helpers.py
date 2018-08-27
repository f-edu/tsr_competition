# Helper functions
import cv2
import os
import glob  # library for loading images from a directory
import xml.etree.ElementTree as pars
import numpy as np

# This function loads in images and their labels and places them in a list
# The list contains all images and their associated labels
# For example, after data is loaded, im_list[0][:] will be the first image-label pair in the list



def load_dataset(image_dir):
    # Populate this empty image list
    im_list = []


    images = os.listdir(image_dir+"/images")

    for image_name in images:

        frame = cv2.imread(image_dir+"/images/" + image_name)
        img_id = image_name.split('.')

        if not frame is None:
            # Append the image, and it's type ("none", "pedistrain", "no_drive","stop","way-out","no_entry","road_works","parking","a_unevenness") to the image list
            im_list.append((img_id[0], frame))


    return im_list

def load_objects(im_list, image_dir):

    object_list = []

    for img in im_list:
        img_id = img[0]
        frame = img[1]

        e = pars.parse(image_dir + '/annotations/xmls/' + img_id + '.xml')

        root = e.getroot()

        objects = []
        for object in root.findall('object'):
            name = object.find('name').text
            for box in object.findall('bndbox'):
                points = [int(box.find('xmin').text),
                                   int(box.find('ymin').text),
                                   int(box.find('xmax').text),
                                   int(box.find('ymax').text)]
            objects.append([name, points])


        object_list.append([frame,img_id,objects])

    # print(object_list[0][2][0][1])
    return object_list
    # return object_list


