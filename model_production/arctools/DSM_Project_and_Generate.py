#!/usr/bin/python
# -*- coding: UTF-8 -*-
import arcpy
from arcpy import env

# 测试代码
# env.overwriteOutput = True
# inRaster = r"D:\myDocuments\Desktop\DataReorder\DSM_Copy\yzCity_DSM.gdb\yzCity_cpH_DSM"
# CityName = "yzCity"
# BuildingName = "cpH"
# env.workspace = r"D:\myDocuments\Desktop\DataReorder\rasterTest.gdb"
# outPath = env.workspace
# spatial_reference = r"D:\myDocuments\Desktop\DataReorder\WGS_1984_Web_Mercator_Auxiliary_Sphere.prj"
#
# out_Raster = CityName + "_" + BuildingName + "_DSM"
# arcpy.CreateRasterDataset_management(outPath, out_Raster, 0.06, "8_BIT_UNSIGNED",
#                                      spatial_reference, 4)
# # arcpy.CopyRaster_management(inRaster, out_Raster, background_value=0, nodata_value=0)
# arcpy.Mosaic_management(inRaster, out_Raster, background_value=0, nodata_value=0)
# ——————————————————————————————————————————

# 执行代码
env.overwriteOutput = True
inRaster = arcpy.GetParameterAsText(0)
CityName = arcpy.GetParameterAsText(1)
BuildingName = arcpy.GetParameterAsText(2)
env.workspace = arcpy.GetParameterAsText(3)
spatial_reference = arcpy.GetParameterAsText(4)

out_Raster = CityName + "_" + BuildingName + "_DSM"
out_Raster_Low = CityName + "_" + BuildingName + "_DSM" + "_Low"
outPath = env.workspace

# Project Raster by coordinate system 3857
arcpy.ProjectRaster_management(inRaster, out_Raster, spatial_reference)
arcpy.AddMessage(out_Raster + " Completed")
Raster_BandCounts = arcpy.GetRasterProperties_management(inRaster, "BANDCOUNT")  # Raster Input BandCount
inRaster_CellSize = str(arcpy.GetRasterProperties_management(inRaster, "CELLSIZEX"))
arcpy.AddMessage(inRaster_CellSize)
arcpy.AddMessage(type(inRaster_CellSize))
arcpy.AddMessage(float(inRaster_CellSize))

# Export Raster by new CellSize Compare
if float(inRaster_CellSize) < 0.06:
    arcpy.CreateRasterDataset_management(outPath, out_Raster_Low, 0.06, "8_BIT_UNSIGNED", spatial_reference,
                                         Raster_BandCounts)
    arcpy.AddMessage(out_Raster_Low + " Created")
    arcpy.AddMessage(out_Raster_Low + " Mosaic_Start")
    arcpy.Mosaic_management(out_Raster, out_Raster_Low, background_value=0, nodata_value=0)
    arcpy.AddMessage(out_Raster_Low + " Mosaic_End")
    out_Raster_Low_CellSize = arcpy.GetRasterProperties_management(out_Raster_Low, "CELLSIZEX")
    arcpy.AddMessage(out_Raster_Low_CellSize)
