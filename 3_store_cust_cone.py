import os, sys, MySQLdb
from datetime import datetime, timedelta
import time
import datetime as dt


db = MySQLdb.connect(host="192.168.2.5",
                     user="hackaton",
                     passwd="password",
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
        elmt =   str(k_year)  + str(k_month) + '01'
    else:
        elmt =   str(k_year) + '0' + str(k_month) + '01'
    #print comb
    #List_possibilities.append(int(comb)
    if k_month == 12:
        k_month = 1
        k_year +=1
    elif k_month<12:
        k_month +=1

    #print elmt

    if elmt not in list_treated_files:
        output = ['.ppdc-ases.txt.gz']
        current_timestamp = int(elmt)
        print current_timestamp
        #sys.exit()
        
        for ext in output:
            
            #Select data from the as-relationship
            sql_command = """select AS1, Customer from CustomerCone where enddate is NULL and IPversion = 4;"""
            cur.execute(sql_command)
            stored_AS_customer_relationships = cur.fetchall()
            #
    
            stored_AS_customer_relationships_list = []
            for link in stored_AS_customer_relationships:
                item = str(link[0]) + '__'  + str(link[1]) 
                print item
                stored_AS_customer_relationships_list.append(item)
                #print stored_AS_customer_relationships
            time.sleep(10)
            print 'I am parsing ', elmt + ext
            current = elmt + ext
            file = 'data.caida.org/datasets/as-relationships/serial-1/' + current
            
            print current_timestamp
            
            ## dezip file
            try:
                command = 'gzip -d  ' + file
                os.system(command)
            except:
                print 'no need to dezip'
            
            if os.path.isfile(file[:-3]):
                with open (file[:-3], 'r') as fh:
                    for line1 in fh:
                        print line1
                        if not line1.startswith("#"):
                            tokens = line1.split()
                            as1 = tokens[0]
                            customers = tokens[1:]
                            for cust in customers:
                                tuple = str(as1) + '__' + str(cust)
                                if tuple not in stored_AS_customer_relationships_list:
                                    sql_command = """ INSERT IGNORE INTO CustomerCone (IPversion,  AS1,  Customer, startdate) VALUES (%s, %s, %s, %s); """
                                    cur.execute(sql_command, (4, as1, cust, current_timestamp))
                                    db.commit()
                                else:
                                     stored_AS_customer_relationships_list.remove(tuple)

                    for couple in stored_AS_customer_relationships_list:
                        sql_command = """ UPDATE CustomerCone set enddate = %s where IPversion = %s and AS1 = %s and Customer = %s and enddate is NULL  ; """
                        print couple
                        tab1 = couple.split('__')
                        print 'update for ', couple, tab1[0], tab1[1]
                        cur.execute(sql_command, ( current_timestamp, 4, int(tab1[0]), int(tab1[1])))
                        db.commit()

    else:
            print 'do not treat ', elmt + ext



#sys.exit()









#sql_command = """ INSERT IGNORE INTO Treated_url (url_to_folder, folder_only, parsing_status) VALUES (%s, %s, %s); """
#cur.execute(sql_command, (url_to_insert, folder_only, 'Notyet'))
#db.commit()


