# features2D Duplicate by floor
# Date 20180511 Modify
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
floorTypical = arcpy.GetParameterAsText(2)
# The features duplicated by floor from [rangeNum01:rangeNum02]
rangeNum01 = int(arcpy.GetParameterAsText(3))
rangeNum02 = int(arcpy.GetParameterAsText(4))

# The floor height
floorZ = float(arcpy.GetParameterAsText(5))
floorD_value = float(arcpy.GetParameterAsText(6))
# Display height
zValue = float(arcpy.GetParameterAsText(7))
# output DataSets path
outPath = arcpy.GetParameterAsText(8)

num01 = len(shortName) + 1
floorNum = floorTypical
floor1st = rangeNum01 - 1

# Features duplicating and Add z_Value
layerType = ['inhydrants', 'fire_curtains']
zValue = zValue + 1.1
for type in layerType:
    for feature in featureLists:
        # arcpy.AddMessage(feature[num01])
        # arcpy.AddMessage(feature[num02:])
        if feature[num01] == floorNum and type in feature:
            # print feature + " yes"
            arcpy.AddMessage(feature + " yes")
            lists = []
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = str(floor)
                arcpy.Copy_management(feature, type + "_floor" + floorStr)
                arcpy.CalculateField_management(type + "_floor" + floorStr, "floor", floorStr)
                arcpy.CalculateField_management(type + "_floor" + floorStr, "floor_z",
                                                (floor - floor1st) * floorD_value + floorZ)
                arcpy.CalculateField_management(type + "_floor" + floorStr, "z",
                                                (floor - floor1st) * floorD_value + floorZ + zValue)
                arcpy.FeatureTo3DByAttribute_3d(type + "_floor" + floorStr, type + "_floor3D" + floorStr, "z")
                arcpy.Delete_management(type + "_floor" + floorStr)
                lists.append(type + "_floor3D" + floorStr)
            # print lists
            arcpy.AddMessage(lists)
            outName = outPath + "/" + shortName + "_" + str(rangeNum01) + "_" + str(rangeNum02) + "_" + type
            arcpy.Merge_management(lists, outName)
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = str(floor)
                arcpy.Delete_management(type + "_floor3D" + floorStr)
            # print(type + floorNum + "_floor3D" + " Finished")
            arcpy.AddMessage(type + floorNum + "_floor3D" + " Finished")

# Features duplicating and Add z_Value
layerType = ['spraysys', 'autoalarmsys', 'handalarmsys', 'broadcastsys', 'pysys', 'sfsys']
zValue = zValue + 1.5
for type in layerType:
    for feature in featureLists:
        # arcpy.AddMessage(feature[num01])
        # arcpy.AddMessage(feature[num02:])
        if feature[num01] == floorNum and type in feature:
            # print feature + " yes"
            arcpy.AddMessage(feature + " yes")
            lists = []
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = str(floor)
                arcpy.Copy_management(feature, type + "_floor" + floorStr)
                arcpy.CalculateField_management(type + "_floor" + floorStr, "floor", floorStr)
                arcpy.CalculateField_management(type + "_floor" + floorStr, "floor_z",
                                                (floor - floor1st) * floorD_value + floorZ)
                arcpy.CalculateField_management(type + "_floor" + floorStr, "z",
                                                (floor - floor1st) * floorD_value + floorZ + zValue)
                arcpy.FeatureTo3DByAttribute_3d(type + "_floor" + floorStr, type + "_floor3D" + floorStr, "z")
                arcpy.Delete_management(type + "_floor" + floorStr)
                lists.append(type + "_floor3D" + floorStr)
            # print lists
            arcpy.AddMessage(lists)
            outName = outPath + "/" + shortName + "_" + str(rangeNum01) + "_" + str(rangeNum02) + "_" + type
            arcpy.Merge_management(lists, outName)
            for floor in range(rangeNum01, rangeNum02 + 1):
                floorStr = str(floor)
                arcpy.Delete_management(type + "_floor3D" + floorStr)
            # print(type + floorNum + "_floor3D" + " Finished")
            arcpy.AddMessage(type + floorNum + "_floor3D" + " Finished")
