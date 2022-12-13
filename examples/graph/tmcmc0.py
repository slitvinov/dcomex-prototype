import math
import statistics
import random
import scipy.stats
import graph


def fun(x, a, b, w, dev):
	coeff = -1 / (2 * dev**2)
	u = coeff * statistics.fsum((e - d)**2 for e, d in zip(x, a))
	v = coeff * statistics.fsum((e - d)**2 for e, d in zip(x, b))
	return scipy.special.logsumexp((u + math.log(w), v + math.log(1 - w)))


D = (
    (2, 0.5, 0.5),
    (2, 0.1, 0.9),
    (4, 0.5, 0.5),
    (4, 0.1, 0.9),
    (6, 0.5, 0.5),
    (6, 0.3, 0.5),
    (6, 0.1, 0.5),
    (6, 0.1, 0.9),
)
seed = 12345
N = 1000
M = 50
random.seed(seed)
for d, dev, w in D:
	a = [0.5] * d
	b = [-0.5] * d
	first_peak = []
	smax = []
	logev = []
	for t in range(M):
		x, S = graph.tmcmc(lambda x: fun(x, a, b, w, dev),
		                   N, [-2] * d, [2] * d,
		                   return_evidence=True)
		cnt = 0
		for e in x:
			da = statistics.fsum((u - v)**2 for u, v in zip(e, a))
			db = statistics.fsum((u - v)**2 for u, v in zip(e, b))
			if da < db:
				cnt += 1
		first_peak.append(cnt / N)
		smax.append(statistics.fmean(max(e) for e in x))
		logev.append(S)
	cv = lambda a: (statistics.mean(a), 100 * abs(scipy.stats.variation(a)))
	print("%.2f (%.1f%%)    %.2f (%.1f%%)    %.2f (%.1f%%)" %
	      (*cv(first_peak), *cv(smax), *cv(logev)))
