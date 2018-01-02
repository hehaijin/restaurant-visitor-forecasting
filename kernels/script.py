import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import csv
from statistics import mean, median,variance,stdev
from datetime import datetime
import re


air_reserve = pd.read_csv("../input/air_reserve.csv")
air_visit_data = pd.read_csv("../input/air_visit_data.csv")
air_store_info = pd.read_csv("../input/air_store_info.csv")
hpg_reserve = pd.read_csv("../input/hpg_reserve.csv")
hpg_store_info = pd.read_csv("../input/hpg_store_info.csv")
store_id_relation = pd.read_csv("../input/store_id_relation.csv")
date_info = pd.read_csv("../input/date_info.csv")
sample_submission = pd.read_csv("../input/sample_submission.csv")


hpg_reserve = pd.merge(hpg_reserve, store_id_relation, how='left', on=['hpg_store_id'])
air_reserve = pd.merge(air_reserve, store_id_relation, how='left', on=['air_store_id'])


hpg_reserve['visit_datetime'] = pd.to_datetime(hpg_reserve['visit_datetime'])
hpg_reserve['visit_year'] = hpg_reserve['visit_datetime'].dt.year
hpg_reserve['visit_month'] = hpg_reserve['visit_datetime'].dt.month
hpg_reserve['visit_date'] = hpg_reserve['visit_datetime'].dt.date
hpg_reserve = hpg_reserve.drop('visit_datetime',axis=1)

air_reserve['visit_datetime'] = pd.to_datetime(air_reserve['visit_datetime'])
air_reserve['visit_year'] = air_reserve['visit_datetime'].dt.year
air_reserve['visit_month'] = air_reserve['visit_datetime'].dt.month
air_reserve['visit_date'] = air_reserve['visit_datetime'].dt.date
air_reserve = air_reserve.drop('visit_datetime',axis=1)

hpg_reserve['reserve_datetime'] = pd.to_datetime(hpg_reserve['reserve_datetime'])
hpg_reserve['reserve_year'] = hpg_reserve['reserve_datetime'].dt.year
hpg_reserve['reserve_month'] = hpg_reserve['reserve_datetime'].dt.month
hpg_reserve['reserve_date'] = hpg_reserve['reserve_datetime'].dt.date
hpg_reserve = hpg_reserve.drop('reserve_datetime',axis=1)

air_reserve['reserve_datetime'] = pd.to_datetime(air_reserve['reserve_datetime'])
air_reserve['reserve_year'] = air_reserve['reserve_datetime'].dt.year
air_reserve['reserve_month'] = air_reserve['reserve_datetime'].dt.month
air_reserve['reserve_date'] = air_reserve['reserve_datetime'].dt.date
air_reserve = air_reserve.drop('reserve_datetime',axis=1)

air_visit_data['visit_datetime'] = pd.to_datetime(air_visit_data['visit_date'])
air_visit_data['visit_year'] = air_visit_data['visit_datetime'].dt.year
air_visit_data['visit_month'] = air_visit_data['visit_datetime'].dt.month
air_visit_data['visit_date'] = air_visit_data['visit_datetime'].dt.date
air_visit_data = air_visit_data.rename(columns={'visit_date':'visit_date'})
air_visit_data = air_visit_data.drop('visit_datetime',axis=1)

date_info['calendar_datetime'] = pd.to_datetime(date_info['calendar_date'])
date_info['visit_year'] = date_info['calendar_datetime'].dt.year
date_info['visit_month'] = date_info['calendar_datetime'].dt.month
date_info['calendar_date'] = date_info['calendar_datetime'].dt.date
date_info = date_info.rename(columns={'calendar_date':'visit_date'})
date_info = date_info.rename(columns={'calendar_datetime':'visit_datetime'})
date_info = date_info.drop('visit_datetime',axis=1)

sample_submission['air_store_id'] = sample_submission['id'].map(lambda x: '_'.join(x.split('_')[:2]))
sample_submission['visit_datetime'] = sample_submission['id'].map(lambda x: str(x).split('_')[2])
sample_submission['visit_datetime'] = pd.to_datetime(sample_submission['visit_datetime'])
sample_submission['visit_year'] = sample_submission['visit_datetime'].dt.year
sample_submission['visit_month'] = sample_submission['visit_datetime'].dt.month
sample_submission['visit_date'] = sample_submission['visit_datetime'].dt.date
sample_submission = sample_submission.drop('visit_datetime',axis=1)


df_ah_re = pd.concat([air_reserve,hpg_reserve],ignore_index = True)
df_ah_re = df_ah_re.fillna(0)

print("first")
print(df_ah_re.head())

df_ah_re = df_ah_re.groupby(['air_store_id','hpg_store_id','visit_date','visit_year','visit_month'])['reserve_visitors'].sum().reset_index()
df_ah_re = pd.merge(df_ah_re, date_info, how = 'left', on=['visit_date','visit_year','visit_month'])
df_ah_re = pd.merge(df_ah_re, air_store_info, how = 'left', on = ['air_store_id'])
df_ah_re = pd.merge(df_ah_re, hpg_store_info, how = 'left', on = ['hpg_store_id'])
df_ah_re = df_ah_re.fillna(0)


