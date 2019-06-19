# features2D Duplicate by floor
# Date 20180511 Modify
import pandas as pd
import arcpy
from arcpy import env

env.overwriteOutput = True
# DataSets Input,Got Feature Class Lists
env.workspace = arcpy.GetParameterAsText(0)
featureLists = arcpy.ListFeatureClasses()
arcpy.AddMessage(featureLists)

# Building Abbreviation input
shortName = arcpy.GetParameterAsText(1)
# The Number of the floor witch needs to be duplicated
# floorTypical = arcpy.GetParameterAsText(2)
# The features duplicated by floor from [rangeNum01:rangeNum02]
rangeNum01 = int(arcpy.GetParameterAsText(2))
rangeNum02 = int(arcpy.GetParameterAsText(3))

rangeNum01_str = "B" + str(abs(rangeNum01)) if rangeNum01 < 0 else str(rangeNum01)
rangeNum02_str = "B" + str(abs(rangeNum02)) if rangeNum02 < 0 else str(rangeNum02)

# Display height
zValue = float(arcpy.GetParameterAsText(4))
# output DataSets path
outPath = arcpy.GetParameterAsText(5)

# CSV import
building_csv = arcpy.GetParameterAsText(6)
building_floor = pd.read_csv(building_csv, usecols=["floor", "floor_z"])

# Features duplicating and Add z_Value
layerType = ['inhydrants', 'fire_curtains']
zValue = zValue + 1.1
for type in layerType:
    for feature in featureLists:
        if type in feature:
            # print feature + " yes"
            arcpy.AddMessage(feature + " yes")
            lists = []
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = "B" + str(abs(floor)) if floor < 0 else str(floor)
                if floor != 0:
                    arcpy.Copy_management(feature, type + "_floor" + floorStr)
                    arcpy.CalculateField_management(type + "_floor" + floorStr, "floor", str(floor))
                    for floor_id in range(len(building_floor.floor)):
                        if building_floor.floor[floor_id] == floor:
                            buildingFloor_z = building_floor.floor_z[floor_id]
                            arcpy.CalculateField_management(type + "_floor" + floorStr, "floor_z", buildingFloor_z)
                            arcpy.CalculateField_management(type + "_floor" + floorStr, "z", buildingFloor_z + zValue)
                    arcpy.FeatureTo3DByAttribute_3d(type + "_floor" + floorStr, type + "_floor3D" + floorStr, "z")
                    arcpy.Delete_management(type + "_floor" + floorStr)
                    arcpy.AddMessage(type + "_floor" + floorStr + "_Part")
                    lists.append(type + "_floor3D" + floorStr)
            # print lists
            arcpy.AddMessage(lists)
            outName = outPath + "/" + shortName + "_" + rangeNum01_str + "_" + rangeNum02_str + "_" + type
            arcpy.Merge_management(lists, outName)
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = str(floor)
                arcpy.Delete_management(type + "_floor3D" + floorStr)
            # print(type + floorNum + "_floor3D" + " Finished")
            arcpy.AddMessage(rangeNum01_str + "_" + rangeNum02_str + "_" + type + "_floor3D" + " Finished")

# Features duplicating and Add z_Value
layerType = ['spraysys', 'autoalarmsys', 'handalarmsys', 'broadcastsys', 'pysys', 'sfsys']
zValue = zValue + 1.5
for type in layerType:
    for feature in featureLists:
        if type in feature:
            # print feature + " yes"
            arcpy.AddMessage(feature + " yes")
            lists = []
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = "B" + str(abs(floor)) if floor < 0 else str(floor)
                if floor != 0:
                    arcpy.Copy_management(feature, type + "_floor" + floorStr)
                    arcpy.CalculateField_management(type + "_floor" + floorStr, "floor", str(floor))
                    for floor_id in range(len(building_floor.floor)):
                        if building_floor.floor[floor_id] == floor:
                            buildingFloor_z = building_floor.floor_z[floor_id]
                            arcpy.CalculateField_management(type + "_floor" + floorStr, "floor_z", buildingFloor_z)
                            arcpy.CalculateField_management(type + "_floor" + floorStr, "z", buildingFloor_z + zValue)
                    arcpy.FeatureTo3DByAttribute_3d(type + "_floor" + floorStr, type + "_floor3D" + floorStr, "z")
                    arcpy.Delete_management(type + "_floor" + floorStr)
                    lists.append(type + "_floor3D" + floorStr)
            # print lists
            arcpy.AddMessage(lists)
            outName = outPath + "/" + shortName + "_" + rangeNum01_str + "_" + rangeNum02_str + "_" + type
            arcpy.Merge_management(lists, outName)
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = str(floor)
                arcpy.Delete_management(type + "_floor3D" + floorStr)
            # print(type + floorNum + "_floor3D" + " Finished")
            arcpy.AddMessage(rangeNum01_str + "_" + rangeNum02_str + "_" + type + "_floor3D" + " Finished")
