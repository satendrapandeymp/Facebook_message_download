from datetime import datetime
from rest import Path_check, download_file, make_zip
from download import final as finalise
import time, os

ending = '</div></div>%#@'
ID = []
NAME = []

def do_rest(thread,client):
	uid = client.uid
	USER = client.fetchUserInfo(client.uid)[client.uid]
	self = USER.name
	check = 0
	timestampbackup = int(19800 + time.time())*100
	data = str(thread).split(" ")

	id = data[len(data)-1].split('(')[1].split(')')[0]

	logfile = open('log.txt', 'rb')
	backup = logfile.read()
	backup = backup.split('\n')
	for test in backup:
		bakupdata = test.split(' ')
		if len(bakupdata)>1:
			idbackup = bakupdata[0]
			if idbackup == id:
				timestampbackup = float(bakupdata[1])
				backup.remove(test)
				break
	logfile.close()

	logfile = open('log.txt', 'wb')
	for test in backup:
		logfile.write(test + '\n')
	logfile.close()

	other = data[1]
	name = str(data[1])

	if len(data) == 4:
		other = data[1] +  " " + data[2]
		name = str(data[1]) + '_' + str(data[2])

	if len(data) == 5:
		other = data[1] +  " " + data[2] +  " " + data[3]
		name = data[1] + '_' + data[2]  + '_' + data[3]

	if len(data) == 6:
		other = data[1] +  " " + data[2] +  " " + data[3] +  " " + data[4]
		name = data[1] + '_' + data[2]  + '_' + data[3] +  '_' + data[4]


	if str(data[0]) != '<GROUP':
		ID.append(id)
		NAME.append(other)
		check = 1

	if other == '' or other == ' ' or name == '' or name == ' ' :
		other = 'Group_' + str(id)
		name = 'Group_' + str(id)

	print "downloading messages from Group/User/Page -: ", other

	starting = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> <title>' + other + '- Messages</title> <link rel="stylesheet" href="../../style.css" type="text/css" /></head><body> <div class="contents"><h1>' + other +'</h1> <div class="thread"> Total number of messages = ' + str(thread.message_count) + '____\n'


	Testing = Path_check(other)
	folder_name = "Data/" + other
	log_file = folder_name+"/" + name + ".txt"
	Log_file = open(log_file, 'wb')
	filename = folder_name+"/html/" + name + ".htm"
	filenametxt = folder_name+"/html/" + name + ".txt"
	file = open(filenametxt, 'wb')

	flag = 100
	num = 0
	timestamp = int(19800 + time.time())*1000

	log = str(id) + ' ' + str(timestamp-19800) + '\n'

	while( flag > 99):
		messages = client.fetchThreadMessages(thread_id=id, limit=100, before=timestamp)
		timestamp = messages[len(messages)-1].timestamp
		flag = len(messages)
		num += flag
		finalise(messages, timestampbackup, file, Log_file, check, uid, self, folder_name, other)
		print num, " messages had been downloaded from today till - ",datetime.utcfromtimestamp(float(timestamp)/1000).strftime('%d-%m-%Y')

	file.close()

	logfile = open('log.txt', 'a')
	logfile.write(log)
	logfile.close()

	file = open(filenametxt, 'rb')
	latest = file.read()
	final = latest
	file.close()

	if os.path.exists(filename):
		file_htm = open(filename, 'rb')
		final = file_htm.read()
		final = final.split('</h1> <div class="thread"> Total number of messages = ')[1]
		final = final.split('____\n')[1]
		final = final.split(ending)[0]
		final = latest + final
		file_htm.close()

	file_htm = open(filename, 'wb')
	file_htm.write(starting)
	file_htm.write(final)
	file_htm.write(ending)
	file_htm.close()
