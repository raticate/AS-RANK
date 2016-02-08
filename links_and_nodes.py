import os, sys, MySQLdb
from datetime import datetime, timedelta
import time
import datetime as dt


## All infos about all ASes
db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="ASRank")
db.autocommit(False)
cur = db.cursor()

#Select data from the as-relationship
sql_command = """select distinct AS1, AS2 from ASRelationships;"""
cur.execute(sql_command)
stored_AS_relationships = cur.fetchall()
print stored_AS_relationships


with open('list_ASes.txt', 'a') as fg:
    fg.write('%s \n'%('begin'))
    fg.write('%s \n'%('asnumber'))
    fg.write('%s \n'%('asname'))
    fg.write('%s \n'%('registry'))


stored_AS_relationships_list = []
for couple in stored_AS_relationships:
    
    if couple[0] not in stored_AS_relationships_list:
        stored_AS_relationships_list.append(couple[0])
        with open('list_ASes.txt', 'a') as fg:
            fg.write('%s \n'%('AS'+str(couple[0]).strip()))
    
    if couple[1] not in stored_AS_relationships_list:
        stored_AS_relationships_list.append(couple[1])
        with open('list_ASes.txt', 'a') as fg:
            fg.write('%s \n'%('AS'+str(couple[1]).strip()))


with open('list_ASes.txt', 'a') as fg:
    fg.write('%s \n'%('end'))



command = """ netcat whois.cymru.com 43 < """ + 'list_ASes.txt' + """ | sort -n >  output_tc.txt"""
os.system(command)


#if 1:
try:
    with open('output_tc.txt', 'r') as fggg:
        for line in fggg:
            if 'Bulk mode; whois.cymru.com' not in line:
                line = line.strip()
                tab = line.split('|')
		print line, tab
                sql_command = """ INSERT IGNORE INTO ASInfo (AS1, region , organization) VALUES (%s, %s, %s); """
                cur.execute(sql_command, ( str(tab[0]).strip(), str(tab[1]).strip(), str(tab[2]).strip()  ))
        db.commit()
                        
except:
        db.rollback()
