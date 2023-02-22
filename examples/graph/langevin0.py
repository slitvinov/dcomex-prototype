import math
import random
import matplotlib.pylab as plt
import graph
import numpy as np


def fun(x):
	return -1 / 2 * x[0]**2


def dfun(x):
	return [-x[0]]


random.seed(123456)
draws = 10000
h = 0.01
step = [1.5]
S0 = graph.langevin(fun, draws, [0], dfun, h, log=True)
S1 = graph.metropolis(fun, draws, [0], step, log=True)
x = np.linspace(-4, 4, 100)
y = [math.exp(fun([x])) / math.sqrt(2 * math.pi) for x in x]
plt.hist([e for (e, ) in S0], 100, histtype='step', density=True, color='red')
plt.hist([e for (e, ) in S1], 100, histtype='step', density=True, color='blue')
plt.plot(x, y, '-g')
plt.savefig('langevin0.png')
