import sys
import os
from robobrowser import RoboBrowser #jmcarp/robobrowser
import base64
import json
from io import StringIO
from requests import Session

# /router.html?wifi_mac
# variables
loginPage = 'http://' + sys.argv[1] + '/login?'

# identifier
session = Session()
session.verify = False
rb = RoboBrowser(history = True, session = session)

# Route login
def routeLogin():
    dataLogin = base64.b64encode((sys.argv[2]).encode())
    rb.open(loginPage + dataLogin.decode() + '&_n=05761&_=1545671875191') #some random necessary integers
    resp = json.load(StringIO(rb.response.content.decode()))
    if resp['valid'] == True:
        print('# Logou')
    else:
        print('Nao Logou')

# 'clear' window
def cls():
    print('\n'*100)

# exe any special command
def doCommand():
    
    cmd = sys.argv[3]


    #if cmd == 'macs':

    return

# main veirify
if __name__ == '__main__':
    cls()
    if len(sys.argv) < 3:
        print('usage: ' + sys.argv[0].rsplit('.', 1)[0] + 'host user:password command [timer(ms)]')
    else:
        routeLogin()
        doCommand()
