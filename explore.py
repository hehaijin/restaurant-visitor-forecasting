# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 15:01:50 2017


"""



import os.path as path
import pandas as pd

#try to merge into a big table first, retain the relevant information while discarding non-relevant info.
#the final table should be air_store_id, date, air_reserve_number, hpg_reserve_number,day of the week,holidy,air_genre_name, air_area_name, hpg_genre_name,hpg_area_name, visitor
#currently ignore cooridnate info.




def preprocessing(df):
    input_path="data"
    air_reserve=pd.read_csv(path.join(input_path,"air_reserve.csv"))
    air_reserve["reserve_date"]= air_reserve.apply(lambda row:row["reserve_datetime"][0:10], axis=1)
    air_reserve_group=air_reserve.groupby(["air_store_id", "reserve_date"], as_index=False)["reserve_visitors"].sum()
    #print(type(air_reserve_group))
    air_visit=pd.read_csv(path.join(input_path,"air_visit_data.csv"))
    
    air_store_info=pd.read_csv(path.join(input_path,"air_store_info.csv"))
    
    date_info= pd.read_csv(path.join(input_path,"date_info.csv"))
    
    hpg_reserve= pd.read_csv(path.join(input_path,"hpg_reserve.csv"))
    hpg_reserve["reserve_date"]=hpg_reserve.apply(lambda row:row["reserve_datetime"][0:10], axis=1)
    hpg_reserve_group=hpg_reserve.groupby(["hpg_store_id", "reserve_date"],as_index=False)["reserve_visitors"].sum()
    
    hpg_store_info=pd.read_csv(path.join(input_path,"hpg_store_info.csv"))
    store_id_relation=pd.read_csv(path.join(input_path,"store_id_relation.csv"))
    m1=pd.merge(df, air_reserve_group, left_on=["air_store_id","visit_date"], right_on=["air_store_id","reserve_date"],how='left')[["air_store_id","visit_date","visitors","reserve_visitors"]]
    print(m1.head())
    m2=pd.merge(store_id_relation, hpg_reserve_group, on='hpg_store_id')[["air_store_id","reserve_date","reserve_visitors"]]
    print(m2.head())
    m3=pd.merge(m1,m2,left_on=["air_store_id",'visit_date'],right_on=["air_store_id","reserve_date"],how="left")
    print(m3.head())
    m4=pd.merge(m3,air_store_info,on='air_store_id',how='left')[["air_store_id","air_genre_name","air_area_name","visit_date","reserve_visitors_x","reserve_visitors_y","visitors"]]
    print(m4.head())
    m5=pd.merge(m4, date_info,left_on='visit_date',right_on='calendar_date',how='left')
    m6=m5.fillna(0)[["air_store_id","air_genre_name","air_area_name","visit_date","reserve_visitors_x","reserve_visitors_y","day_of_week","holiday_flg","visitors"]]
    
    return m6

#it must contain air_store_id,  visit_date, and visitors



def main():
    input_path="data"
    air_visit=pd.read_csv(path.join(input_path,"air_visit_data.csv"))
    sample_submission=pd.read_csv(path.join(input_path,"sample_submission.csv"))
    sample_submission["air_store_id"]=sample_submission.apply(lambda row: row["id"][0:20],axis=1)
    sample_submission["visit_date"]=sample_submission.apply(lambda row: row["id"][21:],axis=1)

    training=preprocessing(air_visit)
    testing=preprocessing(sample_submission)
    training.to_csv("training.csv",index=False)
    testing.to_csv("testing.csv",index=False)
    

if __name__=="__main__":
    main()