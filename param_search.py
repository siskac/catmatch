import pandas as pd
import numpy as np
from createNN import runModel_multiclass

def paramSearch():
    lrList = [1e-4, 5e-4, 1e-3, 5e-3, 1e-2, 1e-1, 5e-1]
    bsList = [32, 64, 80, 96]
    decayList = [1e-6, 5e-6, 1e-5, 5e-5, 1e-4, 5e-4]

    BS = 32
    IMAGE_DIMS = (128, 128, 3)

    paramSearch = []

    for lr in lrList:
        INIT_LR = lr
        for d in decayList:
            DECAY = d
            try:
                model, H, trainX, testX, trainY, testY, mlb = runModel_multiclass(data, labels, 'pattern')
                lr_decay_Dict = {'loss': H.history["loss"], 'acc': H.history["acc"], 'val_loss': H.history["val_loss"], \
                                 'val_acc': H.history["val_acc"], 'learning_rate': np.repeat(lr, EPOCHS), 'decay': np.repeat(d, EPOCHS),
                                 'epochs': range(0, EPOCHS)}
                paramSearch.append(pd.DataFrame(lr_decay_Dict))
            except:
                pass
    return pd.concat(paramSearch)

