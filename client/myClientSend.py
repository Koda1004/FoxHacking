'''
Created on Feb 18, 2010

altered on Feb. 20, 2014
'''

from struct import pack
from sys import maxint, exit
from xmlpackager import XMLClientPackage as xml

version = '0.0.1'

#create new account
def create_request(conn):

    print "CREATING AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue

        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    print "enter a starting balance:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
    
    # should refactor opcodes
    package = xml.client_package(version, 10, [act,bal])
    send_message(package,conn)

    return

#delete an existing account
def delete_request(conn):
    print "DELETING AN ACCOUNT \n"
    print "enter a an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue

        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break

    package = xml.client_package(version, 20, [act])
    send_message(package,conn)
    return

#deposit to an existing account
def deposit_request(conn):
    print "DEPOSITING SOME DOUGH \n"
    print "enter an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue

        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break
    print "enter an amount to deposit:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break

    package = xml.client_package(version, 30, [act,bal])
    send_message(package,conn)
    return

#withdraw from an existing account
def withdraw_request(conn):
    print "WITHDRAWING SOME DOUGH \n"
    print "enter an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue

        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break

    print "enter an amount to withdraw:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue
        if(netBuffer >= 0 and netBuffer < maxint):
            bal = netBuffer
            break
    package = xml.client_package(version, 40, [act,bal])
    send_message(package,conn)
    return

#withdraw from an existing account
def balance_request(conn):
    print "CHECKING THE BALANCE OF AN ACCOUNT \n"
    print "enter an account number 1-100:"
    while True:
        try:
            netBuffer = int(raw_input('>> '))
        except ValueError:
            continue

        if(netBuffer > 0 and netBuffer <= 100):
            act = netBuffer
            break

    package = xml.client_package(version, 50, [act])
    send_message(package,conn)
    return

#end a session
def end_session(conn):
    package = xml.client_package(version, 60, [])
    send_message(package,conn)
    return

def send_message(message, conn):
    try:
        conn.send(message)
    except:
            #close the client if the connection is down
            print "ERROR: connection down"
            exit()
    return
