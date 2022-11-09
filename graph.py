import sys
import statistics
import random
import math


class Integral(object):
	"""Caches the samples to evalute the integral several times
	"""

	def __init__(self,
	             data_given_theta,
	             theta_given_psi,
	             method="metropolis",
	             **options):
		"""data_given_theta : callable
		      the join probability of the observed data viewed
		      as a function of parameter
		theta_given_psi : callable
		      conditional probability of parameters theta given
		      hyper-parameter psi
		method : str or callable, optional
		      the type of the sampling algorithm to sample from
		      data_given_theta. Can be one of

		      - metropolis (default)
		      - korali (WIP)
		      - hamiltonian (WIP)

		options : dict, optional
		      a dictionary of options for the sampling algorithm
		"""
		self.theta_given_psi = theta_given_psi
		if method == "metropolis":
			self.samples = metropolis(data_given_theta, **options)
		elif method == "korali":
			self.samples = korali_sample(data_given_theta, **options)
		else:
			raise ValueError("Unknown sampler '%s'" % method)

	def __call__(self, psi):
		"""Estimate the integral given hyproparameter psi"""
		return statistics.fmean(
		    self.theta_given_psi(theta, psi) for theta in self.samples)


def metropolis(fun, draws, init, scale, log=False):
	"""Metropolis sampler

	fun : callable
	      unnormalized density or log unnormalized probability
	      (see log)
	draws : int
	      the number of samples to draw. Default is 1000
	init : tuple
	      the initial point
	scale : tuple
	      the scale of the proposal distribution (same size as init)
	log : bool
	      set True to assume log-probability (default: False)"""
	x = init[:]
	p = fun(x)
	t = 0
	S = []
	accept = 0

	def flin(pp, p):
		return pp > random.uniform(0, 1) * p

	def flog(pp, p):
		return pp > math.log(random.uniform(0, 1)) + p

	cond = flog if log else flin
	while True:
		S.append(x)
		if t >= draws:
			break
		xp = [e + random.gauss(0, s) for e, s in zip(x, scale)]
		t += 1
		pp = fun(xp)
		if pp > pp or cond(pp, p):
			x, p = xp, pp
			accept += 1
	sys.stderr.write("graph.metropolis: accept = %g\n" % (accept / draws))
	return S
