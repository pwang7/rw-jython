import os

from com.xilinx.rapidwright.design import Design
from com.xilinx.rapidwright.design import NetType
from com.xilinx.rapidwright.design import Unisim
from com.xilinx.rapidwright.device import Device
from com.xilinx.rapidwright.edif   import EDIFCell
from com.xilinx.rapidwright.edif   import EDIFCellInst
from com.xilinx.rapidwright.edif   import EDIFDirection
from com.xilinx.rapidwright.edif   import EDIFNet
from com.xilinx.rapidwright.edif   import EDIFNetlist
from com.xilinx.rapidwright.edif   import EDIFPort
from com.xilinx.rapidwright.edif   import EDIFTools
from com.xilinx.rapidwright.util   import FileTools

outputDirName = "./checkpoints"

# Step 1: Initialize Design & Create Flip Flops

# Initialize an empty design
design = Design("And2Example", Device.PYNQ_Z1)

# We set this to make the DCP Out-of-context -- otherwise Vivado
#  will auto insert buffers on all the inputs
design.setAutoIOBuffers(False)

# extracting some references for convenience
netlist = design.getNetlist()
top = netlist.getTopCell()

# Create some convenience variables
inDir = EDIFDirection.INPUT
outDir = EDIFDirection.OUTPUT
clk = "clk"
pinNames = [clk,   "in0", "in1", "out0"]
pinDirs  = [inDir, inDir, inDir, outDir]

# Make sure FDRE is added to the primitive library
ff = Design.getUnisimCell(Unisim.FDRE)
ff = netlist.getHDIPrimitivesLibrary().addCell(ff)

# Let's create a FF for each top level pin (except clk)
for pin in pinNames:
    if pin == clk: continue
    ffInst = top.createChildCellInst(pin + "FF", ff)

# Write out current progress
outputFileName = "and2example_1_just_flops.dcp"
outputPath = os.path.join(outputDirName, outputFileName)
design.writeCheckpoint(outputPath)
print("Wrote DCP '" + outputPath + "' successfully")


# Step 2: Create Top-level Ports and Nets

# Create top level ports and connect them to flip flops
for name, direction in zip(pinNames, pinDirs):
    # creates a new net in the EDIFCell 'top'
    net = top.createNet(name)
    # creates a new port on the EDIFCell 'top'
    port = top.createPort(name,direction, 1)
    # connects the top-level port to the net
    net.createPortInst(port)

    # skip the top-level clk input for the last step
    if name == clk: continue

    # connects the net to the flip flop
    ffInst = top.getCellInst(name+"FF")
    net.createPortInst("D" if direction == inDir else "Q", ffInst)

# Write out current progress
outputFileName = "and2example_2_flops_and_ports.dcp"
outputPath = os.path.join(outputDirName, outputFileName)
design.writeCheckpoint(outputPath)
print("Wrote DCP '" + outputPath + "' successfully")


# Step 3: Connect clk, GND and VCC to Flip Flops

# Gets or creates appropriate GND/VCC sources and nets in an EDIFCell
gnd = EDIFTools.getStaticNet(NetType.GND, top, netlist)
vcc = EDIFTools.getStaticNet(NetType.VCC, top, netlist)

# Connect clk, VCC/GND to CE/RST on flip flops
for name in pinNames:
    if name == clk: continue
    ffInst = top.getCellInst(name+"FF")
    top.getNet(clk).createPortInst("C", ffInst);
    gnd.createPortInst("R", ffInst);
    vcc.createPortInst("CE", ffInst);

# Write out current progress
outputFileName = "and2example_3_flops_and_ports.dcp"
outputPath = os.path.join(outputDirName, outputFileName)
design.writeCheckpoint(outputPath)
print("Wrote DCP '" + outputPath + "' successfully")


# Step 4: Create Level of Hierarchy and AND2 Instance

# Create hierarchical cell and instance for AND2
and2Wrapper = EDIFCell(netlist.getWorkLibrary(), "and2Wrapper")
and2WrapperInst = top.createChildCellInst("and2WrapperInst", and2Wrapper)

# Create LUT2 AND gate and instance
and2 = Design.getUnisimCell(Unisim.AND2)
netlist.getHDIPrimitivesLibrary().addCell(and2)
and2Inst = and2Wrapper.createChildCellInst("and2Inst", and2)

# Make final connections between flip flops and wrapper/LUT
for name, direction in zip(pinNames,pinDirs):
    if name == clk: continue
    ffInst = top.getCellInst(name+"FF")

    # creates a port for our custom and2Wrapper cell to pass in each flip flop signal
    port = and2Wrapper.createPort(name,direction, 1)

    # create a net and connect each flip flop to and2Wrapper
    net = top.createNet(name+"_2")
    net.createPortInst("Q" if direction == inDir else "D", ffInst)
    net.createPortInst(port, and2WrapperInst)

    # create a net inside the and2Wrapper and connect it to the AND2/LUT2
    innerNet = and2Wrapper.createNet(name)
    innerNet.createPortInst(port)
    innerNet.createPortInst("O" if name == "out0" else name.replace("in","I"), and2Inst)

# Write out current progress
outputFileName = "and2example_4_flops_and_lut.dcp"
outputPath = os.path.join(outputDirName, outputFileName)
design.writeCheckpoint(outputPath)
print("Wrote DCP '" + outputPath + "' successfully")
