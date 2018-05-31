# Created by: Brenda Miao
# Modified by:
#
# Description: This script will be invoked on a server to gather more specific information about which users are logged in.
#
# Intended usage of this script:
# This script will take in a .csv file generated from the raw_audit_script.py and perform the following functions:
# - Prompts users to choose what kind of data they want to output. 
#     - Output data in specified monthly time range (does not include users who are still logged in)
# - Gets rid of duplicate entries (ie, where multiple rows have ALL the exact same column values)
# - Creates a new csv file containing the requested information

import socket
import os
import datetime
import subprocess
import sys
import pandas as pd

########### VALIDATING STRING FORMATS ###########

def is_valid_weekday(day):
    return day == "Mon" or day == "Tue" or day == "Wed" or day == "Thu" or day == "Fri" or day == "Sat" or day == "Sun"

def is_valid_month(month):
    return month == "Jan" or month == "Feb" or month == "Mar" or month == "Apr" or month == "May" or month == "Jun" or \
           month == "Jul" or month == "Aug" or month == "Sep" or month == "Oct" or month == "Nov" or month == "Dec"

def month_to_num(month):
    return ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(month)

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
###### server_name = socket.gethostname()

# Open raw file 
if os.path.exists("audit_raw.csv"):

    #open raw data file to read
    df = pd.read_csv("audit_raw.csv")
    df_clean = df.drop_duplicates()

    #prompts user for type of data to extract
    selection = raw_input("Enter 'a' for all data or 'd' to get data from specific months: ")

    #write all data to csv
    if selection == "a":
        df_clean.to_csv('audit-clean_all-data.csv')

    #write only data from a specific time range
    elif selection == "d":
        #prompts user for monthly time range for data output. 
        start = raw_input("Enter starting month (3 letters) and year: ").split(" ")

        #check correct input for start month and year
        while(not len(start) == 2 or not is_valid_month(start[0]) or not is_valid_year(start[1])):
            start = raw_input("Invalid Input. Enter starting month (3 letters) and year: ").split(" ")

        startMonth = month_to_num(start[0])
        startYear = int(start[1])

        end = raw_input("Enter end month (3 letters) and year: ").split(" ")
        
        #check correct input for end month and year
        while(not len(start) == 2 or not is_valid_month(end[0]) or not is_valid_year(end[1])):
            end = raw_input("Invalid Input. Enter starting month (3 letters) and year: ").split(" ")
            
        endMonth = month_to_num(end[0])
        endYear = int(end[1])


        #remove unneeded values
        row_curr = 0
        df2_clean = df_clean
        for row in df.itertuples():
            if int(row[6]) < startYear or int(row[6]) > endYear:
                df2_clean = df2_clean.drop(row_curr)
            elif month_to_num(row[4]) < startMonth or month_to_num(row[4]) > endMonth:
                df2_clean = df2_clean.drop(row_curr)
            row_curr = row_curr + 1

        #create new file to write cleaned data to
        df2_clean.to_csv('audit-clean_'+start[0]+str(startYear)+'_'+end[0]+str(endYear)+'.csv')

else:
    sys.stdout.write("Run raw_audit_script.py to obtain raw data before running this script")

sys.stdout.write("Done")