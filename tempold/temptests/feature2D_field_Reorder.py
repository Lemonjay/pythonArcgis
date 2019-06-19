# -- coding: utf-8 --
# !/usr/bin/python
# -*- #################

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = arcpy.GetParameterAsText(0)
layerLists = arcpy.ListFeatureClasses()
feature2D_3DSwitch = arcpy.GetParameterAsText(1)

# Building Field reorder
if feature2D_3DSwitch == 0 and feature2D_3DSwitch == 1:
    fieldOrder = ['building_id', 'type', 'floor', 'floor_z', 'status', 'fire_area', 'function_type', 'door_aspect',
                  'name',
                  'z', 'city', 'province']
    fieldAlias = ['建筑ID', '类型', '楼层', '层高', '状态', "防火分区", "功能类型", '门_方向', '建筑名称', '显示高度', '市', '省']

# Chemical Industry Field reorder
if feature2D_3DSwitch == 3:
    fieldOrder = ['building_id', 'type', 'floor', 'floor_z', 'status', 'fire_area', 'function_type', 'door_aspect',
                  'name', 'z', 'city', 'province']
    fieldAlias = ['建筑ID', '类型', '楼层', '层高', '状态', "防火分区", "功能类型", '门_方向', '建筑名称', '显示高度', '市', '省']

for layerList in layerLists:
    arcpy.AddMessage(layerList + "_Start")
    fieldLists = arcpy.ListFields(layerList)
    for i in range(len(fieldOrder)):
        for field in fieldLists:
            fieldList = fieldOrder[i]
            if fieldList == field.name:
                fieldNew = fieldList + "_1"
                arcpy.AddField_management(layerList, fieldNew, field.type, field.precision, field.scale,
                                          field.length)
                expression = '!{}!'.format(fieldList)  # 字符串无法直接变成变量名，需要加一个转换
                arcpy.AddMessage(expression)
                arcpy.CalculateField_management(layerList, fieldNew, expression, "PYTHON_9.3")
                arcpy.DeleteField_management(layerList, fieldList)
                arcpy.AddMessage(fieldList + "_Deleted")

    fieldLists = arcpy.ListFields(layerList)
    for i in range(len(fieldOrder)):
        for field in fieldLists:
            fieldNew = fieldOrder[i]
            if fieldNew + "_1" == field.name:
                arcpy.AddMessage(field.name + "_Start")
                arcpy.AddField_management(layerList, fieldNew, field.type, field.precision, field.scale,
                                          field.length, fieldAlias[i])
                expression = '!{}!'.format(field.name)  # 字符串无法直接变成变量名，需要加一个转换
                arcpy.AddMessage(expression)
                arcpy.CalculateField_management(layerList, fieldNew, expression, "PYTHON_9.3")
                arcpy.DeleteField_management(layerList, field.name)
                arcpy.AddMessage(field.name + "_Deleted")
    arcpy.AddMessage(layerList + "_End")
arcpy.SetLogHistory(True)
