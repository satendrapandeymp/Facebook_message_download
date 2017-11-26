import sys, os, urllib, time, socket, shutil, pyminizip, requests
from glob import glob
from zipfile import ZipFile

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
		Log_file.write(("Unexpected error:" +  str(sys.exc_info())))

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

def download_file(add, name):
	request = requests.get(add, timeout=60, stream=True)
	#Open the output file and make sure we write in binary mode
	flag = 0
	with open(name, 'wb') as fh:
	    # Walk through the request response in chunks of 1024 * 1024 bytes, so 1MiB
	    for chunk in request.iter_content(1024 * 1024):
	        # Write the chunk to the file
		flag += 1
		if flag > 10:
			Log_file.write("This file is bigger than 10MB so download it if you want-- " + add + '\n\n')
			break
		fh.write(chunk)

def make_zip():
	file = open('instruction.txt', 'w')
	file.write("Use your facebook password to decrypt Fb_Data.zip file")
	file.close()
	files = glob("Data/*/*/*")
	files += glob("Data/*/*")
	files += glob("Data/*")
	zipfile = ZipFile("Fb_Data.zip", 'w')
	for file in files:
		if os.path.isfile(file):
			zipfile.write(file)
	zipfile.close()
	shutil.rmtree("Data")
	pyminizip.compress("Fb_Data.zip", "Data.zip", password, 3)
	os.remove('Fb_Data.zip')
	zipfile = ZipFile("Data.zip", 'a')
	zipfile.write('instruction.txt')
	zipfile.close()
	os.remove('instruction.txt')
