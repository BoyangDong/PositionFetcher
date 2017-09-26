import paramiko
import os
import shutil
import datetime as dt
import time
import csv 
import zipfile 
import ftplib

from dumper_api import upload
from ftplib import FTP

yesterday = dt.datetime.now() - dt.timedelta( days = 1 )
dates = yesterday.strftime( '%Y%m%d' )
today = time.time()
#dates = "20170923"

#zipfile_name = ''.join([dates, '.zip'])

text_files = "%s.TXT" % dates

budo_folder = "E:/Repos/Project_3/"+dates+"/"

password = "v3pzegM"
username = "BUDO_TRADING"

username_comm = "BUDO_COM"
password_comm = "OhkLY7H"

query_username = "boyang"
query_password = "Password1234!"
query_server_ip = "172.30.80.4"

files_grab = ("PFOPCTYPOS_{0}.CSV".format(dates), "PFDFPOS_{0}.CSV".format(dates), "PFDFST4_{0}.CSV".format(dates), "PFDFMNY_{0}.CSV".format(dates))


#################################### Make an empty dir for position files reside in ################################
os.mkdir(dates)

#################################### EDF SPAN files and BT files to EDF folder #####################################
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#try:
trans = paramiko.Transport(("ftpc.edfmancapital.com", 2222))
trans.connect(username = username, password = password)

sftp = paramiko.SFTPClient.from_transport(trans)
#sftp.chdir("/")
print "connected"

for budo_span in sftp.listdir():
	#print "looking for files"
	if budo_span.endswith(text_files):
		print budo_span
		sftp.get(budo_span, budo_folder + budo_span)

for budo_file in sftp.listdir():
	if budo_file in files_grab:
		print budo_file
		sftp.get(budo_file, budo_folder + "BT_" + budo_file)

for budo_span in sftp.listdir():
	#print "looking for files"
	if budo_span.startswith(dates):
		print budo_span
		sftp.get(budo_span, budo_folder + budo_span)

ssh.close()

time.sleep(1)
#################################### BC files to EDF folder #####################################

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#try:
trans = paramiko.Transport(("ftpc.edfmancapital.com", 2222))
trans.connect(username = username_comm, password = password_comm)

sftp = paramiko.SFTPClient.from_transport(trans)

for budo_com in sftp.listdir():
	if budo_com in files_grab:
		print budo_com
		sftp.get(budo_com, budo_folder + "BC_" + budo_com)

ssh.close()

#################################### Zip the Folder #####################################		
'''
myZipFile = zipfile.ZipFile(zipfile_name, mode='w', allowZip64=True) 

for root, dirs, files in os.walk(dates):
	for f in files:
		myZipFile.write(os.path.join(root, f))

myZipFile.close()
ssh.close()
'''
#################################### Dump files on the server  #####################################

os.chdir(dates) # "dates" is dir where position files reside 

# Reference http://effbot.org/librarybook/ftplib.htm

ftp = FTP(query_server_ip)
ftp.login(user=query_username, passwd=query_password)

if dates not in ftp.nlst():
	ftp.mkd(dates)

ftp.cwd(dates) # have dir on FTP site ready

for position_filename in os.listdir('.'):
	upload(ftp, position_filename)
	print "%s has been uploaded!" % position_filename 

#upload(ftp, zipfile_name)
#upload(ftp, "dumper.py")

ftp.close()
print "--- All file has been transferred ---"


#################################### Remove files once transfer is complete  #####################################

try:
	os.chdir("..")
	shutil.rmtree(dates)
	#os.remove(zipfile_name) #Once the script is stable, this line will be removed 
except Exception as e:
	print(e)
	raise
print "local copies have been removed.."
