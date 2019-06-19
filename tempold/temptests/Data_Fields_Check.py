#!/usr/bin/python
# -*- coding: UTF-8 -*-

import arcpy
from arcpy import env

env.workspace = arcpy.GetParameterAsText(0)
Datasets = arcpy.ListDatasets()
arcpy.AddMessage(Datasets)