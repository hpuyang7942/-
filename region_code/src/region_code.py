import numpy as np
import pandas as pd
import re

# import source txt file and extra data mining jobs
region = open("行政区划.txt").read()
region = region.replace('\xa0', '')
region_list = re.split('(\d+)',region)
region_list = region_list[1:]

# seperate code and area name
code_list = []
area_list = []
for i in range(len(region_list)):
    if i%2 == 0:
        code_list.append(region_list[i])
    else:
        area_list.append(region_list[i])

# create DataFrame out of the lists
region_df = pd.DataFrame({'name': area_list, 'code': code_list}, columns = ['name', 'code'])

# create new columns and assign default value
region_df['province'] = '北京'
region_df['city'] = '北京'

def province_divisor(dataframe, province_code):
    my_list = []
    #my_df = pd.DataFrame(columns = ['name', 'code', 'province'])
    for i in range(len(dataframe)):
        if int(dataframe['code'].iloc[i]) - province_code < 1000 and int(dataframe['code'].iloc[i]) - province_code > 0:
            my_list.append(dataframe.iloc[i])
    return my_list

# accquire province name
province_list = []
for i in range(len(region_df)):
    if int(region_df['code'].iloc[i]) % 10000 == 0:
        province_list.append(region_df.iloc[i])
province_df = pd.DataFrame(province_list)

# assign real province name
for i in range(len(region_df)):
    for j in range(len(province_df)):
        if int(region_df['code'].iloc[i]) - int(province_df['code'].iloc[j]) >= 0 and int(region_df['code'].iloc[i]) - int(province_df['code'].iloc[j]) < 10000:
            region_df['province'].iloc[i] = province_df['name'].iloc[j]

# accquire city (地级市) name
city_list = []
for i in range(len(region_df)):
    if int(region_df['code'].iloc[i]) % 100 == 0:
        city_list.append(region_df.iloc[i])
city_df = pd.DataFrame(city_list)

# assign real city name
for i in range(len(region_df)):
    for j in range(len(city_df)):
        if int(region_df['code'].iloc[i]) - int(city_df['code'].iloc[j]) >= 0 and int(region_df['code'].iloc[i]) - int(city_df['code'].iloc[j]) < 100:
            region_df['city'].iloc[i] = city_df['name'].iloc[j]

# save the results as csv file
region_df.to_csv('region_code.csv', header=True, index=True)