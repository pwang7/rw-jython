from com.xilinx.rapidwright.device import Device, TileTypeEnum
from com.xilinx.rapidwright.device.helper import TileColumnPattern

from pprint import pprint

partName = "xcvu3p-ffvc1517-2-i" # "xcvu13p-fhgb2104-2-i") #
device = Device.getDevice(partName)
crRowNum = device.getNumOfClockRegionRows()
crColNum = device.getNumOfClockRegionsColumns()
print("part=%s, clock region row Y#=%d, column X#=%d" % (partName, crRowNum, crColNum))

colMap = TileColumnPattern.genColumnPatternMap(device)
print("colMap size: %d" % len(colMap))
# pprint(colMap)

filtered = list(filter(
    lambda e: TileTypeEnum.BRAM in e.getKey() and e.getKey().size() == 1,
    colMap.entrySet()
))
print(filtered)
brams = [device.getTile(0, col) for col in filtered[0].getValue()]
pprint(brams)

filtered = list(filter(
    lambda e: TileTypeEnum.DSP in e.getKey() and e.getKey().size() == 1,
    colMap.entrySet()
))
print(filtered)
dsps = [device.getTile(0, col) for col in filtered[0].getValue()]
pprint(dsps)

filtered = list(filter(
    lambda e: TileTypeEnum.URAM_URAM_DELAY_FT in e.getKey() and e.getKey().size() == 1,
    colMap.entrySet()
))
print(filtered)
urams = [device.getTile(0, col) for col in filtered[0].getValue()]
pprint(urams)

filtered = list(filter(
    lambda e: TileTypeEnum.INT_INTF_L_PCIE4_TERM_T in e.getKey(), # and e.getKey().size() == 1,
    colMap.entrySet()
))
print(filtered)

filtered = list(filter(
    lambda e: TileTypeEnum.CMAC in e.getKey(), # and e.getKey().size() == 1,
    colMap.entrySet()
))
print(filtered)

filtered = list(filter(
    lambda e: TileTypeEnum.BRAM in e.getKey() and not TileTypeEnum.DSP in e.getKey() and e.getKey().size() == 5,
    colMap.entrySet()
))
filtered.sort(key=lambda x: x.getValue().size(), reverse=True)
pprint(filtered)

slrs = device.getSLRs()
pprint(slrs)
crs = device.getClockRegions()
pprint(crs)
tiles = device.getAllTiles()
# pprint(tiles)
tile = device.getTile(1, 94)
print("tile: %s" % tile)
