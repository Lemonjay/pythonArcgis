# -- coding: utf-8 --
# ! usr/bin/python
# coding = utf-8

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = r"D:\myDocuments\Desktop\DataReorder\jsCloud_3D.gdb"

njCity_Data = ["jspH", "hyl"]
zjCity_Data = ["wgB", "snS", "zjH", "zjyh", "ndCI", "bsfCI"]
ycCity_Data = ["znM", "jyS"]
yzCity_Data = ["zgS"]
lygCity_Data = ["snS"]
ncCity_Data = ["xlC"]

CityLists = ["njCity", "zjCity", "ycCity", "yzCity", "lygCity","ncCity"]
for CityName in CityLists:
    Data = CityName + "_Data"
    DataLists = eval(Data)
    for BuildingName in DataLists:
        LayerName = CityName + "_" + BuildingName
        print (LayerName + "_Start")
        arcpy.CreateFeatureDataset_management(r"D:\myDocuments\Desktop\DataReorder\jsCloud_3D.gdb", LayerName,
                                              r"D:\myDocuments\Desktop\DataReorder\jsCloud.gdb\merge20180616")
