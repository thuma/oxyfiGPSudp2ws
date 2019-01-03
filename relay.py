#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent import spawn, sleep, pywsgi
from geventwebsocket.handler import WebSocketHandler
from pymongo import MongoClient
import uuid
import websocket
from datetime import datetime


#
# Global data to be accessed from multipple requests
#
listeners = {}
db = MongoClient().trv

# Listen for WebSocket and attach WebSocket to the listeners array.
#
def listenforevents(environ, start_response):
    global listeners
    print 'ws_request'
    key = uuid.uuid4().hex

    try:
        ws = environ['wsgi.websocket']
    except: 
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return "Only ws support."
    listeners[key] = []
    while 1:
        if len(listeners[key]) > 0:
            tosend = listeners[key].pop(0)
            try:
                ws.send(tosend)
            except:
                break
        else:
            sleep(0.25)
    del listeners[key]

def readnmea(data):
    direction = {"N":1,"S":-1,"W":-1,"E":1}
    out = {}
    parts = data.split(',')
    out["time"] = datetime_object = datetime.strptime(parts[9] + "T" + parts[1].split('.')[0], '%d%m%yT%H%M%S') 
    out["location"] = {
      "type": "Point",
      "coordinates": [
        float(parts[5][0:3]) + float(parts[5][3:])/60.0 * direction[parts[6]],
        float(parts[3][0:2]) + float(parts[3][2:])/60.0 * direction[parts[4]]]
    }
    out["speed"] = float(parts[7]) * 1.85200
    out["id"] = parts[14]
    try:
        out["direction"] = float(parts[8])
    except:
        out["direction"] = None
    return out

#$GPRMC,114632.0,A,6000.966781,N,01308.263916,E,4.7,170.9,030119,0.0,E,A*02,,1414.trains.se,,8964.public.trains.se@2019-01-03;8964.internal.trains.se@2019-01-03,oxyfi
def sendtoall(data):
    global listeners
    global db
    structdata = readnmea(data)
    db.postdata.insert(structdata)
    for one in listeners:
        listeners[one].append(data)

class nologgerclass(object):
  def __init__(self):
    self.current = ''
  def write(self, data):
    pass

nologger = nologgerclass()

websocketport = 7071
wsserver = pywsgi.WSGIServer(("", websocketport), listenforevents, log = nologger , handler_class=WebSocketHandler)
wsserver.start()

def on_message(ws, message):
    sendtoall(message.strip())

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    print "### Open ###"

websocket.enableTrace(True)
#ws = websocket.WebSocketApp("wss://map.thure.org/oxyfigps/",
ws = websocket.WebSocketApp("wss://api.oxyfi.com/trainpos/listen?v=1&key=e6ab725a30ef45f6a38c3a9b83f5f65a",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
ws.on_open = on_open
ws.run_forever()





