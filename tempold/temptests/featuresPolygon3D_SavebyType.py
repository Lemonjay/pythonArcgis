# encoding: utf-8
"""
因为室外飞行受到诸多因素的影响，诸如天气、禁飞区和人的因素等，往往无法再室内建模进行之前完成。因此需要先进行室内建模，然后对模型的polygon合并起来进行调整，该工具就是为此生成的;

modify by date 20180824
"""

# !/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

env.overwriteOutput = True
feature = arcpy.GetParameterAsText(0)
buildingName = arcpy.GetParameterAsText(1)
range1st = str(arcpy.GetParameterAsText(2))
range2nd = str(arcpy.GetParameterAsText(3))
outPath = arcpy.GetParameterAsText(4)

if range1st == range2nd:
    featureNamePart = buildingName + "_" + range1st + "_"
else:
    featureNamePart = buildingName + "_" + range1st + "_" + range2nd + "_"

# 3D features saved by type
valueLists = ["门", "内墙", "外墙", "防火门", "客用电梯", "消防电梯", "疏散楼梯", "地板", "手扶电梯", "线框"]
outputLists = ["doors", "inwalls", "outwalls", "firedoors", "elevators", "firelifts", "stairs", "grounds", "escalators",
               "wireframe"]

for i in range(len(valueLists)):
    featureName = featureNamePart + outputLists[i]
    featureOutput = outPath + '/' + featureName
    arcpy.Select_analysis(feature, featureOutput, "type = '{}'".format(valueLists[i]))
    arcpy.AddMessage(outputLists[i] + "_Finished")
arcpy.AddMessage(feature + "_Finished")

env.workspace = outPath
featureLists = arcpy.ListFeatureClasses()
for feature in featureLists:
    if feature.replace(featureNamePart, '') in outputLists:
        Count = str(arcpy.GetCount_management(feature))
        if Count == "0":
            arcpy.AddMessage(feature + " is Null")
            arcpy.Delete_management(feature)
            arcpy.AddMessage(feature + " Deleted")
