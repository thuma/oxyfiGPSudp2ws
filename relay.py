#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent import spawn, sleep, pywsgi
from geventwebsocket.handler import WebSocketHandler
import uuid
import websocket

#
# Global data to be accessed from multipple requests
#
listeners = {}

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

def sendtoall(data):
    global listeners
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
ws = websocket.WebSocketApp("wss://api.oxyfi.com/trainpos/listen?v=1&key=e6ab725a30ef45f6a38c3a9b83f5f65a",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
ws.on_open = on_open
ws.run_forever()





