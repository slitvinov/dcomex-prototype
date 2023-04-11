ARG BASE_IMAGE
FROM $BASE_IMAGE
COPY . /src
WORKDIR /src/korali
RUN meson setup build --prefix=/usr/local --buildtype=release -Dmpi=true
RUN ninja -C build
RUN meson install -C build
ENV PYTHONPATH=/usr/local/lib/python3.8/site-packages:$PYTONPATH
WORKDIR /src
RUN make
RUN chmod +x msolve/runTest.sh
