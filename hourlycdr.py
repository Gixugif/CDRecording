#!/usr/bin/python
# -*- coding: utf-8 -*-
# Program: Hourly Call Reports
# Description: Reports on # of inbound
# calls from each hour of the day. Then
# averages the hours for each day
# separately.
# Date: 2/2/15
# Author: Jeffrey Zic

def main():
    test = Call_Detail_Directory()
    dates = getDates()
    
    login = test.getLogin()
    count = 1
    CDR_List = []
    page = 1
    while (count != 0):
        cdr = test.get_calls("test",login,page,formatDate(dates[0]),formatDate(dates[1]))
        count = cdr[0]
        CDR_List = CDR_List + cdr[1]
        page += 1
        print(count)

    test.call_detail_directory = CDR_List

    count = Call_Counter()
    count.count_days_of_week(test)
    count.avg_calls_per_hour(test)
    count.avg_calls_per_day(test)
    count.daily_avg_calls_output(count.hourly_averages)
    count.hourly_avg_calls_output(count.hourly_averages)
    count.total_calls_output()


if __name__ == '__main__':
    main()
