#
# An abstract State class: has the run() operation, 
# and can be moved into the next State 
#

import random
import py_mysql

class State:


  def __init__(self,  info_ = {'dob':197010, 'date':0, 'income':0, 'expense':0,  'con': 'dummy' }):
    date_    = info_['date']
    dob_     = info_['dob']
    self.con = info_['con']
    #print("# Make person: dob  = ", dob_)
    #print("# Make person: date = ", date_)
    print("# Make person: dob=%i  date=%i" %  (dob_, date_))
    self.dob = dob_
    if date_ == 0:
      self.date = self.dob
    else:
      self.date = date_
    self.income = info_['income']
    self.expense = info_['expense']
    self.alive = True


  def __call__(self, info_):
    #print("#   state set date: date=%i" % info_['date'])
    self.date = info_['date']
    self.income = info_['income']
    self.expense = info_['expense']
    self.alive = info_['alive']
    return self



  def run(self, customer_id_):

    print("# Start run: dob = %i" % self.dob)
    self.customer_id = customer_id_ 

    # Make a transaction    
    #   customer_id
    #   type is 'income' or 'expenses'
    #   amount

    if ( self.income > 0):
      py_mysql.insert_xact(self.con, self.customer_id, 'income',  self.income)

    if ( self.expense > 0):
      py_mysql.insert_xact(self.con, self.customer_id, 'expenses', self.expense)


    #(type, [(values, horizons)], prob)
    goals[('car',[(2000, 6), (8000, 4*12), (15000, 6*12), (25000, 10*12), (50000, 15*12)], 1.0/(12*10)) , ('house' ,[(100000, 10*12), (200000, 15*12), (400000, 25*12), (500000, 30*12)]), ('consumer_goods', [(500, 1), (1000, 3), (2000, 6), (3000, 12), (5000, 24)], 1.0/12)]
    
    dice = random.uniform(0,1)
    for g in goals:
      if dice < g[2]:
        random.shuffle(g[1])
        expense = g[1][0]
        typ = g[0]
        amount = expense[0]
        horizon = expense[1]
        if  amount < self.income * horizon /0.7 
          #make transaction
          #make goal
          pass
          break


  # implemented by subclasses
  def next(self, input):
    assert 0, "next not implemented"






