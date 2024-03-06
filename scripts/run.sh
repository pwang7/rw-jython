#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o xtrace

java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/helloWorld.py
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/createNetlist.py
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.PolynomialGenerator 3*x^2+x-2 16
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.PolynomialGenerator 8*y^4+43*y*x^3+7*x^2-14 18 # --hand-placer
# java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/satRouter.py
# java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.RunSATRouterExample ./checkpoints/reduce_or_routed_7overlaps.dcp SLICE_X108Y660:SLICE_X111Y664 ./checkpoints/reduce_or_sat_routed.dcp
# java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/probeRerouter.py

java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/basicCircuit.py
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/netSizes.py
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/numOfMemLUTs.py
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/rwRoute.py ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.dcp ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_timing_driven_routed.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/rwRoute.py ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.dcp ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_non_timing_routed.dcp --nonTimingDriven
java -Xmx5g -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/partialRoute.py ./checkpoints/picoblaze_partial.dcp ./checkpoints/picoblaze_routed.dcp --nonTimingDriven
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/reportTiming.py ./checkpoints/microblaze4.dcp

unzip -o ./checkpoints/kcu105_example.zip
# cd kcu105
# vivado -source ../tutorials/kcu105CreateShell.tcl
mkdir -p kcu105
# Copy both kcu105_route.dcp and kcu105_route.edf
cp ./checkpoints/kcu105_route.* ./kcu105
# java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/makeBlackBox.py ./kcu105/kcu105_route.dcp ./kcu105/kcu105_route_shell.dcp VexRiscvLitexSmpCluster_Cc4_Iw64Is8192Iy2_Dw64Ds8192Dy2_ITs4DTs4_Ldw512_Cdma_Ood/cores_1_cpu_logic_cpu
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/makeBlackBox.py \
    ./kcu105/kcu105_route.dcp ./kcu105/kcu105_route_shell.dcp \
    VexRiscvLitexSmpCluster_Cc4_Iw64Is8192Iy2_Dw64Ds8192Dy2_ITs4DTs4_Ldw512_Cdma_Ood/cores_3_cpu_logic_cpu \
    VexRiscvLitexSmpCluster_Cc4_Iw64Is8192Iy2_Dw64Ds8192Dy2_ITs4DTs4_Ldw512_Cdma_Ood/cores_2_cpu_logic_cpu \
    VexRiscvLitexSmpCluster_Cc4_Iw64Is8192Iy2_Dw64Ds8192Dy2_ITs4DTs4_Ldw512_Cdma_Ood/cores_1_cpu_logic_cpu
# vivado -source ../tutorials/kcu105ReuseShell.tcl

java -Xmx5g -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.interchange.DeviceResourcesExample xc7z020clg400-2; #xcvu3p-ffvc1517-2-e
mkdir -p dev
mv *.device ./dev
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.interchange.DcpToInterchange ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.interchange.PhysicalNetlistToDcp ./dpf/gnl_2_4_3_1.3_gnl_3000_07_3_80_80.netlist ./dpf/gnl_2_4_3_1.3_gnl_3000_07_3_80_80.phys ./dpf/gnl_2_4_3_1.3_gnl_3000_07_3_80_80.xdc ./checkpoints/gnl_2_4_3_1.3_gnl_3000_07_3_80_80_placed.dcp --out_of_context
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.interchange.PhysicalNetlistToDcp ./dpf/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.netlist ./dpf/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.phys ./dpf/gnl_2_4_7_3.0_gnl_3500_03_7_80_80.xdc ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_placed.dcp --out_of_context
# vivado ./checkpoints/gnl_2_4_3_1.3_gnl_3000_07_3_80_80_placed.dcp
# vivado ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_placed.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.rwroute.RWRoute ./checkpoints/gnl_2_4_3_1.3_gnl_3000_07_3_80_80_placed.dcp ./checkpoints/gnl_2_4_3_1.3_gnl_3000_07_3_80_80_routed.dcp --nonTimingDriven --outOfContext
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/rwRoute.py ./checkpoints/gnl_2_4_3_1.3_gnl_3000_07_3_80_80_placed.dcp ./checkpoints/gnl_2_4_3_1.3_gnl_3000_07_3_80_80_routed_alt.dcp --nonTimingDriven --outOfContext
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.rwroute.RWRoute ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_placed.dcp ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_routed.dcp --nonTimingDriven --outOfContext
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/rwRoute.py ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_placed.dcp ./checkpoints/gnl_2_4_7_3.0_gnl_3500_03_7_80_80_routed_alt.dcp --nonTimingDriven --outOfContext

