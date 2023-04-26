.POSIX:
.SUFFIXES:
.SUFFIXES: .sh
DOTNET = dotnet
PY = python3
PREFIX = /usr
USER = 0

M = \
setup.py\
follow.py\
graph.py\
kahan.py\

B = \
integration/bio\

all: bin lib msolve
bin: $B
	mkdir -p -- "$(PREFIX)/bin"
	for i in $B; do cp -- "$$i" "$(PREFIX)/bin" || exit 2; done

lib: $M
	case '$(USER)' in \
	    0) '$(PY)' setup.py install ;; \
	    *) '$(PY)' setup.py install --user ;; \
	esac

msolve:
	mkdir -p -- '$(PREFIX)/share' '$(PREFIX)/bin'
	cp -- msolve/ioDir/MeshCyprusTM.mphtxt '$(PREFIX)/share'
	(cd msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali && \
		DOTNET_CLI_TELEMETRY_OPTOUT=1 '$(DOTNET)' publish --nologo --configuration Release --output '$(PREFIX)/bin')

lkorali:
	(cd korali && \
		git clone --quiet --single-branch https://github.com/cselab/korali && \
		(cd korali && git checkout c70d8e32258b7e2b9ed977576997dfe946816419) && \
		make install -j4 'USER = $(USER)' 'PREFIX = $(PREFIX)')

.sh:
	sed 's,%mph%,"$(PREFIX)"/share/MeshCyprusTM.mphtxt,g' $< > $@
	chmod a+x $@

clean:
	rm -f $B
	cd msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali && \
		DOTNET_CLI_TELEMETRY_OPTOUT=1 '$(DOTNET)' clean --nologo
