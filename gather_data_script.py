# Brenda Miao, Marissa Le Coz, and Casey Baer
# This script will be periodically invoked on a server to gather information about which users are logged in.
# This script will output a .csv file with this auditing information.

import socket
from pathlib import Path
from pandas import DataFrame
import os
# from subprocess import call


server_name = socket.gethostname()

# Create file if it doesn't already exist
raw_data_file = Path("audit.csv")
if not raw_data_file.is_file():
    Path("audit.csv").touch()
    f = open('audit.csv', 'w')
    f.write("hostname, uid, login_day_of_week, login_month, login_day, login_year, login_timestamp, logout_day_of_week, logout_month, logout_day, logout_year, logout_timestamp, still_logged_in_as_of, duration_days, duration_hours, duration_minutes")

# Run the `last` command to get the most recent login/logout info
output = os.system('last')
print output

#dummy
output = "luisch   pts/3        10.31.114.223    Fri May 18 14:59:39 2018 - Fri May 18 15:17:20 2018  (00:17) \n luisch   pts/4        10.31.114.223    Fri May 18 14:54:47 2018 - Fri May 18 15:16:15 2018  (00:21) \n ajsheeha pts/3        129.170.91.56    Fri May 18 14:45:39 2018 - Fri May 18 14:55:01 2018  (00:09)"
# parse 'last''s output
row_list = output.split("\n") # each row

for row in row_list:

    fields_list = row.split()

    uid = fields_list[0]

    login_day_of_week = fields_list[3]
    login_month = fields_list[4]
    login_day = fields_list[5]
    login_timestamp = fields_list[6]
    login_year = fields_list[7]

    is_logged_in = False
    if fields_list[8] == "still": # "still logged in"
        is_logged_in = True

    if not is_logged_in:

        logout_day_of_week = fields_list[9]
        logout_month = fields_list[10]
        logout_day = fields_list[11]
        logout_timestamp = fields_list[12]
        logout_year = fields_list[13]

        duration = fields_list[14][1:len(duration)-1] # get rid of parentheses around the duration
        if '+' in duration: # this person has been on for days
            days_and_time = duration.split('+')
            duration_days = days_and_time[0]
            hours_and_mins = days_and_time[1].split(":")
            duration_hours = hours_and_mins[0]
            duration_mins = hours_and_mins[1]
        else: # this person has been on for less than a day
            duration_days = "0"
            hours_and_mins = days_and_time[1].split(":")
            duration_hours = hours_and_mins[0]
            duration_mins = hours_and_mins[1]


    if not is_logged_in:
        f.write(server_name + "," + uid + "," + login_day_of_week + "," + login_month + "," + login_day + "," + login_year + "," + login_timestamp + "," + logout_day_of_week + "," + logout_month + "," + logout_day + "," + logout_year + "," + logout_timestamp + "," + "" + "," + duration)
        "hostname, uid, login_day_of_week, login_month, login_day, login_year, login_timestamp, logout_day_of_week, logout_month, logout_day, logout_year, logout_timestamp, still_logged_in_as_of, total_duration")

# clean up duplicates at the end each time
# also remove all "still logged in" on each run because the most recent run will have all

# # convert file to dataframe
# df = DataFrame.from_csv("audit.csv")
# if df.empty:
#     # output = call('last --since 20180501110000', shell=True)
#     output = os.system('last -F')
#     print output
#
#
#
# # get server name
# server_name = socket.gethostname()

# get



