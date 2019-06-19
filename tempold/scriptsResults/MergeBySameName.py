#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = arcpy.GetParameterAsText(0)
buildingName = arcpy.GetParameterAsText(1)
range1st = arcpy.GetParameterAsText(2)
range2nd = arcpy.GetParameterAsText(3)
# DataSets Output path Add
outPath = arcpy.GetParameterAsText(4)

# 3D features saved by type
typeLists = ['spraysys', 'autoalarmsys', 'handalarmsys', 'inhydrants', 'broadcastsys', 'pysys', 'sfsys',
             'fire_curtains', "doors", "inwalls", "outwalls", "firedoors", "elevators", "firelifts", "stairs",
             "grounds", "escalators"]
featureLists = arcpy.ListFeatureClasses()
for typeL in typeLists:
    featureMerge = []
    for feature in featureLists:
        typeUnique = "_" + typeL
        if typeUnique in feature:
            featureMerge.append(feature)
    if len(featureMerge) != 0:
        arcpy.AddMessage(featureMerge)
        arcpy.AddMessage("Merging_Start")
        featureOutput = outPath + "/" + buildingName + "_" + typeL + "_" + range1st + "_" + range2nd
        arcpy.Merge_management(featureMerge, featureOutput)
