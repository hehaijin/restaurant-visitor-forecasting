# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 20:04:43 2017

@author: heye-
"""


import os.path as path
import pandas as pd


input_path="data"
air_reserve=pd.read_csv(path.join(input_path,"air_reserve.csv"))
print(air_reserve.head())
r=pd.to_datetime(air_reserve["visit_datetime"])
print(type(r))
air_reserve.visit_datetime=r
print(air_reserve.head())
    
#print(air_reserve.reserve_datetime.head())