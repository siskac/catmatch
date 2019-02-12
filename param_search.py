import pandas as pd
import numpy as np
from createNN import runModel_multiclass
import itertools
from preprocessing import kerasImages_multiclass

def paramSearch(dir_path, lrList, decayList, bsList, imagedimList, filterList):
    possible_combos = list(itertools.product(*[lrList, decayList, bsList, filterList]))
    epochs = 8
    paramSearch = []
    model_name = 'test'
    for imagedim in imagedimList:
        print "Image Size: ", imagedim
        data, labels = kerasImages_multiclass(dir_path, imagedim)
        for combos in possible_combos:
            print combos
            learning_rate, decay, batch_size, filter_size = combos
            data, labels = kerasImages_multiclass(dir_path, imagedim)
            try:
                vals = runModel_multiclass(data, labels, model_name, decay, learning_rate, batch_size, imagedim, epochs, filter_size)
                model, H, trainX, testX, trainY, testY, mlb = vals
                param_Dict = {'loss': H.history["loss"], 'acc': H.history["acc"], 'val_loss': H.history["val_loss"], \
                                 'val_acc': H.history["val_acc"], 'learning_rate': np.repeat(learning_rate, epochs), \ 
                                 'decay': np.repeat(decay, epochs), 'batch_size': np.repeat(batch_size, epochs), \
                                 'image_dim': np.repeat(imagedim, epochs), \
                                 'filter_size': np.repeat(filter_size, epochs), 'epochs': range(0, epochs)}
                paramSearch.append(pd.DataFrame(param_Dict))
            except:
                pass
    return pd.concat(paramSearch)

lrList = [3e-3, 3e-2, 0.3, 3]
decayList = [1e-6, 1e-5, 1e-4]
bsList = [32]
imagedimList = [96]
filterList = [16, 32, 64]
path = '/Users/siskac/repos/whatcat/images/coat_color_pattern_multi/'

paramPD = paramSearch(dir_path, lrList, decayList, bsList, imagedimList, filterList)
paramPD.to_csv("paramSearch_coat_color_pattern_multi.csv")
