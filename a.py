from flask import Flask,request, render_template
import pymongo
from bson.objectid import ObjectId

app=Flask(__name__)
def getstatus(mycol,orderid):
    return mycol.find({ "_id" : ObjectId(orderid)},{"_id":0,"reservedic":0,"ssid":0})[0]["status"]

def getstatus2(mycol,ssid):
    return mycol.find({'ssid':ssid},{"reservedic":0,"ssid":0})[0]["_id"],mycol.find({'ssid':ssid},{"reservedic":0,"ssid":0})[0]["status"]


def orderinsert(reservedic):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["order"]
    mycol = mydb["order"]
    reservedic={"reservedic":reservedic,
                "status":"登记预约中",
                "ssid":reservedic["idpwd"]["ssid"],
                "date":reservedic["info"]['dayInfo']
                }
    orderid=mycol.insert_one(reservedic).inserted_id
    status=getstatus(mycol,orderid)
    return orderid,status

@app.route('/find2',methods=['POST'])
def finds2():

    ssid = request.form['ssid']
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["order"]
    mycol = mydb["order"]

    orderid,status = getstatus2(mycol,ssid)

    return render_template("condition.html", orderid=orderid, orderstatus=status)


@app.route('/find',methods=['POST'])
def finds():


    orderid = request.form['rsid']
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["order"]
    mycol = mydb["order"]

    status = getstatus(mycol,orderid)

    return render_template("condition.html", orderid=orderid, orderstatus=status)


@app.route('/findstatus',methods=['GET','POST'])
def findstatus():
    return render_template("findstatus.html")


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        ssid = request.form['ssid']
        pwd = request.form['pwd']
        idpwd = {"ssid":ssid,"pwd":pwd}
        dayInfo = request.form['dayinfo']
        itemId = request.form['itemID']
        time = request.form['time']
        info = {"dayInfo":dayInfo,"itemId":itemId,"time":time}
        phone = int(request.form['phone'])
        if len(request.form['mateid']) == 0:
            mateid=[]
        else:
            mateid = request.form['mateid'].split(";")
        if itemId ==8 and len(request.form['halffull']) != 0:
            halffull = int(request.form['halffull'])
        else:
            halffull = None
        phonemate = {"phone":phone,"mateid":mateid, "halffull": halffull}
        
        reserverdic={"idpwd":idpwd,"info":info, "phonemate":phonemate}
        print(reserverdic)

        id, status=orderinsert(reserverdic)
        # main(reserverdic)
        print(id,print(status))
        return render_template("condition.html",orderid=id,orderstatus=status)
    else:
        return render_template("a.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8000, debug=True)