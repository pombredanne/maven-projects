#!/usr/bin/python

#
# This is the package py_mysql, which can be used with
#
#   import py_mysql
#
# and provides the functions
#
#  get_connection( database )
#  select( con, table )
#  insert( con, table, seq )
#
# Author: Gabriel Mateescu
#

import sys, os
import MySQLdb



#
# Function to get connection
#
def get_connection(server, database ):

  #
  # 1. Connect to MySQL server
  #

  #
  # 1.1 Using _mysql 
  #
  #db = _mysql.connect(host="172.16.0.82", passwd="none", read_default_file="~/.my.cnf", db="one_ng")
  #db = _mysql.connect(host="172.16.0.82", user="root", read_default_file="~/.my.cnf", db="one_ng")

  print "#" * 72
  print "# Connecting to database ", database, "on server ", server
  print "#" * 72


  #
  # 1.2 Using MySQLdb  
  #
  db = MySQLdb.connect(host=server, read_default_file="/etc/my.cnf", db=database)
  print repr(type(db))


  # 1.3 Return connection
  return db

# get_connection()



#
# Function to query a table in a MySQL database
#
def select( con, table ):

  print "#" * 44
  print "# Selecting from table ", table
  print "#" * 44
  
  #
  # 2. Send query to the table passed as arg 
  #    and get the query result object
  #
  con.query("SELECT * from " + table)
  res = con.store_result()
  print "# 2. res has type = %s" % repr(type(res))


  #
  # 3. Fetch rows from result
  #
  rows = res.fetch_row(maxrows=0, how=1)
  print "# 3. rows has type = ", repr(type(rows))

  i = 1
  for row in rows:
    print "# 3.%d row[%d] = %s" % (i, i, row)
    i = i + 1


# end of select()





#
# Function to insert into a table from a MySQL database
#
def insert( con, table, seq ):
  
  #
  # 4. Perform insert of the data in seq into the table passed as arg 
  #

  print ""
  print "#" * 44
  print "# Inserting in table ", table, " the values:"
  print "#" * 44

  for item in seq:
    print "#  ", item


  # 0. Create cursor
  cur = con.cursor()



  # 1. execute: 
  #     INSERT INTO con_data VALUES('11:33:66', '{\'abx\': 33 }');
  #

 
  try: 
    # 1.a
    query = "INSERT INTO " + table + " VALUES(%s, %s, %s);" 
    cur.execute(query, (seq[0], seq[1], seq[2]) )

    # 1.b
    #cur.execute("INSERT INTO " + table + "(label, json) VALUES(%s, %s, %s)", seq )

    # 2. execute 
    #     INSERT INTO con_data(label, json) VALUES("abcdef", "11:33:66", "{ 'abx': 33 }");

    # 2.a
    #query = ( 
    #          "INSERT INTO " + table + "(label, json) VALUES(\"%s\", \"%s\", \"%s\");" %  
    #          (seq[0], seq[1], seq[2]) 
    #        ) 
    #cur.execute(query)


    # 2.b
    #query = "INSERT INTO " + table + "(hash, label, json) VALUES(\"" + seq[0] + "\", \"" + seq[1] + "\", \"" + seq[2] + "\" );" 
    #print "query = ", query
    #cur.execute(query)

    #print "Auto Increment ID: %s" % cur.lastrowid
    print "Executed: %s" % cur._last_executed
    print "Result: %s"   % cur._result


    # Close cursor
    cur.close()

    # Commit insert
    con.commit()


  except MySQLdb.IntegrityError as err:
    print( "##\n## Error: {}".format(err) )
    print("##")   
    pass


# end of insert()







#
# Get the DBs
#
def get_db_list( con ):


  print ""
  print "#" * 44
  print "# Show databases:"
  print "#" * 44


  #  try: 

  con.query("SHOW DATABASES;")
  res = con.store_result()


  rows = res.fetch_row(maxrows=0, how=1)
  i = 1
  for row in rows:
    print "# 3.%d row[%d] = %s" % (i, i, row)
    i = i + 1



  #except MySQLdb.IntegrityError as err:
  #    print( "##\n## Error: {}".format(err) )
  #    print("##")   
  #    pass

# end of get_db_list()






#
# Main program
#

# If this program is run directly by the python interpr,
# then 
#  __name__ = "__main__"
# 
# otherwise __name__ is the name of the module, i.e., 
#
#  __name__ = "py_mysql"
# 
#print "name = %s " % __name__

if __name__ == "__main__":

  #
  # 1. Get connection
  #
  con = get_connection( "172.16.0.82", "one_ng")


  #
  # 2. Get list of DBs
  #
  get_db_list( con )



  #
  # 3. Get data from DB table
  # 
  select( con, "transaction_type")



  #
  # 4. Insert into DB table
  # 
  #insert( con, "con_data", [ '1234567890', '11:33:66', "{'abx': 33}" ] )

  
  #
  # 4. Close connection
  #
  con.close()



