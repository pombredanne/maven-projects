#
# See 
#   http://stackoverflow.com/questions/6486877/python-code-for-the-coin-toss-issues
#
import random

messages = {1: "Heads", 2: "Tails"}

samples = [ random.randint(1, 2) for i in range(100) ]
heads = samples.count(1)
tails = samples.count(2)

print "Heads count=%d, Tails count=%d" % (heads, tails)

#for s in samples:
for i, s in enumerate(samples): 
    #msg = 'Heads' if s==1 else 'Tails'
    #print msg
    print i, messages[s]



