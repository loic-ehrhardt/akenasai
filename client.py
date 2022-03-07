#!/usr/bin/python2

import xmlrpclib
from hashlib import sha256
import socket

class Client:
    def __init__(self, ip, port):
        self.xmlrpc_client = xmlrpclib.ServerProxy(
            'http://{0}:{1}'.format(ip,port))
        self.xorKey = ('P58QH+/1I4u9kJWqPlstle5iIYNo9S7OvuTNbvAzv'+
                       '/pr8g01XVfMG+5xZvp+KdwW+r0=').decode('base64')
        socket.setdefaulttimeout(3)

    def _get_key(self):
        # Get server key
        skey = self.xmlrpc_client.get_key().decode('base64')
        # Compute response key
        self.key = sha256(2 * (skey + self.xorKey + "".join(
            [chr(ord(c1)^ord(c2)) for (c1,c2) in zip(skey,self.xorKey)]))
            ).hexdigest()

    def quit(self):
        self._get_key()
        self.xmlrpc_client.quit(self.key)

    def garage_press(self):
        self._get_key()
        self.xmlrpc_client.garage_press(self.key)

if __name__ == '__main__':
   client = Client('127.0.0.1', 12345)
