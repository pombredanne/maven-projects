class Action:

    def __init__(self, action):
        self.action = action

    def __str__(self): 
        return self.action

    def __cmp__(self, other):
        return cmp(self.action, other.action)

    # Necessary when __cmp__ or __eq__ is defined, in 
    # order to make this class usable as a dictionary key:
    def __hash__(self):
        return hash(self.action)


#
# Map between action names and Action objects
#
Action.turn18   = Action("turn18")
Action.drops    = Action("drops")
Action.turn25   = Action("turn25")
Action.hired    = Action("hired")
Action.fired    = Action("fired")
Action.turn65   = Action("turn65")



