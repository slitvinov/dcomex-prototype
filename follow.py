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
    """ 
    Decorator that allows a function to be "followed" in a call graph.

    Parameters
    ----------
    label : str, optional
        A label for the wrapped function in the call graph. If not provided, 
        the function name will be used as the label.

    Returns
    -------
    function
        A wrapped version of the input function that can be used to generate 
        a call graph.

    Examples
    --------
    >>> @follow()
    ... def add(a, b):
    ...     return a + b
    >>> add(2, 3)
    5

    >>> @follow(label='Subtract')
    ... def sub(a, b):
    ...     return a - b
    >>> sub(5, 2)
    3

    >>> add = follow()(lambda a, b: a + b)
    >>> add(2, 3)
    5

    """    
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
    """
    Decorator that generates a call graph of the decorated functions.

    Parameters
    ----------
    buf : TextIOWrapper
        A file-like object that the graph will be written to.

    Returns
    -------
    None

    """
    
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
    """
    Determines whether there is a loop in the call graph.

    Returns
    -------
    bool
        True if there is a loop in the call graph, False otherwise.

    Examples
    --------
    >>> @follow()
    ... def func1(x):
    ...     if x > 0:
    ...         return func2(x-1)
    ...     else:
    ...         return 0
    >>> @follow()
    ... def func2(x):
    ...     if x > 0:
    ...         return func1(x-1)
    ...     else:
    ...         return 0
    >>> func2(42)
    0
    >>> has_loop = loop()
    >>> print(has_loop)
    True

    >>> @follow()
    ... def func1(x):
    ...     return func2(x-1)
    >>> 
    >>> @follow()
    ... def func2(x):
    ...     pass
    >>> func2(42)
    >>> loop()
    True


    """
    
    adj = {}
    for i, j in Edges:
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
