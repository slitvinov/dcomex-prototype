ARG BASE_IMAGE
FROM $BASE_IMAGE
COPY . /src
WORKDIR /src
RUN make lkorali bin lib msolve
RUN chmod +x msolve/runTest.sh
