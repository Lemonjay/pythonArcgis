#!/usr/bin/python
# -*- coding: UTF-8 -*-
import arcpy
from arcpy import env

# 测试代码
env.overwriteOutput = True
inRaster = r"D:\myDocuments\Desktop\DataReorder\DSM_Copy\yzCity_DSM.gdb\yzCity_cpH_DSM"
CityName = "yzCity"
BuildingName = "cpH"
env.workspace = r"D:\myDocuments\Desktop\DataReorder\rasterTest.gdb"
outPath = env.workspace
spatial_reference = r"D:\myDocuments\Desktop\DataReorder\WGS_1984_Web_Mercator_Auxiliary_Sphere.prj"

out_Raster = CityName + "_" + BuildingName + "_DSM"
inRaster_CellSize = arcpy.GetRasterProperties_management(inRaster, "CELLSIZEX")
arcpy.AddMessage(inRaster_CellSize)
arcpy.AddMessage(type(inRaster_CellSize))

Raster_BandCounts = arcpy.GetRasterProperties_management(inRaster, "BANDCOUNT")
arcpy.CreateRasterDataset_management(outPath, out_Raster, 0.06, "8_BIT_UNSIGNED",
                                     spatial_reference, Raster_BandCounts)
# arcpy.CopyRaster_management(inRaster, out_Raster, background_value=0, nodata_value=0)
arcpy.Mosaic_management(inRaster, out_Raster, background_value=0, nodata_value=0)
# ——————————————————————————————————————————
