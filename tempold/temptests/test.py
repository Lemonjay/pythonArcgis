#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = r"D:\myDocuments\Desktop\DataReorder\bsfCI.gdb\zjCity_bsfCI"
layerName = "zjCity_bsfCI_chemical_tanks"
fieldLists = arcpy.ListFields(layerName)

fieldListText = ['OBJECTID', 'building_id', 'type', 'name', 'Height', 'type_name', 'storage_mode', 'storage_location',
                 'design_stock', 'key_danger', 'single_volume', 'storage_medium', 'single_stock', 'emergency_plan',
                 'tank_mark']

for fieldList in fieldListText:
    rows = arcpy.SearchCursor(layerName, sort_fields="OBJECTID")
    print fieldList
    field_Temp = []
    for row in rows:
        fieldValue = fieldList + "_temp"
        rowValue = row.getValue(fieldList)
        field_Temp.append(rowValue)
        print rowValue
    print field_Temp
    print field_Temp[0]

# for row in rows:
#     for fieldList in fieldListText:
#         print row.getValue(fieldList)


# path = r"D:\myDocuments\Desktop\DataReorder\bsfCI_AttributeUpdate"
# csv_Input = path + "/" + layerName + ".csv"
# building_field = pd.read_csv(csv_Input, encoding='gb2312')
#
# building_fieldSort = building_field.sort_values(by="objectid", axis=0, ascending=True)
# print building_fieldSort


# fieldTable = ['OBJECTID', 'building_id', 'type', 'name', 'Height', 'type_name', 'storage_mode', 'storage_location',
#                  'design_stock', 'key_danger', 'single_volume', 'storage_medium', 'single_stock', 'emergency_plan',
#                  'tank_mark']

# for i in range(len(building_fieldSort.objectid)):
#     building_fieldSort.objectid
arcpy.mapping.CreateMapSDDraft()