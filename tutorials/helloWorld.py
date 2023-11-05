import os

from com.xilinx.rapidwright.design import Cell
from com.xilinx.rapidwright.design import Design
from com.xilinx.rapidwright.design import Net
from com.xilinx.rapidwright.design import PinType
from com.xilinx.rapidwright.design import Unisim
from com.xilinx.rapidwright.device import Device
from com.xilinx.rapidwright.router import Router
from com.xilinx.rapidwright.util   import FileTools

# Create a new empty design
design = Design("HelloWorld", Device.PYNQ_Z1)

# Create cells and place them
lut     = design.createAndPlaceCell("lut", Unisim.AND2, "SLICE_X100Y100/A6LUT")
button0 = design.createAndPlaceIOB("button0", PinType.IN,  "D19", "LVCMOS33")
button1 = design.createAndPlaceIOB("button1", PinType.IN,  "D20", "LVCMOS33")
led0    = design.createAndPlaceIOB("led0",    PinType.OUT, "R14", "LVCMOS33")

# Wire up the AND gate to buttons and LEDs
net0 = design.createNet("button0_IBUF")
net0.connect(button0, "O")
net0.connect(lut, "I0")

net1 = design.createNet("button1_IBUF")
net1.connect(button1, "O")
net1.connect(lut, "I1")

net2 = design.createNet("lut")
net2.connect(lut, "O")
net2.connect(led0, "I")

# Route intra-site connections
design.routeSites()

# Route inter-site connections
Router(design).routeDesign()

# Write out the placed and routed DCP
outputFileName = "checkpoints/HelloWorld-PYNQ_Z1.dcp"
design.writeCheckpoint(outputFileName)

# Print out where the DCP file was written
print("Wrote DCP '" + outputFileName + "' successfully")
