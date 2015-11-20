import random
import string, sys

sys.path += ['./stateMachine', './timeline']

from State        import State
from StateMachine import StateMachine

#
# Time based thresholds
#
turn18 = 2
turn25 = 3
turn65 = 18



#
# Check if the age of a person 
# has reached the age threshold
#
def check_age (dob, info, age):
  date = info['date'] 

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
# 1. The states of the driver are subclasses of State, 
#    with a subclass for each possible state
#


#
# 1.1 Kid state
#
class Kid(State):


  #
  # Stuff done in this state
  #
  def run(self):
    # Make a transaction
    #print("# Run kid:")
    pass



  #
  # Finds next state or change attrs of current state
  #
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



#
# 1.2 Student state
#
class Student(State):

  p_drop = 0.2

  def run(self):
    # Make a transaction
    #print("# Run Student")
    pass



  #
  # Finds next state or change attrs of current state
  #
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



#
# 1.3 Kid state
#
class Employed(State):


  p_fired = 0.3


  def run(self):
    #print("# Run employed: ")
    pass



  #
  # Find next state or change attrs of current state
  #
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



#
# 1.4 Unemployed state
#
class Unemployed(State):

  def run(self):
    #print("# Run unemployed: ")
    pass
 


  #
  # Find next state or change attrs of current state
  #
  def next(self, date):

    print("# Unemployed next statexs: dob = %i" % self.dob)
    #if input == Action.hired:
    #    return Driver.employed(self.dob, date)

    # no state change
    print("#   no state change")
    return Driver.unemployed(date)




#
# 1.5 Retured state
#
class Retired(State):

  def run(self):
    #print("# Run retired: ")
    pass




  #
  # Find next state or change attrs of current state
  #

  def next(self, date):

    print("# Retired next state: dob = %i" % self.dob)

    # no state change
    print("#   no state change")
    return Driver.retired(date)





#
# 2. The Driver class is a subclass of StateMachine
#
class Driver(StateMachine):

  def __init__(self):
    # Initial state is kid
    StateMachine.__init__(self, Driver.kid)





#
# 3. Create a sequence of months to pass to the Driver
#

# Map months to int 
months = map(string.strip, open("./timeline/months.txt").readlines())
mm = [ mo for mo in months if mo != '']
months = map(int, mm)



# 
# 4. Possible states of the Driver, are defined as 
#    Static members of the Driver class initializated 
#    with the states defined at point 1 above.
#

# month of birth
mob  = 199901

# start date of simulation
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
#  5. Run the state machine through the timelines 
#

Driver().runAll( months )