sample_submission = pd.merge(sample_submission,date_info, how = 'left', on = ['visit_date','visit_year','visit_month'])
sample_submission = pd.merge(sample_submission,df_ah_re, how = 'left', on = ['air_store_id','visit_date','day_of_week','holiday_flg','visit_year','visit_month'])


df_ah_re.air_genre_name = df_ah_re.air_genre_name.astype('category')
df_ah_re.hpg_genre_name = df_ah_re.hpg_genre_name.astype('category')
df_ah_re.day_of_week = df_ah_re.day_of_week.astype('category')
df_ah_re.reserve_visitors = df_ah_re.reserve_visitors.astype('float64')
df_ah_re.visit_month =df_ah_re.visit_month.astype('category')
df_ah_re.visit_year =df_ah_re.visit_year.astype('category')

df_ah_re.air_genre_name = df_ah_re.air_genre_name.cat.codes
df_ah_re.hpg_genre_name = df_ah_re.hpg_genre_name.cat.codes
df_ah_re.day_of_week = df_ah_re.day_of_week.cat.codes
df_ah_re.visit_month =df_ah_re.visit_month.cat.codes
df_ah_re.visit_year =df_ah_re.visit_year.cat.codes
print("second")
print(df_ah_re.head())

sample_submission = sample_submission.fillna(0)
sample_submission.air_genre_name = sample_submission.air_genre_name.astype('category')
sample_submission.hpg_genre_name = sample_submission.hpg_genre_name.astype('category')
sample_submission.day_of_week =sample_submission.day_of_week.astype('category')
sample_submission.visit_month =sample_submission.visit_month.astype('category')
sample_submission.visit_year =sample_submission.visit_year.astype('category')

sample_submission.air_genre_name = sample_submission.air_genre_name.cat.codes
sample_submission.hpg_genre_name = sample_submission.hpg_genre_name.cat.codes
sample_submission.day_of_week = sample_submission.day_of_week.cat.codes
sample_submission.visit_month =sample_submission.visit_month.cat.codes
sample_submission.visit_year =sample_submission.visit_year.cat.codes


print("sample_submission")
print(sample_submission.head())

print("df_ah_re")
print(df_ah_re.head())


sample_test = sample_submission.drop(['id','air_store_id','visit_date','hpg_store_id','air_area_name','latitude_x','longitude_x','hpg_area_name','latitude_y','longitude_y','visitors','reserve_visitors'], axis=1)
sample_test = sample_test.reset_index(drop=True)

print("sample_test")
print(sample_test.head())

df_ah_re_test = df_ah_re.drop(['air_store_id','visit_date','hpg_store_id','air_area_name','latitude_x','longitude_x','hpg_area_name','latitude_y','longitude_y','reserve_visitors'], axis=1)
df_ah_re_test = df_ah_re_test.reset_index(drop=True)


print("df_ah_re_test")
print(df_ah_re_test.head())
print( df_ah_re.reserve_visitors.head())


xs = df_ah_re_test

y = df_ah_re.reserve_visitors

forest = RandomForestRegressor(min_samples_leaf=10, n_estimators=300)
forest.fit(xs,y)

print(df_ah_re.isnull().sum())
print(sample_test.isnull().sum())

reserve_pre = forest.predict(sample_test)
reserve_pre = pd.Series(reserve_pre)

sample_test2 = pd.concat([sample_test, reserve_pre], axis=1)
sample_test2.columns = ['visit_year','visit_month','day_of_week','holiday_flg','air_genre_name','hpg_genre_name','reserve_visitors']

print(sample_test2.head())

df_ah_re = pd.merge(df_ah_re, air_visit_data, how = 'left', on = ['air_store_id','visit_date','visit_year','visit_month'])
print("air_visit_data")
print(air_visit_data.head())
print("df_ah_re")
print(df_ah_re.head())


df_ah_re_test2 = df_ah_re.dropna(subset=['visitors'])
df_ah_re_test2 = df_ah_re_test2.reset_index(drop=True)

print("df_ah_re_test2")
print(df_ah_re_test2.head())

y2 = df_ah_re_test2.visitors

df_ah_re_test2 = df_ah_re_test2.drop(['air_store_id','visit_date','hpg_store_id','air_area_name','latitude_x','longitude_x','hpg_area_name','latitude_y','longitude_y','visitors'], axis=1)
df_ah_re_test2 = df_ah_re_test2.reset_index(drop=True)

xs2 = df_ah_re_test2

forest2 = RandomForestRegressor(min_samples_leaf=10, n_estimators=300)
forest2.fit(xs2,y2)

visitors_pre = forest2.predict(sample_test2)
visitors_pre = pd.Series(visitors_pre)

submit = pd.concat([sample_submission.id, visitors_pre], axis=1)
submit.columns = ['id','visitors']

print(submit.head())


submit.to_csv('submit.csv', index=False)