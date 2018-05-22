# Created by: Marissa Le Coz
# Modified by:
#
# Description: This script will be periodically invoked on a server to gather information about which users are logged in.
#              It is an intermediate file that will need a little more processing before being shown to the auditor (see below).
#
# This script will output a .csv file with this auditing information:
# Column descriptions:
# server: the server the script is running on
# uid: the user id whose login information that row holds
# login_day_of_week, login_month, login_day, login_year, login_timestamp - self explanatory
# logout_day_of_week, logout_month, logout_day, logout_year, logout_timestamp - self explanatory. NOTE: these fields
#     empty if the user has not yet ended their session at the time the script is invoked
# still_logged_in_as_of - datetime stamp indicating the time that the script was invoked. NOTE: this field is only
#     populated if the user's session has not yet ended when the script is invoked
# duration_days, duration_hours, duration_minutes - if the session has completed, how long it lasted for. NOTE: this
#     field is only populated if the user's session has ended
#
# Intended usage of this script:
# The server will invoke this script at periodic intervals. Data will be amassed in audit_raw.csv.
# Another script should be written that takes this .csv file and:
# - creates a new csv file, perhaps audit.csv (this is the one the auditor will look at)
# - copies data in some user-specified date range from this original csv (I would recommend working with a pandas dataframe).
#   (Alternatively, the user could instead specify that they want the x most recent entries, or something like that.)
# - gets rid of duplicate entries (ie, where multiple rows have ALL the exact same column values)
# - For all "still logged in" entries in the range:
#     - If there is an entry that shows the user did eventually log out of that session, delete all the "still logged in" entries because they are irrelevant.
#     - If there is not an entry that shows the user logged out, delete all the "still logged" in entries except the most recent.

import socket
import os
import datetime
import subprocess

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
if not os.path.exists("audit_raw.csv"):
    f = open('audit_raw.csv', 'w+')
    f.write("server, uid, login_day_of_week, login_month, login_day, login_year, login_timestamp, logout_day_of_week, logout_month, logout_day, logout_year, logout_timestamp, still_logged_in_as_of, duration_days, duration_hours, duration_minutes \n")
    f.close()

# Run the `last` command to get the most recent login/logout info
proc = subprocess.Popen(['last', '-F'], stdout=subprocess.PIPE)
(output, err) = proc.communicate()

# parse `last`'s output
row_list = output.split("\n") # a list where each row of the output is an element

f = open('audit_raw.csv', 'a')
for row in row_list:

    fields_list = row.split()

    # some initial validation checks
    if len(fields_list) != 11 and len(fields_list) != 15:
        continue # this would be weird formatting. not a format this program knows how to parse.

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