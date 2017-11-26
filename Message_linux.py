from fbchat import Client, log
from getpass import getpass
from datetime import datetime
from rest import Path_check, download_file, make_zip
from process import do_rest
import sys, os, urllib, time, socket, shutil, pyminizip, requests

socket.setdefaulttimeout(60)
reload(sys)
sys.setdefaultencoding("utf-8")

username = str(raw_input("Username: "))
password = getpass()
client = Client(username, password)

zipping = str(raw_input("Want to save your data as a .Zip file y/n?: "))
username = str(raw_input("want to download messages from a specific friend type(y/n): "))

if username.lower() == 'y':
	names = str(raw_input("Name of that friends separated by a comma like - satyendra pandey, Narendra pandey--: "))
	names = names.split(',')
	for name in names:
		thread = client.searchForThreads(name)[0]
		do_rest(thread, client)
	if zipping.lower() == 'y':
		make_zip()

else:
	num = int(raw_input("Number of friends from top of your chatlist:"))
	if num < 20:
		threads = client.fetchThreadList(limit = num)

	else:
		threads = client.fetchThreadList( limit = 20)
		num = (num-20)/20

		for i in range(num):
			offset = 20*(i+1)
			threads += client.fetchThreadList(offset = offset, limit= 20)

	for thread in threads:
		do_rest(thread, client)
	if zipping.lower() == 'y':
		make_zip()
