from datetime import datetime
from dotenv import load_dotenv
import bson
from bson.objectid import ObjectId
import flask
import os
import json
import pymongo

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
    try:
        date_obj = datetime.strptime(date, '%d-%m-%y')
        format_data = date_obj.strftime('%d %b %y')
        data = list(db.banktransactiondetails.find({ "Date": format_data }))
        if(data):
            for value in data:
                value["_id"] = str(value["_id"])
            return json.dumps(data)
        return f"No transactions on {date}"
    except ValueError: 
        return f"Check date format. {date} does not match format '%d-%m-%y'"

@app.route('/balance/<date>')
def get_balance(date):
    try:
        date_obj = datetime.strptime(date, '%d-%m-%y')
        format_data = date_obj.strftime('%d %b %y')
        data = list(db.banktransactiondetails.find({ "Date": format_data}))
        if(data):
            for value in data:
                value["_id"] = str(value["_id"])
            balance = data[-1]["Balance AMT"]
            return f"Balance at the end of {date} is: {balance}"
        return f"No transactions on {date}"
    except ValueError: 
        return f"Check date format. {date} does not match format '%d-%m-%y'"

@app.route('/details/<id>')
def get_details(id):
    try:
        objId = ObjectId(id)
        data = db.banktransactiondetails.find_one({"_id" : objId})
        if(data):
            data["_id"] = str(data["_id"])
            return json.dumps(data)
        return f"No data Found for Id: {id}. Check Id"
    except bson.errors.InvalidId:
        return "Invalid Id. Id must be a valid BsonId"

if __name__=="__main__":
    app.run(debug=True)