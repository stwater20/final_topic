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





connStr = 'DRIVER={ODBC Driver 11 for SQL Server};SERVER=localhost;DATABASE=Road_Info;Trusted_Connection=yes'
conn = pyodbc.connect(connStr)
cursor = conn.cursor()

Main_field = ("region", "srcdetail", "areaNm", "UID",
                  "direction", "y1", "happentime", "roadtype", "road", "modDttm",
                  "comment", "happendate", "x1")

url = 'https://od.moi.gov.tw/MOI/v1/pbs'

def check_sid():
    sql = 'select * from Road_Info_main order by sid desc'
    cursor.execute(sql)
    row = cursor.fetchone()
    if not row:
        return 0
    else:
        return row.sid
'''      
class Info:
    def _init_(self,region,srcdetail,areaNm,UID,direction,y1,happentime,roadtype,road,modDttm,comment,happendate,x1):
        self.region = region
        self.srcdetail=srcdetail
        self.areaNm = areaNm
'''       
    

def Insertdata(data):
    sid = check_sid()
    sql = 'insert into Road_Info_main values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
    for i in range(0,len(data)):
        sid+=1
        row = {}
        row[0] = data[i]['region']
        row[1] = data[i]['srcdetail']
        row[2] = data[i]['areaNm']
        row[3] = data[i]['UID']
        row[4] = data[i]['direction']
        row[5] = data[i]['y1']
        row[6] = data[i]['happentime'] 
        row[7] = data[i]['roadtype']
        row[8] = data[i]['road']
        row[9] = data[i]['modDttm']
        row[10] = data[i]['comment'] #忽略上限太高
        row[11] = data[i]['happendate']
        row[12] = data[i]['x1']
        # max = 0 算最大值
        # if max < row[10]:
        #     max = row[10]
        # print(max)
        cursor.execute(sql,sid,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])
        conn.commit()
    conn.close()


    
data = crawlerNewData(url)


Insertdata(data)



#def insertData(data):

