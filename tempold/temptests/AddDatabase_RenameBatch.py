# -- coding: utf-8 --
# ! usr/bin/python
# coding = utf-8

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = arcpy.GetParameterAsText(0)
layerLists = arcpy.ListFeatureClasses()

CityName = arcpy.GetParameterAsText(1)
BuildingName = arcpy.GetParameterAsText(2)

# GDB database output
outPath = arcpy.GetParameterAsText(3)

# Create new Database
databaseName = CityName + '_' + BuildingName
dataBaseInput = env.workspace
arcpy.CreateFeatureDataset_management(outPath, databaseName, dataBaseInput)

# Feature select mode
feature2Dor3D = arcpy.GetParameterAsText(4)

if feature2Dor3D == "1":
    typeLists = ["doors", "inwalls", "outwalls", "firedoors", "elevators", "firelifts", "stairs", "grounds",
                 "escalators", "exits", "hazards", "wireframe"]

if feature2Dor3D == "0":
    typeLists = ['inhydrants', 'pysys', 'sfsys', 'fire_curtains', 'spraysys', 'autoalarmsys', 'handalarmsys',
                 'broadcastsys', 'firedoors', 'fireregions', 'pumpadapter', 'videosys', 'outhydrant',
                 'roads', 'hazards', 'refuge_room', 'firepassage', 'control_room', 'fire_waterfeatures']
if feature2Dor3D == "2":
    typeLists = ["chemical_tanks", "outhydrants", "pipings", "pools", "streets", "walls", "workshops", "hazards"]

for typeList in typeLists:
    type_List = "_" + typeList
    for layerList in layerLists:
        if type_List in layerList:
            arcpy.AddMessage(layerList + "_Start")
            layerName = CityName + "_" + BuildingName + "_" + typeList
            out_data = outPath + "/" + databaseName + "/" + layerName
            arcpy.AddMessage(out_data)
            arcpy.Copy_management(layerList, out_data)
            arcpy.AddMessage(layerName + "_End")
