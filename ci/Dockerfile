ARG REGISTRY_PATH=finkandreas
FROM $REGISTRY_PATH/dcomex-prototype_base:1.0

COPY . /src

# build korali
RUN cd /src/korali \
  && CC=gcc CXX=g++ meson setup build --prefix=/usr/local --buildtype=release -Dmpi=true \
  && meson compile -C build \
  && meson install -C build

ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTONPATH

# build msolve
RUN cd /src/msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali \
  && dotnet build \
  && chmod +x ../../runTest.sh
