###########################################
## Program: Hourly Call Reports          ##
## Description: Reports on # of inbound  ##
## calls from each hour of the day. Then ##
## averages the hours for each day       ##
## separately.							 ##
## Date: 2/2/15							 ##
## Author: Jeffrey Zic					 ##
###########################################

import re
import fileinput
import sys
from datetime import date, timedelta
import os.path
import datetime
import re

hourlycounts = [0]*24
fname = sys.stdin.readlines() # Receives from stdin, built to work with cdr.sh

inbound_group = ['"CCR South Front Desk"', '"Cindy Business Office"', '"Tom Back Office"', '"CCR North Front Desk"', '"CCR Workstation"', '"Nan Office Mgr"', '"Library East"', '"Doctor Workstation South"', '"Pharmacy Counter"', '"Team Leader Station"', '"Library South West"', '"Back Office North"', '"Sandi CCR TL"', '"Chris P Back Office South"', '"Tx Room West"']

class CDR: #There are other parameters available for the CDRs but I just added the ones that are needed

	def __init__(self):
		self.end_timestamp = ""
		self.direction = ""
		self.destination_name = ""
		self.hangup_cause = ""
		self.caller_id_name = ""
		self.destination_type = ""
	def set_end_timestamp(self, end_timestamp):
		self.end_timestamp = end_timestamp
	def set_direction(self, direction):
		self.direction = direction
	def set_destination_name(self, destination_name):
		self.destination_name = destination_name
	def set_hangup_cause(self, hangup_cause):
		self.hangup_cause = hangup_cause
	def set_caller_id_name(self, caller_id_name):
		self.caller_id_name =  caller_id_name
	def set_destination_type(self, destination_type):
		self.destination_type = destination_type
	  
def transferF(old, new):
# for replacing a file of the same name
	os.remove(new)
	os.rename(old, new)
	
def dailyCalls():
# records the calls/ hr of each hour every day
	weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	yesterdayDate = date.today() - timedelta(1)
		
	with open("./Daily/" + weekdays[yesterdayDate.weekday()], 'a') as f:
	
		f.write(str(yesterdayDate)[:10] + ": \n")
		for i in range(24):
			f.write(str(i) + ": " + str(hourlycounts[i]) + "\n")
		f.write("\n")
	
		
	
def getCalls():
# grabs calls from a file generated from the Cudatel's REST API, run in bash and filename grabbed from STDIN
	newCall = True
	CDR_List = []

	with open(fname[0].rstrip('\n'),'r') as f:
		
		for line in f:
				
			if newCall == True: # In the records, the parameters always appear in the same order so a new call is determined by
				newCDR = CDR() # seeing when it reaches the last parameter in a call, then the next one will be of a new call
				newCall = False
			
			words = line.rstrip('\n').partition(":")
			type = words[0].lstrip(' ').rstrip(' ')
			data = words[-1].rstrip(',').rstrip(' ').lstrip(' ')
						
			if (type == '"end_timestamp"'):
				newCDR.end_timestamp = data
			elif (type == '"direction"'):
				newCDR.direction = data
			elif (type == '"destination_name"'):
				newCDR.destination_name = data
			elif (type == '"hangup_cause"'):
				newCDR.hangup_cause = data
			elif (type == '"caller_id_name"'):
				newCDR.caller_id_name = data
			elif (type == '"destination_type"'):
				newCDR.destination_type = data
				CDR_List.append(newCDR)
				newCall = True
	return CDR_List			
					
def CountCalls():
# Counts the incoming calls received each hour.
	calls = getCalls()

	for call in calls:
		
		if (call.direction == '"inbound"') and ((call.hangup_cause == '"NORMAL_CLEARING"') or (call.hangup_cause == '"NONE"')) and (not call.caller_id_name in inbound_group): #Filtering out any calls in the inbound group so we don't count any intra-office calls
			
			hourlycounts[int(call.end_timestamp.split()[1][:2])] += 1
				
def AvgCalls():
# records the average amount of calls received each hour for each day of the week
	weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
	firstTime = False
	currentDate = date.today() - timedelta(1)
	currentDay = weekdays[currentDate.weekday()]
	dailyAvgs = []
	
	indvHrs = [[[] for y in range(24)] for x in range(7)]

	if not os.path.isfile("./Reports/Averages"): #if the file to store the data doesn't exist we need to create it with correct formatting
		
		for day in weekdays:
		
			with open("./Reports/Averages", 'a') as f:
				f.write(day + '\n')
				count = 0
				while count < 24:
					f.write(str(count).zfill(2) + " : -\n") #If a lines are marked with a dash that means the program has never been run for that day
					count += 1
				f.write("\n")
		
	for day in range(7):
		dailyAvgs.append([])
		with open("./Daily/" + weekdays[int(day)], 'r') as f, open("./Reports/tempavg", 'w') as o:
	
			pastAvg = [None] * 24
			foundHour = 0
			count = 1
		
			for hour in range(24):
				for line in f:
			
					if line != "\n":
						nums = line.rstrip('\n').split(":")
				
					if nums[0] == str(hour):
						indvHrs[day][hour].append(int(nums[1]))
					
					foundHour = 0
				f.seek(0)
	
		for hourlycalls in indvHrs[day]:
			
			dailyAvgs[day].append(int(sum(hourlycalls) / len(hourlycalls)))
	
	with open("./Reports/Averages", 'w') as f:
		for day in range(7):
			f.write(weekdays[day] + "\n")
			
			for hour in range(24):
				f.write(str(hour) + " : " + str(dailyAvgs[day][hour]) + '\n')
			f.write('\n')
	
def main():	
	CountCalls()
	dailyCalls()
	AvgCalls()

if __name__ == "__main__":
	main()