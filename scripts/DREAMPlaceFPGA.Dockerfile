FROM ubuntu

WORKDIR /opt/DREAMPlaceFPGA

COPY ./DREAMPlaceFPGA /opt/DREAMPlaceFPGA
COPY ./scripts/DREAMPlaceFPGA.diff /opt/DREAMPlaceFPGA

RUN apt-get update && apt-get install -y libboost-all-dev libfl-dev python3-pip cmake bison libcairo2
RUN cd /opt/DREAMPlaceFPGA && patch -p 1 < DREAMPlaceFPGA.diff && \
    pip install -r requirements.txt
RUN cd /opt/DREAMPlaceFPGA && mkdir build && cd build && \
    cmake .. -DCMAKE_INSTALL_PREFIX=.. && make install
