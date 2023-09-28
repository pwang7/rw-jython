import argparse
import os
import sys

from com.xilinx.rapidwright.examples import PipelineGenerator

from com.xilinx.rapidwright.design import Cell, ConstraintGroup, Design, Net, NetType, SiteInst, Unisim
from com.xilinx.rapidwright.design.blocks import PBlock
from com.xilinx.rapidwright.device import BEL, Device, Part, PartNameTools, Site, SiteTypeEnum, Tile
from com.xilinx.rapidwright.edif import EDIFCell, EDIFDirection, EDIFNet, EDIFPort, EDIFTools, EDIFValueType
from com.xilinx.rapidwright.router import Router
from com.xilinx.rapidwright.tests import CodePerfTracker
from com.xilinx.rapidwright.util import MessageGenerator

from java.lang import Class, RuntimeException
from java.lang.reflect import Field

def createOptionParser():
    parser = argparse.ArgumentParser(description='Jython Command-line Argument Parser')

    # Add arguments
    parser.add_argument('-p', '--part', default='xcvu3p-ffvc1517-2-e', help='device part')
    parser.add_argument('-d', '--design', default='pipeline', help='design name')
    parser.add_argument('-o', '--output', default='pipeline.dcp', help='output DCP file name')
    parser.add_argument('-c', '--clock', default='clk', help='clock name')
    parser.add_argument('-x', '--clock_period', default=1.291, type=float, help='clock period') # 775MHz

    parser.add_argument('-n', '--width', default=10, type=int, help='width')
    parser.add_argument('-m', '--depth', default=3, type=int, help='depth')
    parser.add_argument('-l', '--distance', default=10, type=int, help='distance')

    parser.add_argument('-e', '--direction', default=0, type=int, help='direction, 0=horizontal, 1=vertical')

    parser.add_argument('-s', '--slice_site', default='SLICE_X42Y70', help='lower left slice to be used for pipeline')
    parser.add_argument('-v', '--verbose', action='store_const', const=True, default=False, help='verbose')

    return parser

# Extract program options
parser = createOptionParser()
opts = parser.parse_args()

perfTracker = CodePerfTracker(PipelineGenerator.name, True)
perfTracker.start("Init")

partName = opts.part
designName = opts.design
outputDCPFileName = opts.output
clkName = opts.clock
clkPeriodConstraint = opts.clock_period

width = opts.width
depth = opts.depth
distance = opts.distance
sliceName = opts.slice_site

directionEnum = Class.forName("%s$direction" % PipelineGenerator.name)
# print(dir(directionEnum))
directionEnumValues = directionEnum.getEnumConstants()
# print(directionEnumValues)
(VERTICAL, HORIZONTAL) = directionEnumValues
direction = VERTICAL if opts.direction else HORIZONTAL
print("direction=%s" % direction)

# Perform some error checking on inputs
part = PartNameTools.getPart(partName)
if not part.isUltraScalePlus() and not part.isUltraScale(): # part.isVersal() or part.isSeries7():
    raise RuntimeException(
        "ERROR: Invalid/unsupported part %s, only work for UltraScale or UltraScale+ devices" % partName
    )

design = Design(designName, partName)
design.setAutoIOBuffers(False)
device = design.getDevice()

perfTracker.stop().start("Create Pipeline")
pipelineSlice = device.getSite(sliceName)
PipelineGenerator.createPipeline(design, pipelineSlice, width, depth, distance, direction, True)

# Add a clock constraint
tcl = "create_clock -name %s -period %.2f [get_ports %s]" % (clkName, clkPeriodConstraint, clkName)
print(tcl)
design.addXDCConstraint(ConstraintGroup.LATE, tcl)
design.setAutoIOBuffers(False)

perfTracker.stop()
if outputDCPFileName != "/dev/null":
    design.writeCheckpoint(outputDCPFileName, perfTracker)
    if opts.verbose:
        print("Wrote final DCP: " + outputDCPFileName)

