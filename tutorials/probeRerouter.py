import os
import subprocess

from com.xilinx.rapidwright.debug  import ProbeRouter
from com.xilinx.rapidwright.design import Design
from com.xilinx.rapidwright.util   import FileTools
from java.util import Collections
from java.util import HashMap
from pprint    import pprint

dcpDirName = "./checkpoints"

# read our checkpoint and keep a handle to the design
inputFileName = os.path.join(dcpDirName, "microblaze_with_ila_routed.dcp")
design = Design.readCheckpoint(inputFileName)

# keep a handle to our EDIF Netlist
netlist = design.getNetlist()
print "Finished loading our design!"


ProbeRouter.findILAs(design)
netlist.getCellInstFromHierName("u_ila_0").getCellPorts()


# Get the net connected to the probe port instance
net = netlist.getHierCellInstFromName("u_ila_0").getPortInst("probe0[4]").getHierarchicalNet()
# net = netlist.getCellInstFromHierName("u_ila_0").getPortInst("probe0[4]").getNet()

# Method to traverse netlist and extract net aliases from the netlist
hierNetAliases = netlist.getNetAliases(net)
netAliases = [hna.getHierarchicalNetName() for hna in hierNetAliases]
# netAliases = netlist.getNetAliases(net.getName())

# Extra Python code to print the net and aliases
Collections.sort(netAliases)
print "Connected net = '" + str(net) + "'\\n"
print "Net aliases ="
pprint([x.encode('ascii') for x in netAliases])


# Probe input name -> Desired net name to debug
probesMap = HashMap()
probesMap.put("u_ila_0/probe0[4]", "base_mb_i/axi_uartlite_0/U0/AXI_LITE_IPIF_I/I_SLAVE_ATTACHMENT/bus2ip_rnw_i")

# Invoke the probe re-router to un-route existing connection, route to net(s) specified
ProbeRouter.updateProbeConnections(design, probesMap)

outputFileName = "microblaze_updated_probe.dcp"
outputPath = os.path.join(dcpDirName, outputFileName)
design.writeCheckpoint(outputPath)
print "Wrote Probe re-routed DCP to: '" + outputPath + "'"


# if FileTools.isWindows():
#     os.system("START /B vivado " + outputFileName)
# else:
#     os.system("vivado "+outputFileName+" &")

print "If vivado fails to open or load, you could run the following command:"
print ""
print "    'vivado " + os.path.join(os.getcwd(), outputFileName) + "'"


# Get the net connected to the probe port instance
net = netlist.getCellInstFromHierName("u_ila_0").getPortInst("probe0[4]").getNet()

# Method to traverse netlist and extract net aliases from the netlist
netAliases = netlist.getNetAliases(net.getName())

# Extra Python code to print the net and aliases
Collections.sort(netAliases)
print "Connected net = '" + str(net) + "'\n"
print "Net aliases ="
pprint([x.encode('ascii') for x in netAliases])
