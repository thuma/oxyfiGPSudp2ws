import websocket
import socket
import local
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

def on_message(ws, message):
    global sock
    sock.sendto(message, (local.ip, local.port))

def on_error(ws, error):
    print error
    exit()

def on_close(ws):
    print "### closed ###"
    exit()

def on_open(ws):
    print "### Open ###"


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://trainpos.oxyfi.com/connect/listen?bWFydGluQDQ2ZWxrcy5jb21AQDRmMDVkOWVjZjcxMjgyZWU4NzA3NGY5ZTUyYzBhOGQ5M2I0YzJjMTM=",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
