#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True
# New DataSets path input
dataNEW = arcpy.GetParameterAsText(0)
env.workspace = dataNEW
# Got featureClass datasets
features_New = arcpy.ListFeatureClasses()

# Old DataSets path input
dataOld = arcpy.GetParameterAsText(1)
env.workspace = dataOld
features_Old = arcpy.ListFeatureClasses()

# cityName input
cityName = arcpy.GetParameterAsText(2)

# Iteration Number
IterationN = arcpy.GetParameterAsText(3)

# DataSets Target path Input
dataTarget = arcpy.GetParameterAsText(4)

typeLists = ['inhydrants', 'pysys', 'sfsys', 'fire_curtains', 'spraysys', 'autoalarmsys', 'handalarmsys',
             'broadcastsys']
for layer in typeLists:
    for featureNew in features_New:
        for featureOld in features_Old:
            layerUnique = layer
            if layerUnique in featureNew:
                if layerUnique in featureOld:
                    arcpy.AddMessage(featureNew + "_" + featureOld + "_" + "Started")
                    featureNew_path = dataNEW + "/" + featureNew
                    featureOld_path = dataOld + "/" + featureOld
                    featureInput = [featureNew_path, featureOld_path]
                    featureOutput = dataTarget + "/" + cityName + "_" + layer + "_" + "Merge" + "0" + IterationN
                    arcpy.Merge_management(featureInput, featureOutput)
                    arcpy.AddMessage(cityName + "_" + layer + "0" + IterationN + "_Merged_Finished")
