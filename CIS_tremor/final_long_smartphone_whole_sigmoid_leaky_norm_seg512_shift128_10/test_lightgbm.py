import numpy as np
import pickle
import lightgbm as lgb
import copy

import sys

name=copy.copy(sys.argv[1])
name=name.replace('test','train')+'finalized_model.sav'
est=pickle.load(open(name, 'rb'))
feature=np.loadtxt(sys.argv[1])[:,1:]
gs=np.loadtxt(sys.argv[1])[:,0]
value=est.predict(feature)
np.savetxt((sys.argv[1]+'prediction.dat'),value)




