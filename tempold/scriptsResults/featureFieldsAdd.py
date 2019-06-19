#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True

# input datasets
# env.workspace = arcpy.GetParameterAsText(0)
# env.workspace = r"D:\myDocuments\Desktop\znc_1_test_2d.gdb\znc_1_results"

# fields = arcpy.ListFields("jsph_inwall")
# for field in fields:
#     print(field.name)
# env.workspace = r"D:\myDocuments\Desktop\znc_1_test_2d.gdb\znc_1_results"
env.workspace = arcpy.GetParameterAsText(0)
features = arcpy.ListFeatureClasses()
# fieldTypes = ['OBJECTID', 'Shape', 'building_id', 'type', 'floor', 'floor_z', 'z', 'name', 'city', 'province']
field_Names = ['building_id', 'type', 'floor', 'floor_z', 'z', 'name', 'city', 'province']
field_Types = ['TEXT', 'TEXT', 'SHORT', 'FLOAT', 'FLOAT', 'TEXT', 'TEXT', 'TEXT']
field_Alias = ['建筑Id', '类型', '楼层', '层高', '显示高度', '建筑名称', '市', '省']

for feature in features:
    # print(feature)
    arcpy.AddMessage(feature)
    fieldLists = arcpy.ListFields(feature)
    # print(fieldLists)
    featureField = []
    for field in fieldLists:
        # name = field.name
        featureField.append(field.name)
    # print(featureField)
    arcpy.AddMessage(featureField)
    for i in range(len(field_Names)):
        field_Name = field_Names[i]
        if field_Name in featureField:
            # print(field_Name + "_existed")
            arcpy.AddMessage(field_Name + "_existed")
        else:
            arcpy.AddField_management(feature, field_Name, field_Types[i], field_alias=field_Alias[i])
            arcpy.AddMessage(feature + "_" + field_Name + "_" + "Add")

# Input new field_Names Range
# delete more unused fields
field_NewInputs = ['OBJECTID', 'Shape', 'RefName', 'Layer', 'Shape_Length', 'Shape_Area', 'SHAPE', 'SHAPE_Length',
                   'SHAPE_Area']
for field_NewInput in field_NewInputs:
    field_Names.append(field_NewInput)

for feature in features:
    print(feature)
    fieldLists = arcpy.ListFields(feature)
    # print(fieldLists)
    featureField = []
    for field in fieldLists:
        if field.name in field_Names:
            # print(field.name + "_used")
            arcpy.AddMessage(field.name + "_used")
        else:
            arcpy.DeleteField_management(feature, field.name)
