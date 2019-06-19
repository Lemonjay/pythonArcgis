#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pandas as pd
import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = r"D:\myDocuments\Desktop\DataReorder\bsfCI.gdb\zjCity_bsfCI"
layerName = "zjCity_bsfCI_chemical_tanks"
fieldLists = arcpy.ListFields(layerName)

fieldListText = ['OBJECTID', 'building_id', 'type', 'name', 'Height', 'type_name', 'storage_mode',
                 'storage_location', 'design_stock', 'key_danger', 'single_volume', 'storage_medium', 'single_stock',
                 'emergency_plan', 'tank_mark']

# for field in fieldLists:
#     fieldListText.append(field.name.encode('utf-8'))  # 编码去掉u."Shape"
# print fieldListText

# CSV import
# building_csv = r"D:\myDocuments\Desktop\DataReorder\bsfCI_AttributeUpdate\zjCity_bsfCI_chemical_tanks.csv"
# building_field = pd.read_csv(building_csv, encoding='gb2312')
# print building_field.objectid
path = r"D:\myDocuments\Desktop\DataReorder\bsfCI_AttributeUpdate"
csv_Input = path + "/" + layerName + ".csv"
arcpy.TableToDBASE_conversion(csv_Input, path)
dbf_Input = path + "/" + layerName + ".dbf"
# building_dbf = r"D:\myDocuments\Desktop\DataReorder\bsfCI_AttributeUpdate\zjCity_bsfCI_chemical_tanks.dbf"
arcpy.JoinField_management(layerName, 'OBJECTID', dbf_Input, 'objectid')
for field in fieldLists:
    print field.name
# arcpy.CalculateField_management(layerName,)