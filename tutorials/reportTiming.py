
import sys

from com.xilinx.rapidwright.examples import ReportTimingExample
# print(sys.argv)
# ReportTimingExample.main(sys.argv[1:])

from com.xilinx.rapidwright.design import Design
from com.xilinx.rapidwright.tests import CodePerfTracker
from com.xilinx.rapidwright.timing import TimingEdge
from com.xilinx.rapidwright.timing import TimingManager
from com.xilinx.rapidwright.timing import TimingVertex
from org.jgrapht import GraphPath

if (len(sys.argv) < 2):
    print("USAGE: <dcp_file_name>")
    exit(-1)

perfTracker = CodePerfTracker(ReportTimingExample.name)
perfTracker.useGCToTrackMemory(True)

# Read in an example placed and routed DCP
perfTracker.start("Read DCP")
design = Design.readCheckpoint(sys.argv[1], CodePerfTracker.SILENT)

# Instantiate and populate the timing manager for the design
perfTracker.stop().start("Create TimingManager")
timingManager = TimingManager(design)

# Get and print out worst data path delay in design
perfTracker.stop().start("Get Max Delay")
criticalPath = timingManager.getTimingGraph().getMaxDelayPath()

# Print runtime summary
perfTracker.stop().printSummary()
pathDelay = criticalPath.getWeight()
print("\nCritical path: %.2f ps" % pathDelay)
print("\nPath details:")
print(criticalPath.toString().replace(",", ",\n"))
