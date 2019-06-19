# -- coding: utf-8 --
# !/usr/bin/python
# -*- #################

import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True

env.workspace = arcpy.GetParameterAsText(0)
features = arcpy.ListFeatureClasses()
# fieldTypes = ['OBJECTID', 'Shape', 'building_id', 'type', 'floor', 'floor_z', 'z', 'name', 'city', 'province']
field_Names = ['building_id', 'type', 'floor', 'floor_z', 'z', 'floor_d', 'name', 'city', 'province']
field_Types = ['TEXT', 'TEXT', 'SHORT', 'FLOAT', 'FLOAT', 'FLOAT', 'TEXT', 'TEXT', 'TEXT']
field_Alias = ['建筑Id', '类型', '楼层', '层高', '显示高度', '层差', '建筑名称', '市', '省']

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

featureGrounds_Name = ["fire_area", "function_type"]
featureGrounds_type = ['TEXT', 'TEXT']
featureGrounds_Alias = ["防火分区", "功能类型"]

for feature in features:
    if "grounds" in feature:
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
        for i in range(len(featureGrounds_Name)):
            field_Name = featureGrounds_Name[i]
            if field_Name in featureField:
                # print(field_Name + "_existed")
                arcpy.AddMessage(field_Name + "_existed")
            else:
                arcpy.AddField_management(feature, field_Name, featureGrounds_type[i],
                                          field_alias=featureGrounds_Alias[i])
                arcpy.AddMessage(feature + "_" + field_Name + "_" + "Add")

# Input new field_Names Range
# delete more unused fields
field_NewInputs = ['RefName', 'text', "fire_area", "function_type"]

for field_NewInput in field_NewInputs:
    field_Names.append(field_NewInput.lower())

for feature in features:
    print(feature)
    fieldLists = arcpy.ListFields(feature)
    # print(fieldLists)
    featureField = []
    for field in fieldLists:
        fieldName = field.name
        if fieldName.lower() in field_Names:
            # print(field.name + "_used")
            arcpy.AddMessage(field.name + "_used")
        else:
            try:
                arcpy.DeleteField_management(feature, field.name)
            except:
                arcpy.AddMessage(field.name + "_error")
