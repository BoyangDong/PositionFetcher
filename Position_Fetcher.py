import paramiko
import os
import shutil
import datetime as dt
import time
import csv
import zipfile 
import ftplib
from dumper import upload
from ftplib import FTP


yesterday = dt.datetime.now() - dt.timedelta( days = 1 )
date = yesterday.strftime( '%Y%m%d' )
#date = "20170913"


password = "v3pzegM"
username = "BUDO_TRADING"

query_username = "boyang"
query_password = "Password1234!"
query_server_ip = "172.30.80.4"


files_to_grab = [	
	"%s.GMICLCF2.CSV" % date,

	"BC_PFDFMNY_%s.CSV" % date,
	"BC_PFDFPOS_%s.CSV" % date,
	"BC_PFDFST4_%s.CSV" % date,

	"BT_PFDFMNY_%s.CSV" % date,
	"BT_PFDFPOS_%s.CSV" % date,
	"BT_PFDFST4_%s.CSV" % date,
	"BT_PFOPCTYPOS_%s.CSV" % date,
	"PFDFPOS_%s.CSV" % date, 

	"PFS80021.%s.TXT" % date,
	"PFS80023.%s.TXT" % date,
	"PFS80033.%s.TXT" % date,
	"PFS80036.%s.TXT" % date
]

files = []

#################################### Fetch position files from EDF #####################################

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#try:
trans = paramiko.Transport(("ftpc.edfmancapital.com", 2222))
trans.connect(username = username, password = password)
sftp = paramiko.SFTPClient.from_transport(trans)

print "clearing firm connected.."

path = r'%s' % (''.join(['E:/Repos/Project_3/', date, '/']))
zipfile_name = ''.join([date, '.zip'])

'''Create dir on local workstation'''
if not os.path.exists(path):
	os.makedirs(path)

'''Fetch file from Clearing Firm'''
for budo_file in sftp.listdir():
	if budo_file in files_to_grab:
		local_path = ''.join([path, budo_file])
		sftp.get(budo_file, local_path)
		files.append(local_path)

myZipFile = zipfile.ZipFile(zipfile_name, mode='w', allowZip64=True) 

for root, dirs, files in os.walk(date):
	for f in files:
		myZipFile.write(os.path.join(root, f))

myZipFile.close()

#################################### Dump files on the server  #####################################
# Reference http://effbot.org/librarybook/ftplib.htm

ftp = FTP(query_server_ip)
ftp.login(user=query_username, passwd=query_password)

upload(ftp, zipfile_name)
#upload(ftp, "dumper.py")

ftp.close()
print "file has been transferred"


#################################### Remove files once transfer is complete  #####################################
try:
    shutil.rmtree(date)
    os.remove(zipfile_name)
except Exception as e:
    print(e)
    raise
print "local copies have been removed.."


'''FILE STILL MISSING
BT_PFDFMNY_20170913.CSV
BT_PFDFPOS_20170913.CSV
BT_PFDFST4_20170913.CSV
BT_PFOPCTYPOS_20170913.CSV
'''

''' FILE CAN BE FOUND 
username_comm = "BUDO_COM"
password_comm = "OhkLY7H"

BC_PFDFMNY_20170913.CSV
BC_PFDFPOS_20170913.CSV
BC_PFDFST4_20170913.CSV
'''


''' FILE FOUNDED
20170913.GMICLCF2.CSV
PFDFPOS_20170913.CSV
PFS80021.20170913.TXT
PFS80023.20170913.TXT
PFS80033.20170913.TXT
PFS80036.20170913.TXT
'''