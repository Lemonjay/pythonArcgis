# -- coding: utf-8 --
# ! usr/bin/python
# coding = utf-8

import arcpy
from arcpy import env
import os
import time


# Write Log file
def log_write(_name, _msg):
    desktop_path = r'D:\myDocuments\Desktop\DataReorder\data_log'
    full_path = desktop_path + '/' + _name + '.log'
    log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if not os.path.exists(full_path):
        log_file = open(full_path, 'w')
    else:
        log_file = open(full_path, 'a')
    log_file.writelines(log_time + '        ' + _msg + '\n')
    log_file.close()
    # print('Done')


env.overwriteOutput = True
env.workspace = arcpy.GetParameterAsText(0)
layerLists = arcpy.ListFeatureClasses()

CityName = arcpy.GetParameterAsText(1)
BuildingName = arcpy.GetParameterAsText(2)
arcpy.AddMessage(CityName)

outPath = arcpy.GetParameterAsText(3)
database = arcpy.Describe(outPath)
arcpy.AddMessage(database.extension)

if database.extension == 'gdb':
    arcpy.CreateFeatureDataset_management(outPath, CityName + '_' + BuildingName, layerLists[0])
    CBName = CityName + "_" + BuildingName
    outPath += '/' + CBName
else:
    CBName = outPath.split('\\')[len(outPath.split('\\')) - 1]

arcpy.AddMessage(outPath)
arcpy.AddMessage(CBName)

feature2Dor3D = arcpy.GetParameterAsText(4)

if feature2Dor3D == "1":
    typeLists = ["doors", "inwalls", "outwalls", "firedoors", "elevators", "firelifts", "stairs", "grounds",
                 "escalators", "exits", "hazards", "wireframe"]

if feature2Dor3D == "0":
    typeLists = ['inhydrants', 'pysys', 'sfsys', 'fire_curtains', 'spraysys', 'autoalarmsys', 'handalarmsys',
                 'broadcastsys', 'firedoors', 'fireregions', 'pumpadapter', 'videosys', 'outhydrant',
                 'roads', 'hazards', 'refuge_room', 'firepassage', 'control_room', 'fire_waterfeatures']
if feature2Dor3D == "2":
    typeLists = ["chemical_tanks", "outhydrants", "pipings", "pools", "streets", "walls", "workshops", "hazards"]

for typeList in typeLists:
    type_List = "_" + typeList
    for feature in layerLists:
        if type_List in feature:
            arcpy.AddMessage(feature + "_Start")
            layerName = CBName + "_" + typeList
            out_data = outPath + "/" + layerName
            arcpy.Copy_management(feature, out_data)
            arcpy.AddMessage(layerName + "_End")
            log_write(CBName, '{0} was renamed and Imported.    The layer name: {1}'.format(feature, layerName))
