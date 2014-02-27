'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''

version = '0.0.1'

import socket
from myClientSend import *
from myClientReceive import *
import sys
from struct import unpack
import xml.etree.ElementTree as ET
from XMLvalidator import XMLValidate as val

#opcode associations; note that these opcodes will be returned by the server
opcodes = { 11: create_success,
            12: general_failure,
            21: delete_success,
            22: general_failure,
            31: deposit_success,
            32: general_failure,
            41: withdraw_success,
            42: general_failure,
            51: balance_success,
            52: general_failure,
            61: end_session_success,
            62: unknown_opcode
           }

def getInput():
    print '''
CONNECTED TO ATM SERVER - type the number of a function:
    (1) Create Account
    (2) Delete Account
    (3) Deposit Money to an Account
    (4) Withdraw Money from an Account
    (5) Check the Balance of an Account
    (6) End Session
    '''
    netBuffer = raw_input('>> ')
    return netBuffer

def processInput(netBuffer, mySocket):
    #create
    if netBuffer == str(1):
        create_request(mySocket)

    #delete
    elif netBuffer == str(2):
        delete_request(mySocket)

    #deposit
    elif netBuffer == str(3):
        deposit_request(mySocket)

    #withdraw
    elif netBuffer == str(4):
        withdraw_request(mySocket)

    #balance
    elif netBuffer == str(5):
        balance_request(mySocket)

    #quit
    elif netBuffer == str(6):
        end_session(mySocket)

    return

def getResponse(mySocket):

    # wait for server responses...
    while True:
        try:
            retBuffer = mySocket.recv( 1024 )
        except:

            # close the client if the connection is down
            print "ERROR: connection down"
            sys.exit()

        if len(retBuffer) != 0:

            # parse the buffer string into xml format
            xml = ET.fromstring(retBuffer)

            # only allow correct version numbers and checksums
            if val.validate(xml):

                # send packet to correct handler
                try:
                    opcode = int(xml.find('status').text)
                    opcodes[opcode](mySocket,xml)
                except KeyError:
                    break

            break
        return

if __name__ == '__main__':
    if(len(sys.argv) != 3):
        print "ERROR: Usage 'python myClient.py <host> <port>'"
        sys.exit()

    #get the address of the server
    myHost = sys.argv[1]
    myPort = sys.argv[2]
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        mySocket.connect ( ( myHost, int(myPort)) )
    except:
        print "ERROR: could not connect to " + myHost + ":" + myPort
        sys.exit()

    while True:
        netBuffer = getInput()
        #menu selection and function priming
        processInput(netBuffer, mySocket)
        getResponse(mySocket)

    mySocket.close()
