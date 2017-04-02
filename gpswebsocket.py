#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gevent import monkey; monkey.patch_all()
from gevent import pywsgi
from gevent import spawn
from geventwebsocket.handler import WebSocketHandler
from time import sleep
import socket
from base64 import b64decode
from hashlib import sha1
from copy import copy
import local
import trafiklabapi
import urlparse
import json

#
# Global data to be accessed from multipple requests
#
listeners = {}
active = {}

def info(name, *args):
    t = str(name)
    for a in args:
       t = t + "," + str(a)
    print t

#
# Listen for WebSocket and attach WebSocket to the listeners array.
#
def listenforevents(environ, start_response):

    info('ws_request', environ['PATH_INFO'])
    global listeners
    global active

    if environ['PATH_INFO'].startswith('/listen'):
        try:
            ws = environ['wsgi.websocket']
        except: 
            start_response('200 OK', [('Content-Type', 'text/plain')])
            info('no ws found',environ)
            info('test',environ['wsgi.input'])
        return "Only ws support"

        getdata = urlparse.parse_qs(environ['QUERY_STRING'])

        if 'key' in  getdata:
            keydata = trafiklabapi.getOneKey(getdata['key'][0])
            if keydata["Active"] == True:
                info('Authok', getdata['key'])
                key = getdata['key']
            else:
                ws.send('authincorrect')
                return None
        else:
            ws.send('authincorrect')
            return None

        active[key] = ws
        listeners[key] = []

        while 1:

            if active[key] != ws:
                break

            if len(listeners[key]) > 0:
                tosend = listeners[key].pop(0)
                try:
                    ws.send(tosend)
                except:
                    break
            else:
                sleep(0.5)

        info("websocketend", ws)
        if active[key] == ws:
            del listeners[key]
            del active[key]

def wrapper(data):
    return json.dumps({
            "StatusCode" : 200,
            "Message" : "",
            "ExecutionTime" : 72,
            "ResponseData" : data }
            )
 
#
# Handle incoming requests.
#
def sendcall(environ, start_response):
    global listeners
    
    # Headers for return on text / json  = error / ok.
    textheader = [
        ('Content-Type', 'text/plain'),
        ('Access-Control-Allow-Credentials', 'true')]

    jsonheaders = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Credentials', 'true')]

    info('request', environ['PATH_INFO'], environ['REQUEST_METHOD'])

    if 'HTTP_AUTHORIZATION' not in environ:
        start_response('401 Unauthorized', textheader)
        return['Basic Auth Required']

    if environ['HTTP_AUTHORIZATION'] not in local.auth:
        start_response('401 Unauthorized', textheader)
        return['Credentials incorrect']

    get = False
    post = False
    put = False
    delete = False
    
    if environ['REQUEST_METHOD'] == 'GET':
        get = True
    elif  environ['REQUEST_METHOD'] == 'POST':
        post = json.loads(environ['wsgi.input'].read())
    elif  environ['REQUEST_METHOD'] == 'PUT':
        put = json.loads(environ['wsgi.input'].read())
    elif  environ['REQUEST_METHOD'] == 'DELETE':
        delete = True

    if environ['PATH_INFO'] == '/v1/apikeys/apis/oxygps/profiles' and get:
        start_response('200 OK', jsonheaders)
        return [wrapper([
            {
            "Id": "One",
            "Name": "Standard",
            "Api": "oxygps",
            "RateLimit": {
                "Month": 24000,
                "Minute": 6
                },
            "Default": true,
            "CreatedDate": "2017-01-01T15:00:00.000Z",
            "UpdatedDate": "2017-01-01T15:00:00.000Z"
            }
        ])]
     
    if environ['PATH_INFO'] == '/v1/apikeys/apis/oxygps/keys' and post:
        start_response('200 OK', jsonheaders)
        newkey = trafiklabapi.makeKey(post)
        info('newkeycreated')
        return [wrapper(newkey)]

    if environ['PATH_INFO'] == '/v1/apikeys/apis/oxygps/keys' and get:
        start_response('200 OK', jsonheaders)
        list = []
        for key in trafiklabapi.getAllKeys():
            list.append(key)
        return [wrapper(list)]
    
    if environ['PATH_INFO'].startswith('/v1/apikeys/keys/') and get:
        start_response('200 OK', jsonheaders)
        key = environ['PATH_INFO'].split("/")[-1]
        keydata = trafiklabapi.getOneKey(key)
        return [wrapper(keydata)]
    
    if environ['PATH_INFO'].startswith('/v1/apikeys/keys/') and put:
        start_response('200 OK', jsonheaders)
        key = environ['PATH_INFO'].split("/")[-1]
        return [wrapper(trafiklabapi.updateKey(key,put))]

    if environ['PATH_INFO'].startswith('/v1/apikeys/keys/') and delete:
        start_response('200 OK', jsonheaders)
        key = environ['PATH_INFO'].split("/")[-1]
        keydata = trafiklabapi.dissableKey(key)
        return [wrapper(keydata)]

    else:
        start_response('404 Not Found', textheader)
        return['']

def sendtoall(data):
    global listeners
    for one in listeners:
        listeners[one].append(data)

def runsocket():
    UDP_IP = local.ip
    UDP_PORT = local.port
    sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
        sendtoall(data)

class nologgerclass(object):
  def __init__(self):
    self.current = ''
  def write(self, data):
      pass

nologger = nologgerclass()

websocketport = 7071
webapiport = 7081

info('Starting WS on port %s' % websocketport)
wsserver = pywsgi.WSGIServer(("", websocketport), listenforevents, log = nologger , handler_class=WebSocketHandler)
wsserver.start()

sockrunner = spawn(runsocket)

info('Starting POST API on port %s' % webapiport)
server = pywsgi.WSGIServer(("", webapiport), sendcall, log = nologger)
server.serve_forever()
