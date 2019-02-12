from keras.models import Sequential
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import Conv2D
from keras.layers.convolutional import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Flatten
from keras.layers.core import Dropout
from keras.layers.core import Dense
from keras import backend as K

from keras.preprocessing.image import ImageDataGenerator
from sklearn.preprocessing import LabelBinarizer
from keras.optimizers import Adam
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from imutils import paths
import numpy as np
import argparse
import random
import pickle
import cv2
import os

EPOCHS = 3
INIT_LR = 1e-3
BS = 32
IMAGE_DIMS = (128, 128, 3)
DECAY = 1e-5

class SmallerVGGNet:
# taken from https://www.pyimagesearch.com/2018/05/07/multi-label-classification-with-keras/
	@staticmethod
	def build(filter_size, width, height, depth, classes, finalAct="softmax"):
		# initialize the model along with the input shape to be
		# "channels last" and the channels dimension itself
		model = Sequential()
		inputShape = (height, width, depth)
		chanDim = -1
		# if we are using "channels first", update the input shape
		# and channels dimension
		if K.image_data_format() == "channels_first":
			inputShape = (depth, height, width)
			chanDim = 1
		# CONV => RELU => POOL
		model.add(Conv2D(filter_size, (3, 3), padding="same", input_shape=inputShape))
		model.add(Activation("relu"))
		model.add(BatchNormalization(axis=chanDim))
		model.add(MaxPooling2D(pool_size=(3, 3)))
		model.add(Dropout(0.25))
		# (CONV => RELU) * 2 => POOL
		filter_size = filter_size * 2
		model.add(Conv2D(filter_size, (3, 3), padding="same"))
		model.add(Activation("relu"))
		model.add(BatchNormalization(axis=chanDim))
		model.add(Conv2D(filter_size, (3, 3), padding="same"))
		model.add(Activation("relu"))
		model.add(BatchNormalization(axis=chanDim))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.25))
		# (CONV => RELU) * 2 => POOL
		filter_size = filter_size * 2
		model.add(Conv2D(filter_size, (3, 3), padding="same"))
		model.add(Activation("relu"))
		model.add(BatchNormalization(axis=chanDim))
		model.add(Conv2D(filter_size, (3, 3), padding="same"))
		model.add(Activation("relu"))
		model.add(BatchNormalization(axis=chanDim))
		model.add(MaxPooling2D(pool_size=(2, 2)))
		model.add(Dropout(0.25))
		# first (and only) set of FC => RELU layers
		filter_size = filter_size * 8
		model.add(Flatten())
		model.add(Dense(filter_size))
		model.add(Activation("relu"))
		model.add(BatchNormalization())
		model.add(Dropout(0.5))
		# softmax classifier
		model.add(Dense(classes))
		model.add(Activation(finalAct))
		# return the constructed network architecture
		return model

def runModel(data, labels, model_name):
	# prepare data and labels
	lb = LabelBinarizer()
        labels = lb.fit_transform(labels)
	(trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2)
	# create generator to augment images
	aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")
	# run model
	print "training"
	model = SmallerVGGNet.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0], depth=IMAGE_DIMS[2], classes=len(lb.classes_))
	opt = Adam(lr=INIT_LR, decay= DECAY)
	model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
	H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS), validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
				epochs=EPOCHS, verbose=1)
	print "saving model to disk"
	model.save(model_name + '_model')
	f = open(model_name + '_labels', "wb")
	f.write(pickle.dumps(lb))
	f.close()
	return model, H, trainX, testX, trainY, testY, lb

def runModel_multiclass(data, labels, model_name, decay, learning_rate, batch_size, image_dim, epochs, filter_size):
        # prepare data and labels
	mlb = MultiLabelBinarizer() 
       	labels = mlb.fit_transform(labels)
        (trainX, testX, trainY, testY) = train_test_split(data, labels, test_size=0.2)
        # create generator to augment images
        aug = ImageDataGenerator(rotation_range=25, width_shift_range=0.1, height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")
        # run model
        print "training"
        model = SmallerVGGNet.build(filter_size, width = image_dim, height = image_dim, depth= 3, classes=len(mlb.classes_), finalAct = 'sigmoid')
        opt = Adam(lr = learning_rate, decay= decay)
        model.compile(loss="binary_crossentropy", optimizer=opt, metrics=["accuracy"])
        H = model.fit_generator(aug.flow(trainX, trainY, batch_size= batch_size), validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
                                epochs= epochs, verbose=1)
        print "saving model to disk"
        model.save(model_name + '_model')
        f = open(model_name + '_labels', "wb")
        f.write(pickle.dumps(mlb))
        f.close()
        return model, H, trainX, testX, trainY, testY, mlb

