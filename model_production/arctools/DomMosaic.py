#!/usr/bin/python
# -*- coding: UTF-8 -*-

import arcpy, os
from arcpy import env

env.workspace = r'G:\南通\凤凰广场\DOM\Production_11'
folderPath = r'G:\南通\凤凰广场\DOM'
imageName = 'ntCity_flight01'

imageDs = arcpy.ListFiles()
imLists = []
for im in imageDs:
    if 'tif' == im.split('.')[-1]:
        print(im)
        imLists.append(im)
print(imLists)

gdbNew = 'dom_mosaic.gdb'
arcpy.CreateFileGDB_management(folderPath, gdbNew)
arcpy.MosaicToNewRaster_management(imLists, os.path.join(folderPath, gdbNew), imageName, imLists[0], '8_BIT_UNSIGNED',
                                   None, 3, 'LAST', 'FIRST')

#
env.workspace = r'G:\南通\圆融广场\DOM\Production_11'
folderPath = r'G:\南通\圆融广场\DOM'
imageName = 'ntCity_flight02'

imageDs = arcpy.ListFiles()
imLists = []
for im in imageDs:
    if 'tif' == im.split('.')[-1]:
        print(im)
        imLists.append(im)
print(imLists)

gdbNew = 'dom_mosaic.gdb'
arcpy.CreateFileGDB_management(folderPath, gdbNew)
arcpy.MosaicToNewRaster_management(imLists, os.path.join(folderPath, gdbNew), imageName, imLists[0], '8_BIT_UNSIGNED',
                                   None, 3, 'LAST', 'FIRST')
