"""
RWRoute is a new open-source, timing-based router written
in RapidWright. It provides a substantial speedup to routing
when compared to Vivado's router, with a sacrifice in the
critical path delay. This may be useful for applications such
as quick design iterations.

This program not as much of a tutorial as much as it
is a simple wrapper over the RWRouter main function. To use
simply run 'python rwroute <input.dcp> <output.dcp>'.
Note that RWRoute currently only works with UltraScale+
devices.

This file also contains the code of RWRoute.main() converted
from Java into Python. This code is commented out, and can be
used to understand and manipulate the main function of RWRoute.
"""

import sys

# from java.lang import ClassLoader
# from org.python.google.common.reflect import ClassPath
# cl = ClassLoader.getSystemClassLoader()
# cp = ClassPath.from(cl)

from com.xilinx.rapidwright.rwroute import RWRoute
# print(sys.argv)
# RWRoute.main(sys.argv[1:])

###############################################################
# The following commented code is RWRoute.main converted into #
# python. This may be useful if one wants to play around with #
# the code.                                                   #
###############################################################

from com.xilinx.rapidwright.tests import CodePerfTracker
from com.xilinx.rapidwright.design import Design

if (len(sys.argv) < 3):
    print("USAGE: <input.dcp> <output.dcp> [options]")
    exit(-1)

perfTracker = CodePerfTracker(RWRoute.name, True)

# Reads in a design checkpoint
unroutedDesign = Design.readCheckpoint(sys.argv[1])
# Routes design checkpoint
startIdx = 3
routeArgs = sys.argv[startIdx : ]
print("routeArgs: ", routeArgs)
routedDesign = RWRoute.routeDesignWithUserDefinedArguments(unroutedDesign, routeArgs)

routedDesign.writeCheckpoint(sys.argv[2], perfTracker)
print("\nINFO: Write routed design\n " + sys.argv[2] + "\n")
