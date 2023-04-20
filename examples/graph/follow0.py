import follow


@follow.follow()
def a(i):
    b(i)


@follow.follow(label="B")
def b(i):
    c(i)


c = follow.follow(label="c")(lambda i: i, )
a(10)

with open("follow.gv", "w") as file:
    follow.graphviz(file)
