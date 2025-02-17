"""
This tutorial shows how to use RapidWright to extract some basic
information of a design. It also does some post-processing (plotting
the info in matplotlib) to show some of the advantages of using
RapidWright with Python.
"""

#import matplotlib.pyplot as plt

from com.xilinx.rapidwright.design import Design

design = Design.readCheckpoint("checkpoints/hash_circuit_routed.dcp", "checkpoints/hash_circuit_routed.edf")

netSizes = {}
maxSize = 0

for net in design.getNets():
    netName = net.toString()
    if net.isStaticNet():
        continue

    size = len(net.getPIPs())
    if size in netSizes:
        netSizes[size] += 1
    else:
        netSizes[size] = 1

    if size > maxSize:
        maxSize = size
        largestNet = net



print("The largest net is {} with {} PIPs.".format(largestNet, maxSize))

#plt.bar(netSizes.keys(), netSizes.values(), 1.0, color="g")
#plt.yscale('log')
#plt.show()
