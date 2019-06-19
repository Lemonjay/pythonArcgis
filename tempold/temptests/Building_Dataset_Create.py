#!/usr/bin/python
# -*- coding: UTF-8 -*-
import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = arcpy.GetParameterAsText(0)
CityName = arcpy.GetParameterAsText(1)
BuildingName = arcpy.GetParameterAsText(2)
spatial_Reference = arcpy.GetParameterAsText(3)

dataset_Name = CityName + "_" + BuildingName
arcpy.CreateFeatureDataset_management(env.workspace, dataset_Name, spatial_Reference)
