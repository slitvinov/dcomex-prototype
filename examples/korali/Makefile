.POSIX:
.SUFFIXES:
.SUFFIXES: .c .cpp .o

MPICC = mpicc
MPICXX = mpicxx
LINK = $(MPICXX)

include obj.mk
all: libkorali.so

.c.o:
	$(MPICC) -fPIC $(CFLAGS) -c $< -o $@

.cpp.o:
	$(MPICXX) -I. -fPIC -std=c++17 `pkg-config --cflags python3 eigen3` $(CXXFLAGS) -c $< -o $@

libkorali.so: $O
	$(LINK) $(LDFLAGS) -shared $O -o $@
