import os
import sys
import random
import sqlite3
import time
import configparser
import telepot
from telepot.loop import MessageLoop
from datetime import datetime

sqliteConnection = sqlite3.connect('main.db', check_same_thread=False)
cur = sqliteConnection.cursor()

config = configparser.ConfigParser()

config.read('config.ini')


path = config['DEFAULT']['path']
token = config['DEFAULT']['token']
chanid = config['DEFAULT']['channelid']

bot = 0

tg_commands = {}

 # return cmd, params
def parse_cmd(cmd_string):
	text_split = cmd_string.split()
	return text_split[0], text_split[1:]

def add_command(cmd, func):
	global tg_commands
	tg_commands[cmd] = func

def remove_command(cmd):
	global tg_commands
	del tg_commands[cmd]

def on_message(message):
	global bot 
	content_type, chat_type, chat_id = telepot.glance(message)

	if content_type == "text":
		msg_text = message['text']
		chat_id = message['chat']['id']
		
		print("[MSG] {uid} : {msg}".format(uid=message['from']['id'], msg=msg_text))

		if msg_text[0] == '/':
			cmd, params = parse_cmd(msg_text)
			try:
				tg_commands[cmd](chat_id, params)
			except KeyError:
				bot.sendMessage(chat_id, "Unknown command: {cmd}\n /help for a list of commands".format(cmd=cmd))
		else:
			bot.sendMessage(chat_id, "Message is a plain text")

def getrandom():
    cur.execute('''SELECT file FROM ig_listfile;''')
    allFiles = cur.fetchall()
    #print(allFiles)
    randomfile = random.choice(allFiles)

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

def send(channel):
	# content_type, chat_type, chat_id = telepot.glance(msg)
	# print(content_type, chat_type, chat_id)
	try:
#		now = datetime.datetime.now()
		randomfile = getrandom()
		#randomfilenormpath = randomfile.replace("\\","/")
		#print("[send] Fichier trouvé")
		#splittedfilelocation = randomfilenormpath.split("/")
		# filename = splittedfilelocation[len(splittedfilelocation)-1]
		#filename = ""
		bot.sendPhoto(channel, photo=open(randomfile, 'rb'), parse_mode='Markdown')

		print("[send] Envoyé")
	except Exception as e:
		print(e)
		print("[send] CRAAAAAAAAAAAAAAASH")
		send("")

def cmd_image(chat_id, params):
	send(chat_id)

def cmd_start(chat_id, params):
	bot.sendMessage(chat_id, "µ'sic start !")

def cmd_help(chat_id, params):
	cmds = ""
	for k in tg_commands:
		cmds = cmds + k + "\n"
	bot.sendMessage(chat_id, cmds)
def main():
    global bot
    bot = telepot.Bot(token)
    add_command("/start", cmd_start)
    add_command("/help", cmd_help)
    add_command("/image", cmd_image)
    MessageLoop(bot, on_message).run_as_thread() 
    print("Listening messages")
    
   
 
if __name__ == "__main__":
	main()
	while True:
		time.sleep(10)