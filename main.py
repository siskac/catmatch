from preprocessing import *
from createNN import runModel
import pandas as pd

# cat coat color

# preprocess images
data, labels = kerasImages_multiclass('/Users/siskac/repos/whatcat/images/coat_color_pattern_multi')

EPOCHS = 100
INIT_LR = 1e-3
BS = 32
IMAGE_DIMS = (128, 128, 3)
DECAY = 1e-5

# build model
model, H, trainX, testX, trainY, testY, lb = runModel(data, labels, 'pattern')

