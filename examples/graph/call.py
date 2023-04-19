import graph


@graph.trace()
def a(i):
    print("a")
    b(i)


@graph.trace(label="B")
def b(i):
    print("a")
    c(i)


c = graph.trace(label="c")(lambda i: i, )
a(10)

with open("call.gv", "w") as file:
    graph.graphviz(file)
