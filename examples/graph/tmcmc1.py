import math
import statistics
import graph
import random
import numpy as np


def gauss(x):
	return -statistics.fsum(e**2 for e in x) / 2


seed = 123456
N = 2000
M = 50
d = 3
np.random.seed(seed)
random.seed(seed)
mean = []
var0 = []
var1 = []
var2 = []
lo = -5
hi = 5
for t in range(M):
	x = graph.tmcmc(gauss, N, d * [lo], d * [hi])
	mean.append(statistics.fmean(e[0] for e in x))
	var0.append(statistics.variance(e[0] for e in x))
	var1.append(statistics.variance(e[1] for e in x))
	var2.append(statistics.variance(e[2] for e in x))
print("%.3f %.4f %.4f %.4f" % (statistics.fmean(mean), statistics.fmean(var0),
                               statistics.fmean(var1), statistics.fmean(var2)))
