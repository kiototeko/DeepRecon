#!/usr/bin/env python
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16
import keras
import sys

# iteration count
_iter = 1 


"""
    Main
"""
if __name__ == '__main__':
    # load the model
    ic = int(sys.argv[1])
    ker = int(sys.argv[2])
    model = keras.Sequential([keras.layers.Conv2D(ic, (ker, ker),activation='relu',padding='same') for i in range(200)])
    """
    keras.layers.Conv2D(64, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(64, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(128, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(128, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(256, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(256, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(512, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(512, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(1024, (ker, ker),activation='relu',padding='same'),
    keras.layers.Conv2D(1024, (ker, ker),activation='relu',padding='same')])
    """

    # load an image from file
    image = load_img('../etc/mug.jpg', target_size=(224, 224))
    # convert the image pixels to a numpy array
    image = img_to_array(image)
    # reshape data for the model
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    # prepare the image for the VGG model
    image = preprocess_input(image)

    # predict the probability across all output classes
    for i in range(_iter):
        #raw_input('{} iteration, press any key to perform...'.format(str(i)))
        yhat = model.predict(image)

    # return if no iteration
    if not _iter: exit() 

