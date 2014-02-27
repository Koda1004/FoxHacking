'''
Created on Feb 18, 2010

Altered Feb 20, 2014
'''
from myServerSend import general_failure, end_session_success,create_success, delete_success,deposit_success,withdraw_success,balance_success
from struct import unpack
import sys

# create new account
def create_request(conn,xml,myData,lock):

    # get arguments from xml
    arguments = xml.find('arguments').findall('arg')
    act = int(arguments[0].text)
    bal = int(arguments[1].text)

    lock.acquire()
    try:
        # get balance
        if bal < 0 or bal > sys.maxint:
            general_failure(conn, 'create', "invalid balance")
            return

        # get account number
        if act <= 0 or act > 100 or act in myData:
            general_failure(conn, 'create',"account already in use")
            return

        myData[act] = bal
        create_success(conn,act)
    finally:
        lock.release()
        print myData

    return

# delete an existing account
def delete_request(conn,xml,myData,lock):
    
    # get arguments from xml
    arguments = xml.find('arguments').findall('arg')
    act = int(arguments[0].text)

    lock.acquire()
    try:

        if act <= 0 or act > 100:
            general_failure(conn,'delete',"invalid account number")
            return

        if act not in myData:
            general_failure(conn,'delete',"nonexistent account number")
            return

        if myData[act] != 0:
            general_failure(conn,'delete',"nonzero money in that account")
            return

        del myData[act]
        delete_success(conn)
    finally:
        lock.release()
        print myData

    return

# deposit to an existing account
def deposit_request(conn,xml,myData,lock):
    
    # get arguments from xml
    arguments = xml.find('arguments').findall('arg')
    act = int(arguments[0].text)
    bal = int(arguments[1].text)

    lock.acquire()
    try:
        # get account number
        if act <= 0 or act > 100:
            general_failure(conn,'deposit',"invalid account number")
            return

        # check for existence of account
        if act not in myData:
            general_failure(conn,'deposit',"nonexistent account number")
            return

        # check for a valid deposit amount
        if bal <= 0:
            general_failure(conn,'deposit',"nonsense deposit amount")
            return

        curr_bal = myData[act]

        # check that the new balance won't overflow
        if bal < sys.maxint - curr_bal - 1:
            myData[act] = curr_bal + bal
        else:
            general_failure(conn,'deposit',"account overflow... damn you are rich")
            return
        deposit_success(conn, curr_bal + bal)
    finally:
        lock.release()
        print myData


    return

# withdraw from an existing account
def withdraw_request(conn,xml,myData,lock):
    
    # get arguments from xml
    arguments = xml.find('arguments').findall('arg')
    act = int(arguments[0].text)
    bal = int(arguments[1].text)

    lock.acquire()
    try:
        # get account number
        if act <= 0 or act > 100:
            general_failure(conn,'withdraw',"invalid account number")
            return

        # check for existence of account
        if act not in myData:
            general_failure(conn,'withdraw',"nonexistent account number")
            return

        # check for a valid deposit amount
        if bal <= 0:
            general_failure(conn,'withdraw',"nonsense withdrawal amount")
            return

        curr_bal = myData[act]

        # check that the new balance won't overflow
        if curr_bal - bal >= 0:
            myData[act] = curr_bal - bal
        else:
            general_failure(conn,'withdraw',"not enough money in account")
            return
        withdraw_success(conn, curr_bal - bal)
    finally:
        lock.release()
        print myData
    return

# withdraw from an existing account
def balance_request(conn,xml,myData,lock):
    
    #no need to lock: we are just reading a value from a dict, which is thread-safe
    arguments = xml.find('arguments').findall('arg')
    act = int(arguments[0].text)

    #get balance
    if act <= 0 or act > 100:
        general_failure(conn,'balance',"invalid account number")
        return

    #get the current balance
    try:
        bal = myData[act]
    except KeyError:
        general_failure(conn,'balance',"nonexistent account")
        return

    balance_success(conn,bal)

    return

# end a session
def end_session(conn,xml,myData,lock):
    end_session_success(conn)
    conn.close()
    return
