#!/usr/bin/env python3
import cv2
import feature_extraction
import numpy as np
import config
import os
import glob
from skimage.transform import pyramid_gaussian
import pickle
from multiprocessing.pool import Pool
import logging

# TODO use a path from config
D = np.load(config.DICT_PATH)  # get dictionary


# get all windows of a image
def sliding_window(img, step_size=1):
    for y in range(0, img.shape[0]-32, step_size):
        for x in range(0, img.shape[1]-32, step_size):
            yield x, y, img[y:min(y+32, img.shape[0]), x:min(x+32, img.shape[1]), :]


def async_predict(args):
    x, y, window = args
    print(x, y)
    features = feature_extraction.get_features_for_window(window.astype('float32'))
    # reshape it so it contains a single sample
    v = model.predict_proba(features[1].flatten().reshape(1, -1))
    return x, y, v[0][1]


# return the value of every pixels of a image
def get_prediction_values(img, model):
    layers = []
    for layer_img in get_all_layers(img):
        pool = Pool(processes=8)
        values = np.zeros(shape=[img.shape[0]-31, img.shape[1]-31],
                          dtype='float')

        for x, y, v in pool.imap(async_predict, sliding_window(layer_img, 8), 8):
            print(v)
            values[y, x] = v

        pool.close()
        pool.join()

        layers.append(values)
    return layers


# return all Scaling image of a Image,save into Layer Matrix
def get_all_layers(img):
    for (i, resized) in enumerate(pyramid_gaussian(img,
                                                   downscale=1.3,
                                                   max_layer=0)):  # TODO use 7
        # if the image is too small, break from the loop
        if resized.shape[0] < 32 or resized.shape[1] < 32:
            break
        yield resized

if __name__ == "__main__":
    model = pickle.load(open(config.TEXT_MODEL_PATH, 'rb'))  # get model
    # image_files = glob.glob(os.path.join(config.TEST_IMAGE_PATH, '*.jpg'))
    image_files = [os.path.join(config.TEST_IMAGE_PATH, '111-1137_IMG.jpg')]

    for filename in image_files:
        img = cv2.imread(filename)
        prediction_layers = get_prediction_values(img, model)

        # now draw the image
        text_probability_image = np.zeros(img.shape, float)

        for y in range(0, img.shape[0]):
            for x in range(0, img.shape[1]):
                max_probability = 0
                for layer in prediction_layers:
                    # x and y in the layer which correspond to position in
                    # original image
                    #trans_y = (layer.shape[0]/img.shape[0]) * y
                    #trans_x = (layer.shape[1]/img.shape[1]) * y

                    window = layer[max(0, x-32):
                                   min(y+1, layer.shape[0]),
                                   max(0, x-32):
                                   min(x+1, layer.shape[1])]

                    max_probability = max(max_probability, window.max())

                text_probability_image[y, x] = max_probability

        cv2.imshow("image 1", img)
        cv2.imshow("image 2", text_probability_image)
        cv2.waitKey(0)
