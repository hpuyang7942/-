import pandas as pd
import numpy as np
import re

# load and seperate data by province
houses = open("Houses.txt").read()
houses = houses.replace('高院', '高级法院').replace('中院', '中级法院').replace('法院','人民法院')
province_house_list = houses.split('*')
for i in range(len(province_house_list)):
    province_house_list[i] = province_house_list[i].split('\n')

# divide into different levels
supreme_houses_list = []
middle_houses_list = []
primary_houses_list = []

for i in range(len(province_house_list)):
    for j in range(len(province_house_list[i])):
        if province_house_list[i][j] == '' or province_house_list[i][j] == '\t\t':
            continue
        if '高级' in province_house_list[i][j]:
            supreme_houses_list.append([province_house_list[i][j], '最高人民法院', '高级'])
        elif '\t\t' in province_house_list[i][j]:
            primary_houses_list.append([province_house_list[i][j].replace('\t\t', ''), middle_houses_list[-1][0], '基层'])
        elif province_house_list[i][j] == '新疆兵团分院':
            supreme_houses_list.append(['新疆兵团分院', '最高人民法院', '高级'])
        else:
            middle_houses_list.append([province_house_list[i][j], supreme_houses_list[-1][0], '中级'])

supreme_houses_df = pd.DataFrame(supreme_houses_list, columns = ['法院名称', '上诉法院', '级别'])
middle_houses_df = pd.DataFrame(middle_houses_list, columns = ['法院名称', '上诉法院', '级别'])
primary_houses_df = pd.DataFrame(primary_houses_list, columns = ['法院名称', '上诉法院', '级别'])

# save the results
primary_houses_df.to_csv('primary_courts.csv', header=True, index=True)
middle_houses_df.to_csv('middle_courts.csv', header=True, index=True)
supreme_houses_df.to_csv('supreme_courts.csv', header=True, index=True)