# Reference http://effbot.org/librarybook/ftplib.htm

from ftplib import FTP
import os

def upload(ftp, file):
	ext = os.path.splitext(file)[1]
	if ext in (".txt"):
		ftp.storlines("STOR " + file, open(file))
	else:
		ftp.storbinary("STOR " + file, open(file, "rb"), 1024)

