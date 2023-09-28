import argparse

from com.xilinx.rapidwright.examples import SLRCrosserGenerator

from com.xilinx.rapidwright.design import ConstraintGroup, Design
from com.xilinx.rapidwright.device import Device, Part, PartNameTools, Site
from com.xilinx.rapidwright.router import Router
from com.xilinx.rapidwright.tests import CodePerfTracker

from java.util import ArrayList

def createOptionParser():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='Jython Command-line Argument Parser')

    # Add arguments
    parser.add_argument('-p', '--part', default='xcvu9p-flgb2104-2-i', help="UltraScale+ Part Name")
    parser.add_argument('-d', '--design', default='slr_crosser', help="Design Name")
    parser.add_argument('-t', '--tx_clk_wire', default='GCLK_B_0_0', help="INT clk Laguna TX flops")
    parser.add_argument('-r', '--rx_clk_wire', default='GCLK_B_0_1', help="INT clk Laguna RX flops")
    parser.add_argument('-o', '--output', default='slr_crosser.dcp', help="Output DCP File Name")
    parser.add_argument('-b', '--bufgce_site', default='BUFGCE_X0Y218', help="Clock BUFGCE site name")
    parser.add_argument('-y', '--bufgce_inst', default='BUFGCE_inst', help="BUFGCE cell instance name")
    parser.add_argument('-c', '--clock', default='clk', help="Clk net name")
    parser.add_argument('-a', '--clk_in', default='clk_in', help="Clk input net name")
    parser.add_argument('-u', '--clk_out', default='clk_out', help="Clk output net name")
    parser.add_argument('-x', '--clk_period', default=1.333, type=float, help="Clk period constraint (ns)")
    parser.add_argument('-w', '--width', default=512, type=int, help="SLR crossing bus width")
    parser.add_argument('-i', '--input_prefix', default='input', help="Input bus name prefix")
    parser.add_argument('-q', '--output_prefix', default='output', help="Output bus name prefix")
    parser.add_argument('-n', '--north_prefix', default='_north', help="North bus name suffix")
    parser.add_argument('-s', '--south_prefix', default='_south', help="South bus name suffix")
    parser.add_argument('-l', '--laguna_sites', default='LAGUNA_X2Y120', help="Comma separated list of Laguna sites for each SLR crossing")
    parser.add_argument('-z', '--use_common_centroid', action='store_true', default=False, help="Use common centroid")
    parser.add_argument('-v', '--verbose', action='store_true', default=False, help="Print verbose output")

    return parser

# Extract program options
parser = createOptionParser()
opts = parser.parse_args()

partName = opts.part
designName = opts.design
txClkWire = opts.tx_clk_wire
rxClkWire = opts.rx_clk_wire
outputDCPFileName = opts.output
bufgceSiteName = opts.bufgce_site
bufgceInstName = opts.bufgce_inst
clkName = opts.clock
clkInName = opts.clk_in
clkOutName = opts.clk_out
clkPeriodConstraint = opts.clk_period
busWidth = opts.width
inputPrefix = opts.input_prefix
outputPrefix= opts.output_prefix
northSuffix = opts.north_prefix
southSuffix = opts.south_prefix
lagunaNames = opts.laguna_sites.split(",")
commonCentroid = opts.use_common_centroid
verbose = opts.verbose

perfTracker = CodePerfTracker(SLRCrosserGenerator.name, True).start("Init")

# Perform some error checking on inputs
part = PartNameTools.getPart(partName)
if part is None or not part.isUltraScalePlus():
    raise RuntimeException("ERROR: Invalid/unsupport part %s" % partName)

design = Design(designName, partName)
design.setAutoIOBuffers(False)
dev = design.getDevice()

if dev.getSite(bufgceSiteName) is None:
    raise RuntimeException(
        "ERROR: BUFGCE site '%s' not found on part %s" % (bufgceSiteName, partName)
    )

for lagunaSite in lagunaNames:
    site = dev.getSite(lagunaSite)
    if site is None:
        raise RuntimeException(
            "ERROR: LAGUNA site '%s' not found on part %s" % (lagunaSite, partName)
        )

    curClkRegion = site.getTile().getClockRegion()
    southernNeighborSite = site.getNeighborSite(0, -1)
    if southernNeighborSite is not None:
        below = southernNeighborSite.getTile().getClockRegion()
        if curClkRegion.equals(below) or (curClkRegion.getRow() - below.getRow() == 1) or (site.getInstanceX() % 2 != 0):
            raise RuntimeException("ERROR: Laguna site '%s' is not a bottom row LAGUNA site." % site)

busNames = ArrayList()
for idx in range(len(lagunaNames)):
    busNames.add(inputPrefix + str(idx) + northSuffix + "," + outputPrefix + str(idx) + northSuffix)
    busNames.add(inputPrefix + str(idx) + southSuffix + "," + outputPrefix + str(idx) + southSuffix)

perfTracker.stop().start("Create Netlist")
SLRCrosserGenerator.createBUFGCEAndFlops(design, busWidth, busNames, clkName, clkInName, clkOutName, bufgceInstName)
SLRCrosserGenerator.placeBUFGCE(design, dev.getSite(bufgceSiteName), bufgceInstName)

perfTracker.stop().start("Place SLR Crossings")
idx = 0
for lagunaStart in lagunaNames:
    northLagunaStartSite = dev.getSite(lagunaStart)
    northBusName = busNames.get(idx + 0).replace(",", "_")
    southBusName = busNames.get(idx + 1).replace(",", "_")
    SLRCrosserGenerator.placeAndRouteSLRCrossing(design, northLagunaStartSite, northBusName, southBusName, busWidth)
    idx += 2

perfTracker.stop().start("Custom Clock Route")
SLRCrosserGenerator.customRouteSLRCrossingClock(design, clkName, lagunaNames, txClkWire, rxClkWire, commonCentroid)

perfTracker.stop().start("Route VCC/GND")
router = Router(design)
router.routeStaticNets()
perfTracker.stop()

# Add a clock constraint
design.addXDCConstraint(
    ConstraintGroup.LATE,
    "create_clock -name %s -period %s [get_nets %s]" % (clkName, clkPeriodConstraint, clkName)
)
design.addXDCConstraint(ConstraintGroup.LATE, "create_property MAX_PROG_DELAY net")
design.addXDCConstraint(ConstraintGroup.LATE, "set_property MAX_PROG_DELAY 0 [get_nets %s]" % clkName)

design.writeCheckpoint(outputDCPFileName, perfTracker)
print("Wrote final DCP: %s" % outputDCPFileName)
