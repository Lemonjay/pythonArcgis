#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释
# UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0'in position
# problem solved
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import arcpy
from arcpy import env

arcpy.env.overwriteOutput = True

# new file path input
# env.workspace = r"E:\100Model\njcity_20180504.gdb\zjsn_20180504"

# import feature Datasets path
dataSetsPath = arcpy.GetParameterAsText(0)
building_id = arcpy.GetParameterAsText(1)
name = arcpy.GetParameterAsText(2)
city = arcpy.GetParameterAsText(3)
province = arcpy.GetParameterAsText(4)

dataSets = dataSetsPath.split(';')
arcpy.AddMessage(dataSets)
# arcpy.AddMessage(type(dataSets))
for dataSet in dataSets:
    env.workspace = dataSet
    featureLists = arcpy.ListFeatureClasses()
    # print(featureLists)

    field_Names = ['building_id', 'name', 'city', 'province']
    field_Values = [building_id, name, city, province]
    # for field in field_Values:
    #     arcpy.AddMessage(field)
    # # field_Value.append(building_id)
    for feature in featureLists:
        arcpy.AddMessage(feature + "_" + "Start")
        for i in range(len(field_Names)):
            if len(field_Values[i]) != 0:
                arcpy.CalculateField_management(feature, field_Names[i], "'{}'".format(field_Values[i]), "PYTHON_9.3")
                arcpy.AddMessage('The value {0} was added in the {1} field'.format(field_Values[i], field_Names[i]))
        print(feature + "_Finished")
        arcpy.AddMessage(feature + "_Finished")
