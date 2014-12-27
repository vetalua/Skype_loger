#coding=utf-8
'''
This programe make log-file of selecting dialog in Skype
'''
import sqlite3
import sys
import datetime
import os

########################################################################################################################################

def main():
    '''Main function '''
    path = path_to_base_reading (attemt=3)
    print 'Reading config file complit, connecting now to', path
    if path!=None:
        try:
            conn = sqlite3.connect(path)
            c = conn.cursor()
            c.execute('select * from Messages')
            data = c.fetchall()
            contact = select_contact(data)
            log_contact = log(data, contact)
            write_file(log_contact, contact)
        
        except sqlite3.OperationalError:
            print 'Connecting error, please, input your real nickname in Skype'
        finally:
            conn.close()
    else:
        return None

##################################################################################################

def path_to_base_reading(attemt):
    '''
    This function create the path to Skype database file (main.db).
    It's possibol if you OS - Linux, you input existing skype_nickname in Skype and main.db is in standart path in your PC
    TODO:   1. Make function, wich must build path to database automaticaly to other platforms (Windows, Mac)
            
    '''
    def path_isdir(your_path):
        if os.path.isdir(your_path)==True:
            path_database = your_path + '/main.db'
            return path_database
        else:
            print 'some error in input or/and path'
            return None
                
        # must be input from keyboard
    def made_path():
        skype_nickname = raw_input("Input your nickname in Skype for finding database - ")
        database_dir = '/home/'+os.getlogin() + '/.Skype/'+ skype_nickname
        path_database = path_isdir(database_dir)
        return path_database

    if os.uname()[0] =='Linux':
        #create path to database in Unix OS
        #skype_nickname = 'harm_vetal'
        path = None
        step = 0
        print os.uname()[0], attemt, path, step
        
        while step < attemt:
            path = made_path()
            if path != None: break
            step +=1
        return path
    else:
        print 'your OS not supporting now'
        return None

        
            

        #find path 
    #try:
    #    f = open(conf_file, 'r')
    #    path_database = f.read()
    #    print 'open.........................'
    #except : #sqlite3.OperationalError:
    #    print 'Config file is not found'
    #   return None
    
    #finally:
    #    f.close()
    #    #print path_database
    #return path_database

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