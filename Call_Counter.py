#!/usr/bin/python
# -*- coding: utf-8 -*-
# Title: Call_Counter
# Description: Counts the number of
# calls in a Call Detail Record hourly,
# daily.
# Date: 6/9/16
# Author: Jeffrey Zic

import re
import fileinput
import sys
import datetime
from datetime import date, timedelta
import time
import os.path
import csv
import calendar

class Call_Counter:

    """Counts the number of true calls"""

    def __init__(self, counts=[0] * 24):
        """Initializes a Call_Counter.

        :param counts: A list of counted calls for each hour of a day.
        :param daily_counts: A count of calls by the hour, divided by the day
        :type counts: int[]
        :type daily_counts: dict
        """

        self.weekdays = [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday',
            'Saturday',
            'Sunday',
            ]

        self.hourly_counts = {
            'Monday': [0] * 24,
            'Tuesday': [0] * 24,
            'Wednesday': [0] * 24,
            'Thursday': [0] * 24,
            'Friday': [0] * 24,
            'Saturday': [0] * 24,
            'Sunday': [0] * 24,
            }

        self.hourly_averages = {
            'Monday': [0] * 24,
            'Tuesday': [0] * 24,
            'Wednesday': [0] * 24,
            'Thursday': [0] * 24,
            'Friday': [0] * 24,
            'Saturday': [0] * 24,
            'Sunday': [0] * 24,
            }

        self.daily_averages = {
            'Monday': 0,
            'Tuesday': 0,
            'Wednesday': 0,
            'Thursday': 0,
            'Friday': 0,
            'Saturday': 0,
            'Sunday': 0,
            }

    def count_days_of_week(
        self,
        calls,
        start_date=None,
        end_date=None,
        ):
        """Counts the number of each day of the week in a date range.

        This will count the number of each days of the week in a date range (e.g. number of mondays, tuesdays, etc.).
        You can either provide a Call Detail Directory and it will use the range of dates in that, or specify the date range
        yourself. Specifying a Call Detail Directory will override specified date ranges.

        :param call: An optional list of calls to count the days of week in.
        :param start_date: An optional date to use as the beginning of your range.
        :param end_date: An optional  date to use as the end of your range.
        :type calls: Call_Detail_Directory
        :type start_date: date
        :type end_date: date
        :return days_of_week_count
        :rtype dict
        """

        days_of_week_count = {
            'Monday': 0,
            'Tuesday': 0,
            'Wednesday': 0,
            'Thursday': 0,
            'Friday': 0,
            'Saturday': 0,
            'Sunday': 0,
            }

        if calls:
            start_date = \
                calls.call_detail_directory[0].end_timestamp.split(' '
                    )[0]
            end_date = \
                calls.call_detail_directory[-1].end_timestamp.split(' '
                    )[0]

        current_date = start_date.split('-')
        current_date = date(int(current_date[0].lstrip('"')),
                            int(current_date[1]), int(current_date[2]))

        end_date = date(int(end_date[1:5]), int(end_date[6:8]),
                        int(end_date[9:]))

        while current_date <= end_date:
            days_of_week_count[self.weekdays[current_date.weekday()]] += \
                1
            current_date = current_date + timedelta(1)

        return days_of_week_count

    def count_calls(self, calls):
        """Counts the amount of real calls in a directory.

        This counts the amount of real calls in a directory. When grabbing calls from Barracuda Communications Server
        there will be erroneous records due to each ringing phone being counted, transfers, call-parking, etc. Inbound calls
        will always have a "direction" equal to "inbound", which sounds obvious however calls that are transferred around
        an office or intra-office calls tend to show up and won't be listed as "inbound". The hangup cause also won't be
        listed as a transfer or something else and only phones in the inbound_group can be taking inbound calls.

        :param calls: List of the calls you are counting
        :type calls: Call_Detail_Directory
        :returns hourly_counts
        :rtype int[]
        """

        monitoredPhones = getMonitoredPhones()

        for call in calls:

            # Filtering out any calls in the inbound group so we don't count any intra-office calls
            if call.direction == '"inbound"' and (call.hangup_cause
                    == '"NORMAL_CLEARING"' or call.hangup_cause == '"NONE"'
                    ) and call.destination_type != 'internal' \
                and not call.caller_id_name in monitoredPhones \
                and call.destination_name in monitoredPhones:

                call_date = call.end_timestamp.split('-')

                day_of_week = date(int(call_date[0].lstrip('"')),
                                   int(call_date[1]),
                                   int((call_date[2])[:2])).weekday()
                self.hourly_counts[self.weekdays[day_of_week]][int((call.end_timestamp.split()[1])[:2])] += \
                    1

        return self.hourly_counts

    def avg_calls_per_hour(self, calls):
        """Finds the average amount of calls for each day of the week divided by hour.

        Takes a call directory and finds the average number of calls divided by day of the week by the hour.

        :param call_directory: list of call detail records to average
        :type call_directory: Call_Detail_Directory
        :returns daily_averages
        :rtype dict
        """

        num_days_of_week = self.count_days_of_week(calls)
        self.count_calls(calls.call_detail_directory)
        for i in self.weekdays:
            for hour in range(24):
                if num_days_of_week[i] != 0:
                    self.hourly_averages[i][hour] = \
                        self.hourly_counts[i][hour] \
                        / num_days_of_week[i]
                else:
                    self.hourly_averages[i][hour] = 0

        return self.hourly_averages

    def avg_calls_per_day(self, calls):
        """Finds the average amount of calls for each day of the week

        Takes a call directory and finds the average number of calls divided by day of the week.

        :param call_directory: list of call detail records to average
        :type call_directory: Call_Detail_Directory
        :returns daily_averages
        :rtype dict
        """

        num_days_of_week = self.count_days_of_week(calls)

        for i in self.weekdays:
            daily_counts = sum(self.hourly_counts[i])
            if num_days_of_week[i] > 0:
                self.daily_averages[i] = daily_counts / num_days_of_week[i]
            else:
                self.daily_averages[i] = 0

        return self.daily_averages

    def hourly_avg_calls_output(self, averages):
        """Outputs the average calls into a file

        :param averages: list of average call divided by day of the week and hour
        :type averages: int[][]
        """

        with open('hourly_averages.csv', 'wb') as csvfile:
            avgs_writer = csv.writer(csvfile, dialect='excel')
            avgs_writer.writerow([''] + self.weekdays)

            for hour in range(24):
                daily_hours = []
                for day in self.weekdays:
                    daily_hours.append(self.hourly_averages[day][hour])
                hour_str = str(hour) + ': '
                avgs_writer.writerow([hour_str] + daily_hours)

    def daily_avg_calls_output(self, averages):
        """Outputs the average calls divided by day into a file

        :param averages: list of average call divided by day of the week and hour
        :type averages: int[]
        """

        with open('daily_averages.csv', 'wb') as csvfile:
            avgs_writer = csv.writer(csvfile, dialect='excel')
            avgs_writer.writerow(self.weekdays)

            daily = []
            for day in self.weekdays:
                daily.append(self.daily_averages[day])
            avgs_writer.writerow(daily)

    def total_calls_output(self):
        """Outputs the total calls for each hour of each day into a .csv"""

        with open('totals.csv', 'wb') as csvfile:
            totals_writer = csv.writer(csvfile, dialect='excel')
            totals_writer.writerow([''] + self.weekdays)

            for hour in range(24):
                daily_hours = []
                for day in self.weekdays:
                    daily_hours.append(self.hourly_counts[day][hour])
                hour_str = str(hour) + ': '
                totals_writer.writerow([hour_str] + daily_hours)

    def specify_days_of_week(self):
        """Allows the user to specify the specific days of the week to
        count in a date range.
        """

        days_of_week = raw_input("Please input a comma delimited list of days of week to be included in count (leave blank for all): ").split(',')

        if days_of_week != "":
            self.weekdays = days_of_week

        return days_of_week

