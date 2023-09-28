import argparse
import os
import sys

from com.xilinx.rapidwright.examples import PicoBlazeArray
from com.xilinx.rapidwright.tests import CodePerfTracker
from com.xilinx.rapidwright.util import FileTools

from java.io import File
from java.lang import RuntimeException
from java.nio.file import Paths

def createOptionParser():
    parser = argparse.ArgumentParser(description='Jython Command-line Argument Parser')

    # Add arguments
    parser.add_argument('-d', '--src_dir', default='./', help="input source directory")
    parser.add_argument('-o', '--output', default='picoblaze_array.dcp', help="output DCP file name")
    parser.add_argument('-p', '--part', default='xcvu3p-ffvc1517-2-e', help="device part")

    parser.add_argument('-b', '--block_placer', action='store_true', default=False, help="Place Instances via Block Placer")
    parser.add_argument('-n', '--no_hand_placer', action='store_true', default=False, help="Disable Hand Placer")
    parser.add_argument('-i', '--impls', action='store_true', default=False, help="Use Impls instead of Modules")

    return parser

# Extract program options
parser = createOptionParser()
opts = parser.parse_args()

# handPlacer = opts.hand_placer
handPlacer = not opts.no_hand_placer
useImples = opts.impls
blockPlacer = opts.block_placer

if not os.path.isdir(opts.src_dir):
    raise RuntimeException("ERROR: Couldn't read directory: %s" % opts.src_dir)

srcDir = File(opts.src_dir)
outName = Paths.get(opts.output)
part = opts.part

print(
    "args: handPlacer=%s, useImples=%s, blockPlacer=%s, srcDir=%s, outName=%s, part=%s" %
    (handPlacer, useImples, blockPlacer, srcDir, outName, part)
)

perfTracker = CodePerfTracker(PicoBlazeArray.name, True)
perfTracker.useGCToTrackMemory(True)

creator = PicoBlazeArray.makeImplsCreator() if useImples else PicoBlazeArray.makeModuleCreator()
design = creator.createDesign(srcDir, part, perfTracker)

if blockPlacer:
    perfTracker.stop().start("BlockPlacer")
    graphDataFile = FileTools.replaceExtension(outName, "_graph.tsv")
    creator.createPlacer(design, graphDataFile).placeDesign(False)

creator.lowerToModules(design, perfTracker)

if handPlacer:
    perfTracker.stop().start("Hand Placer")
    print("start hand placer")
    # Avoid loading GUI library if no using hand placer
    from com.xilinx.rapidwright.placer.handplacer import HandPlacer
    HandPlacer.openDesign(design)
    print("finish hand placer")

perfTracker.stop().start("Write DCP")

design.setAutoIOBuffers(False)
design.addXDCConstraint("create_clock -name clk -period 2.850 [get_nets clk]")
design.writeCheckpoint(outName, CodePerfTracker.SILENT)
perfTracker.stop().printSummary()
