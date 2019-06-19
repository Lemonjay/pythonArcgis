#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = arcpy.GetParameterAsText(0)
buildingName = arcpy.GetParameterAsText(1)
range1st = str(arcpy.GetParameterAsText(2))
range2nd = str(arcpy.GetParameterAsText(3))

# 3D features saved by type
valueLists = ["门", "内墙", "外墙", "防火门", "客用电梯", "消防电梯", "疏散楼梯", "地板", "手扶电梯"]
outputLists = ["doors", "inwalls", "outwalls", "firedoors", "elevators", "firelifts", "stairs", "grounds", "escalators"]

features = arcpy.ListFeatureClasses()
for feature in features:
    for i in range(len(valueLists)):
        featureOutput = buildingName + "_" + range1st + "_" + range2nd + "_" + outputLists[i]
        arcpy.Select_analysis(feature, featureOutput, "type = '{}'".format(valueLists[i]))
        arcpy.AddMessage(outputLists[i] + "_Finished")
    arcpy.AddMessage(feature + "_Finished")
