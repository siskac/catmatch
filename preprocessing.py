import cv2
import os
import numpy as np
from PIL import Image
from keras.preprocessing.image import img_to_array
import random

IMAGE_DIMS = (128, 128, 3)

tabby_classes = ['classictabby', 'mackeraltabby', 'tickedtabby', 'spottedtabby', 'tabby', 'notabby']
body_classes = ['harlequin', 'van', 'full']
point_classes = ['point', 'nopoint']
color_classes = ['onecolor', 'bicolor', 'tortoise']


def kerasImages(dir_path):
# parse through directories in path and save images to file
	data = []
	labels = []
	group_labels = os.listdir(dir_path)
	if '.DS_Store' in group_labels:  group_labels.remove('.DS_Store')
	for group in group_labels:
		print group
		group_path = dir_path + '/' + group + '/'
        	images = os.listdir(group_path)
        	for i in images:
			try:
				# make sure image is good
				check = Image.open(group_path + i)
                        	check.verify()
				# load image, convert to arry and save
				image = cv2.imread(group_path + i)
				image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
		#		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		#		image = cv2.Canny(image, 30, 200)
				image = img_to_array(image)
				data.append(image)
				labels.append(group)
			except:
			# sometimes files create errors that verify() doesn't catch
				pass	
	index = range(0, len(labels))
	random.shuffle(index)
	data = [data[x] for x in index]
	labels = [labels[x] for x in index]
	data = np.array(data, dtype="float") #/ 255.0
	labels = np.array(labels)
	return data, labels


def kerasImages_multiclass(dir_path, imagedim):
# parse through directories in path and save images to file
        data = []
        labels = []
        image_names = os.listdir(dir_path)
        for i in image_names:
		i_name, i_extension = os.path.splitext(i)
        	try:
			# make sure image is good
                        check = Image.open(dir_path + i)
                        check.verify()
                        # load image, convert to arry and save
                        image = cv2.imread(dir_path + i)
                        image = cv2.resize(image, (imagedim, imagedim))
                #               image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                #               image = cv2.Canny(image, 30, 200)
                        image = img_to_array(image)
                        data.append(image)
			l = []
			group = i_name.split('_')
			group.pop(0)
			labels.append(tuple(group))
                except:
                # sometimes files create errors that verify() doesn't catch
                        pass
        index = range(0, len(labels))
        random.shuffle(index)
        data = [data[x] for x in index]
        labels = [labels[x] for x in index]
        data = np.array(data, dtype="float") / 255.0
        labels = np.array(labels)
#	assert(len(labels) == 0, "no images were collected")
        return data, labels

