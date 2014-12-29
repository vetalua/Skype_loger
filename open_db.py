#coding=utf-8
'''
This programe make log-file of selecting dialog in Skype
Programe help you open end read all dialogs with searching users
For using you must know and input skype_nickname 
Programe adopte to open databathe with standart path in Linux and
 can be used after some change for opening database with your own path
'''
import sqlite3
import sys
import datetime
import os
import codecs


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
            log_contact, save_to_file = log(data, contact)
            print ' - result', type(log_contact)
            if save_to_file == 'Y' or save_to_file == 'y':
                write_file(log_contact, contact)
            else:
                print 'You chose are:  do not creating logfile. Exiting...'
        
        except sqlite3.OperationalError:
            print 'Connecting error, please, input your real nickname in Skype'
        finally:
            conn.close()
    else:
        return None

#--------------------------------------------------------------------------------------------------------------------------------#

def path_to_base_reading(attemt):
    '''
    This function create the path to Skype database file (main.db).
    It's possibol if you OS - Linux, you input existing 
    skype_nickname in Skype and main.db is in standart path in your PC
    TODO:   1. Make function, wich must build path to database automaticaly
               to other platforms (Windows, Mac)
            
    '''
    #---------------------------------------------------------------------------------------#

    def path_isdir(your_path):
        if os.path.isdir(your_path)==True:
            path_database = your_path + '/main.db'
            return path_database
        else:
            print 'some error in input or/and path'
            return None
                
        # ----------------------------------------------------------------------------------#
    
    def made_path():
        skype_nickname = raw_input("Input your nickname in Skype for finding database - ")
        if skype_nickname =='Q' or skype_nickname == 'q':   # Q/q for exit
            print 'Exiting...'
            exit()
        database_dir = '/home/'+os.getlogin() + '/.Skype/'+ skype_nickname
        path_database = path_isdir(database_dir)
        return path_database

    #--------------------------------------------------------------------------------------#

    if os.uname()[0] =='Linux':
        #create path to database in Unix OS
        #skype_nickname = 'harm_vetal'
        path = None
        step = 0
        #print os.uname()[0], attemt, path, step      # use for controll of parameters
        
        while step < attemt:
            path = made_path()
            if path != None: break
            step +=1
        return path
    else:
        print 'your OS not supporting now'
        return None

        #find path  #  read path from configfile
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

#--------------------------------------------------------------------------------------------------------------------------------#

def select_contact(data):
    '''
    Function create a list of all contacts of user's Skype. 
    Then user must select contact: he must write number in list of interestin contact
    '''
    all_contacts = []                   # list of all contacts in Skype
    for dat in data:
        if dat[8] not in all_contacts:
            all_contacts.append(dat[8])

    num = 1
    for dialog_partner in all_contacts:  # it print to screen full list of contacts in format:  num  -> nickname
        print num, ' ->', dialog_partner
        num +=1
    num_contact = None
    while  num_contact<=0 or num_contact> len(all_contacts):  # For choosing of contact enter it number, if error - try again, for exit 'Q' or 'q'    
        num_contact = input('Choose your dialog_partner number ')
        
        if num_contact == 'Q' or num_contact == 'q':
            print 'Exiting now...'
            exit()
        else:
            print 'Input Error, try again or input Q or q for exit'
    contact = all_contacts[num_contact-1]
    print contact
    return contact

#-------------------------------------------------------------------------------------------------------------------------------#

def log (data, contact):
    '''
    The function creates a unicode string, each containing 
    all information about all messages in the dialogue with 
    the selected skype's nickname.
    Data for writing into file consist of: skype_nickname, text of messege
    '''
    result = ''
    print 'Dialog with', contact, ' : '
    for i in data:
        if i[8]==contact:
            print i[9], i[4], i[17]
            #messege = []
            #messege.append(i[9])
            #messege.append(i[4])
            #messege.append(i[17])
            #result.append(messege)
            if i[17] == None: continue
            result += i[4] + ':  ' + i[17] + '\n'
            #+ i[4]
    #result = str(result)
    
    save_to_file = raw_input ('Save this log to file (y/n)?')
    print save_to_file, '   ----i n', result, type(result)
    return result, save_to_file

#-------------------------------------------------------------------------------------------------------------------------------#

def write_file(data, contact):
    '''
    Creating of log-file in .txt format. Name of file consists of:  selected Skype's nickname
     and creating date & time it log-file. The file will creat in the working directory.
    '''
    time_now = datetime.datetime.now()
    #contact = contact + '.txt'
    file_name = contact + '_' + str(time_now.year) + '_' +str(time_now.month) + '_' + str(time_now.day) + '_' + str(time_now.hour) + '_' + str(time_now.minute) + '.txt'
    print file_name, ' - is your logfile name'
    try:
        #f = open(contact, 'w')
        with codecs.open(file_name, 'w','utf-8') as f: # write unicode into file
            f.write('---------=============           LOG FILE from Skype          =============---------')
            f.write('\n'*3)
            f.write(data)
            f.write('\n'*3)
            f.write('---------=============   THANK YOU FOR USING THIS PROGRAMM!   =============---------')
    finally:
        print 'Closing file with error '
        f.close()
import codecs

#########################################################################################################################################

if __name__ == '__main__':
    main()