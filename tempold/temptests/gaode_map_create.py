#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd

import arcpy
from arcpy import env

# env.workspace = r"D:\myDocuments\Documents\ArcGIS\Projects\MyProject\jsCloud_20180718.gdb"
# inRaster = "njCity_hyl_DSM"
# inRaster_bound = r"D:\myDocuments\Documents\ArcGIS\Projects\MyProject\gaode_DSM.gdb\hyl_bound"
# outPath = r"D:\myDocuments\Documents\ArcGIS\Projects\MyProject\gaode_DSM.gdb"
# outRaster = outPath + "/" + "hyl" + "_" + "Clip01"
# arcpy.Clip_management(inRaster, inRaster_bound, outRaster)

# env.outputCoordinateSystem = arcpy.SpatialReference("WGS 1984")


# env.workspace = arcpy.GetParameterAsText(0)
env.workspace = r'D:\myDocuments\Desktop\ToolTests\flight_modify.gdb'
for img in arcpy.ListRasters():
    RasterTop = arcpy.GetRasterProperties_management(img, "TOP")
    RasterRight = arcpy.GetRasterProperties_management(img, "RIGHT")
    RasterLeft = arcpy.GetRasterProperties_management(img, "LEFT")
    RasterBottom = arcpy.GetRasterProperties_management(img, "BOTTOM")
    arcpy.AddMessage('{0},{1},{2},{3},{4}'.format(img, RasterTop, RasterLeft, RasterBottom, RasterRight))
