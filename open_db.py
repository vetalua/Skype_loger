#coding=utf-8
'''
This programe make log-file of selecting dialog in Skype
'''
import sqlite3
import sys
import datetime

########################################################################################################################################

def main():
    '''Main function '''
    path = path_to_base_reading('config.py')
    print 'Reading config file complit, connecting now to', path
    try:
        conn = sqlite3.connect(path)
        c = conn.cursor()
        c.execute('select * from Messages')
        data = c.fetchall()
        contact = select_contact(data)
        log_contact = log(data, contact)
        write_file(log_contact, contact)
        
    except sqlite3.OperationalError:
        print 'Connecting error'
    finally:
        conn.close()

##################################################################################################

def path_to_base_reading(conf_file):
    '''
    This function read the path to the Skype database file (main.db) from file config.py.
    TODO:   1. Make function, wich must build path to database automaticaly
            2. Do it for all platforms
    '''
    try:
        f = open(conf_file, 'r')
        path_database = f.read()
        print 'open.........................'
    except : #sqlite3.OperationalError:
        print 'Config file is not found'
        return None
    
    finally:
        f.close()
        #print path_database
    return path_database

###############################################################################################

def select_contact(data):
    '''
    Function create a list of all contacts of user's Skype. Then user must select contact name.
    TODO 3. Make selection without nickname, but only with ordering number in list (dictionary)
    '''
    all_contacts = []                   # list of all contacts in Skype
    for dat in data:
        if dat[8] not in all_contacts:
            all_contacts.append(dat[8])

    num = 0
    for dialog_partner in all_contacts:
        print num, ' ->', dialog_partner
        num +=1
    while True:
        contact = input('Choose your dialog_partner  ')
        print contact
        if contact in all_contacts: break
        if contact == 'Q' or contact == 'q':
            print 'Exiting now'
        else:
            print 'Input Error'
            exit()
    return contact

###############################################################################################

def log (data, contact):
    '''
    The function creates a list of lists, each containing information about a single message in
    the dialogue with the selected contact person Skype.
    Data consist of: [writing time, autor of message, text of messege]
    TODO: 4 I fined the problems with coding in file. 
    '''
    result = []
    for i in data:
        if i[8]==contact:
            print i[9], i[4], i[17]
            messege = []
            messege.append(i[9])
            messege.append(i[4])
            messege.append(i[17])
            result.append(messege)
    result = str(result)
    print('You search ', contact, ' for writing into file')
    return result

##################################################################################################

def write_file(data, contact):
    '''
    Creating of log-file in .txt format. Name of file consists of the selected User name
    of contact Skype and creating time it log-file. The file is created in the working directory.
    '''
    a = datetime.datetime.now()
    #contact = contact + '.txt'
    contact = contact + str(a.year) + str(a.month) + str(a.hour) + str(a.minute) + '.txt'
    print contact, ' - is your logfile name'
    f = open(contact, 'w')
    print data
    f.write(data)
    f.close()

#########################################################################################################################################

if __name__ == '__main__':
    main()