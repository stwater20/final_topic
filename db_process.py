import pyodbc
import sys
import json
import requests


def crawlerNewData(url):
    resp = requests.get(url)
    json_dict = (resp.json())
    return json_dict
#print(type(json_dict))
#print(type(json_dict[0]))
#print(len(json_dict))
#region(路況區域)、srcdetail(資料來源)、areaNm(地區區分說明)
# 、UID(唯一編號)、direction(方向)、y1(緯度)、happentime(發生時間)
# 、roadtype(路況類別)、road(道路名稱)、modDttm(修改時間)、comment(路況說明)
# 、happendate(發生時間)、x1(經度)





connStr = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=localhost;DATABASE=bike_crime;Trusted_Connection=yes'
conn = pyodbc.connect(connStr)
cursor = conn.cursor()

Main_field = list("region", "srcdetail", "areaNm", "UID",
                  "direction", "y1", "happentime", "roadtype", "road", "modDttm",
                  "comment", "happendate", "x1")

url = 'https://od.moi.gov.tw/MOI/v1/pbs'



data = crawlerNewData(url)
print(data)

#def insertData(data):

