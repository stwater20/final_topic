from flask_bootstrap import Bootstrap
from config import DevConfig
from flask import Flask, render_template, request, jsonify
from db_process import Main_field, search_fun1, crawlerNewData, check_sid, check_last_Repeating, Insertdata,search_fun2,search_fun3
import datetime
import random

app = Flask(__name__)
app.config.from_object(DevConfig)
bootstrap = Bootstrap(app)

t1 = "region"
t2 = "desc"

@app.route('/')
def test():
    return render_template('test.html')


@app.route('/setData/')  # 路由
def setData():
    # now = datetime.datetime.now().strftime('%H:%M:%S')
    a = request.args.get('a',0,type=str)
    road = search_fun2("roadtype")
    temp = []
    for rd in road:
        temp.append(rd[0])
    data = { 'data': temp}
    return jsonify(data)  # 將數據以字典的形式傳回

@app.route('/t2')
def t2():
    return render_template('test2.html')


@app.route('/t3')
def t3():
    return render_template('test3.html')

@app.route('/at2')
def at2():
    a = request.args.get('a', 0, type=str)
    b1 = request.args.get('b', 0, type=str)
    b2 = request.args.get('c', 0, type=str)
    c1 = request.args.get('d', 0, type=str)
    c2 = request.args.get('e', 0, type=str)
    print(a,b1,b2,c1,c2)
    road = search_fun3(a,b1,b2,c1,c2)
    temp1 = []
    temp2 = []
    for rd in road:
        temp1.append(rd[0])
        temp2.append(rd[1])
    data = {'data1':temp1,'data2':temp2 ,'data3':a}
    return jsonify(data) 

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=str)
    b = request.args.get('b', 0, type=str)
    c = request.args.get('c', 0, type=str)
    road = search_fun1(a,b,c)
    output = "  <table class='table table-hover'><tr><td>路況區域</td>"
    output += "<td>資料來源</td>"
    output += "<td>地區區分說明</td>"
    # output += "<td>唯一編號</td>"
    output += "<td>方向</td>"
    # output += "<td>緯度</td>"
    output += "<td>發生時間</td>"
    output += "<td>路況類別</td>"
    output += "<td>道路名稱</td>"
    # output += "<td>修改時間</td>"
    output += "<td>路況說明</td>"
    output += "<td>發生時間</td></tr>"
    # output += "<td>經度</td></tr>"

    for rd in road:
        output = output \
        + "<tr><td>" + rd.region + "</td>" \
        + "<td>" + rd.srcdetail + "</td>" \
        + "<td>" + rd.areaNm + "</td>" \
        + "<td>" + rd.direction + "</td>" \
        + "<td>" + rd.happentime + "</td>" \
        + "<td>" + rd.roadtype + "</td>" \
        + "<td>" + rd.road + "</td>" \
        + "<td>" + rd.commemt + "</td>" \
        + "<td>" + rd.happendate + "</td></tr>" 
    output+="</table>"
    return jsonify(result=output)


@app.route("/demo", methods=["POST", "GET"])
def demo():
    nick_name = request.form.get("username")
    print(nick_name)
    return "ok"





if __name__ == '__main__':
    app.run()
