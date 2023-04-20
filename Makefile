.POSIX:
.SUFFIXES:
.SUFFIXES: .sh
DOTNET = dotnet
PY = python3
PREFIX = /usr
USER = 0

M = \
follow.py\
graph.py\
kahan.py\

B = \
integration/bio\

all: bin lib ms
bin: $B
	mkdir -p -- "$(PREFIX)/bin"
	for i in $B; do cp -- "$$i" "$(PREFIX)/bin" || exit 2; done

lib: $M
	case '$(USER)' in \
	    0) p=`'$(PY)' -c "import sysconfig; print(sysconfig.get_path('purelib'))"` || exit 2 ;; \
	    *) p=`'$(PY)' -m site --user-site` || exit 2 ;; \
	esac && \
	mkdir -p -- "$$p" && \
	for i in $M; do cp -- "$$i" "$$p/$$f" || exit 2; done

ms:
	mkdir -p -- '$(PREFIX)/share' '$(PREFIX)/bin'
	cp -- msolve/ioDir/MeshCyprusTM.mphtxt '$(PREFIX)/share'
	(cd msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali && \
		DOTNET_CLI_TELEMETRY_OPTOUT=1 '$(DOTNET)' publish --nologo --configuration Release --output '$(PREFIX)/bin')

.sh:
	sed 's,%mph%,"$(PREFIX)"/share/MeshCyprusTM.mphtxt,g' $< > $@
	chmod a+x $@

clean:
	rm -f $B
	cd msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali && \
		DOTNET_CLI_TELEMETRY_OPTOUT=1 '$(DOTNET)' clean --nologo
