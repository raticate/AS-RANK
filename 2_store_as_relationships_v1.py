import os, sys, MySQLdb
from datetime import datetime, timedelta
import time
import datetime as dt

db = MySQLdb.connect(host="localhost", user="root", passwd="edjrosse07", db="ASRank")
db.autocommit(False)
cur = db.cursor()


## download all the relationship if needed
link = """data.caida.org/datasets/as-relationships/"""
command = """wget --no-parent -r """ +link
print '\n download list of files :', command
#os.system(command)


## Load the list of treated files :
list_treated_files = []
try:
    with open('list_of_treated_files_rel.txt', 'r') as fg:
        for line in fg:
            line= str(line).strip()
            if line not in list_treated_files:
                list_treated_files.append(str(line).strip())
except:
    with open('list_of_treated_files_rel.txt', 'a') as fk:
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
    output = ['.as-rel.txt.gz', '.as-rel.txt.bz2']
    for ext in output:
        current = elmt + ext
        if  str(current).strip() not in list_treated_files:
                print
                current_timestamp = int(elmt)
                print current_timestamp
                
                #Select data from the as-relationship
                sql_command = """select AS1, AS2, relation from ASRelationships where enddate is NULL and IPversion = 4;"""
                cur.execute(sql_command)
                stored_AS_relationships = cur.fetchall()
                
                stored_AS_relationships_list = []
                for link in stored_AS_relationships:
                    stored_AS_relationships_list.append(str(link[0]).strip() + '|'  + str(link[1]).strip() + '|' + str(link[2]).strip())
                    #print stored_AS_relationships
            
                print 'len_before_sup = ', len(stored_AS_relationships_list) #, stored_AS_relationships_list
                time.sleep(10)
                print 'I am parsing ', current
                
                file = 'data.caida.org/datasets/as-relationships/serial-1/' + current
                
                print 'current_date =', current_timestamp
                
                ## dezip file
                try:
                    if  '.as-rel.txt.gz' in file and os.path.isfile(file):
                        command = 'gzip -d  ' + file
                        os.system(command)
                
                    elif '.as-rel.txt.bz2' in file and os.path.isfile(file) :
                        command = 'bunzip2  ' + file
                        os.system(command)

                except:
                    print 'no need to dezip'


                if os.path.isfile(file[:-3]):
                    with open (file[:-3], 'r') as fh:
                        try:
                            for line1 in fh:
                                #print line1
                                tab = line1.split('|')
                                if len(tab) == 3:
                                    test_vc = str(tab[0]).strip() + '|'  + str(tab[1]).strip() + '|' + str(tab[2]).strip()
                                    if test_vc not in stored_AS_relationships_list:
                                        sql_command = """ INSERT IGNORE INTO ASRelationships (IPversion,  AS1,  AS2, relation, startdate) VALUES (%s, %s, %s, %s, %s); """
                                        cur.execute(sql_command, (4, int(tab[0]), int(tab[1]), int(tab[2]), current_timestamp   ))
                                        #db.commit()
                                        
                                    elif test_vc in stored_AS_relationships_list:
                                        print 'I found it so I suppressed ', test_vc
                                        stored_AS_relationships_list.remove(test_vc)

                            print 'len_after_sup = ', len(stored_AS_relationships_list) #, stored_AS_relationships_list


                            for couple in stored_AS_relationships_list:
                                sql_command = """ UPDATE ASRelationships set enddate = %s where IPversion = %s and AS1 = %s and AS2 = %s and relation = %s and enddate is NULL; """
                                print couple
                                tab1 = couple.split('|')
                                print 'update for ', couple, tab1[0], tab1[1], tab1[2]
                                cur.execute(sql_command, (current_timestamp, 4, int(tab1[0]), int(tab1[1]),  int(tab1[2])))
                                #db.commit()
                                
                            ## after treatment put it into the list of treated file
                            with open('list_of_treated_files.txt', 'a') as fh:
                                fh.write('%s \n' %(elmt+ext))

                            db.commit()
                                
                        except:
                            db.rollback()
                else:
                    print 'file ', file, ' not found in the folder; we pass '



        else:
                print 'do not treat ', elmt + ext




