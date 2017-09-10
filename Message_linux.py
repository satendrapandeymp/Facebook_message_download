from fbchat import Client, log
from getpass import getpass
import sys, os, urllib
reload(sys)
sys.setdefaultencoding("utf-8")

username = str(raw_input("Username: "))
password = getpass()

client = Client(username, password)

uid = client.uid
USER = client.fetchUserInfo(client.uid)[client.uid]
self = USER.name

docs = ['docx', 'doc', 'pdf', 'pptx', 'txt', 'xlsx']
media = ['mp3', 'mp4']

def do_rest(thread):
	data = str(thread).split(" ")
	if len(data) == 4:
		other = data[1] +  " " + data[2]

		id = data[3].split('(')[1].split(')')[0]
		folder_name = str(data[1]) + '_' + str(data[2])
		Testing = Path_check(folder_name)
		filename = folder_name+"/" + str(data[1]) + '_' + str(data[2]) + ".txt"
		file = open(filename, 'wb')
		messages = client.fetchThreadMessages(thread_id=id, limit=number)
		messages.reverse()
		for message in messages:
			if message.text is not None:
				if message.author == uid:
					file.write(self + ' -- ' + message.text.encode('utf-8') + ' \n' )
				else:
					file.write(other + ' -- ' + message.text.encode('utf-8') + ' \n' )
			if message.attachments:
				for attachment in message.attachments:
				# For Image
					Filename = attachment['filename']
					if  Filename.split("-")[0] == 'image':
						add = attachment['large_preview']['uri']
						name = folder_name +"/images/"+ attachment['filename']+'.'+attachment['original_extension']
						urllib.urlretrieve(add, name)
					elif len(Filename.split(".")) > 1 and Filename.split(".")[1] in docs:
						add = attachment['url']
						test = urllib.urlopen(add)
						temp = test.read().split('replace("')[1]
						temp = temp.split('");</script>')[0]
						temp = temp.replace("\\","")
						Filename = folder_name + "/docs/" + Filename
						urllib.urlretrieve(temp, Filename)
					elif len(Filename.split(".")) > 1 and Filename.split(".")[1] in media:
						add = attachment['playable_url']
						Filename = folder_name + "/media/" + Filename
						urllib.urlretrieve(add, Filename)
					else:
						add = attachment['url']
						test = urllib.urlopen(add)
						temp = test.read().split('replace("')[1]
						temp = temp.split('");</script>')[0]
						temp = temp.replace("\\","")
						Filename = folder_name + "/Random/" + Filename
						urllib.urlretrieve(temp, Filename)
		file.close()


def Path_check(name):

	path = name
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/docs"
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/images"
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/media"
	if not os.path.exists(path):
		os.mkdir(path)

	path = name + "/Random"
	if not os.path.exists(path):
		os.mkdir(path)

	return True

username = str(raw_input("want to download messages from a specific friend type(y/n): "))

number = int(raw_input("Maximum number of messages from 1 person: "))

if username.lower() == 'y':
	names = str(raw_input("Name of that friends separated by a comma like - satyendra pandey, Narendra pandey ,... , ... "))
	names = names.split(',')
	for name in names:
		thread = client.searchForThreads(name)[0]
		do_rest(thread)

else: 
	num = int(raw_input("Number of frieds messages you wanna download from your inbox top : "))

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
