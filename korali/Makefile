.POSIX:
.SUFFIXES:
.SUFFIXES: .c .cpp .o

PY = python3
MPICXX = mpicxx
LINK = $(MPICXX)
USER = 0
CXXFLAGS_PYBIND11 =
CXXFLAGS_PYTHON = `pkg-config --cflags python3`
CXXFLAGS_EIGEN3 = `pkg-config --cflags eigen3`
CXXFLAGS_GSL = `pkg-config --cflags gsl`

LDFLAGS_GSL = `pkg-config --libs gsl`

include obj.mk
include py.mk

all: libkorali.so

.c.o:
	$(CC) -c -fPIC $(CFLAGS) $< -o $@

.cpp.o:
	$(MPICXX) -c -fPIC -std=c++17 -I. -Ikorali/source $(CXXFLAGS_PYTHON) $(CXXFLAGS_EIGEN3) $(CXXFLAGS_GSL) $(CXXFLAGS_PYBIND11) $(CXXFLAGS) $< -o $@

libkorali.so: $O
	$(LINK) -shared $O $(LDFLAGS_GSL) $(LDFLAGS) -o $@

clean:
	rm -f $O libkorali.so

install: libkorali.so $P
	case '$(USER)' in \
	    0) p=`$(PY) -c "import site; print(site.getsitepackages()[0])"` || exit 2 ;; \
	    *) p=`$(PY) -m site --user-site` || exit 2 ;; \
	esac && \
	for i in $P; \
	do b=`echo "$$i" | sed 's,korali/python/,,g'` && \
	   d=`dirname "$$b"` && \
	   mkdir -p -- "$$p/$$d/" && \
	   cp -- "$$i" "$$p/$$d/" || exit 2; \
	done && \
	cp -- libkorali.so "$$p/korali/" && \
	printf '%s\n' "$$p"
