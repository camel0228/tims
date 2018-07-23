import pysftp
import os,sys
import time
from os.path import join
from os.path import splitext
from datetime import date
import shutil
import warnings
warnings.filterwarnings('ignore')
def getstp():
	cnopts = pysftp.CnOpts()
	cnopts.hostkeys = None
	host = 'sftp.bloomberg.com'
	password = 'uI-4_P_5.[PU%0_h'
	username ='CCMSFTP'
	working_path = 'C:\Bloomberg_Trade_File\Temp'
	final_position='C:\Bloomberg_Trade_File'
	

	if not os.path.exists(working_path):
		os.makedirs(working_path)
	os.chdir(working_path)

	with pysftp.Connection(host, username =username,password=password, cnopts=cnopts) as sftp:
		#with sftp.cd('/'):
			 print ("connect to BBG sftp successfully.")
			 sftp.get('BBG.TRADES')

			 print("BBG.TRADES is downloaded  successfully.")
			 sftp.get('BBGALLOC.TRADES')
			 print("BBGALLOC.TRADES is downloaded and converted to csv file successfully.")

			 sftp.close()

					
	print ("SFTP connection is closed successfully")		 	
	today=date.today()
	datestamp=today.strftime("%Y%m%d") 
	files=os.listdir(working_path)
	for file in files:
		newfilename= os.path.splitext(file)[0]+"_TRADES_"+ datestamp+ ".csv"
		os.rename(file, newfilename)
	files=os.listdir(working_path)
	for file in files:
		src=working_path+"\\"+file
		dst=final_position+"\\"+file
		shutil.move(src,dst)
	print('All of the files from BBG has been converted into csv files and stored in C:\Bloomberg_Trade_File ')
	return ""

#def csvconvert():
""" Python Password Check """
import hashlib
import sys

Password = "heron7056"

# def main():
#     # Code goes here
#     print "Doing some stuff"
#     getstp()
#     sys.exit(0)


# while True:
#      input = raw_input("Enter password: ")
#      if input == Password:
#          print "welcome to the program"
#          main()
#      else:
#          print "Wrong Password"
#
