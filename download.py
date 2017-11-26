from rest import Path_check, download_file
from datetime import datetime
import time, urllib

ID = []
NAME = []

docs = ['docx', 'doc', 'pdf', 'pptx', 'txt', 'xlsx']
media = ['mp3', 'mp4', 'aac', 'webm', 'avi', '3gp']
gen = ['jpg', 'png', 'jpeg']

def final(messages, timestampbackup, file, Log_file, check, uid , self, folder_name, other):
    for message in messages:
			if int(message.timestamp) < timestampbackup:
				print 'old message than ' + datetime.utcfromtimestamp(float(timestampbackup)/1000).strftime('%d-%m-%Y') +' has been already downloaded'
				flag = 0
				break

			if check == 0:
				if message.author not in ID:
					USER = client.fetchUserInfo(message.author)[message.author]
					other = USER.name
					ID.append(message.author)
					NAME.append(other)
				else:
					for i in range(len(ID)):
						if message.author == ID[i]:
							other = NAME[i]
							break

			if message.extensible_attachment:

				if message.extensible_attachment['story_attachment']['url']:


					if message.author == uid:
						file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
						file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
						file.write('</span></div></div><p> <a href="' + message.extensible_attachment['story_attachment']['url'] + ' "> ' + message.extensible_attachment['story_attachment']['url'] + '  </p> \n' )
					else:
						file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
						file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
						file.write('</span></div></div><p> <a href="' + message.extensible_attachment['story_attachment']['url'] + ' "> ' + message.extensible_attachment['story_attachment']['url'] + '  </p> \n' )


				if message.extensible_attachment['story_attachment']['media']:
					if message.extensible_attachment['story_attachment']['media']['is_playable']:
						add = message.extensible_attachment['story_attachment']['media']['playable_url']
						Filename = folder_name + "/shares/" + str(message.timestamp)  + '.mp4'
						if add is not None:
							try:
								download_file(add, Filename)
								if message.author == uid:
									file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
									file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
									file.write('</span></div></div><p> <video width="500" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
								else:
									file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
									file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
									file.write('</span></div></div><p> <video width="500" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
							except:
								Log_file.write("Getting some error now on url -: " +  add + '\n\n')
						else:
							Log_file.write("Look at this separately--" + str(message.extensible_attachment) + '\n\n')

			elif message.attachments:
				for attachment in message.attachments:
				# For Image
					time.sleep(.1)
					Filename = attachment['filename']
					if  Filename.split("-")[0] == 'image':
						add = attachment['large_preview']['uri']
						print message.author
						name = folder_name +"/images/"+ attachment['filename']+'.' +attachment['original_extension']
						try:
							download_file(add, name)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" width="500" > </a></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" width="500" > </a></p> \n' )
						except:
							Log_file.write( "Getting some error now on url -: " + add +  '\n\n')
					elif len(Filename.split(".")) > 1 and Filename.split(".")[len(Filename.split("."))-1] in docs:
						add = attachment['url']
						test = urllib.urlopen(add)
						temp = test.read().split('replace("')[1]
						temp = temp.split('");</script>')[0]
						temp = temp.replace("\\","")
						Temp = Filename
						Filename = folder_name + "/docs/" + Filename
						try:
							download_file(temp, Filename)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ Filename +'">' + Temp + '</a></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ Filename +'">' + Temp + '</a></p> \n' )
						except:
							Log_file.write( "Getting some error now on url -: " + temp  + '\n\n')
					elif len(Filename.split(".")) > 1 and Filename.split(".")[len(Filename.split("."))-1] in media:
						try:
							add = attachment['playable_url']
							Filename = folder_name + "/media/" + Filename
							download_file(add, Filename)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <video width="500" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <video width="500" controls> <source src="../../../' + Filename + '" type="video/mp4"></p> \n' )
						except:
							Log_file.write( "Getting some error now on url -: " + add + '\n\n')
					elif Filename.split("-")[0] == 'gif':
						add = attachment['animated_image']['uri']
						Filename = folder_name + "/media/" + Filename
						try:
							download_file(add, Filename)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" width="500" > </a></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ name +'"> <img src="../../../'+ name + '" alt="Folder" width="500" > </a></p> \n' )
						except:
							Log_file.write( "Getting some error now on url -: " + add + '\n\n')
					else:
						add = attachment['url']
						test = urllib.urlopen(add)
						temp = test.read().split('replace("')[1]
						temp = temp.split('");</script>')[0]
						temp = temp.replace("\\","")
						Temp = Filename
						Filename = folder_name + "/Random/" + Filename
						try:
							download_file(temp, Filename)
							if message.author == uid:
								file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ Filename +'">' + Temp + '</a></p> \n' )
							else:
								file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
								file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
								file.write('</span></div></div><p> <a href="../../../'+ Filename +'">' + Temp + '</a></p> \n' )
						except:
							Log_file.write( "Getting some error now on url -: " + temp + '\n\n')

			elif message.text is not None and message.sticker is None:

				if message.author == uid:
					file.write('<div class="message"><div class="message_header"><span class="user">' + self +  ' </span><span class="meta"> ')
					file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
					file.write('</span></div></div><p>' + message.text + ' </p> \n' )
				else:
					file.write('<div class="message"><div class="message_header"><span class="user">' + other +  ' </span><span class="meta"> ')
					file.write(str(datetime.fromtimestamp(float(int(message.timestamp)/1000))))
					file.write('</span></div></div><p>' + message.text + ' </p> \n' )
