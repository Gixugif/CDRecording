#!/usr/bin/python
# -*- coding: utf-8 -*-
# Program: Hourly Call Reports
# Description: Reports on # of inbound
# calls from each hour of the day. Then
# averages the hours for each day
# separately.
# Date: 2/2/15
# Author: Jeffrey Zic

import Call_Detail_Directory
import Call_Detail_Record
import Call_Counter

def main():
    test = Call_Detail_Directory.Call_Detail_Directory()
    dates = Call_Counter.getDates()
    
    login = test.getLogin()
    count = 1
    CDR_List = []
    page = 1
    while (count != 0):
        cdr = test.get_calls("test",login,page,Call_Counter.formatDate(dates[0]),Call_Counter.formatDate(dates[1]))
        count = cdr[0]
        CDR_List = CDR_List + cdr[1]
        page += 1
        print(count)

    test.call_detail_directory = CDR_List

    count = Call_Counter.Call_Counter()
    count.count_days_of_week(test)
    count.count_calls(test.call_detail_directory)
    count.avg_calls_per_hour(test)
    count.avg_calls_per_day(test)
    count.daily_avg_calls_output(count.hourly_averages)
    count.hourly_avg_calls_output(count.hourly_averages)
    count.total_calls_output()

    count = Call_Counter.Call_Counter()
    count.count_missed_calls(test.call_detail_directory)
    count.avg_calls_per_hour(test)
    count.avg_calls_per_day(test)
    count.daily_avg_calls_output(count.hourly_averages,'missed')
    count.hourly_avg_calls_output(count.hourly_averages,'missed')
    count.total_calls_output('missed')


if __name__ == '__main__':
    main()
