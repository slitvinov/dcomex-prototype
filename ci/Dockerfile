FROM finkandreas/dcomex-prototype_base:1.0

COPY . /src

RUN cd /src/korali \
  && CC=gcc CXX=g++ meson setup build --prefix=/usr/local --buildtype=release -Dmpi=true \
  && ninja -C build \
  && meson install -C build

ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTONPATH

# build msolve
# not yet merged to main branch
#RUN cd /src/MSolveApp/ISAAR.MSolve.MSolve4Korali \
#  && dotnet build \
#  && chmod ../../runTest.sh
