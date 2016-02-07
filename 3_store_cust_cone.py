import os, sys, MySQLdb
from datetime import datetime, timedelta
import time
import datetime as dt

db = MySQLdb.connect(host="localhost",
                     user="hackaton",
                     passwd="password",
                     db="ASRank")

cur = db.cursor()

def process_file(date):
    extension = '.ppdc-ases.txt.gz'
    current_timestamp = int(date)

	# querie actual relationships
    sql_command = """select AS1, Customer from CustomerCone where enddate is NULL and IPversion = 4;"""
    cur.execute(sql_command)
    stored_AS_customer_relationships = cur.fetchall()

    # make tuple list
    stored_AS_customer_relationships_list = []
    for row in stored_AS_customer_relationships:
        item = (row[0], row[1])
        stored_AS_customer_relationships_list.append(item)
 

    print 'I am parsing ', date + extension
    current = date + extension
    file = 'data.caida.org/datasets/as-relationships/serial-1/' + current
    
    ## dezip file
    try:
        command = 'gzip -d  ' + file
        os.system(command)
    except:
        print 'no need to dezip'


    if os.path.isfile(file[:-3]):
    	#open file, read each line
        with open (file[:-3], 'r') as fh:
            for line1 in fh:
            	# skip headers
            	if not line1.startswith("#"):
            		# split line to obtain as and customers
                    tokens = line1.split()
                    as1 = tokens[0]
                    customers = tokens[1:]
                    print as1
                    #iterate customers
                    print "iterating customers..."
                    if(as1 != 1 and as1!= 3320):
                        for cust in customers:
                            tuple = (as1, cust)
                            # tuple not in the database, add it with file timestamp
                            if tuple not in stored_AS_customer_relationships_list:
                                sql_command = """ INSERT IGNORE INTO CustomerCone (IPversion,  AS1,  Customer, startdate) VALUES (%s, %s, %s, %s); """
                                cur.execute(sql_command, (4, as1, cust, current_timestamp))
                                db.commit()
                            # tuple is in the file and the db, unmark in from db to get rows in the db that are not in the file
                            else:
                                 stored_AS_customer_relationships_list.remove(tuple)

        # iterate remaining db rows, update their enddate
        print "updating remaining db rows..."
    	for row in stored_AS_customer_relationships_list:
            sql_command = """ UPDATE CustomerCone set enddate = %s where IPversion = %s and AS1 = %s Customer = %s and enddate is NULL  ; """
            print 'update for ', row[0], row1[1]
            cur.execute(sql_command, (current_timestamp, 4, int(row[0]), int(row[1])))
            db.commit()

    else:
    	print file[:-3]


#process_file('20041001')
process_file('20041101')

