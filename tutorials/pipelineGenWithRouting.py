import argparse

from com.xilinx.rapidwright.examples import PipelineGeneratorWithRouting

from com.xilinx.rapidwright.design import Cell, ConstraintGroup, Design, Net, NetType, SiteInst, Unisim
from com.xilinx.rapidwright.design.blocks import PBlock
from com.xilinx.rapidwright.device import BEL, Device, Part, PartNameTools, Site, SiteTypeEnum, Tile
from com.xilinx.rapidwright.edif import EDIFCell, EDIFDirection, EDIFNet, EDIFPort, EDIFTools, EDIFValueType
# from com.xilinx.rapidwright.router import Router
from com.xilinx.rapidwright.rwroute import RWRoute
from com.xilinx.rapidwright.tests import CodePerfTracker
from com.xilinx.rapidwright.timing import GroupDelayType, GroupDistance, TimingDirection, TimingEdge, TimingGraph, TimingGroup, TimingManager, TimingModel, TimingVertex
from com.xilinx.rapidwright.util import MessageGenerator

from java.lang import Class, RuntimeException
from java.lang.reflect import Field

def createOptionParser():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Jython Command-line Argument Parser')

    # Add arguments
    parser.add_argument('-p', '--part', default='xcvu3p-ffvc1517-2-e', help='device part')
    parser.add_argument('-d', '--design', default='pipeline', help='design name')
    parser.add_argument('-o', '--output', default='pipeline.dcp', help='output DCP file name')
    parser.add_argument('-c', '--clock', default='clk', help='clock name')
    parser.add_argument('-x', '--clock_period', default=(1000.0 / 775), type=float, help='clock period') # 775MHz

    parser.add_argument('-n', '--width', default=1, type=int, help='width')
    parser.add_argument('-m', '--depth', default=2, type=int, help='depth')
    parser.add_argument('-t', '--distanceX', default=4, type=int, help='distance X')
    parser.add_argument('-u', '--distanceY', default=16, type=int, help='distance Y')

    parser.add_argument('-e', '--direction', default=0, type=int, help='direction, 0=horizontal, 1=vertical')
    parser.add_argument('-r', '--non_timing_route', action='store_const', const=True, default=False, help='non-timing driven route')

    parser.add_argument('-s', '--slice_site', default='SLICE_X10Y4', help='lower left slice to be used for pipeline')
    parser.add_argument('-v', '--verbose', action='store_const', const=True, default=False, help='verbose')

    return parser

# Extract program options
parser = createOptionParser()
opts = parser.parse_args()

perfTracker = CodePerfTracker(PipelineGeneratorWithRouting.name, True)
perfTracker.start("Init")

partName = opts.part
designName = opts.design
outputDCPFileName = opts.output
clkName = opts.clock
clkPeriodConstraint = opts.clock_period

width = opts.width
depth = opts.depth
distanceX = opts.distanceX
distanceY = opts.distanceY
sliceName = opts.slice_site

directionEnum = Class.forName("%s$direction" % PipelineGeneratorWithRouting.name)
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
shouldRoute = True
PipelineGeneratorWithRouting.createPipeline(design, pipelineSlice, width, depth, distanceX, distanceY, direction, shouldRoute, not opts.non_timing_route)
# print("opts.non_timing_route=%s" % opts.non_timing_route)
routedDesign = RWRoute.routeDesignFullNonTimingDriven(design) if opts.non_timing_route else design

# Add a clock constraint
tcl = "create_clock -name %s -period %.2f [get_ports %s]" % (clkName, clkPeriodConstraint, clkName)
print(tcl)
routedDesign.addXDCConstraint(ConstraintGroup.LATE, tcl)
routedDesign.setAutoIOBuffers(False)

if opts.verbose:
    # Reporting timing on the routed design
    tm = TimingManager(routedDesign)
    dm1 = tm.getTimingModel()
    tg = tm.getTimingGraph()

    # GraphPath<TimingVertex, TimingEdge>
    maxPath = tg.getMaxDelayPath()
    maxDelay = maxPath.getWeight()
    clkPeriodPs = clkPeriodConstraint * 1000
    tg.setTimingRequirement(clkPeriodPs)

    print(
        "Requested frequency: %.4f MHz for a period of %.4f ps" % (1000.0 / clkPeriodConstraint, clkPeriodPs)
    )
    print("Max net delay: %.4f ps" % maxDelay)
    print("Worst slack: %.4f ps" % tg.getWorstSlack())

    print("The following is a print out of the TimingGroups for the critical path:")

    # TimingEdge
    for edge in maxPath.getEdgeList():
        dm1.debug = True
        dm1.verbose = True
        tg.debug = True

        if edge.getNet(): # skip below if the net is null, e.g. edges from/to the timing graph's
            # "SuperSource" and "SuperSink"
            dm1.calcDelay(edge.getNet().getSource(), edge.getNet().getSinkPins().get(0), edge.getNet())

            print(
                "Critical path TimingEdge/physical net name: %s,\n\t net_delay: %.4f ps,\n\t logic_delay: %.4f ps,\n\t --------------------\n\t total_delay: %.4f ps\n" %
                (edge.getNet(), edge.getNetDelay(), edge.getLogicDelay(), edge.getDelay())
            )

    tg.generateGraphvizDotVisualization("pipeline.dot")

perfTracker.stop()
if outputDCPFileName != "/dev/null":
    design.writeCheckpoint(outputDCPFileName, perfTracker)
    if opts.verbose:
        print("Wrote final DCP: " + outputDCPFileName)

