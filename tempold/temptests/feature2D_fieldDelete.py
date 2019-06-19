# -- coding: utf-8 --
# !/usr/bin/python
# -*- #################

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = arcpy.GetParameterAsText(0)
layerLists = arcpy.ListFeatureClasses()
feature3DSelect = arcpy.GetParameterAsText(1)

if feature3DSelect == "0":
    fieldOrder = ['building_id', 'type', 'floor', 'floor_z', 'status', 'name', 'z', 'city', 'province', 'q', 'tube_d',
                  'pipe_net', 'watersupply_mode', 'watersupply_pressure', 'purpose']
if feature3DSelect == "1":
    fieldOrder = ['building_id', 'type', 'floor', 'floor_z', 'status', 'name', 'z', 'city', 'province', 'door_aspect',
                  'fire_area', 'function_type']

fieldOrderLower = []
for fieldType in fieldOrder:
    print fieldType.lower()
    fieldOrderLower.append(fieldType.lower())

for layer in layerLists:
    fieldLists = arcpy.ListFields(layer)
    arcpy.AddMessage(layer + "_Start")
    for field in fieldLists:
        fieldName = field.name
        arcpy.AddMessage(fieldName.lower())
        if '{}'.format(fieldName.lower()) in fieldOrderLower:
            arcpy.AddMessage(fieldName.lower() + "_Pass")
        else:
            try:
                arcpy.DeleteField_management(layer, field.name)
                arcpy.AddMessage("_______________________")
                arcpy.AddMessage(fieldName.lower() + "_Deleted")
            except:
                arcpy.AddMessage(field.name + "_pass error")
    arcpy.AddMessage(layer + "_End")
    arcpy.AddMessage("**************************")
