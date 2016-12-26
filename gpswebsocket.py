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
    if environ['PATH_INFO'].startswith('/listen'):
        try:
            ws = environ['wsgi.websocket']
        except: 
            start_response('200 OK', [('Content-Type', 'text/plain')])
            info('no ws found',environ)
            info('test',environ['wsgi.input'])
	    return "Only ws support"
	
        try:
            (email, authkey) = b64decode(environ['QUERY_STRING']).split('@@')
        except:
            ws.send('authincorrect')
            return None

        listeners[email] = []
        active[email] = ws
        
        info('email',email)
        info('auth', authkey)
        checkauth = sha1(email+local.key).hexdigest()
        
        
        if authkey != checkauth:
            ws.send('authincorrect')
            return None

        while 1:
            if active[email] != ws:
                break

            if len(listeners[email]) > 0:
                tosend = listeners[email].pop(0)
                try:
                    ws.send(tosend)
                except:
                    break
            else:
                sleep(1)

        info("websocketend", ws)

#
# Handle incoming requests.
#
def sendcall(environ, start_response):
    global listeners

    # Headers for return on text / json  = error / ok.
    textheader = [
        ('Content-Type', 'text/plain'),
        #('Access-Control-Allow-Origin', 'http://46elks.dev:80'),
        ('Access-Control-Allow-Credentials', 'true')]

    headers = [
        ('Content-Type', 'application/json'),
        #('Access-Control-Allow-Origin', 'http://46elks.dev:80'),
        ('Access-Control-Allow-Credentials', 'true')]

    info('request', environ['PATH_INFO'], environ['REQUEST_METHOD'])

    #
    # Incoming SMS
    #
    if environ['PATH_INFO'] == '/list':

        start_response('200 OK', textheader)
        users = []
        for one in listeners:
            users.append(one)
        info(','.join(users))
        return[','.join(users)]
    else:
        start_response('404 Not Found', textheader)
        return['']
        
def sendtoall(data):
    global listeners
    for one in listeners:
        listeners[one].append(data)

def runsocket():
    UDP_IP = "195.154.5.127"
    UDP_PORT = 6565
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

websocketport = 7070
webapiport = 7080

info('Starting WS on port %s' % websocketport)
wsserver = pywsgi.WSGIServer(("", websocketport), listenforevents, log = nologger , handler_class=WebSocketHandler)
wsserver.start()

sockrunner = spawn(runsocket)

info('Starting POST API on port %s' % webapiport)
server = pywsgi.WSGIServer(("", webapiport), sendcall, log = nologger)
server.serve_forever()
