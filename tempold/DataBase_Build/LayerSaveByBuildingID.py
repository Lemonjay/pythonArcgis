# -- coding: utf-8 --
# ! usr/bin/python
# coding = utf-8

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = r"D:\myDocuments\Desktop\jscloud.gdb\merge20180616"
layerLists = arcpy.ListFeatureClasses()

typeLists = ['inhydrants', 'pysys', 'sfsys', 'fire_curtains', 'spraysys', 'autoalarmsys', 'handalarmsys',
             'broadcastsys', 'firedoors', 'fireregions', 'pumpadapter', 'videosys', 'outhydrant',
             'roads']

building_ID = ['001', '002', 'nc001', 'yc001', 'yc002', 'zj001', 'zj002']
DataName = ['njCity_hyl', 'njCity_jspH', 'ncCity_xlC', 'ycCity_znM', 'ycCity_jyS','zjCity_wgB', 'zjCity_snS']

for typeList in typeLists:
    for layerList in layerLists:
        if typeList in layerList:
            outPath = r"D:\myDocuments\Desktop\jscloud.gdb"
            for i in range(len(building_ID)):
                layerName = DataName[i] + "_" + typeList
                print(layerName + "_Start")
                out_feature_class = outPath + "/" + DataName[i] + "/" + layerName
                arcpy.Select_analysis(layerList, out_feature_class, "building_id = '{}'".format(building_ID[i]))
                Count = str(arcpy.GetCount_management(out_feature_class))
                print Count
                if Count == "0":
                    arcpy.Delete_management(out_feature_class)
                    print(layerName + "_Deleted")
                else:
                    print(layerName + "_finished")
