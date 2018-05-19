# Brenda Miao, Marissa Le Coz, and Casey Baer
# This script will be periodically invoked on a server to gather information about which users are logged in.
# This script will output a .csv file with this auditing information.

import socket
# from pandas import DataFrame
import os
import datetime
import subprocess
# from subprocess import call

########### VALIDATING STRING FORMATS ###########

def is_valid_weekday(day):
    return day == "Mon" or day == "Tue" or day == "Wed" or day == "Thu" or day == "Fri" or day == "Sat" or day == "Sun"

def is_valid_month(month):
    return month == "Jan" or month == "Feb" or month == "Mar" or month == "Apr" or month == "May" or month == "Jun" or \
           month == "Jul" or month == "Aug" or month == "Sep" or month == "Oct" or month == "Nov" or month == "Dec"

def is_valid_day(day):
    return 32 > int(day) > 0

def is_valid_timestamp(timestamp):
    return len(timestamp) == 8 and timestamp.count(":") == 2

def is_valid_year(year):
    return len(year) == 4 and int(year) >= 2018

def is_valid_duration(duration):
    return ':' in duration and duration[0] == '(' and duration[len(duration)-1] == ')'

#######################################################

# get server name to be written to .csv
server_name = socket.gethostname()

# Create file and init columns if file doesn't already exist
if not os.path.exists("audit.csv"):
    f = open('audit.csv', 'w+')
    f.write("server, uid, login_day_of_week, login_month, login_day, login_year, login_timestamp, logout_day_of_week, logout_month, logout_day, logout_year, logout_timestamp, still_logged_in_as_of, duration_days, duration_hours, duration_minutes \n")
    f.close()

# Run the `last` command to get the most recent login/logout info
# proc = subprocess.Popen(["last", "-F"], stdout=subprocess.PIPE, shell=False) # True?
# (output, err) = proc.communicate()

# dummy output for testing; comment this out or delete later
# output = "luisch   pts/3        10.31.114.223    Fri May 18 14:59:39 2018 - Fri May 18 15:17:20 2018  (00:17) \n luisch   pts/4        10.31.114.223    Fri May 18 14:54:47 2018 - Fri May 18 15:16:15 2018  (00:21) \n ajsheeha pts/3        129.170.91.56    Fri May 18 14:45:39 2018 - Fri May 18 14:55:01 2018  (00:09) \n gbsnlspl pts/91       129.170.212.20   Wed May  2 12:18:12 2018 - Thu May  3 14:33:19 2018 (1+02:15) \n annie823 pts/4        10.31.187.42     Fri May 18 19:26:04 2018   still logged in"
output = "yanxin   pts/7        73.69.250.216    Fri May 18 21:54:04 2018   still logged in \n \
luisch   pts/6        38.111.19.130    Fri May 18 21:48:21 2018   still logged in \n \
kad      pts/5        10.31.47.145     Fri May 18 21:47:30 2018   still logged in \n \
luisch   pts/0        38.111.19.130    Fri May 18 21:44:14 2018   still logged in \n \
annie823 pts/4        10.31.187.42     Fri May 18 19:26:04 2018   still logged in \n \
annie823 pts/3        10.31.187.42     Fri May 18 19:25:41 2018   still logged in \n \
mlecoz   pts/2        10.31.206.31     Fri May 18 19:07:56 2018   still logged in \n \
mlecoz   pts/0        10.31.117.155    Fri May 18 17:26:22 2018 - Fri May 18 19:47:20 2018  (02:20) \n \
mlecoz   pts/0        10.31.117.155    Fri May 18 16:57:54 2018 - Fri May 18 17:25:41 2018  (00:27) \n \
gszypko  pts/6        10.31.38.38      Fri May 18 15:03:24 2018 - Fri May 18 19:25:01 2018  (04:21)"


# parse `last`'s output
row_list = output.split("\n") # a list where each row of the output is an element

f = open('audit.csv', 'a')
for row in row_list:

    fields_list = row.split()

    # some initial validation checks
    if len(fields_list) != 11 and len(fields_list) != 15:
        continue # this would be weird formatting. not a format this program knows how to parse

    if fields_list[9] == "still" and fields_list[10] == "running":
        continue # this is a system reboot line. not relevant.


    # Start parsing the fields, making checks when necessary

    uid = fields_list[0]

    login_day_of_week = fields_list[3]
    if not is_valid_weekday(login_day_of_week):
        continue # something about the formatting of this output line is messed up

    login_month = fields_list[4]
    if not is_valid_month(login_month):
        continue

    login_day = fields_list[5]
    if not is_valid_day(login_day):
        continue

    login_timestamp = fields_list[6]
    if not is_valid_timestamp(login_timestamp):
        continue

    login_year = fields_list[7]
    if not is_valid_year(login_year):
        continue

    # Here's where the formatting changes if you're dealing with a user who has logged out or who is still logged in
    is_logged_in = False
    # "still logged in"; must check for *each* word because there is also "still running" for system reboots
    if fields_list[8] == "still" and fields_list[9] == "logged" and fields_list[10] == "in":
        is_logged_in = True

    # the additional fields for logout info
    if not is_logged_in:

        logout_day_of_week = fields_list[9]
        if not is_valid_weekday(logout_day_of_week):
            continue

        logout_month = fields_list[10]
        if not is_valid_month(logout_month):
            continue

        logout_day = fields_list[11]
        if not is_valid_day(logout_day):
            continue

        logout_timestamp = fields_list[12]
        if not is_valid_timestamp(logout_timestamp):
            continue

        logout_year = fields_list[13]
        if not is_valid_year(logout_year):
            continue

        duration = fields_list[14]
        if not is_valid_duration(duration):
            continue
        duration = duration[1:len(duration)-1] # get rid of parentheses around the duration

        if '+' in duration: # this person has been on for days. Example: 1+10:10 means 1 day, 10 hours, 10 minutes
            days_and_time = duration.split('+')
            duration_days = days_and_time[0]
            hours_and_mins = days_and_time[1].split(":")
            duration_hours = hours_and_mins[0]
            duration_mins = hours_and_mins[1]
        else: # this person has been on for less than a day
            duration_days = "0"
            hours_and_mins = duration.split(":") # we already validated that there's a colon
            duration_hours = hours_and_mins[0]
            duration_mins = hours_and_mins[1]

        f.write(server_name + "," + uid + "," + login_day_of_week + "," + login_month + "," + login_day + "," + login_year + "," + login_timestamp + "," + logout_day_of_week + "," + logout_month + "," + logout_day + "," + logout_year + "," + logout_timestamp + "," + "" + "," + duration_days + "," + duration_hours + "," + duration_mins + "\n")

    else: # is logged in still
        f.write(server_name + "," + uid + "," + login_day_of_week + "," + login_month + "," + login_day + "," + login_year + "," + login_timestamp + "," + "" + "," + "" + "," + "" + "," + "" + "," + "" + "," + datetime.datetime.now().strftime("%a %B %d %Y %I:%M:%S") + "," + "" + "," + "" + "," + "" + "\n")

f.close()

# clean up duplicates at the end each time
# also remove all "still logged in" on each run because the most recent run will have all
