FROM docker.io/nvidia/cuda:11.2.0-cudnn8-devel-ubuntu20.04
ARG GIT_SSL_NO_VERIFY=1
ARG MPICH_VERSION=3.1.4
ARG TZ=Europe/Zurich
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -qq update
RUN apt-get -qq --fix-missing upgrade
RUN apt-get -qq install --no-install-recommends apt-transport-https
RUN apt-get -qq install --no-install-recommends cmake
RUN apt-get -qq install --no-install-recommends g++
RUN apt-get -qq install --no-install-recommends git
RUN apt-get -qq install --no-install-recommends libgsl-dev
RUN apt-get -qq install --no-install-recommends libmkldnn-dev
RUN apt-get -qq install --no-install-recommends meson
RUN apt-get -qq install --no-install-recommends ninja-build
RUN apt-get -qq install --no-install-recommends pkg-config
RUN apt-get -qq install --no-install-recommends python3-dev
RUN apt-get -qq install --no-install-recommends python3-matplotlib
RUN apt-get -qq install --no-install-recommends python3-mpi4py
RUN apt-get -qq install --no-install-recommends python3-numpy
RUN apt-get -qq install --no-install-recommends python3-pybind11
RUN apt-get -qq install --no-install-recommends python3-scipy
RUN apt-get -qq install --no-install-recommends wget
RUN wget --no-check-certificate -q http://www.mpich.org/static/downloads/${MPICH_VERSION}/mpich-${MPICH_VERSION}.tar.gz -O /tmp/mpich-${MPICH_VERSION}.tar.gz
RUN tar -zxf /tmp/mpich-${MPICH_VERSION}.tar.gz -C /tmp/
WORKDIR /tmp/mpich-${MPICH_VERSION}
RUN ./configure --disable-fortran --enable-fast=all,O3 --prefix=/usr
RUN make -j
RUN make install
WORKDIR /
RUN wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb
RUN dpkg --install /tmp/packages-microsoft-prod.deb
RUN apt-get -qq update
RUN apt-get -qq install --no-install-recommends dotnet-sdk-6.0
RUN git clone --quiet --single-branch --depth 1 --recurse-submodules https://github.com/DComEX/dcomex-prototype src
WORKDIR /src/korali
RUN meson setup build --prefix=/usr/local --buildtype=release -Dmpi=true
RUN ninja -C build
RUN meson install -C build
WORKDIR /src/msolve/MSolveApp/ISAAR.MSolve.MSolve4Korali
RUN dotnet build --nologo --configuration Release
RUN mkdir -p $HOME/.local/bin/
RUN mkdir -p $HOME/.local/share/
RUN cp bin/Release/net6.0/ISAAR.MSolve.MSolve4Korali $HOME/.local/bin/
RUN cp bin/Release/net6.0/ISAAR.MSolve.MSolve4Korali.runtimeconfig.json $HOME/.local/bin/
RUN cp bin/Release/net6.0/*.dll $HOME/.local/bin/
RUN cp /src/msolve/ioDir/MeshCyprusTM.mphtxt $HOME/.local/share/
WORKDIR /src
RUN make
RUN echo 'PATH=$HOME/.local/bin:$PATH' > $HOME/.bashrc
RUN echo 'PYTHONPATH=/usr/local/lib/python3.8/site-packages' >> $HOME/.bashrc
RUN . $HOME/.bashrc
