#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True

# new file path input
# env.workspace = r"E:\100Model\njcity_20180504.gdb\zjsn_20180504"

# import feature Datasets path
env.workspace = arcpy.GetParameterAsText(0)
featureLists = arcpy.ListFeatureClasses()
print(featureLists)

# Add status field and fill Value
typeLists = ['pysys', 'sfsys', 'handalarmsys']
for type in typeLists:
    for feature in featureLists:
        # typeLenth = len(type)
        # if feature[0:typeLenth] == type:
        if type in feature:
            arcpy.AddField_management(feature, "status", "TEXT", field_length="50", field_alias="状态")
            arcpy.CalculateField_management(feature, "status", "'运行'", "PYTHON_9.3")
            # print(feature + "Finished")
            arcpy.AddMessage(feature + "_Finished")

typeLists = ['inhydrants', 'autoalarmsys', 'broadcastsys', 'spraysys', 'fire_curtains']
for type in typeLists:
    for feature in featureLists:
        typeLenth = len(type)
        if type in feature:
            arcpy.AddField_management(feature, "status", "TEXT", field_length="50", field_alias="状态")
            arcpy.CalculateField_management(feature, "status", "'正常'", "PYTHON_9.3")
            # print(feature + "Finished")
            arcpy.AddMessage(feature + "_Finished")
