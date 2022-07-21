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



def getListOfFiles(dirName):

    listOfFile = os.listdir(dirName)
    allFiles = list()

    for entry in listOfFile:

        fullPath = os.path.join(dirName, entry)
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
            
        else:
            allFiles.append(fullPath)
            
               
    return allFiles

def InsertonDatabase():

    table_file = getListOfFiles(path)
    print(table_file)
    for i in table_file :
        print(i)
        cur.execute("INSERT INTO ig_listfile (file) VALUES (?);", (i, ))
        sqliteConnection.commit()






def main():
    global bot
    bot = telepot.Bot(token)


    InsertonDatabase()

 
main()