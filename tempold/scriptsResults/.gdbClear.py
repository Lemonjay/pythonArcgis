#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

gdbPath = arcpy.GetParameterAsText(0)
# env.workspace = r'D:\myDocuments\Documents\ArcGIS\Default.gdb'
if 'Default.gdb' in gdbPath:
    arcpy.AddMessage('True')
    env.workspace = gdbPath
    featureClassLists = arcpy.ListFeatureClasses()
    featureDatasets = arcpy.ListDatasets()
    if len(featureDatasets) != 0:
        for featureDataset in featureDatasets:
            arcpy.AddMessage(featureDataset)
            arcpy.Delete_management(featureDataset)

    if len(featureClassLists) != 0:
        for feature in featureClassLists:
            arcpy.AddMessage(feature)
            arcpy.Delete_management(feature)
else:
    arcpy.AddMessage('The Gdb is not "Default GDB"!')
