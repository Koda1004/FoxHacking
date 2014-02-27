'''
Created on Feb 18, 2010

Altered Feb. 20, 2014
'''
from struct import unpack
from sys import exit

#handle errors from server side.
def general_failure(conn, xml):
    reason = xml.find('error').text
    print "\nERROR: " + reason
    return

#create new account
def create_success(conn, xml):
    value = xml.find('value').text
    print "Account creation successful " + value
    return

#delete an existing account
def delete_success(conn, xml):
    print "Account deletion successful"
    return

#deposit to an existing account
def deposit_success(conn,xml):
    value = xml.find('value').text
    print "Deposit success. The updated balance: " + value
    return

#withdraw from an existing account
def withdraw_success(conn,xml):
    value = xml.find('value').text
    print "Withdrawal success. The updated balance: " + value
    return

#withdraw from an existing account
def balance_success(conn,xml):
    value = xml.find('value').text
    print "The balance of that account is: " + value
    return

#end a session
def end_session_success(conn,xml):
    print "SHUTTING DOWN"
    conn.close()
    exit()
    return

#handle invalid opcodes
def unknown_opcode(conn):
    print "ERROR: INCORRECT OPCODE"
    return
