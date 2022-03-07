#!/usr/bin/python

#-----------------------------------------------------------------------
# Imports and parameters
#-----------------------------------------------------------------------

import xmlrpclib
from hashlib import sha256
import socket

#-----------------------------------------------------------------------
# Client class
#-----------------------------------------------------------------------

class Client:

   def __init__(self,ip,port):
      self.p = xmlrpclib.ServerProxy('http://{0}:{1}'.format(ip,port))
      self.xorKey = ('P58QH+/1I4u9kJWqPlstle5iIYNo9S7OvuTNbvAzv'+
                    '/pr8g01XVfMG+5xZvp+KdwW+r0=').decode('base64')
      # Socket timeout set to 3 seconds
      socket.setdefaulttimeout(3)

   def _get_key(self):
      # Get server key
      skey = self.p.get_key().decode('base64')
      # Compute second key
      self.key = sha256( 2 * ( skey + self.xorKey + "".join(
                 [chr(ord(c1)^ord(c2)) for (c1,c2) in zip
                 (skey,self.xorKey)]))).hexdigest()

   def quit(self):
      self._get_key()
      self.p.quit(self.key)

   def garage_press(self):
      self._get_key()
      self.p.garage_press(self.key)

#-----------------------------------------------------------------------
# Main program
#-----------------------------------------------------------------------

if __name__ == '__main__':
   client = Client('127.0.0.1',34859)


