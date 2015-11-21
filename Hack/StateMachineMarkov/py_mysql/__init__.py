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

  print ""
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

  print ""
  print "#" * 44
  print "# Selecting from table ", table
  print "#" * 44
  

  #
  # 1. Send query to the table passed as arg 
  #    and get the query result object
  #
  con.query("SELECT * from " + table)
  res = con.store_result()
  print "# 2. res has type = %s" % repr(type(res))


  #
  # 2. Fetch rows from result
  #
  rows = res.fetch_row(maxrows=0, how=1)
  print "# 3. rows has type = ", repr(type(rows))

  i = 1
  for row in rows:
    print "# 3.%d row[%d] = %s" % (i, i, row)
    i = i + 1


# end of select()






#
# Function to map types to IDs
#
def map_type_2_id( con, table ):

  type_2_id = {}

  print ""
  print "#" * 44
  print "# Mapping types to IDs for table ", table
  print "#" * 44
  

  #
  # 1. Send query to the table passed as arg 
  #    and get the query result object
  #
  con.query("SELECT * from " + table)
  res = con.store_result()
  #print "# 2. res has type = %s" % repr(type(res))


  #
  # 2. Fetch rows from result
  #
  rows = res.fetch_row(maxrows=0, how=1)
  #print "# 3. rows has type = ", repr(type(rows))

  i = 1
  for row in rows:
    dic = {}
    ls = []
    print "# 3.%d row[%d] = %s" % (i, i, row)
    for k, v in row.iteritems():
      #print  (" %s =>  %s" % (k, v) )
      dic[k] = v    
    for v in dic.values():
      ls.append(v)    
    type_2_id[ls[0]] = int(ls[1])

    i = i + 1


  #print  ("## type_2_id ", type_2_id )

  return type_2_id


# end of map_type_2_id( con, table )









#
# Function to map attr name to IDs
#
def map_attr_2_id( con, table, attr ):

  name_2_id = {}

  print ""
  print "#" * 44
  print "# Mapping attr names to IDs for table ", table
  print "#" * 44
  

  #
  # 1. Send query to the table passed as arg 
  #    and get the query result object
  #
  con.query("SELECT " + attr + ", id from " + table)
  res = con.store_result()
  #print "# 2. res has type = %s" % repr(type(res))


  #
  # 2. Fetch rows from result
  #
  rows = res.fetch_row(maxrows=0, how=1)
  #print "# 3. rows has type = ", repr(type(rows))

  i = 1
  for row in rows:
    dic = {}
    ls = []
    print "# 3.%d row[%d] = %s" % (i, i, row)
    for k, v in row.iteritems():
      #print  (" %s =>  %s" % (k, v) )
      dic[k] = v    
    for v in dic.values():
      ls.append(v)    
    name_2_id[ls[0]] = int(ls[1])

    i = i + 1


  #print ("## name_2_id map: "), 
  #print (name_2_id )

  return name_2_id


# end of map_attr_2_id( con, table )











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


  columns = [ 'type_id',  'customer_id', 'goal_id', 'amount' ]

  i = 0
  for item in seq:
    print ("#  ", columns[i]),
    print ("  = ", item)
    i += 1


  # 0. Create cursor
  cur = con.cursor()



  # 1. execute: 
  #     INSERT INTO con_data VALUES('11:33:66', '{\'abx\': 33 }');
  #
 
  try: 

    # 1.a
    # insert into transactions(type_id, customer_id, goal_id, amount)  values(1, 13, 4, 12345.0);
    query = "INSERT INTO " + table + "(type_id, customer_id, goal_id, amount) VALUES(%s, %s, %s, %s);" 
    cur.execute(query, (seq[0], seq[1], seq[2], seq[3]) )


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
#    insert_xact(customer_id, 'income', self.income)
#    insert_xact(customer_id, 'expenses', self.expense)
#
def insert_xact(con, customer_id_, type, amount):

  #
  # See the comments in section 5.2 for 
  # where goal_id comes from
  #
  goal_id = 4


  # Get the mapping from trans type name to  trans type ID 
  type_id = map_type_2_id( con, "transaction_type")

  # The set of values to insert
  values = [ type_id[type], customer_id_,  goal_id,  amount ]

  # Insert
  insert( con, "transactions",  values) 







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
  # 3. Get maps
  #

  # 3.1 transaction_type[type] = id 
  type_id = map_type_2_id( con, "transaction_type")
  for k, v in type_id.iteritems():
    print  ("##  type_id[%s] =  %s" % (k, v) )


  # 3.2 goal_type[type] = id 
  goal_id = map_type_2_id( con, "goal_type")
  for k, v in goal_id.iteritems():
    print  ("##  goal_id[%s] =  %s" % (k, v) )


  # 3.3 cust_id[name] = id 
