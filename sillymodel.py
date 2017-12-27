# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 12:26:38 2017

A silly model.

Just look at the last year of the same day and look for the visitor number.

public score: 2.445

"""


import os.path as path
import pandas as pd

def getLastYearDate(date):
    return '2016'+date[4:]




def main():
    input_path="data"
    
    air_reserve=pd.read_csv(path.join(input_path,"air_reserve.csv"))
    air_reserve["reserve_date"]= air_reserve.apply(lambda row:row["reserve_datetime"][0:10], axis=1)
    
    air_reserve_group=air_reserve.groupby(["air_store_id", "reserve_date"])["reserve_visitors"].sum()
    #print(air_reserve["air_store_id"=="air_0164b9927d20bcc3"])
    air_visit=pd.read_csv(path.join(input_path,"air_visit_data.csv"))
    sample_submission=pd.read_csv(path.join(input_path,"sample_submission.csv"))
    
    sample_submission["air_store_id"]=sample_submission.apply(lambda row: row["id"][0:20],axis=1)
    sample_submission["date"]=sample_submission.apply(lambda row: row["id"][21:],axis=1)
    sample_submission["last_year_date"]=sample_submission.apply(lambda row: getLastYearDate(row["date"]),axis=1)
    r=pd.merge(sample_submission, air_visit, left_on=["air_store_id","last_year_date"], right_on=["air_store_id","visit_date"], how='left')
   
    submission=pd.DataFrame()
    submission["id"]=r["id"]
    submission["visitors"]=r["visitors_y"]
    submission.fillna(0, inplace=True)
    print(submission.head())
    submission.to_csv("submission.csv", index=False)

if __name__=="__main__":
    main()