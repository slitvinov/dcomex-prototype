def cumvariance(a):
	n = 0
	s = 0.0
	s2 = 0.0
	for e in a:
		n += 1
		y = e - s
		s += y / n
		s2 += y * (e - s)
		yield s, s2 / n


def cummean(a):
	s = 0.0
	c = 0.0
	n = 0
	for e in a:
		y = e - c
		t = s + y
		c = (t - s) - y
		s = t
		n += 1
		yield s / n


def cumsum(a):
	s = 0.0
	c = 0.0
	for e in a:
		y = e - c
		t = s + y
		c = (t - s) - y
		s = t
		yield s


def sum(a):
	s = 0.0
	c = 0.0
	for e in a:
		y = e - c
		t = s + y
		c = (t - s) - y
		s = t
	return s


def mean(a):
	s = 0.0
	c = 0.0
	n = 0
	for e in a:
		y = e - c
		t = s + y
		c = (t - s) - y
		s = t
		n += 1
	return s / n
