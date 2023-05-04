import graph
import matplotlib.pylab as plt
import subprocess
import sys


def fun(x):
    time = 3
    k1, mu = x
    sys.stderr.write("%s\n" % x)
    command = ["bio", "%.16e" % k1, "%.16e" % mu, "%d" % time]
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
    sys.stderr.write("%g\n" % volume)
    return -(volume / 1e-7 - 1)**2


lo = (0.1, 1)
hi = (0.5, 5)
samples, S = graph.korali(fun,
                          draws=10,
                          lo=lo,
                          hi=hi,
                          return_evidence=True,
                          num_cores=4)
print("log evidence: ", S)
plt.plot(*zip(*samples), 'o', alpha=0.5)
plt.xlim(-5, 5)
plt.ylim(-5, 5)
plt.xlabel("a")
plt.ylabel("b")
plt.savefig("bio.png")
