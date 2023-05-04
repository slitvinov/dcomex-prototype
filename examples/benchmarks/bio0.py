import graph
import matplotlib.pylab as plt
import subprocess
import sys
from timeit import default_timer as timer


def fun(x):
    time = 1
    k1, mu = x
    if Verbose:
        sys.stderr.write("%s\n" % x)
    command = ["bio"]
    if Surrogate:
        command.append("-s")
    command.append("%.16e" % k1)
    command.append("%.16e" % mu)
    command.append("%d" % time)
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
    if Verbose:
        sys.stderr.write("%.16e\n" % volume)
    return -((volume / scale - 5.0)**2 / sigma**2)


Surrogate = False
Verbose = False
draws = None
num_cores = None
while True:
    sys.argv.pop(0)
    if not sys.argv or sys.argv[0][0] != "-" or len(sys.argv[0]) < 2:
        break
    if sys.argv[0][1] == "h":
        sys.stderr.write("usage bio0.py -d draws\n")
        sys.exit(2)
    elif sys.argv[0][1] == "n":
        sys.argv.pop(0)
        if not sys.argv:
            sys.stderr.write("bio0.py: error: option -n needs an argument\n")
            sys.exit(2)
        try:
            num_cores = int(sys.argv[0])
        except ValueError:
            sys.stderr.write("bio0: not an integer '%s'\n" % sys.argv[0])
            sys.exit(2)
    elif sys.argv[0][1] == "d":
        sys.argv.pop(0)
        if not sys.argv:
            sys.stderr.write("bio0.py: error: option -d needs an argument\n")
            sys.exit(2)
        try:
            draws = int(sys.argv[0])
        except ValueError:
            sys.stderr.write("bio0: not an integer '%s'\n" % sys.argv[0])
            sys.exit(2)
    elif sys.argv[0][1] == "s":
        Surrogate = True
    elif sys.argv[0][1] == "v":
        Verbose = True
    else:
        sys.stderr.write("bio0.py: error: unknown option '%s'\n" % sys.argv[0])
        sys.exit(2)
sys.argv.append('')
if draws == None:
    sys.stderr.write("bio0.py: -d is not set\n")
    sys.exit(2)
if num_cores == None:
    sys.stderr.write("bio0.py: -n is not set\n")
    sys.exit(2)

lo = (0.1, 1)
hi = (0.5, 5)
start = timer()
samples, S = graph.korali(fun,
                          draws=draws,
                          lo=lo,
                          hi=hi,
                          return_evidence=True,
                          num_cores=num_cores)
end = timer()
print(num_cores, end - start)
# plt.plot(*zip(*samples), 'o', alpha=0.5)
# plt.xlim(lo[0], hi[0])
# plt.ylim(lo[1], hi[1])
# plt.xlabel("k1, 1/second")
# plt.ylabel("mu, kPa")
# plt.savefig("bio1.png")
