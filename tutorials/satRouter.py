import os

from com.xilinx.rapidwright.router import SATRouter
from com.xilinx.rapidwright.design import Design
from com.xilinx.rapidwright.device import Device
from com.xilinx.rapidwright.design.blocks import PBlock

dcpDirName = "./checkpoints"

# Difficult Congestion Example:

# Load our design that failed to route in Vivado
inputFileName = os.path.join(dcpDirName, "reduce_or_routed_7overlaps.dcp")
design = Design.readCheckpoint(inputFileName)

# We will unroute all the nets (except clk, GND, VCC)
for net in design.getNets():
    if net.isClockNet() or net.isStaticNet():
        continue
    net.unroute()

# Load the same pblock used in the Vivado design for area constraint
# Note: the SAT Router will treat the pblock as if the CONTAIN_ROUTING
#       flag was set in Vivado
pblock = PBlock(design.getDevice(),"SLICE_X108Y660:SLICE_X111Y664")
satRouter = SATRouter(design, pblock, False)

# Here is where we actually invoke the external SAT router
# a few log files will be generated and this processs can take
# several minutes.  This command will also process the output
# result from the SAT router and import it back into the RapidWright
# design.
satRouter.route()

outputFileName = "reduce_or_sat_routed.dcp"
outputPath = os.path.join(dcpDirName, outputFileName)
design.writeCheckpoint(outputPath)
print("Wrote DCP '" + outputPath + "' successfully")


# Partial Routing Example:

# Load the same design used in the ILA Probe Re-router example
# we will unroute the design, so that we can route a portion
# of it with the SAT router
inputFileName = os.path.join(dcpDirName, "microblaze_with_ila_routed.dcp")
design = Design.readCheckpoint(inputFileName)
design.unrouteDesign()


# We will choose the area to be routed -- The SAT Router
# automatically determines which nets are physically within
# the pblock and will include them in the routing problem
# to the SAT Router
pblock = PBlock(design.getDevice(), "SLICE_X68Y134:SLICE_X72Y149")
satRouter = SATRouter(design, pblock)

# Here is where we actually invoke the external SAT router
# a few log files will be generated and this processs can take
# several minutes.  This command will also process the output
# result from the SAT router and import it back into the RapidWright
# design.
satRouter.route()

outputFileName = "microblaze_partially_sat_routed.dcp"
outputPath = os.path.join(dcpDirName, outputFileName)
design.writeCheckpoint(outputPath)
print("Wrote DCP '" + outputPath + "' successfully")
