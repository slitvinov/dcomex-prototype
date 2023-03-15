import graph
import os
import subprocess
import multiprocessing
import random
import itertools
import statistics
from xml.dom.minidom import parse


def fun(args):
	k1, mu = args
	with open("config.xml", "w") as file:
		file.write('''<MSolve4Korali version="1.0">
	<Mesh>
		<File>MeshCyprusTM.mphtxt</File>
	</Mesh>
	<Physics type="TumorGrowth">
		<Time>20</Time>
		<Timestep>1</Timestep>
	</Physics>
	<Output>
		<TumorVolume/>
	</Output>
	<Parameters>
		<k1>%.16e</k1>
		<mu>%.16e</mu>
	</Parameters>
</MSolve4Korali>
''' % (k1, mu))
	rc = subprocess.call(["msolve_bio"])
	if rc != 0:
		raise Exception("bio.py: msolve_bio failed for parameters %s" %
		                str(args))
	document = parse("result.xml")
	Vtag = document.getElementsByTagName("Volume")
	if not Vtag:
		raise Exception(
		    "bio.py: result.xml does not have Volume for parameters %s" %
		    str(args))
	V = float(Vtag[0].childNodes[0].nodeValue)
	return -(V - 1.0)**2


def worker(i):
	random.seed(os.getpid())
	path = "%05d.out" % i
	os.makedirs(path, exist_ok=True)
	os.chdir(path)
	return list(
	    graph.metropolis(fun, 500, init=[0, 0], scale=[0.5, 0.5], log=True))


np = multiprocessing.cpu_count()
pool = multiprocessing.Pool(np)
samples = pool.map(worker, range(np))
print(statistics.fmean(mu + 2 * k1 for k1, mu in itertools.chain(*samples)))
