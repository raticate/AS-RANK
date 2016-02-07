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



#print List_possibilities


#Select data from the as-relationship
sql_command = """select AS1, AS2, relation from ASRelationships where enddate is NULL and IPversion = 4;"""
cur.execute(sql_command)
stored_AS_relationships = cur.fetchall()
#print "stored_AS_relationships = ", stored_AS_relationships

#for elmt in stored_AS_relationships:




stored_AS_relationships_list = []
for link in stored_AS_relationships:
    print str(link[0]) + '__'  + str(link[1]) + '__' + str(link[2])
    stored_AS_relationships_list.append(str(link[0]) + '__'  + str(link[1]) + '__' + str(link[2]))
#print stored_AS_relationships




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
        #output = ['.as-rel.txt.gz', '.ppdc-ases.txt.gz']
        output = ['.as-rel.txt.gz']
        
        
        current_timestamp = int(elmt)
        print current_timestamp
        #sys.exit()
        
        for ext in output:
            
            #Select data from the as-relationship
            sql_command = """select AS1, AS2, relation from ASRelationships where enddate is NULL and IPversion = 4;"""
            cur.execute(sql_command)
            stored_AS_relationships = cur.fetchall()
            #
    
            stored_AS_relationships_list = []
            for link in stored_AS_relationships:
                print str(link[0]) + '__'  + str(link[1]) + '__' + str(link[2])
                stored_AS_relationships_list.append(str(link[0]) + '__'  + str(link[1]) + '__' + str(link[2]))
                #print stored_AS_relationships
        
        
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
                        tab = line1.split('|')
                        if len(tab) == 3:
                            if str(link[0]) + '__'  + str(link[1]) + '__' + str(link[2]) not in stored_AS_relationships_list:
                                sql_command = """ INSERT IGNORE INTO ASRelationships (IPversion,  AS1,  AS2, relation, startdate) VALUES (%s, %s, %s, %s, %s); """
                                cur.execute(sql_command, (4, int(tab[0]), int(tab[1]), int(tab[2]), current_timestamp   ))
                                db.commit()
                            else:
                                stored_AS_relationships_list.remove(str(link[0]) + '__'  + str(link[1]) + '__' + str(link[2]))


                    for couple in stored_AS_relationships_list:
                        sql_command = """ UPDATE ASRelationships set enddate = %s where IPversion = %s and AS1 = %s and AS2 = %s and relation = %s and enddate is NULL  ; """
                        print couple
                        tab1 = couple.split('__')
                        print 'update for ', couple, tab[0], tab[1], tab[2]
                        cur.execute(sql_command, ( current_timestamp, 4, int(tab[0]), int(tab[1]),  int(tab[2])))
                        db.commit()


        #sys.exit()


        #sys.exit()
        ## after treatment put it into the file
            
        # with open('list_of_treated_files.txt', 'a') as fh:
        #fh.write('%s \n' %(elmt+ext))

    else:
            print 'do not treat ', elmt + ext



#sys.exit()









#sql_command = """ INSERT IGNORE INTO Treated_url (url_to_folder, folder_only, parsing_status) VALUES (%s, %s, %s); """
#cur.execute(sql_command, (url_to_insert, folder_only, 'Notyet'))
#db.commit()


