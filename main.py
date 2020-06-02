from flask import Flask, render_template,request,redirect,url_for # For flask implementation    
from bson import ObjectId # For ObjectId to work    
from pymongo import MongoClient    
import os    
import datetime as dt

app = Flask(__name__)
title = 'Diary'
heading = 'Your Diary'


@app.route('/write')
def write():
    todo.insert({"name":'abc'})
    return redirect('/list')

@app.route('/list')
def list():
    t = todo.find()
    x = ""
    for to in t:
        x = to['name']
    return x

@app.route('/addNotes/', methods = ['POST'])
def addNotes():
    notes = ''
    if request.method == 'POST':
        notes = request.form
        notes = notes['notes']
    today = dt.datetime.now()
    year = today.year
    month = today.strftime("%B")
    day = today.day
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['dbDiary']
    coll = db['diaryNotes']
    id = str(today.year) + str(today.month) + str(today.day)
    data = [
        {
            "_id":id,
            "notes": notes
        }
    ]
    if coll.count_documents({"_id":id}, limit = 1):
        res = coll.update_one({"_id":id}, {"$set":{"notes":notes}})
    else:
        res = coll.insert(data)
    print(res)
    
    return '<h5> Success </h5>'

@app.route('/')
def index():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['dbDiary']
    print("Created or Connected to the database: dbDiary")
    today = dt.datetime.now()
    coll = db['diaryNotes']
    id = str(today.year) + str(today.month) + str(today.day)
    preText = ''
    if coll.count_documents({"_id":id}, limit = 1):
        i = coll.find_one({'_id':id})
        print(i['notes'])
        preText = i["notes"]
    return render_template('index.html', day = today.day ,month = today.strftime("%B"), year = today.year, preText = preText)

if __name__ == "__main__":
    app.run(debug = True)