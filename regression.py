# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 17:50:01 2018

@author: heye-
"""

#this is when already generated train and test files.



import sklearn
import numpy as np
import pandas as pd
from datetime import datetime



train=pd.read_csv("training.csv")
test=pd.read_csv("testing.csv")

train_X=train.drop(["visitors","air_store_id"],axis=1)
train_Y=train["visitors"]
test_X=test.drop(["visitors","air_store_id"])



