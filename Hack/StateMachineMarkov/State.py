#
# An abstract State class: has the run() operation, 
# and can be moved into the next State 
#

import random

class State:
  def __init__(self,  info_ = {'dob':197010,'date':0, 'income':0, 'expense':0}):
    date_ = info_['date']
    dob_ = info_['dob']
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



  # implemented by subclasses
  def run(self):
    assert 0, "run not implemented"

  # implemented by subclasses
  def next(self, input):
    assert 0, "next not implemented"






