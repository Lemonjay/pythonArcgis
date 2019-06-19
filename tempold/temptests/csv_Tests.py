# -- coding: utf-8 --
# !/usr/bin/python
# -*- #################

import csv
import pandas as pd
import arcpy
from arcpy import env

building_csv = arcpy.GetParameterAsText(0)
building_floor = pd.read_csv(r"D:\myDocuments\Desktop\DataReorder\building.csv", usecols=["floor", "floor_z"])

print building_floor
print building_floor.floor[0]
