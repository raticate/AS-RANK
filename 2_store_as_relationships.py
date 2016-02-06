import os, sys, MySQLdb
from datetime import datetime, timedelta
import time
import datetime as dt


db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="edjrosse07",
                     db="ASRank")

cur = db.cursor()




link = """data.caida.org/datasets/as-relationships/"""
print link

## download all the relationship and store it
command = """wget --no-parent -r """ +link
print '\n download list of files :', command
#os.system(command)


## Load the list of files treated:
list_treated_files = []
with open('list_of_treated_files.txt', 'r') as fg:
    for line in fg:
        line= str(line).strip()
        if line not in list_treated_files:
            list_treated_files.append(line)



A = str(datetime.now() + timedelta(days=-1))
table = A.split(' ')
date_info = table[0].split('-')
date_info_end = [int(date_info[0]), int(date_info[1]) ]
#print date_info_end
date_info_start = [1998, 01]

k_year = date_info_start[0]
k_month = date_info_start[1]


List_possibilities = []
while (k_year <= date_info_end[0]) :
    if k_month >9:
        comb =   str(k_year)  + str(k_month) + '01'
    else:
        comb =   str(k_year) + '0' + str(k_month) + '01'
    #print comb
    List_possibilities.append(comb)
    if k_month == 12:
        k_month = 1
        k_year +=1
    elif k_month<12:
        k_month +=1

#print List_possibilities


#Select data from the as-relationship
sql_command = """select AS1, AS2, startdate from ASRelationships where enddate is NULL and IPversion = 4;"""
cur.execute(sql_command)
stored_AS_relationships = cur.fetchall()

print stored_AS_relationships



for elmt in List_possibilities:
    if elmt not in list_treated_files:
        #output = ['.as-rel.txt.gz', '.ppdc-ases.txt.gz']
        output = ['.as-rel.txt.gz']
        
        year = elmt[:4]
        month = elmt[4:6]
        day = elmt[6:]
        current_date = day+'/'+month+'/'+year
        
        for ext in output:
            print 'treat ', elmt + ext
            current = elmt + ext
            file = 'data.caida.org/datasets/as-relationships/serial-1/' + current
            current_timestamp = time.mktime(dt.datetime.strptime(current_date, "%d/%m/%Y").timetuple())
            print current_timestamp
            sys.exit()
            ## dezip file
            try:
                command = 'gzip -d  ' + file
                os.system(command)
            except:
                print 'no need to dezip'
            
            with open (file[:-3], 'r') as fh:
                for line1 in fh:
                    print line1



            print date, month, day


            

        sys.exit()

    else:
            print 'do not treat ', elmt + ext
            ## after treatment put it into the file

            # with open('list_of_treated_files.txt', 'a') as fh:
                #fh.write('%s \n' %(elmt+ext))


#sys.exit()









#sql_command = """ INSERT IGNORE INTO Treated_url (url_to_folder, folder_only, parsing_status) VALUES (%s, %s, %s); """
#cur.execute(sql_command, (url_to_insert, folder_only, 'Notyet'))
#db.commit()


