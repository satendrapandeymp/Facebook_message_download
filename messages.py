from fbchat import Client, log
from getpass import getpass
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

username = str(raw_input("Username: "))
password = getpass()

client = Client(username, password)

uid = client.uid
USER = client.fetchUserInfo(client.uid)[client.uid]
self = USER.name

threads = client.fetchThreadList()

path = "messages/"
if not os.path.exists(path):
	os.mkdir(path)

num = str(raw_input("Number of frieds messages: "))

num = int(num)/20

for i in range(num):
	offset = 20*(i+1)
	threads += client.fetchThreadList(offset = offset)

for thread in threads:
	data = str(thread).split(" ")
	if len(data) == 4:
		other = data[1] +  " " + data[2]

		id = data[3].split('(')[1].split(')')[0]
		filename = "messages/" + str(data[1]) + '_' + str(data[2]) + ".txt"
		file = open(filename, 'wb')
		messages = client.fetchThreadMessages(thread_id=id, limit=20000)
		messages.reverse()
		for message in messages:
			if message.text is not None:
				if message.author == uid:
					file.write(self + ' -- ' + message.text.encode('utf-8') + ' \n' )
				else:
					file.write(other + ' -- ' + message.text.encode('utf-8') + ' \n' )
		file.close()
	
