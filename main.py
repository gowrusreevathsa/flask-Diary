from flask import Flask, render_template,request,redirect,url_for # For flask implementation    
from bson import ObjectId # For ObjectId to work    
from pymongo import MongoClient    
import os    
import datetime as dt

app = Flask(__name__)
title = 'Diary'
heading = 'Your Diary'
day = None
month = None
year = None
monthName = None
id = None


@app.route('/showPrevNotes/', methods=['POST'])
def showPrevNotes(dateidP = None):
    if dateidP != None:
        print(dateidP)
        return redirect(url_for('showNotes', dateid = dateidP))
    if request.method == 'POST':
        dateidT = request.form
        dateidT = dateidT['dateInput']
    return showPrevNotes(dateidT)


@app.route('/<dateid>')
@app.route('/showNotes/<dateid>')
def showNotes(dateid):
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['dbDiary']
    coll = db['diaryNotes']
    showId = str(dateid)
    if len(dateid) != 8:
        return redirect(url_for('index'))
    i = coll.find_one({"_id":showId})
    dayT, monthT, yearT = detailsFromDateId(dateid)
    if i == None:
        preText = "Oops! You don't have any notes for this day :(" 
        return render_template('index.html', day = dayT, month = dt.date(2020, int(monthT), 1).strftime('%B'), year = yearT, preText = preText)
    else:
        return render_template('index.html', day = dayT, month = dt.date(2020, int(monthT), 1).strftime('%B'), year = yearT, preText = i['notes'])

@app.route('/addNotes/', methods = ['POST'])
def addNotes():
    notes = ''
    if request.method == 'POST':
        notes = request.form
        notes = notes['notes']
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['dbDiary']
    coll = db['diaryNotes']
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

    for i in coll.find():
        print(i)
    
    return redirect(url_for('showNotes', dateid = id))

@app.route('/')
@app.route('/index/')
def index():
    client = MongoClient("mongodb://127.0.0.1:27017")
    db = client['dbDiary']
    print("Created or Connected to the database: dbDiary")
    coll = db['diaryNotes']
    preText = ''
    if coll.count_documents({"_id":id}, limit = 1):
        i = coll.find_one({'_id':id})
        print(i['notes'])
        preText = i["notes"]
    return render_template('index.html', day = day ,month = monthName, year = year, preText = preText)

def getID():
    today = dt.datetime.now()
    day = today.day
    month = today.month
    if day < 10:
        day = '0' + str(day)
    if month < 10:
        month = '0' + str(month)
    year = str(today.year)
    return day, month, year, day + month + year

def detailsFromDateId(dateid):
    day = dateid[:2]
    month = dateid[2:4]
    year = dateid[4:]

    return day, month, year

if __name__ == "__main__":
    day, month, year, id = getID()
    monthName = dt.datetime.now().strftime("%B")
    app.run(debug = True)