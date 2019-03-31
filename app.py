# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

dateparse = lambda x: pd.datetime.strptime(x, '%Y/%m/%d')
weather = pd.read_csv('weather.csv',encoding="utf_8_sig",engine='python',parse_dates=['date'],date_parser = dateparse,index_col= 0)
dateparse = lambda x: pd.datetime.strptime(x, '%Y%m%d')
df3 = pd.read_csv('20170101-20181231.csv',encoding="utf_8_sig",engine='python',parse_dates=['日期'],date_parser = dateparse,index_col= 0)
power2017_2018 = df3['尖峰負載(MW)']
weather = weather['T Max']

weekday = pd.Series(power2017_2018.index)
Sunday = []
Monday = []
Tuesday = []
Wednesday = []
Thursday = []
Friday = []
Saturday = []
for i in weekday:
    if i.weekday() == 0:
        Monday.append(i)
    elif i.weekday() == 1:
        Tuesday.append(i)
    elif i.weekday() == 2:
        Wednesday.append(i)
    elif i.weekday() == 3:
        Thursday.append(i)
    elif i.weekday() == 4:
        Friday.append(i)
    elif i.weekday() == 5:
        Saturday.append(i)
    else:
        Sunday.append(i)
w = [Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday]
word = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
i = 1
model = [None]*7
plt.figure(figsize=(15,20))
for c in w:
    poly_features = PolynomialFeatures(degree=2)
    weather_poly = poly_features.fit_transform(weather[c].values.reshape(-1,1))
    weather_quadratic = poly_features.transform(weather[c].values.reshape(-1,1))
    
    model[i-1] = LinearRegression()
    model[i-1].fit(weather_quadratic, power2017_2018[c])
    power_predict = model[i-1].predict(weather_quadratic)
    i += 1

date = ['2019-04-02','2019-04-03','2019-04-04','2019-04-05','2019-04-06','2019-04-07','2019-04-08']
predict_date = pd.to_datetime(date)
temp = [26,28,28,28,29,28,28]
result = []
for i in range(len(date)):
    poly_features.fit(temp[i])
    tt = poly_features.transform(temp[i])
    if predict_date[i].weekday() == 0:
        result.append(model[0].predict(tt))
    if predict_date[i].weekday() == 1:
        result.append(model[1].predict(tt))
    if predict_date[i].weekday() == 2:
        result.append(model[2].predict(tt))
    if predict_date[i].weekday() == 3:
        result.append(model[3].predict(tt))
    if predict_date[i].weekday() == 4:
        result.append(model[4].predict(tt))
    if predict_date[i].weekday() == 5:
        result.append(model[5].predict(tt))
    if predict_date[i].weekday() == 6:
        result.append(model[6].predict(tt))
for i in range(len(result)):
    result[i] = int(round(result[i][0]))
dit = {'date':date, 'peak_load(MW)':result}
df = pd.DataFrame(dit)
df.to_csv(r'./submission.csv',columns=['date','peak_load(MW)'],index=False,sep=',')