#  cust_id = map_attr_2_id( con, "customers", "name")
#  for k, v in cust_id.iteritems():
#    print  ("##  cust_id[%s] =  %s" % (k, v) )


  # 3.4 stat_id[name] = id 
  status_id = map_attr_2_id( con, "goal_status",  "status")
  for k, v in status_id.iteritems():
    print  ("##  stat_id[%s] =  %s" % (k, v) )




  #
  # 4. Get data from DB table
  # 
  #select( con, "transaction_type")



  #
  # 5. Insert into DB table
  #
  #  [
  #    trans_type = { type_id['income'], type_id['expenses'],  type_id['on_hold'] }
  #    cust_id    
  #    goal_id = { goal_id['savings'], goal_id['car'], goal_id['house'], goal_id['pension'], goal_id['consumer_product'] }
  #    amount
  #    create_time
  #  ]
  #

  #
  # 5.1 Created a default goal with id = 4 of type 5 (savings) and status 4 (amber)
  #
  #      type_id     = 5 # savings goal
  #      customer_id = 1
  #      type_id     = 4 # amber goal status
  #            
  #
  #     mysql> insert into goals(type_id, customer_id, status_id) values(5, 1, 4);
  #     Query OK, 1 row affected, 1 warning (0.01 sec)
  #
  #
  #     mysql> select * from goals where customer_id = 1;
  #     +----+---------+-------------+-----------+--------+---------------------+---------------------+---------------------+
  #     | id | type_id | customer_id | status_id | amount | start_time          | end_time            | created_time        |
  #     +----+---------+-------------+-----------+--------+---------------------+---------------------+---------------------+
  #     |  4 |       5 |           1 |         4 |      0 | 0000-00-00 00:00:00 | 0000-00-00 00:00:00 | 2015-11-20 23:44:37 |
  #     +----+---------+-------------+-----------+--------+---------------------+---------------------+---------------------+
  #     1 row in set (0.00 sec)
  #
  #
  #
  # 5.2 Use the default goal to insert into transactions tabls
  #
  #     mysql> insert into transactions(type_id, customer_id, goal_id, amount)  values(1, 13, 4, 12345.0);
  #     Query OK, 1 row affected (0.01 sec)
  #
  #     mysql> select * from transactions where customer_id = 13;
  #     +----+---------+-------------+---------+--------+---------------------+
  #     | id | type_id | customer_id | goal_id | amount | created_time        |
  #     +----+---------+-------------+---------+--------+---------------------+
  #     |  4 |       1 |          13 |       4 |  12345 | 2015-11-20 23:57:33 |
  #     +----+---------+-------------+---------+--------+---------------------+
  #     1 row in set (0.00 sec)
  #


  #     mysql> insert into transactions(type_id, customer_id, goal_id, amount)  values(1, 13, 4, 12345.0);

  #insert( con, "transactions", [ '1234567890', '11:33:66', "{'abx': 33}" ] ) 

  #customer_id = 13
  goal_id = 4
  # type
  values = [ type_id['income'], customer_id,  goal_id, 2222.13 ]
  insert( con, "transactions",  values) 



  #
  # 6. Close connection
  #
  con.close()







