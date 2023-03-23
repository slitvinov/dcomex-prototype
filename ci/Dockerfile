ARG REGISTRY_PATH=finkandreas
FROM $REGISTRY_PATH/dcomex-prototype_base:1.0
COPY . /src
WORKDIR /src/korali
RUN meson setup build --prefix=/usr/local --buildtype=release -Dmpi=true
RUN ninja -C build
RUN meson install -C build
ENV PYTHONPATH=/usr/local/lib/python3/dist-packages:$PYTONPATH
WORKDIR /src
RUN make
RUN chmod +x msolve/runTest.sh
