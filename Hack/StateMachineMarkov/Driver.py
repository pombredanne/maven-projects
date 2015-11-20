import random
import string, sys

sys.path += ['./stateMachine', './actions']

from State        import State
from StateMachine import StateMachine


turn18 = 2
turn25 = 3
turn65 = 18



#
# Check if the age of a person 
# has reached the age threshold
#
def check_age (dob, date, age):

  m1 = 12 * (date / 100) + date % 100
  m0 = 12 * (dob / 100)  + dob % 100

  months = m1 - m0
  #print("# months = %i" % months)

  years = months/12
  #print("# years = %i" % years)

  if ( years - age ) >= 0:
    return 1
  else:
    return 0






#
# 1. The possible states of the driver are 
#    subclasses os State, with a subclass 
#    for each possible state
#

class Kid(State):

  def run(self):
    #print("# Run kid:")
    pass


  def next(self, date):

    print("# Kid next state: dob = %i" % self.dob)

    #
    # Check for time-events
    #

    res = check_age(self.dob, date, turn65)
    if res:
      print("#   graduate to retired")
      return Driver.retired(date)

    res = check_age(self.dob, date, turn25)
    if res:
      print("#   graduate to employed or unemployed")
      return Driver.employed(date) 

    res = check_age(self.dob, date, turn18)
    if res:
      print("#   graduate to student")
      return Driver.student(date) 



    # no state change
    print("#   no state change")
    return Driver.kid(date)



class Student(State):

  p_drop = 0.2

  def run(self):
    #print("# Run Student")
    pass


  def next(self, date):

    print("# Student next state: dob = %i" % self.dob)

    #
    # Check for time-events
    #
    
    res = check_age(self.dob, date, turn25)
    if res:
      print("#   graduate to employed or unemployed")
      return Driver.employed(date) 



    #
    # Check for prob events
    #

    # drops out
    dice = random.uniform(0,1)
    if dice < self.p_drop:
      return Driver.unemployed(date)

    # no state change
    print("#   no state change")
    return Driver.student(date)



class Employed(State):


    p_fired = 0.3


    def run(self):
      #print("# Run employed: ")
      pass


    def next(self, date):

      print("# Employed next state: dob = %i" % self.dob)

      #
      # Check for time-events
      # 
      res = check_age(self.dob, date, turn65)
      if res:
        print("#   graduate to retired")
        return Driver.retired(date)


      #
      # Check for prob events
      #

      # fired
      dice = random.uniform(0,1)
      if dice < self.p_fired:
        return Driver.unemployed(date)


      #if action == Action.fired:
      #    return Driver.unemployed

      # no state change
      print("#   no state change")
      return Driver.employed(date)



class Unemployed(State):

    def run(self):
      #print("# Run unemployed: ")
      pass
 

    def next(self, date):

      print("# Unemployed next statexs: dob = %i" % self.dob)
      #if input == Action.hired:
      #    return Driver.employed(self.dob, date)

      # no state change
      print("#   no state change")
      return Driver.unemployed(date)




class Retired(State):

  def run(self):
    #print("# Run retired: ")
    pass


  def next(self, date):

    print("# Retired next state: dob = %i" % self.dob)

    # no state change
    print("#   no state change")
    return Driver.retired(date)




#
# 2. Subclass of StateMachine
#
class Driver(StateMachine):

  def __init__(self):
    # Initial state is kid
    StateMachine.__init__(self, Driver.kid)




#
# 3. Create a sequence of months
#

# Map months to int 
months = map(string.strip, open("./timeline/months.txt").readlines())
mm = [ mo for mo in months if mo != '']
months = map(int, mm)



# 
# 4. Possible states of the Driver, are defined as 
#    Static members of the MouseDriver class initializated 
#    with the states defined at 1 above.
#

mob  = 199901
date = months[0]

Driver.kid         = Kid(mob, date)
Driver.student     = Student(mob, date)
Driver.employed    = Employed(mob, date)
Driver.unemployed  = Unemployed(mob, date)
Driver.retired     = Retired(mob, date)



#res = check_age(201101, 201511, 5)
#print("# Check age %i" % res)
#sys.exit()




#
#  5. Run all the actions by passing the 
#     Action objects to the runAll() method
#

Driver().runAll( months )

