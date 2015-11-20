import random
import string, sys

sys.path += ['./stateMachine', './actions']

from State        import State
from StateMachine import StateMachine
from Action       import Action


turn18 = 2
turn65 = 4



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
    print("# Run kid:")


  def next(self, date):

    print("# Kid next state: dob = %i" % self.dob)

    #
    # Check for time-events
    #
    res = check_age(self.dob, date, turn18)
    if res:
       return Student(self.dob, date) 

    # no state change
    return Driver.kid(date)



class Student(State):

  p_drop = 0.2

  def run(self):
    print("# Run Student")


  def next(self, date):


    print("# Student next state: dob = %i" % self.dob)

    # Check for time-events
    #if input == Action.turn25:
    #  return Driver.employed

    # if input == Action.drops:
    dice = random.uniform(0,1)
    if dice < self.p_drop:
      return Driver.unemployed(date)

    # no state change
    return Driver.student(date)



class Employed(State):

    def run(self):
        print("# Run employed: ")


    def next(self, date):

      print("# Employed next state: dob = %i" % self.dob)

      #
      # Check for time-events
      # 
      res = check_age(self.dob, date, turn65)
      if res:
        return Driver.retired(date)


      #if action == Action.fired:
      #    return Driver.unemployed

      # no state change
      return Driver.employed(date)



class Unemployed(State):

    def run(self):
        print("# Run unemployed: ")

    def next(self, date):

      print("# Next for unemployed: dob = %i" % self.dob)
      #if input == Action.hired:
      #    return Driver.employed(self.dob, date)

      # no state change
      return Driver.unemployed(date)




class Retired(State):

    def run(self):

      print("# Run retired: ")



    def next(self, date):

      print("# Next for unemployed: dob = %i" % self.dob)

      # no state change
      return Driver.retired(date)



#
# 2. Subclass of StateMachine
#
class Driver(StateMachine):

  def __init__(self):
    # Initial state
    StateMachine.__init__(self, Driver.kid)


# 
# 3. Possible states of the Driver, are defined as 
#    Static members of the MouseDriver class initializated 
#    with the states defined at 1 above.
#

mob = 199901
Driver.kid         = Kid(mob)
Driver.student     = Student(mob)
Driver.employed    = Employed(mob)
Driver.unemployed  = Unemployed(mob)
Driver.retired     = Retired(mob)


#res = check_age(201101, 201511, 5)
#print("# Check age %i" % res)
#sys.exit()



#
# 4. Create a sequence of months
#

# Map months to int 
months = map(string.strip, open("./actions/actions_seq.txt").readlines())
mm = [ mo for mo in months if mo != '']
months = map(int, mm)



#
#  5. Run all the actions by passing the 
#     Action objects to the runAll() method
#

Driver().runAll( months )