def getMonitoredPhones():

    monitoredPhones = []

    with open('inbound', 'r') as file:

        for line in file:
            monitoredPhones.append(line.rstrip('\r\n'))

    return monitoredPhones

def convertDate(date):
    """Convert date of MM/DD/YYYY format to Date() object

    :returns convertedDate
    :rtype datetime.date()
    """

    convertedDate = datetime.date(int(date[6:]),int(date[:2]),int(date[3:5]))

    return convertedDate

def getDates():
    """Ask the user to provide dates in the format: MM/DD/YYYY

    :returns dateRange
    :rtype [datetime.date(),datetime.date()]
    """

    startDate = convertDate(raw_input("Please enter starting date (MM/DD/YYYY): " ))
    endDate = convertDate(raw_input("Please enter ending date (MM/DD/YYYY): "))

    dateRange = [startDate,endDate]

    return dateRange

def formatDate(date):
    """Format a datetime.Date() object to be fed into the script to retrieve
    call detail records from the Cudatel Communications Server

    :return: formatedDate
    :rtype: String
    """

    formatedDate = "{month}+{day}%2C+{year}".format(month=calendar.month_name[date.month],day=date.day,year=date.year)

    return formatedDate

def formatDate2(date):
    """Format a String written as "XX/XX/XXXX" to be fed into the script to retrieve
    call detail records from the Cudatel Communications Server

    :param date: date written as "XX/XX/XXXX"
    :type date: String
    :return: formatedDate
    :rtype: String
    """

    formatedDate = "{month}+{day}%2C+{year}".format(month=calendar.month_name[int(date[:2])],day=date[3:5],year=date[6:])

    return formatedDate

