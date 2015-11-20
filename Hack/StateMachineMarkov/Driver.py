import random
import string, sys

sys.path += ['./stateMachine', './actions']

from State        import State
from StateMachine import StateMachine
from Action       import Action



#
# 1. The possible states of the driver are 
#    subclasses os State, with a subclass 
#    for each possible state
#

class Kid(State):

  def run(self):
    print("# Kid: growing up")


  def next(self, input):

    print("# Kid: born on %i" % self.dob)

    if input == Action.turn18:
      return Driver.student
    # no state change
    return Driver.kid



class Student(State):

  p_drop = 0.2

  def run(self):
    print("# Student: learning")

  def next(self, input):

    # Check for time-events
    if input == Action.turn25:
      return Driver.employed

    # if input == Action.drops:
    dice = random.uniform(0,1)
    if dice < self.p_drop:
      return Driver.unemployed

    # no state change
    return Driver.student



class Employed(State):

    def run(self):
        print("# Employed: Making money")

    def next(self, action):
        if action == Action.turn65:
            return Driver.retired
        if action == Action.fired:
            return Driver.unemployed
        # no state change
        return Driver.employed


class Unemployed(State):

    def run(self):
        print("# Unemployed: broke")

    def next(self, input):
        if input == Action.hired:
            return Driver.employed

        # no state change
        return Driver.unemployed



class Retired(State):

    def run(self):
        print("# Retired: happy")

    def next(self, input):

        # no state change
        return Driver.unemployed



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
Driver.kid         = Kid(19990101)
Driver.student     = Student()
Driver.employed    = Employed()
Driver.unemployed  = Unemployed()
Driver.retired     = Retired()


#
# 4. Create a sequence of action objects from 
#    a list of action names 
#
moves = map(string.strip, open("./actions/actions_seq.txt").readlines())

#
#  5. Run all the actions by passing the 
#     Action objects to the runAll() method
#
Driver().runAll( map(Action, moves) )

