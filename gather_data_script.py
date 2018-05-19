# Brenda Miao, Marissa Le Coz, and Casey Baer
# This script will be periodically invoked on a server to gather information about which users are logged in.
# This script will output a .csv file with this auditing information.

import socket
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
# proc = subprocess.Popen(["last", "-F"], stdout=subprocess.PIPE, shell=True) # False?
# (output, err) = proc.communicate()

# dummy output for testing; comment this out or delete later
# output = "luisch   pts/3        10.31.114.223    Fri May 18 14:59:39 2018 - Fri May 18 15:17:20 2018  (00:17) \n luisch   pts/4        10.31.114.223    Fri May 18 14:54:47 2018 - Fri May 18 15:16:15 2018  (00:21) \n ajsheeha pts/3        129.170.91.56    Fri May 18 14:45:39 2018 - Fri May 18 14:55:01 2018  (00:09) \n gbsnlspl pts/91       129.170.212.20   Wed May  2 12:18:12 2018 - Thu May  3 14:33:19 2018 (1+02:15) \n annie823 pts/4        10.31.187.42     Fri May 18 19:26:04 2018   still logged in"
output = "yanxin   pts/7        73.69.250.216    Fri May 18 21:54:04 2018 - Fri May 18 21:58:30 2018  (00:04) \n \
luisch   pts/6        38.111.19.130    Fri May 18 21:48:21 2018 - Fri May 18 22:08:14 2018  (00:19) \n \
kad      pts/5        10.31.47.145     Fri May 18 21:47:30 2018   still logged in \n \
luisch   pts/0        38.111.19.130    Fri May 18 21:44:14 2018 - Fri May 18 22:08:12 2018  (00:23) \n \
annie823 pts/4        10.31.187.42     Fri May 18 19:26:04 2018   still logged in \n \
annie823 pts/3        10.31.187.42     Fri May 18 19:25:41 2018   still logged in \n \
mlecoz   pts/2        10.31.206.31     Fri May 18 19:07:56 2018   still logged in \n \
mlecoz   pts/0        10.31.117.155    Fri May 18 17:26:22 2018 - Fri May 18 19:47:20 2018  (02:20) \n \
mlecoz   pts/0        10.31.117.155    Fri May 18 16:57:54 2018 - Fri May 18 17:25:41 2018  (00:27) \n \
gszypko  pts/6        10.31.38.38      Fri May 18 15:03:24 2018 - Fri May 18 19:25:01 2018  (04:21) \n \
luisch   pts/3        10.31.114.223    Fri May 18 14:59:39 2018 - Fri May 18 15:17:20 2018  (00:17) \n \
luisch   pts/4        10.31.114.223    Fri May 18 14:54:47 2018 - Fri May 18 15:16:15 2018  (00:21) \n \
ajsheeha pts/3        129.170.91.56    Fri May 18 14:45:39 2018 - Fri May 18 14:55:01 2018  (00:09) \n \
hnich    pts/40       10.31.183.64     Fri May 18 14:00:41 2018 - Fri May 18 17:27:31 2018  (03:26) \n \
babagadi pts/39       172.21.206.205   Fri May 18 14:00:00 2018 - Fri May 18 16:19:15 2018  (02:19) \n \
hnich    pts/37       10.31.183.64     Fri May 18 13:59:39 2018 - Fri May 18 15:07:39 2018  (01:08) \n \
kad      pts/36       10.31.40.192     Fri May 18 13:53:08 2018 - Fri May 18 14:12:44 2018  (00:19) \n \
luisch   pts/35       10.31.114.223    Fri May 18 13:44:21 2018 - Fri May 18 16:48:12 2018  (03:03) \n \
ss98     pts/36       10.31.126.242    Fri May 18 13:35:17 2018 - Fri May 18 13:36:42 2018  (00:01) \n \
luisch   pts/35       10.31.114.223    Fri May 18 13:29:58 2018 - Fri May 18 13:44:02 2018  (00:14) \n \
luisch   pts/0        10.31.114.223    Fri May 18 13:26:59 2018 - Fri May 18 16:48:12 2018  (03:21) \n \
dmwhang  pts/30       10.31.121.55     Fri May 18 13:09:32 2018 - Fri May 18 15:26:05 2018  (02:16) \n \
johnconn pts/31       10.31.182.235    Fri May 18 13:05:16 2018 - Fri May 18 15:31:44 2018  (02:26) \n \
tongxu   pts/32       10.31.124.68     Fri May 18 12:57:00 2018 - Fri May 18 15:29:33 2018  (02:32) \n \
alexisbh pts/31       10.31.190.73     Fri May 18 12:56:54 2018 - Fri May 18 12:59:12 2018  (00:02) \n \
yanxin   pts/28       10.31.125.223    Fri May 18 12:54:01 2018 - Fri May 18 14:12:10 2018  (01:18) \n \
yanxin   pts/29       10.31.125.223    Fri May 18 12:50:18 2018 - Fri May 18 14:12:13 2018  (01:21) \n \
luisch   pts/28       10.31.114.223    Fri May 18 12:49:01 2018 - Fri May 18 12:53:09 2018  (00:04) \n \
olivermc pts/15       10.31.123.93     Fri May 18 12:07:34 2018 - Fri May 18 15:12:05 2018  (03:04) \n \
tongxu   pts/3        10.31.124.68     Fri May 18 11:44:39 2018 - Fri May 18 14:37:08 2018  (02:52) \n \
yanxin   pts/3        10.31.125.223    Fri May 18 11:29:31 2018 - Fri May 18 11:32:04 2018  (00:02) \n \
sburack  pts/0        10.31.40.29      Fri May 18 11:02:45 2018 - Fri May 18 13:10:42 2018  (02:07) \n \
elenadot pts/30       10.31.228.186    Fri May 18 10:38:48 2018 - Fri May 18 13:09:20 2018  (02:30) \n \
johnconn pts/29       10.31.208.200    Fri May 18 10:09:20 2018 - Fri May 18 12:21:41 2018  (02:12) \n \
tongxu   pts/6        10.31.124.68     Fri May 18 09:43:49 2018 - Fri May 18 11:44:32 2018  (02:00) \n \
cs50     pts/6        74.94.163.125    Fri May 18 09:08:43 2018 - Fri May 18 09:30:38 2018  (00:21) \n \
cs50     pts/7        74.94.163.125    Fri May 18 08:47:12 2018 - Fri May 18 09:08:16 2018  (00:21) \n \
cs50     pts/7        107.107.62.238   Fri May 18 08:22:52 2018 - Fri May 18 08:40:32 2018  (00:17) \n \
hnich    pts/6        10.31.231.18     Fri May 18 07:21:03 2018 - Fri May 18 08:50:24 2018  (01:29) \n \
hnich    pts/5        10.31.231.18     Fri May 18 05:19:21 2018 - Fri May 18 12:57:36 2018  (07:38) \n \
hnich    pts/2        10.31.231.18     Fri May 18 05:19:02 2018 - Fri May 18 12:57:36 2018  (07:38) \n \
mdcobb   pts/10       10.31.196.229    Thu May 17 23:44:13 2018 - Fri May 18 01:52:37 2018  (02:08) \n \
luisch   pts/9        10.31.114.223    Thu May 17 23:43:07 2018 - Fri May 18 00:11:14 2018  (00:28) \n \
luisch   pts/8        10.31.114.223    Thu May 17 23:22:33 2018 - Fri May 18 00:11:16 2018  (00:48) \n \
babagadi pts/7        172.21.234.68    Thu May 17 23:13:31 2018 - Fri May 18 01:36:42 2018  (02:23) \n \
kad      pts/5        10.31.237.21     Thu May 17 22:43:12 2018 - Thu May 17 23:48:12 2018  (01:05) \n \
tongxu   pts/0        76.118.42.148    Thu May 17 22:22:42 2018 - Fri May 18 10:41:12 2018  (12:18) \n \
tongxu   pts/0        76.118.42.148    Thu May 17 22:21:03 2018 - Thu May 17 22:22:34 2018  (00:01) \n \
spark    pts/0        172.21.12.231    Thu May 17 21:55:31 2018 - Thu May 17 22:02:24 2018  (00:06) \n \
tomyoung pts/9        10.31.43.14      Thu May 17 21:50:55 2018 - Thu May 17 23:09:03 2018  (01:18) \n \
tongxu   pts/4        76.118.42.148    Thu May 17 21:49:28 2018 - Thu May 17 22:20:56 2018  (00:31) \n \
rguju    pts/35       10.31.210.236    Thu May 17 21:09:39 2018 - Fri May 18 01:43:48 2018  (04:34) \n \
luisch   pts/34       10.31.114.223    Thu May 17 20:53:08 2018 - Thu May 17 21:16:00 2018  (00:22) \n \
kiron    pts/30       75.69.135.90     Thu May 17 20:33:27 2018 - Thu May 17 21:22:54 2018  (00:49) \n \
akarki   pts/26       172.21.219.85    Thu May 17 20:32:24 2018 - Thu May 17 22:39:17 2018  (02:06) \n \
syedt21  pts/34       129.170.132.183  Thu May 17 20:25:43 2018 - Thu May 17 20:45:43 2018  (00:20) \n \
syedt21  pts/34       129.170.132.183  Thu May 17 20:21:52 2018 - Thu May 17 20:24:17 2018  (00:02) \n \
akarki   pts/33       172.21.219.85    Thu May 17 20:20:00 2018 - Thu May 17 22:39:17 2018  (02:19) \n \
guraz    pts/32       129.170.90.91    Thu May 17 20:18:58 2018 - Thu May 17 21:59:49 2018  (01:40) \n \
akarki   pts/31       172.21.219.85    Thu May 17 20:18:13 2018 - Thu May 17 22:39:17 2018  (02:21) \n \
luisch   pts/30       10.31.114.223    Thu May 17 20:17:18 2018 - Thu May 17 20:31:11 2018  (00:13) \n \
guraz    pts/29       129.170.90.91    Thu May 17 20:17:16 2018 - Thu May 17 21:59:49 2018  (01:42) \n \
akarki   pts/20       172.21.219.85    Thu May 17 20:16:51 2018 - Thu May 17 22:39:17 2018  (02:22) \n \
guraz    pts/18       129.170.90.91    Thu May 17 20:16:51 2018 - Thu May 17 21:59:49 2018  (01:42) \n \
hnich    pts/27       10.31.200.63     Thu May 17 19:58:36 2018 - Thu May 17 23:47:16 2018  (03:48) \n \
elenadot pts/0        10.31.236.91     Thu May 17 19:52:23 2018 - Thu May 17 21:53:54 2018  (02:01) \n \
elenadot pts/27       10.31.236.91     Thu May 17 19:45:43 2018 - Thu May 17 19:46:24 2018  (00:00) \n \
dkern    pts/27       10.31.183.221    Thu May 17 19:43:00 2018 - Thu May 17 19:44:11 2018  (00:01) \n \
dkern    pts/27       10.31.183.221    Thu May 17 19:41:08 2018 - Thu May 17 19:42:07 2018  (00:00) \n \
luisch   pts/26       10.31.114.223    Thu May 17 19:40:48 2018 - Thu May 17 20:31:04 2018  (00:50) \n \
spark    pts/20       172.21.14.92     Thu May 17 19:40:38 2018 - Thu May 17 20:03:09 2018  (00:22) \n \
spark    pts/16       172.21.14.92     Thu May 17 19:40:11 2018 - Thu May 17 20:03:07 2018  (00:22) \n \
mdcobb   pts/15       10.31.217.14     Thu May 17 19:36:14 2018 - Thu May 17 22:40:18 2018  (03:04) \n \
gszypko  pts/8        10.31.38.38      Thu May 17 19:23:14 2018 - Thu May 17 21:41:19 2018  (02:18) \n \
roberthe pts/6        10.31.117.153    Thu May 17 19:19:50 2018 - Fri May 18 01:43:48 2018  (06:23) \n \
johnconn pts/8        10.31.208.200    Thu May 17 19:05:21 2018 - Thu May 17 19:11:50 2018  (00:06) \n \
johnconn pts/8        10.31.208.200    Thu May 17 19:03:36 2018 - Thu May 17 19:03:42 2018  (00:00) \n \
babagadi pts/4        172.21.234.68    Thu May 17 19:03:10 2018 - Thu May 17 21:38:35 2018  (02:35) \n \
dkern    pts/16       10.31.183.221    Thu May 17 18:52:36 2018 - Thu May 17 19:14:50 2018  (00:22) \n \
tongxu   pts/5        10.31.117.102    Thu May 17 18:44:26 2018 - Thu May 17 22:22:50 2018  (03:38) \n \
johnconn pts/4        10.31.208.200    Thu May 17 18:44:10 2018 - Thu May 17 18:58:23 2018  (00:14) \n \
tomyoung pts/25       129.170.212.141  Thu May 17 18:19:34 2018 - Thu May 17 18:37:17 2018  (00:17) \n \
tomyoung pts/22       129.170.212.141  Thu May 17 18:18:13 2018 - Thu May 17 18:36:59 2018  (00:18) \n \
avarma   pts/21       129.170.212.141  Thu May 17 18:10:01 2018 - Thu May 17 21:17:17 2018  (03:07) \n \
hnich    pts/2        10.31.200.63     Thu May 17 18:07:08 2018 - Thu May 17 23:47:16 2018  (05:40) \n \
hnich    pts/0        10.31.200.63     Thu May 17 18:05:57 2018 - Thu May 17 19:48:20 2018  (01:42) \n \
dmwhang  pts/0        10.31.206.43     Thu May 17 17:30:01 2018 - Thu May 17 17:50:31 2018  (00:20) \n \
hnich    pts/3        10.31.200.63     Thu May 17 17:19:25 2018 - Thu May 17 20:02:28 2018  (02:43) \n \
alexisbh pts/60       10.31.212.228    Thu May 17 17:17:25 2018 - Thu May 17 18:33:26 2018  (01:16) \n \
hnich    pts/59       10.31.200.63     Thu May 17 17:13:47 2018 - Thu May 17 20:04:27 2018  (02:50) \n \
luisch   pts/58       10.31.114.223    Thu May 17 17:13:37 2018 - Thu May 17 17:42:12 2018  (00:28) \n \
luisch   pts/45       10.31.114.223    Thu May 17 17:09:20 2018 - Thu May 17 17:11:42 2018  (00:02) \n \
luisch   pts/22       10.31.114.223    Thu May 17 17:09:10 2018 - Thu May 17 17:42:03 2018  (00:32) \n \
dmwhang  pts/54       10.31.206.43     Thu May 17 17:02:20 2018 - Thu May 17 17:58:15 2018  (00:55) \n \
ccpalmer pts/53       71.192.139.182   Thu May 17 17:01:10 2018 - Thu May 17 19:14:57 2018  (02:13) \n \
luisch   pts/45       10.31.114.223    Thu May 17 16:37:22 2018 - Thu May 17 17:07:13 2018  (00:29) \n \
blozano  pts/40       10.31.33.153     Thu May 17 16:34:41 2018 - Thu May 17 16:59:54 2018  (00:25) \n \
tongxu   pts/3        10.31.117.102    Thu May 17 16:33:36 2018 - Thu May 17 17:17:57 2018  (00:44) \n \
ss98     pts/3        10.31.114.192    Thu May 17 16:29:37 2018 - Thu May 17 16:29:55 2018  (00:00) \n \
guraz    pts/18       10.31.180.210    Thu May 17 16:22:21 2018 - Thu May 17 20:07:23 2018  (03:45) \n \
johnconn pts/19       10.31.182.138    Thu May 17 16:14:45 2018 - Thu May 17 18:27:35 2018  (02:12) \n \
stephen  pts/18       10.31.115.11     Thu May 17 16:14:08 2018 - Thu May 17 16:20:01 2018  (00:05) \n \
roberthe pts/6        10.31.117.153    Thu May 17 16:11:36 2018 - Thu May 17 19:11:27 2018  (02:59) \n \
roberthe pts/6        10.31.117.153    Thu May 17 16:09:33 2018 - Thu May 17 16:11:27 2018  (00:01) \n \
blozano  pts/3        10.31.33.153     Thu May 17 16:07:17 2018 - Thu May 17 16:25:45 2018  (00:18) \n \
blozano  pts/36       10.31.33.153     Thu May 17 15:53:49 2018 - Thu May 17 20:34:09 2018  (04:40) \n \
blozano  pts/35       10.31.33.153     Thu May 17 15:53:46 2018 - Thu May 17 20:37:58 2018  (04:44) \n \
cjacobse pts/34       10.31.239.51     Thu May 17 15:52:21 2018 - Thu May 17 20:11:45 2018  (04:19) \n \
cjacobse pts/33       10.31.239.51     Thu May 17 15:52:08 2018 - Thu May 17 20:11:45 2018  (04:19) \n \
dmwhang  pts/32       10.31.127.85     Thu May 17 15:49:27 2018 - Thu May 17 18:04:26 2018  (02:14) \n \
guraz    pts/32       10.31.180.210    Thu May 17 15:42:01 2018 - Thu May 17 15:44:14 2018  (00:02) \n \
szhu     pts/8        10.31.45.74      Thu May 17 15:41:29 2018 - Thu May 17 18:57:29 2018  (03:16) \n \
spark    pts/31       172.21.12.175    Thu May 17 15:35:31 2018 - Thu May 17 17:50:10 2018  (02:14) \n \
spark    pts/30       172.21.12.175    Thu May 17 15:35:11 2018 - Thu May 17 18:26:54 2018  (02:51) \n \
spark    pts/27       172.21.12.175    Thu May 17 15:34:57 2018 - Thu May 17 18:26:54 2018  (02:51) \n \
guraz    pts/30       10.31.180.210    Thu May 17 15:31:03 2018 - Thu May 17 15:31:10 2018  (00:00) \n \
guraz    pts/29       10.31.180.210    Thu May 17 15:30:25 2018 - Thu May 17 18:58:26 2018  (03:28) \n \
gabeboni pts/29       10.31.46.75      Thu May 17 15:26:53 2018 - Thu May 17 15:26:58 2018  (00:00) \n \
tomyoung pts/28       10.32.35.15      Thu May 17 15:25:31 2018 - Thu May 17 21:41:26 2018  (06:15) \n \
iraphael pts/27       10.31.179.55     Thu May 17 15:25:08 2018 - Thu May 17 15:31:19 2018  (00:06) \n \
luisch   pts/22       10.31.114.223    Thu May 17 15:23:08 2018 - Thu May 17 17:07:16 2018  (01:44) \n \
sburack  pts/14       10.31.204.238    Thu May 17 15:23:05 2018 - Thu May 17 18:31:16 2018  (03:08) \n \
tomyoung pts/10       10.32.35.15      Thu May 17 15:23:00 2018 - Thu May 17 21:41:26 2018  (06:18) \n"

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
