
import sys

from com.xilinx.rapidwright.util import MakeBlackBox
# print(sys.argv)
# MakeBlackBox.main(sys.argv[1:])

from com.xilinx.rapidwright.design import Design
from com.xilinx.rapidwright.design import DesignTools
from com.xilinx.rapidwright.tests import CodePerfTracker

if (len(sys.argv) < 4):
    print("USAGE: <input.dcp> <output.dcp> <cellinst-to-be-blackboxed> [another-cellinst-to-be-blackboxed] [...]")
    exit(-1)

perfTracker = CodePerfTracker(MakeBlackBox.name)

perfTracker.start("Read DCP")
design = Design.readCheckpoint(sys.argv[1], CodePerfTracker.SILENT)
perfTracker.stop().start("Blackbox cell(s)")

startIdx = 3
for cellName in sys.argv[3:]:
    DesignTools.makeBlackBox(design, cellName)

# Necessary to make the design place-able by Vivado later
DesignTools.prohibitPartialHalfSlices(design)

perfTracker.stop().start("Write DCP")
design.writeCheckpoint(sys.argv[2], CodePerfTracker.SILENT)
perfTracker.stop().printSummary()
