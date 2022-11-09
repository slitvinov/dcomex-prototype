.POSIX:
.SUFFIXES:
PY = python3

all: install
M = \
graph.py

install: $M
	@p=`"$(PY)" -m site --user-site` || exit 2 && \
	mkdir -p "$$p" && \
	for i in $M; do cp -- "$$i" "$$p/$$f" || exit 2; done && \
	printf '%s\n' "$$p"
