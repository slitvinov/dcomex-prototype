import functools

Stack = []
Edges = set()
Labels = {}


class Follow:

    def __init__(self, fn):
        self.fn = fn

    def __enter__(self):
        if Stack:
            Edges.add((Stack[-1], self.fn))
        Stack.append(self.fn)
        return self

    def __exit__(self, type, value, followback):
        Stack.pop()


def follow(label=None):

    def wrap(f):
        Labels[f] = label if label != None else f.__name__ if hasattr(
            f, '__name__') else str(f)

        @functools.wraps(f)
        def wrap0(*args, **kwargs):
            with Follow(f) as T:
                return f(*args, **kwargs)

        wrap0._f = f
        return wrap0

    return wrap


def graphviz(buf):
    Numbers = {}
    Vertices = set()
    buf.write("digraph {\n")
    for v, w in Edges:
        Vertices.add(v)
        Vertices.add(w)
    for i, v in enumerate(Vertices):
        Numbers[v] = i
        buf.write('%d [label = "%s"]\n' % (i, Labels[v]))
    for v, w in Edges:
        buf.write("%d -> %d\n" % (Numbers[v], Numbers[w]))
    buf.write("}\n")


def loop():
    return loop0(Edges)


def loop0(edges):
    adj = {}
    for i, j in edges:
        if not i in adj:
            adj[i] = set()
        if not j in adj:
            adj[j] = set()
        adj[i].add(j)
    for v in adj:
        visited = set()
        if not v in visited:
            stack = [v]
            while stack:
                v = stack.pop()
                if v in visited:
                    return True
                else:
                    visited.add(v)
                    stack.extend(adj[v])
    return False
