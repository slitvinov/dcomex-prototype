.POSIX:
.SUFFIXES:
PY = python3

M = \
graph.py\
kahan.py\

all: lib
lib: $M
	@p=`"$(PY)" -m site --user-site` || exit 2 && \
	mkdir -p "$$p" && \
	for i in $M; do cp -- "$$i" "$$p/$$f" || exit 2; done && \
	printf '%s\n' "$$p"
