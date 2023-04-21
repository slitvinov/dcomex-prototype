.POSIX:
.SUFFIXES:
.SUFFIXES: .c .cpp .o

MPICC = mpicc
MPICXX = mpicxx
LINK = $(MPICXX)

include obj.mk
all: libkorali.so

.c.o:
	$(MPICC) -c -fPIC $(CFLAGS) $< -o $@

.cpp.o:
	$(MPICXX) -c -fPIC -std=c++17 -I. -Isource `pkg-config --cflags python3 eigen3` $(CXXFLAGS) $< -o $@

libkorali.so: $O
	$(LINK) $(LDFLAGS) -shared $O -o $@

clean:
	rm -f $O libkorali.so
