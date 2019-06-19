# -- coding: utf-8 --
# ! usr/bin/python
# coding = utf-8

import arcpy
from arcpy import env

env.overwriteOutput = True

DataName = ['njCity_hyl', 'njCity_jspH', 'ncCity_xlC', 'ycCity_znM', 'ycCity_jyS','zjCity_wgB', 'zjCity_snS']
for Data in DataName:
    env.workspace = r"D:\myDocuments\Desktop\jscloud.gdb" + "/" + Data
    layerLists = arcpy.ListFeatureClasses()
    for layerList in layerLists:
        Count = str(arcpy.GetCount_management(layerList))
        print layerList
        print Count
        if Count == "0":
            arcpy.Delete_management(layerList)
            print layerList + "_Deleted"
