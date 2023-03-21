.POSIX:
.SUFFIXES:
PY = python3

M = \
graph.py\
kahan.py\

B = \
integration/bio

all: lib bin
bin: $B
	@p=$(HOME)/.local/bin || exit 2 && \
	mkdir -p "$$p" && \
	for i in $B; do cp -- "$$i" "$$p/$$f" || exit 2; done && \
	printf '%s\n' "$$p"

lib: $M
	@p=`"$(PY)" -m site --user-site` || exit 2 && \
	mkdir -p "$$p" && \
	for i in $M; do cp -- "$$i" "$$p/$$f" || exit 2; done && \
	printf '%s\n' "$$p"
