.POSIX:
.SUFFIXES:
.SUFFIXES: .c .cpp .o

PY = python3
CXX = g++
LINK = $(CXX)
USER = 0

include obj.mk
include py.mk

all: libkorali.so

.c.o:
	$(CC) -c -fPIC $(CFLAGS) $< -o $@

.cpp.o:
	$(CXX) -c -fPIC -std=c++17 -I. -Ikorali/source `pkg-config --cflags python3 eigen3 mpi-cxx` $(CXXFLAGS) $< -o $@

libkorali.so: $O
	$(LINK) -shared $O $(LDFLAGS) `pkg-config --libs gsl mpi-cxx` -o $@

clean:
	rm -f $O libkorali.so

install: libkorali.so $P
	case '$(USER)' in \
	    0) p=`'$(PY)' -c "import sysconfig; print(sysconfig.get_path('purelib'))"` || exit 2 ;; \
	    *) p=`'$(PY)' -m site --user-site` || exit 2 ;; \
	esac && \
	for i in $P; \
	do b=`echo "$$i" | sed 's,korali/python/,,g'` && \
	   d=`dirname "$$b"` && \
	   mkdir -p -- "$$p/$$d/" && \
	   cp -- "$$i" "$$p/$$d/" || exit 2; \
	done && \
	cp -- libkorali.so "$$p/korali/" && \
	printf '%s\n' "$$p"
