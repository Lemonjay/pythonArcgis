# -- coding: utf-8 --
# ! usr/bin/python
# coding = utf-8

import pandas as pd
import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = r"D:\myDocuments\Desktop\DataReorder\bsfCI.gdb\zjCity_bsfCI"
layerName = "zjCity_bsfCI_chemical_tanks"
fieldLists = arcpy.ListFields(layerName)

fieldListText = ['building_id', 'type', 'name', 'Height', 'type_name', 'storage_mode',
                 'storage_location', 'design_stock', 'key_danger', 'single_volume', 'storage_medium', 'single_stock',
                 'emergency_plan', 'tank_mark']

fieldPass = []

for field in fieldLists:
    if field.name in fieldListText:
        fieldPass.append(field.name)
    else:
        try:
            arcpy.DeleteField_management(layerName, field.name)
        except:
            print field.name + "_passed"
