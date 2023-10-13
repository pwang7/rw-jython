#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

DREAM_PLACER_FPGA="DREAMPlaceFPGA"

if [ -d $DREAM_PLACER_FPGA ]; then
    echo "$DREAM_PLACER_FPGA exits, no need to download"
else
    git clone --depth 1 --recursive https://github.com/rachelselinar/DREAMPlaceFPGA.git
fi

# apt-get install -y capnproto libcapnp-dev
# PyTorch versions: 1.11.0, 1.12.0, 1.12.1, 1.13.0, 1.13.1, 2.0.0, 2.0.1, 2.1.0
docker build . --file ./scripts/DREAMPlaceFPGA.Dockerfile --tag pwang7/dreamplacefpga:torch-1.13.1

docker run --rm pwang7/dreamplacefpga:torch-1.13.1 python3 ./dreamplacefpga/Placer.py ./test/FPGA-example1.json
# docker run --rm pwang7/dreamplacefpga:torch-1.13.1 python3 ./dreamplacefpga/Placer.py ./test/FPGA-example2.json
# docker run --rm pwang7/dreamplacefpga:torch-1.13.1 python3 ./dreamplacefpga/Placer.py ./test/FPGA-example3.json
# docker run --rm pwang7/dreamplacefpga:torch-1.13.1 python3 ./dreamplacefpga/Placer.py ./test/FPGA-example4.json

# docker run --rm -v ./dev:/tmp/dev pwang7/dreamplacefpga:torch-1.13.1 /bin/bash -c "\
#     cp /tmp/dev/*.device /opt/DREAMPlaceFPGA/IFsupport && \
#     python3 ./dreamplacefpga/Placer.py ./test/gnl_2_4_3_1.3_gnl_3000_07_3_80_80.json && \
#     cp results/design/design.phys /tmp/dev \
# "
# docker run --rm -v ./dev:/tmp/dev -v ./dpf:/tmp/dpf pwang7/dreamplacefpga:torch-1.13.1 /bin/bash -c "\
#     cp /tmp/dev/*.device /opt/DREAMPlaceFPGA/IFsupport && \
#     python3 ./IFsupport/IF2bookshelf.py --netlist /tmp/dpf/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.netlist && \
#     python3 ./dreamplacefpga/Placer.py /tmp/dpf/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.json && \
#     cp results/design/design.phys /tmp/dev \
# "

# docker push pwang7/dreamplacefpga:torch-1.13.1
