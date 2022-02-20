import flask
import os
import json
from datetime import datetime
from dotenv import load_dotenv
import pymongo
from bson.objectid import ObjectId
from models.bank import BankTransactionDetail
from schemas.bank import serializeDict, serializeList

load_dotenv()


MONGO_KEY = os.getenv('MONGO_URI')
client = pymongo.MongoClient(MONGO_KEY)
db = client["bankCallify"]
app = flask.Flask(__name__)

@app.route('/')
def home():
    return "Hello World"

@app.route('/transactions/<date>')
def get_transactions(date):
    #go to db and find the 
    print(date)
    date_obj = datetime.strptime(date, '%d-%m-%y')
    print(date_obj)
    rd=date_obj.strftime('%d %b %y')
    print(rd)
    data = list(db.banktransactiondetails.find({ "Date": rd}))
    for details in data:
        details["_id"] = str(details["_id"])
    return json.dumps(data)

@app.route('/balance/<date>')
def get_balance(date):
    print(date)
    #go to db and find the 
    date_obj = datetime.strptime(date, '%d-%m-%y')
    print(date_obj)
    rd=date_obj.strftime('%d %b %y')
    print(rd)
    data = list(db.banktransactiondetails.find({ "Date": rd}))
    for i in data:
        i["_id"] = str(i["_id"])
    balance=data[-1]["Balance AMT"]
    print(balance)
    return json.dumps(balance)

@app.route('/details/<id>')
def get_details(id):
    print(id)
    data = list(db.banktransactiondetails.find_one(id))
    for i in data:
        i["_id"] = str(i["_id"])
    return json.dumps(data)

if __name__=="__main__":
    app.run(debug=True)