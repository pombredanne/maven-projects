import random
import string, sys

sys.path += ['./stateMachine', './actions']

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

def isAlive(dob, info):
  date = info['date'] 

  m1 = 12 * (date / 100) + date % 100
  m0 = 12 * (dob / 100)  + dob % 100

  months = m1 - m0
  #print("# months = %i" % months)

  years = months/12
  #print("# years = %i" % years)

  if years > 110 :
	print ("# I just died.")
	return False

#
# 1. The states of the driver are subclasses of State, 
#    with a subclass for each possible state
#

class Kid(State):

  p_sideJob = 0.02
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
  def next(self, info):
    

    print("# Kid next state: dob = %i" % self.dob)

    #
    # Check for time-events
    #

    res = check_age(self.dob, info, turn65)
    if res:
      print("#   graduate to retired")
      return Driver.retired(info)

    res = check_age(self.dob, info, turn25)
    if res:
      print("#   graduate to employed or unemployed")
      return Driver.employed(info) 

    res = check_age(self.dob, info, turn18)
    if res:
      print("#   graduate to student")
      return Driver.student(info) 

   
    if info['income'] == 0:
      dice = random.uniform(0,1)
      if dice < self.p_sideJob:
        #print("#I have a job now")
        #print(info)
        info['income'] = 400
        info['expense'] = 300
        
	
    # no state change
    print("#   no state change")
    return Driver.kid(info)



class Student(State):

  p_drop = 0.2

  def run(self):
    # Make a transaction
    #print("# Run Student")
    pass



  #
  # Finds next state or change attrs of current state
  #
  def next(self, info):

    print("# Student next state: dob = %i" % self.dob)


    #
    # Check for time-events
    #    
    res = check_age(self.dob, info, turn25)
    if res:
      print("#   graduate to employed or unemployed")
      return Driver.employed(info) 



    #
    # Check for prob events
    #

    # drops out
    dice = random.uniform(0,1)
    if dice < self.p_drop:
      return Driver.unemployed(info)


    # no state change
    print("#   no state change")
    return Driver.student(info)



class Employed(State):


  p_fired = 0.3


  def run(self):
    #print("# Run employed: ")
    pass



  #
  # Find next state or change attrs of current state
  #
  def next(self, info):

    print("# Employed next state: dob = %i" % self.dob)

    #
    # Check for time-events
    # 
    res = check_age(self.dob, info, turn65)
    if res:
      print("#   graduate to retired")
      return Driver.retired(info)


    #
    # Check for prob events
    #

    # fired
    dice = random.uniform(0,1)
    if dice < self.p_fired:
      return Driver.unemployed(info)


    #if action == Action.fired:
    #    return Driver.unemployed

    # no state change
    print("#   no state change")
    return Driver.employed(info)



class Unemployed(State):

  def run(self):
    #print("# Run unemployed: ")
    pass
 


  #
  # Find next state or change attrs of current state
  #
  def next(self, info):

    print("# Unemployed next statexs: dob = %i" % self.dob)
    #if input == Action.hired:
    #    return Driver.employed(self.dob, info)

    # no state change
    print("#   no state change")
    return Driver.unemployed(info)




class Retired(State):

  def run(self):
    #print("# Run retired: ")
    pass




  #
  # Find next state or change attrs of current state
  #

  def next(self, info):

    print("# Retired next state: dob = %i" % self.dob)

    # no state change
    print("#   no state change")
    info.alive = isAlive(self.dob, info)
   
    return Driver.retired(info)




#
# 2. Then Driver class is a subclass of StateMachine
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
#    Static members of the MouseDriver class initializated 
#    with the states defined at 1 above.
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



# Example
#res = check_age(201101, 201511, 5)
#print("# Check age %i" % res)

# Example
#res = gen_timeline (201501, 3)
#print res





#
#  5. Run the state machine through the timelines 
#

Driver().runAll( months )

