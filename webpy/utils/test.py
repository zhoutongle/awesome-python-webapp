#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import hashlib
import socket
import base64
from time import sleep

flag = 0
ths = []

class websocket_thread(threading.Thread):
    def __init__(self, connection):
        super(websocket_thread, self).__init__()
        self.connection = connection

    def run(self):
        global flag
        print 'new websocket client joined!'
        reply = 'i got u, from websocket server.'
        length = len(reply)
        while True:
            data = self.connection.recv(1024)
            re = parse_data(data)
            print re
            self.connection.send('%c%c%s' % (0x81, length, reply))
def parse_data(msg):
    v = ord(msg[1]) & 0x7f
    if v == 0x7e:
        p = 4
    elif v == 0x7f:
        p = 10
    else:
        p = 2
    mask = msg[p:p + 4]
    data = msg[p + 4:]

    return ''.join([chr(ord(v) ^ ord(mask[k % 4])) for k, v in enumerate(data)])


def parse_headers(msg):
    headers = {}
    header, data = msg.split('\r\n\r\n', 1)
    for line in header.split('\r\n')[1:]:
        key, value = line.split(': ', 1)
        headers[key] = value
    headers['data'] = data
    return headers


def generate_token(msg):
    key = msg + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    ser_key = hashlib.sha1(key).digest()
    return base64.b64encode(ser_key)

def change():
    global flag
    if flag == 0:
        flag = 1
        
def play():
    global flag, ths
    print flag, ths
    #return ths
    print len(ths)
    for i in ths:
        reply = 'hello world 123.'
        length = len(reply)
        i.send('%c%c%s' % (0x81, length, reply))
        

if __name__ == '__main__':
    flag, ths
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 3000))
    sock.listen(5)

    while True:
        connection, address = sock.accept()
        try:
            data = connection.recv(1024)
            headers = parse_headers(data)
            token = generate_token(headers['Sec-WebSocket-Key'])
            connection.send('\
HTTP/1.1 101 WebSocket Protocol Hybi-10\r\n\
Upgrade: WebSocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Accept: %s\r\n\r\n' % token)
            thread = websocket_thread(connection)
            thread.start()
            ths.append(connection)
            play()
            # print ths
            # for i in ths:
                # reply = 'hello world.'
                # length = len(reply)
                # i.send('%c%c%s' % (0x81, length, reply))
        except socket.timeout:
            print 'websocket connection timeout'
