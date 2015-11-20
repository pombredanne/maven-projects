import numpy as np
import itertools as it

start=1970
numYears = 150
np.random.seed(2)

bonds = np.random.normal(4, 2, numYears*12)
bonds = [round(b/12.0, 3) for b in bonds]
stocks = np.random.normal(8, 10, numYears*12)
stocks = [round(s/12.0, 3) for s in stocks]
interest = np.random.normal(0, 0.01, numYears*12)
interest = list([round(sum(interest[:z]),3) for z in range(1, len(interest) + 1)])
interest = map(lambda x: x+2, interest)

print bonds
print len(stocks)
print len(interest)


bonds = iter(bonds)
stocks = iter(stocks)
interest = iter(interest)

years = range(start, start+numYears)
months = range(1, 12+1)

f = open('product_table.csv', 'w')
f.write ("type_id, subtype_id, start_time, end_time, duration, interest_rate \n")
for y in years:
  for m in months:
    b = next(bonds)
    s = next(stocks)
    #print b, s
    i = next(interest)
    for type in ['savings', 'fixed', 'investment']:
      #[type, subtype, decr, duration, extra_base_points]
      for sub in [(1, 10, 'flex', 1, 0)]:
        # typeID, subtypeID, start_time, end_time+1, duration, interest
	print("%i, %i, '%i-%i-01 00:00:00', , %i, %.3f" % (sub[0], sub[1], y, m, sub[3],i+sub[4]))
        f.write("%i, %i, '%i-%i-01 00:00:00', , %i, %.3f\n" % (sub[0], sub[1], y, m, sub[3],i+sub[4]))

      for sub in [(2, 6, '3y', 3*12,0.23), (2, 5, '2y',2*12,0.11), (2, 4,'1y',12,0.05), (2, 3, '9m',9,0.003), (2, 2, '6m',6,0.002), (2, 1, '3m',3,0.001)]:
        print("%i, %i, '%i-%i-01 00:00:00', , %i, %.3f" % (sub[0], sub[1], y, m, sub[3],i+sub[4]))
        f.write("%i, %i, '%i-%i-01 00:00:00', , %i, %.3f\n" % (sub[0], sub[1], y, m, sub[3],i+sub[4]))

      for sub in [(3, 9, 'high', 1,0), (3, 8, 'middle', 1,0), (3, 7, 'low', 1,0)]:
        if sub[1] == 7:
          bs = b
        elif sub[1] == 8:
          bs = (s+b)/2.0
        else:
          bs = s
	print("%i, %i, '%i-%i-01 00:00:00', , %i, %.3f" % (sub[0], sub[1], y, m, sub[3],bs))
        f.write("%i, %i, '%i-%i-01 00:00:00', , %i, %.3f\n" % (sub[0], sub[1], y, m, sub[3],bs))
