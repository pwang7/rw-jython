
import sys

from com.xilinx.rapidwright.rwroute import PartialRouter
# print(sys.argv)
# PartialRouter.main(sys.argv[1:])

from com.xilinx.rapidwright.tests import CodePerfTracker
from com.xilinx.rapidwright.design import Design

if (len(sys.argv) < 4):
    print("USAGE: <input.dcp> <output.dcp> [options]")
    exit(-1)

perfTracker = CodePerfTracker(PartialRouter.name, True)

#Reads in a design checkpoint
unroutedDesign = Design.readCheckpoint(sys.argv[1])
#Routes design checkpoint
startIdx = 3
routeArgs = sys.argv[startIdx : ]
print("routeArgs: ", routeArgs)
routedDesign = PartialRouter.routeDesignWithUserDefinedArguments(unroutedDesign, routeArgs)

routedDesign.writeCheckpoint(sys.argv[2], perfTracker)
print("\nINFO: Write routed design\n " + sys.argv[2] + "\n")
