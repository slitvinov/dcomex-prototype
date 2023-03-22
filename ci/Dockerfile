ARG REGISTRY_PATH=finkandreas
FROM $REGISTRY_PATH/dcomex-prototype_base:1.0

COPY . /src

# build korali
RUN cd /src/korali \
  && meson setup build --prefix=/usr/local --buildtype=release -Dmpi=true \
  && ninja -C build \
  && meson install -C build

ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTONPATH

# build msolve
RUN make
RUN chmod +x msolve/runTest.sh
