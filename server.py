from flask import Flask, request
from flask import *
from flask_cors import CORS
from bson import json_util
from pymongo import MongoClient
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv(find_dotenv())
password = os.environ.get("MONGODB_PASS")
cluster = f"mongodb+srv://user:{password}@cluster0.pxarpgw.mongodb.net/test?retryWrites=true&w=majority"
client = MongoClient(cluster)
db = client.test

@app.route("/publish", methods=["POST"])
def publish():
    collection = db.test
    uid = request.form['uid']
    title = request.form['title']
    content = request.form['content']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    document = {
        "uid": uid,
        "title": title,
        "content": content,
        "start_date": start_date,
        "end_date": end_date,
    }
    collection.insert_one(document)
    return "ok"

@app.route("/get-news", methods=["GET"])
def get_news():
    news_list = []
    news_collection = db.test
    news = news_collection.find()
    for elem in news:
        news_list.append(elem)
    return json.loads(json_util.dumps(news_list))

@app.route('/remove')
def remove():
    uid = request.args.get('uid')
    print(uid)
    news_collection = db.test
    news_collection.delete_one({"uid": uid})
    return "file removed"

if __name__ == "__main__":
    app.run(debug=True)