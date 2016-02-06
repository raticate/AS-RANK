import time
import datetime

import _mysql
import sys

try:
    con = _mysql.connect('132.249.65.124', 'hackaton', 'password', 'asrank')
        
    con.query("SELECT VERSION()")
    result = con.use_result()
    
    print "MySQL version: %s" % \
        result.fetch_row()[0]

	#file_name = "20160101.ppdc-ases.txt-1"
	#f = open(file_name, "r")
	#d = file_name.split(".")[0]
	#file_ts = time.mktime(datetime.datetime.strptime(d, "%Y%m%d").timetuple())
	#for line in f:
	 #       token_list = line.split()
	  #      if token_list[0] != '#':
	   #     	as1 = token_list[0]
	    #    	cust_list = token_list[1:]


    
except _mysql.Error, e:
  
    print "Error %d: %s" % (e.args[0], e.args[1])
    sys.exit(1)

finally:
    
    if con:
        con.close()



