import pyodbc
import sys
import json
import requests
#gmaps = googlemaps.Client(key='GOOGLE_API_KEY', queries_per_second=50, retry_over_query_limit=False)
#Handling google map API quota exception




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



def search_fun1(search,sort,limit):
    sql = 'select TOP ' + str(limit) + ' * from Road order by ' + search \
        + ' ' + sort 
    cursor.execute(sql)
    rows = cursor.fetchall()  #記得要for row in rows
    return rows


def search_fun2(search):
    sql = 'select count(*), ' + search + ' from Road group by ' + search
    cursor.execute(sql)
    rows = cursor.fetchall()  # 記得要for row in rows
    return rows

def search_fun3(a,b1,b2,c1,c2):
    # sql = 'select count(*), ' +  a + ' from Road where \
    # substring(happendate, 6, 2)  between ' + b2 + ' and '+ c2 +' \
    # and substring(happendate,1,4) between ' + b1 + ' and ' + c1 + ' group by ' + a
    sql = 'select count(*), ' + str(a) +' from Road where \
    substring(happendate, 6, 2)  between ? and ?  \
    and substring(happendate,1,4) = ? or substring(happendate,1,4)= ? group by ' + str(a)
    cursor.execute(sql,b2,c2,b1,c1)
    rows = cursor.fetchall()  # 記得要for row in rows
    return rows


#以後有錢再說 one request per a day
def google_Geocoding(rows):
    ids = []
    for row in rows:
        geocode_result = gmaps.geocode(row.areaNm)
        loc = geocode_result[0]['geometry']['location']
        print("以" + row.areaNm + "為中心的半徑25000公尺的休息站數量：" + str(len(gmaps.places_radar(keyword="休息站",
                                                                                    location=loc, radius=25000)['result'])))
        for place in gmaps.places_radar(keyword="休息站",location=loc, radius=25000)['result']:
            ids.append(place['place_id'])
        break
    return ids


    
def check_sid():
    sql = 'select * from Road order by sid desc'
    cursor.execute(sql)
    row = cursor.fetchone()
    if not row:
        return 0
    else:
        return row.sid  
        
def check_last_Repeating():
    sql = 'select top 1 * from Road order by sid desc'
    cursor.execute(sql)
    row = cursor.fetchone()
    return row.modDttm

def Insertdata(data):
    sid = check_sid()
    check_modDttm = check_last_Repeating()
    sql = 'insert into Road values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
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
        if check_modDttm ==row[9]:
           break 
        cursor.execute(sql,sid,row[0],row[1],row[2],row[3],
        row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12])
        conn.commit()
    # conn.close()


    
data = crawlerNewData(url)
#Insertdata(data)
#search_fun1("region", "desc", 1)
#Insertdata(data)
# t = search_fun3("roadtype", "2018", "01","2019","08")
# for l in t:
#     print(l)