def compareDates(startDate,endDate):
    """Compare two dates that are Strings in the format MM/DD/YYYY. Returns true if
    startDate is earlier than endDate

    :param startDate: date written as MM/DD/YYYY
    :param startDate: date written as MM/DD/YYYY
    :type startDate: String
    :type endDate: String
    return: isDateEarlier
    :rtype: Bool
    """

    isDateEarlier = True

    if (int(startDate[6:]) >= int(endDate[6:])):
        if (int(startDate[6:]) == int(endDate[6:])):
            if (int(startDate[:2]) > int(endDate[:2])):
                isDateEarlier = False
        elif ((int(startDate[6:]) > int(endDate[6:]))):
            isDateEarlier = False

    return isDateEarlier

def pullCallsDateRange(callData,dates,login):
    """Grab call metadata in a date range from CCS

    Currently you cannot grab more than a months worth of data, so in order
    to get around this limitation this function runs get_calls for each month
    individually in a date range, and appends the results each time to the file

    :param callData: call detail records to analyze
    :param dates: range of dates to get calls from
    :param login: login info for the CCS
    :type dates: [String,String]
    :type callData: Call_Detail_Directory
    """

    startDate = dates[0]
    endDate = str(int(dates[0][:2]) + 1).zfill(2) + dates[0][2:]

    if (int(endDate[:2]) > 12):
        newMonth = "1"
        newMonth = newMonth.zfill(2)
        newYear = int(endDate[6:]) + 1
        endDate = str(newMonth) + str(endDate[2:6]) + str(newYear)

    while (compareDates(endDate,dates[1])):
        print(formatDate2(startDate))
        print(formatDate2(endDate))

        callData.get_calls('test',login[0],login[1],formatDate2(startDate),formatDate2(endDate))

        startDate = endDate
        endDate = str(int(endDate[:2]) + 1).zfill(2) + endDate[2:]

        if (int(endDate[:2]) > 12):
            newMonth = "1"
            newMonth = newMonth.zfill(2)
            newYear = int(endDate[6:]) + 1
            endDate = str(newMonth) + str(endDate[2:6]) + str(newYear)