java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.SLRCrosserGenerator -w 720 -o ./checkpoints/slr_crosser_vu9p.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/slrCrosserGenerator.py --width 720 -o ./checkpoints/slr_crosser_vu9p_alt.dcp
LAGUNA_SITES=LAGUNA_X0Y120,LAGUNA_X2Y120,LAGUNA_X4Y120,LAGUNA_X6Y120,LAGUNA_X8Y120,LAGUNA_X10Y120,LAGUNA_X12Y120,LAGUNA_X14Y120,LAGUNA_X16Y120,LAGUNA_X18Y120,LAGUNA_X20Y120,LAGUNA_X22Y120,LAGUNA_X0Y360,LAGUNA_X2Y360,LAGUNA_X4Y360,LAGUNA_X6Y360,LAGUNA_X8Y360,LAGUNA_X10Y360,LAGUNA_X12Y360,LAGUNA_X14Y360,LAGUNA_X16Y360,LAGUNA_X18Y360,LAGUNA_X20Y360,LAGUNA_X22Y360
java -Xmx5g -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.SLRCrosserGenerator -p xcvu13p-fhgb2104-2-i -w 720 -o ./checkpoints/slr_crosser_vu13p.dcp -l $LAGUNA_SITES
java -Xmx5g -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/slrCrosserGenerator.py --part xcvu13p-fhgb2104-2-i --width 720 -o ./checkpoints/slr_crosser_vu13p_alt.dcp  --laguna_sites $LAGUNA_SITES

java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.PipelineGenerator -v -l 10 -m 3 -n 10 -o ./checkpoints/pipeline.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/pipelineGen.py -v --direction 0 --distance 10 --depth 3 --width 10 -o ./checkpoints/pipeline_horizontal.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/pipelineGen.py -v --direction 1 --distance 10 --depth 3 --width 16 -o ./checkpoints/pipeline_vertical.dcp

java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.PipelineGeneratorWithRouting -v -m 2 -n 1 -t 4 -u 16 -o ./checkpoints/pipeline_w_route.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/pipelineGenWithRouting.py -v --direction 0 --distanceX 16 --distanceY 4 --depth 2 --width 1 -o ./checkpoints/pipeline_w_route_horizontal.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/pipelineGenWithRouting.py -v --direction 1 --distanceX 16 --distanceY 4 --depth 2 --width 1 -o ./checkpoints/pipeline_w_route_vertical.dcp

# vivado -mode gui -source ./tutorials/picoblazePreImpl.tcl
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/picoblazePreImpl.py
cat <<EOF >> ./picoblaze_pblocks.txt
RAMB36_X1Y47:RAMB36_X1Y47 RAMB18_X1Y94:RAMB18_X1Y95 SLICE_X13Y235:SLICE_X16Y239
RAMB36_X0Y47:RAMB36_X0Y47 RAMB18_X0Y94:RAMB18_X0Y95 SLICE_X7Y235:SLICE_X10Y239
RAMB36_X11Y47:RAMB36_X11Y47 RAMB18_X11Y94:RAMB18_X11Y95 SLICE_X157Y235:SLICE_X160Y239
EOF
# java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.PerformanceExplorer -y `which vivado` -z 24 -p Explore -r Explore -u 0,0.025 -d ./tmp -c clk -t 2.85 -i ./checkpoints/picoblaze_synth.dcp -b ./picoblaze_pblocks.txt
DST_DIR=./best
mkdir -p $DST_DIR
unzip -o -d $DST_DIR ./checkpoints/picoblaze_best.zip
# for pblock_idx in 0 1 2; do
#     SRC_DIR="./tmp/Explore_Explore_0_pblock${pblock_idx}"
#     cp $SRC_DIR/routed_0_metadata.txt "$DST_DIR/pblock${pblock_idx}_${pblock_idx}_metadata.txt"
#     cp $SRC_DIR/routed.dcp "$DST_DIR/pblock${pblock_idx}.dcp"
#     cp $SRC_DIR/routed.edf "$DST_DIR/pblock${pblock_idx}.edf"
# done
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.PicoBlazeArray --no_hand_placer ./best xcvu3p-ffvc1517-2-i ./checkpoints/picoblaze_array.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/picoblazeArray.py --no_hand_placer --src_dir ./best --part xcvu3p-ffvc1517-2-i --output ./checkpoints/picoblaze_array_alt.dcp
# vivado -mode gui -source ./tutorials/picoblazeCheckPreImpl.tcl

java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.examples.SLRCrosserGenerator -l LAGUNA_X20Y120 -b BUFGCE_X1Y80 -w 32 -p xcvu7p-flva2104-2-i -o ./checkpoints/slr_crosser_vu7p_32.dcp
java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/slrCrosserGenerator.py --laguna_sites LAGUNA_X20Y120 --bufgce_site BUFGCE_X1Y80 --width 32 --part xcvu7p-flva2104-2-i -o ./checkpoints/slr_crosser_vu7p_32_alt.dcp
# vivado -mode gui -source ./tutorials/slrCrosserCheck.tcl

cd eco
# ./gradlew -Dmain=ProbeRouter :run
./gradlew -Dmain=EcoInsertRouteDebug :run
./gradlew -Dmain=EcoRelocateRouteDebug :run
./gradlew -Dmain=EcoInsertRouteMultiDebug :run
./gradlew -Dmain=EcoInsertRouteDebugApp :fatJar
# vivado -mode gui -source ./src/eco_insert_route_debug.tcl
# java -cp ./rapidwright-2023.1.4-standalone-lin64.jar com.xilinx.rapidwright.util.Jython ./tutorials/ecoInsertRouteDebug.py ./checkpoints/boom_medium_routed.dcp ./checkpoints/fifo36_routed.dcp ./checkpoints/boom_medium_debug.dcp
# vivado -mode gui -source ./tutorials/ecoInsertRouteDebug.tcl
