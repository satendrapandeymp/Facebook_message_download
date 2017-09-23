from fbchat import Client, log
from getpass import getpass
from datetime import datetime
import sys, os, urllib, time, socket, shutil, pyminizip
from glob import glob
from zipfile import ZipFile

socket.setdefaulttimeout(60)
reload(sys)
sys.setdefaultencoding("utf-8")

ending = '</div></div>'

username = str(raw_input("Username: "))
password = getpass()

client = Client(username, password)

zipping = str(raw_input("Want to save your data as a .Zip file y/n?: "))

uid = client.uid
USER = client.fetchUserInfo(client.uid)[client.uid]
self = USER.name

docs = ['docx', 'doc', 'pdf', 'pptx', 'txt', 'xlsx']
media = ['mp3', 'mp4', 'aac', 'webm', 'avi', '3gp']
gen = ['jpg', 'png']


def make_zip():
	file = open('instruction.txt', 'w')
	file.write("Use your facebook password to decrypt Fb_Data.zip file")
	file.close()
	files = glob("Data/*/*/*")
	zipfile = ZipFile("Fb_Data.zip", 'w')
	for file in files:
		zipfile.write(file)
	zipfile.close()
	shutil.rmtree("Data")
	pyminizip.compress("Fb_Data.zip", "Data.zip", password, 3)
	os.remove('Fb_Data.zip')
	zipfile = ZipFile("Data.zip", 'a')
	zipfile.write('instruction.txt')
	zipfile.close()
	os.remove('instruction.txt')

def do_rest(thread):
	data = str(thread).split(" ")

	print str(thread.message_count)

	print thread.message_count

	print thread.uid

	print thread.name

	id = data[len(data)-1].split('(')[1].split(')')[0]

	if len(data) == 4:
		other = data[1] +  " " + data[2]
		name = str(data[1]) + '_' + str(data[2])

	if len(data) == 3:
		other = data[1]
		name = str(data[1])

	if len(data) == 5:
		other = data[1] +  " " + data[2] +  " " + data[3]
		name = data[1] + '_' + data[2]  + '_' + data[3]

	starting = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8" /> <title>' + other + '- Messages</title> <link rel="stylesheet" href="../../style.css" type="text/css" /></head><body> <div class="contents"><h1>' + other +'</h1> <div class="thread"> Total number of messages = ' + str(thread.message_count)


	Testing = Path_check(other)
	folder_name = "Data/" + other
	filename = folder_name+"/html/" + name + ".htm"
	file = open(filename, 'wb')
	file.write(starting)
	flag = 1000
	num = 0
	timestamp = int(19800 + time.time())*1000
	while( flag > 999):
		messages = client.fetchThreadMessages(thread_id=id, limit=1000, before=timestamp)
		timestamp = messages[len(messages)-1].timestamp

		for message in messages:

			if message.extensible_attachment:
				if message.extensible_attachment['story_attachment']['media']:
					if message.extensible_attachment['story_attachment']['media']['is_playable']:
						add = message.extensible_attachment['story_attachment']['media']['playable_url']
						Filename = folder_name + "/shares/" + str(message.timestamp)  + '.mp4'
						if add is not None:
							try:
								urllib.urlretrieve(add, Filename)
								if message.author == uid:
									file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
									file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
									file.write('</span></div></div><p> <video width="400" height="400" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
								else:
									file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
									file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
									file.write('</span></div></div><p> <video width="400" height="400" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
							except:
								print "Getting some error now on url -: ", add
						else:
							print message.extensible_attachment

			elif message.attachments:
				for attachment in message.attachments:
				# For Image
					time.sleep(.1)
					Filename = attachment['filename']
					if  Filename.split("-")[0] == 'image':
						add = attachment['large_preview']['uri']
						name = folder_name +"/images/"+ attachment['filename']+'.' +attachment['original_extension']
						try:
							urllib.urlretrieve(add, name)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" height="400" width="400" > </a></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" height="400" width="400" > </a></p> \n' )
						except:
							print "Getting some error now on url -: ", add
					elif len(Filename.split(".")) > 1 and Filename.split(".")[len(Filename.split("."))-1] in docs:
						add = attachment['url']
						test = urllib.urlopen(add)
						temp = test.read().split('replace("')[1]
						temp = temp.split('");</script>')[0]
						temp = temp.replace("\\","")
						Filename = folder_name + "/docs/" + Filename
						try:
							urllib.urlretrieve(temp, Filename)
						except:
							print "Getting some error now on url -: ", temp
					elif len(Filename.split(".")) > 1 and Filename.split(".")[len(Filename.split("."))-1] in media:
						add = attachment['playable_url']
						Filename = folder_name + "/media/" + Filename
						try:
							urllib.urlretrieve(add, Filename)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <video width="400" height="400" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <video width="400" height="400" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
						except:
							print "Getting some error now on url -: ", add
					elif Filename.split("-")[0] == 'gif':
						add = attachment['animated_image']['uri']
						Filename = folder_name + "/media/" + Filename
						try:
							urllib.urlretrieve(add, Filename)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" height="400" width="400" > </a></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" height="400" width="400" > </a></p> \n' )
						except:
							print "Getting some error now on url -: ", add
					else:
						add = attachment['url']
						test = urllib.urlopen(add)
						temp = test.read().split('replace("')[1]
						temp = temp.split('");</script>')[0]
						temp = temp.replace("\\","")
						Filename = folder_name + "/Random/" + Filename
						try:
							urllib.urlretrieve(temp, Filename)
						except:
							print "Getting some error now on url -: ", temp

			elif message.text is not None and message.sticker is None:

				if message.author == uid:
					file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
					file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
					file.write('</span></div></div><p>' + message.text + ' </p> \n' )
				else:
					file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
					file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
					file.write('</span></div></div><p>' + message.text + ' </p> \n' )

		flag = len(messages)
		num += flag
		print num, " messages had been downloaded from today till - ",datetime.utcfromtimestamp(float(timestamp)/1000).strftime('%d-%m-%Y')
	file.write(ending)
	file.close()


def Path_check(name):

	path = "Data"
	if not os.path.exists(path):
		os.mkdir(path)

	source = 'Resources/style.css'
	target = 'Data'

	try:
		shutil.copy(source, target)
	except IOError as e:
		print("Unable to copy file. %s" % e)
	except:
	    print("Unexpected error:", sys.exc_info())

	name = path + '/' +name

	path = name
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/docs"
	if not os.path.exists(path):
		os.mkdir(path)


	path = name + "/html"
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/images"
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/media"
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/shares"
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/Random"
	if not os.path.exists(path):
		os.mkdir(path)

	return True

username = str(raw_input("want to download messages from a specific friend type(y/n): "))

if username.lower() == 'y':
	names = str(raw_input("Name of that friends separated by a comma like - satyendra pandey, Narendra pandey--: "))
	names = names.split(',')
	for name in names:
		thread = client.searchForThreads(name)[0]
		do_rest(thread)
	if zipping.lower() == 'y':
		make_zip()

else:
	num = int(raw_input("Number of friends from top of your chatlist:"))
	if num < 20:
		threads = client.fetchThreadList(limit = num)

	else:
		threads = client.fetchThreadList(limit = 20)
		num = (num-20)/20

		for i in range(num):
			offset = 20*(i+1)
			threads += client.fetchThreadList(offset = offset, limit= 20)

	for thread in threads:
		do_rest(thread)
	if zipping.lower() == 'y':
		make_zip()
