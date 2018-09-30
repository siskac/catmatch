import os
import sys
from random import sample
import shutil

segment = 'coat_color/'

global train_path
global test_path

train_path = os.getcwd() + '/images/build/train/'
test_path = os.getcwd() + '/images/build/test/'

def prepareBuildDir():
	if os.path.exists(train_path):
		shutil.rmtree(train_path)
		os.makedirs(train_path)
	if os.path.exists(test_path):
        	shutil.rmtree(test_path)
        	os.makedirs(test_path)

def moveFiles(segment):
	dir_path = os.getcwd() + '/images/' + segment
	for group in os.listdir(dir_path):
		if group == '.DS_Store': continue
		images = os.listdir(dir_path + group)
		shuffle_index = sample(range(len(images)), len(images))
		train_index = len(images) * 0.7
		os.makedirs(train_path + group)
		os.makedirs(test_path + group)
		for x in shuffle_index:
			image_x = images[shuffle_index[x]]
			try:
				check = Image.open(dir_path + group + '/' + image_x)
                        	check.verify()
				if x < train_index:
					shutil.copy(dir_path + group + '/' + image_x, train_path + group)
				if x >= train_index:
					shutil.copy(dir_path + group + '/' + image_x, test_path + group)
                        except (IOError, SyntaxError) as e: continue

