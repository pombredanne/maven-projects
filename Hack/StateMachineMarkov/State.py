#
# An abstract State class: has the run() operation, 
# and can be moved into the next State 
#

class State:

  def __init__(self, dob_ = 197010, date_ = 0):
    print("# Make person: dob=%i  date=%i" %  (dob_, date_))
    self.dob = dob_
    if date_ == 0:
      self.date = self.dob
    else:
      self.date = date_
    self.income = 0
    self.expense = 0


  def __call__(self, info_):
    print("#   state set date: date=%i" % info_['date'])
    self.date = info_['date']
    self.income = info_['income']
    self.expense = info_['expense']
    return self



  # implemented by subclasses
  def run(self):
    assert 0, "run not implemented"

  # implemented by subclasses
  def next(self, input):
    assert 0, "next not implemented"




