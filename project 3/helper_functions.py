import re
import csv
from datetime import date, timedelta
import datetime
from dateutil.relativedelta import relativedelta
import calendar

def give_dates(lastdate_) :
	lastdate_=datetime.datetime.strptime(str(lastdate_),'%Y%m%d').date()
	start_date=lastdate_
	data = []
	data.append(start_date)
	for i in range(7):
		days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
		dt = start_date + timedelta(days=days_in_month)
		start_date = dt
		data.append(dt)
	return data

def give_last_date(cname, lename):
	with open("F:/project3_frontend/processed_data.csv", 'r') as csvfile:
		csvreader = csv.reader(csvfile)
		fields=next(csvreader)
		last_date =""
		for row in csvreader:
			if row[1]==cname and row[2]==lename :
				last_date=row[0]
	lastdate_=""
	for w in last_date:
		if w!='-':
			lastdate_+=w
	return lastdate_


def take_fields():
	f = open("F:/project3_frontend/fields_to_take.txt", "r")
	listofatt=[]
	for x in f:
		listofatt.append(re.sub('\n', '', x))
	return listofatt
