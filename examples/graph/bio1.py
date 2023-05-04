import graph
import matplotlib.pylab as plt
import subprocess
import sys
import mpi4py.MPI


def fun(x):
    time = 3
    k1, mu = x
    command = ["bio", "-s", "%.16e" % k1, "%.16e" % mu, "%d" % time]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        sys.stderr.write("bio.py: command '%s' failed\n" % command)
        exit(1)
    output = output.decode()
    try:
        volume = float(output)
    except ValueError:
        sys.stderr.write("bio.py: not a float '%s'\n" % output)
        exit(1)
    sigma = 0.5
    scale = 1e-6
    return -((volume / scale - 5.0)**2 / sigma**2)


lo = (0.1, 1)
hi = (0.5, 5)
samples, S = graph.korali(fun,
                          draws=10,
                          lo=lo,
                          hi=hi,
                          return_evidence=True,
                          comm=mpi4py.MPI.COMM_WORLD)
if mpi4py.MPI.COMM_WORLD.Get_rank() == mpi4py.MPI.COMM_WORLD.Get_size() - 1:
    print("log evidence: %g [%ld]" % (S, len(samples)))
    plt.plot(*zip(*samples), 'o', alpha=0.5)
    plt.xlim(lo[0], hi[0])
    plt.ylim(lo[1], hi[1])
    plt.xlabel("k1, 1/second")
    plt.ylabel("mu, kPa")
    plt.savefig("bio1.png")
