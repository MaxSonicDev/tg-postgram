import os
import sys
import random
import sqlite3
import time
import configparser
import telepot
from telepot.loop import MessageLoop
from datetime import datetime

sqliteConnection = sqlite3.connect('main.db')
cur = sqliteConnection.cursor()

config = configparser.ConfigParser()

config.read('config.ini')


path = config['DEFAULT']['path']
token = config['DEFAULT']['token']
chanid = config['DEFAULT']['channelid']



#def getListOfFiles():



 #   cur.execute("SELECT file FROM ig_listfile;")
  #  allFiles = cur.fetchall()
   # print(allFiles)
    #return allFiles
#    listOfFile = os.listdir(dirName)
#    allFiles = list()

#    for entry in listOfFile:

#        fullPath = os.path.join(dirName, entry)
#        if os.path.isdir(fullPath):
#            allFiles = allFiles + getListOfFiles(fullPath)
#            
#        else:
#            allFiles.append(fullPath)
            
               
#    return allFiles


def strip_chars(str, chars):
        return "".join(c for c in str if c not in chars)
    

def getrandom():
    cur.execute('''SELECT file FROM ig_listfile;''')
    allFiles = cur.fetchall()
    #print(allFiles)
    randomfile = random.choice(allFiles)
    print(randomfile[0])
    cur.execute("SELECT file FROM ig_dupli WHERE file = '" + randomfile[0] + "'")
    
    row = cur.fetchall()
    print(row)
 
 

    if randomfile[0].endswith('.gif'):
        getrandom()
    elif row == []:
        print(randomfile[0])
        cur.execute("INSERT INTO ig_dupli (file) VALUES (?);", (randomfile[0],))
        sqliteConnection.commit()
        return randomfile[0]
    else :
        print("get niqued")
        
        randomfile = getrandom()
        return randomfile[0]

    
    cur.close()

def handle(msg):
    randomfile = getrandom()
    bot.sendPhoto(chanid, photo=open(randomfile, 'rb'))  
    time.sleep(1)
    exit()

def main():
    global bot
    bot = telepot.Bot(token)

    if random.randint(0, 1000)  == 689:
        cur.execute("DELETE FROM ig_dupli")
    handle("")
    
   
 
main()