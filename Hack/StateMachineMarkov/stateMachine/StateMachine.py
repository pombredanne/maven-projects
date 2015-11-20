

#  The StateMachine keeps track of the current state, which is
#  is initialized by the constructor. 
#
#  The runAll( ) method takes a list of Input objects ("actions"), 
#  and for each action:
#
#   o moves to the next state invoking the next() method 
#     on the State object;
#
#   o invokes run() on the new state.
#


class StateMachine:

  def __init__(self, initialState):

    # This is a State object
    self.currentState = initialState

    # Invoke State.run()
    self.currentState.run()

  def runAll(self, timeline):
    if self.currentState.alive:
      for date in timeline:
        print("#---")
        print("# Time stamp %i, Income %i, Expense %i" % (date, self.currentState.income, self.currentState.expense))
        self.currentState = self.currentState.next({'date':date, 'income':self.currentState.income, 'expense':self.currentState.expense, 'alive':self.currentState.alive})
        self.currentState.run()



