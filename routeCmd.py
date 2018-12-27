# WIP Maurício de Castro Pasquotto
# https://mpasquotto.com.br
# https://github.com/maupasquotto

import sys
import os
from robobrowser import RoboBrowser  # jmcarp/robobrowser
import base64
import json
from requests import Session
import warnings
import texttable as tt
import numpy.ma as ma

# prepare
warnings.filterwarnings("ignore", category=UserWarning, module='robobrowser')

# variables
loginPage = 'http://' + sys.argv[1] + '/login?'
macAddressControl = 'http://' + sys.argv[1] + '/?wifi_mac'
macAddressControlList = 'http://' + sys.argv[1] + '/walk?oids=1.3.6.1.4.1.4115.1.20.1.1.3.28;&_n=42247&_=1545947481712'

# identifier
session = Session()
session.verify = False
rb = RoboBrowser(history=True, session=session, parser=None)

def base64Encode(strToEncode):
    return base64.b64encode(str(strToEncode).encode())

# Route login
def routeLogin():
    dataLogin = base64Encode(sys.argv[2])
    rb.open(loginPage + dataLogin.decode() + '&_n=05761&_=1545671875191')  # some random necessary integers
    resp = json.loads(rb.response.content.decode())
    if resp['valid'] == True:
        resp['technician'] = True #Found out that this flag allows me to have some more control
        print('- Route Login Successful')
        session.cookies.update({'credential' : base64Encode(resp).decode()})
    else:
        print('- Login Error')
        sys.exit()


# 'clear' window
def cls():
    print('\n' * 100)


# show mac List filter
def showMacList():
    # get json mac values
    rb.open(macAddressControlList)
    jsonMacList = json.loads(rb.response.content.decode())
    macValues = list(jsonMacList.values())
    # slice only macs
    macs = macValues[: int((len(macValues) -1) / 2)]
    ids = range(1, len(macs))

    # mask everything
    for key, val in enumerate(macs):
        macs[key] = val.replace('$', '')
        macs[key] = macs[key][:2] + ':' + macs[key][2:4] + ':' + macs[key][4:6] + ':' + macs[key][6:8] + ':' + macs[key][8:10] + ':' + macs[key][10:12]

    # make pretty
    tab = tt.Texttable()
    headings = ['#', 'Mac']
    tab.header(headings)
    for row in zip(ids, macs):
        tab.add_row(row)

    print('\n')
    print(tab.draw())
    print('\n')
    


# exe any special command
def doCommand(cmd):
    if cmd == '1':
        print('You have choosen MAC list')
        showMacList()
    if cmd == '0':
        print('\n# thank you\n')
        sys.exit()


def showMenu():
    print('- Route Command Available')
    print('=======================')
    print('| [ 0 ] Close         |')
    print('| [ 1 ] Show MAC list |')
    print('=======================')
    doCommand(input('# '))


# main verify
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: ' + sys.argv[0].rsplit('.', 1)[0] + 'host user:password [timer(ms)]')
    else:
        # clear
        cls()

        # route login with credentials
        routeLogin()

        while (True):
            # show Menu
            showMenu()
