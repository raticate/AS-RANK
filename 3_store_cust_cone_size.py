import os, sys, MySQLdb
from datetime import datetime, timedelta
import time
import datetime as dt

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="ASRank")

cur = db.cursor()

def process_file(date, ext):
    current_timestamp = int(date)
 
    print 'I am parsing ', date + ext
    current = date + ext
    file = 'data.caida.org/datasets/as-relationships/serial-1/' + current
    check = "alert.txt"
    ## dezip file
    try:
        if  '.ppdc-ases.txt.gz' in file and os.path.isfile(file):
            command = 'gzip -d  ' + file
            check = file[:-3]
            os.system(command)
    
        elif '.ppdc-ases.txt.bz2' in file and os.path.isfile(file) :
            command = 'bunzip2  ' + file
            check = file[:-4]
            os.system(command)

    except:
        print 'no need to dezip'


    if os.path.isfile(check):
        #open file, read each line
        with open (check, 'r') as fh:
            for line1 in fh:
                # skip headers
                if not line1.startswith("#"):
                    # split line to obtain as and customers
                    tokens = line1.split()
                    as1 = tokens[0]
                    customers = tokens[1:]
                    print as1
                    
                    sql_command = """ INSERT IGNORE INTO CustomerConeSize (IPversion,  AS1,  Size, startdate) VALUES (%s, %s, %s, %s); """
                    cur.execute(sql_command, (4, as1, len(customers), current_timestamp))
                    db.commit()

    else:
        print "didn't find", check

## function ends


## download all the relationship if needed
link = """data.caida.org/datasets/as-relationships/"""
command = """wget --no-parent -r """ +link
print '\n download list of files :', command
os.system(command)


## Load the list of treated files :
list_treated_files = []
try:
    with open('list_of_treated_files_rel3.txt', 'r') as fg:
        for line in fg:
            line= str(line).strip()
            if line not in list_treated_files:
                list_treated_files.append(str(line).strip())
except:
    with open('list_of_treated_files_rel3.txt', 'a') as fk:
        print



## Current date
A = str(datetime.now() + timedelta(days=-1))
table = A.split(' ')
date_info = table[0].split('-')
date_info_end = [int(date_info[0]), int(date_info[1]) ]
#print date_info_end
date_info_start = [1998, 01]

k_year = date_info_start[0]
k_month = date_info_start[1]




while (k_year <= date_info_end[0]) :
    if k_month >9:
        elmt =   str(k_year)  + str(k_month) + '01'
    else:
        elmt =   str(k_year) + '0' + str(k_month) + '01'

    if k_month == 12:
        k_month = 1
        k_year +=1
    elif k_month<12:
        k_month +=1


    #output = ['.as-rel.txt.gz', '.ppdc-ases.txt.gz']
    output = ['.ppdc-ases.txt.gz', '.ppdc-ases.txt.bz2']
    for ext in output:
        current = elmt + ext
        if  str(current).strip() not in list_treated_files:
            process_file(elmt, ext)
            with open('list_of_treated_files_rel3.txt', 'a') as fh:
                fh.write('%s \n' %(elmt+ext))

        else:
            print 'do not treat ', elmt + ext


