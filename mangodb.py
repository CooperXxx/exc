import pymongo
from bson.objectid import ObjectId

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb= myclient["order"]
mycollcetion = mydb["order"]

reserverdic1 = {
    "idpwd": {
        'ssid': 220184358,
        'pwd': "xwd2617976"
    },
    "info": {
        'dayInfo': "2019-09-02",
        'itemId': "7",
        'time': '12:00-13:00'
    },
    "phonemate": {
        "phone": 1885187965558,
        "mateid": [220184346],  # list 所有好友id
        "halffull": 1  # 1表示全场，2表示半场，非蓝球默认位1，或者空
    }
}


# print(datetime.date.today().strftime("%b%d%y"))
# x=mycollcetion.insert_one(reserverdic1)
# id=x.inserted_id

# print(x)
# print(id)



myresult = mycollcetion.find({ "_id" : ObjectId("5d6e0fd642f80cb7652fb613")},{"_id":0,"reservedic":0})

print(myresult[0]["status"])
for x in myresult:
    print(x["status"])

