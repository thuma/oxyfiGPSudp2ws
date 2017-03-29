# -*- coding: utf-8 -*-
import lmdb
import json
from datetime import datetime
import uuid
import pickle

db = lmdb.open('oxyapi.lmdb', 500000000)

def updatedb(key, data):
    with db.begin(write=True) as dbconn:
        dbconn.put(key, pickle.dumps(data))

def makeKey(data):
    fulldate = datetime.utcnow().isoformat('T') + "Z" 
    data = {
      "Key":uuid.uuid4().get_hex(),
      "Note":data["Note"],
      "Api":"oxygps",
      "Profile":"One",
      "Project": data["Project"]["Id"],
      "CreatedDate":fulldate,
      "UpdatedDate":fulldate,
      "Active":True
    }
    updatedb(data['Key'],data)
    return data
    
def getAllKeys():
    with db.begin() as dbconn:
        with dbconn.cursor() as curs:
            for key in curs:
                 yield pickle.loads(key[1])

def getOneKey(key):
    with db.begin() as dbconn:
        return pickle.loads(dbconn.get(key))

def updateKey(key,putdata):
    data = getOneKey(key)
    if 'Note' in putdata:
        data['Note'] = putdata['Note']
        updatedb(data["Key"], data)
    return data

def dissableKey(key):
    data = getOneKey(key)
    data["Active"] = False
    updatedb(data["Key"], data)
    return data

newkeyrequest = '''{
  "Note":"2014-01-01: Nyckel skapas",
  "Project":{
    "Id":"23134",
    "Name":"Ny cool app",
    "Status":[
      "Test",
      "Terminated"
    ],
    "ShortDescription":"We do stuff",
    "LongDescription":"We do a lot of stuff",
    "Users":[
      {
        "Id":"87987",
        "FirstName":"Hans",
        "LastName":"Hansson",
        "Email":"hans@hansson.nu"
      },
      {
        "Id":"42",
        "FirstName":"Per",
        "LastName":"Pärzon",
        "Email":"per@hansson.nu"
      }
    ]
  }
}'''

