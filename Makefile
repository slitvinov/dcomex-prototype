.POSIX:
.SUFFIXES:
PY = python3

M = \
graph.py\
kahan.py\

B = \
integration/bio\

all: bin lib ms
bin: $B
	@p=/usr/bin || exit 2 && \
	mkdir -p "$$p" && \
	for i in $B; do cp -- "$$i" "$$p/$$f" || exit 2; done

lib: $M
	@p=`"$(PY)" -c "import sysconfig; print(sysconfig.get_path('purelib'))"` || exit 2 && \
	mkdir -p "$$p" && \
	for i in $M; do cp -- "$$i" "$$p/$$f" || exit 2; done

ms:
	mkdir -p /usr/share && \
	cp msolve/ioDir/MeshCyprusTM.mphtxt /usr/share/
	(cd msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali && \
		dotnet publish --nologo --configuration Release --output /usr/bin)

clean:
	(cd msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali &&
		dotnet clean --nologo)
