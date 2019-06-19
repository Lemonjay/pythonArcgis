# !/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy
from arcpy import env

env.overwriteOutput = True

# Import feature Datasets path
dataSetsPath = arcpy.GetParameterAsText(0)
buildingName = arcpy.GetParameterAsText(1)
outPath = arcpy.GetParameterAsText(2)
SpatialReference = arcpy.GetParameterAsText(3)
feature2Dor3D = arcpy.GetParameterAsText(4)
MultipatchOrPolygon = arcpy.GetParameterAsText(5)

arcpy.AddMessage(feature2Dor3D)
arcpy.AddMessage(MultipatchOrPolygon)


# Typelists select by number (0,1)
def type_lists_select(_number):
    # feature 3d lists -- number = "1"
    _feature_3d_lists = ["inwalls", "outwalls", "grounds", "doors", "firedoors", "elevators", "firelifts", "stairs",
                         "escalators", "firearea", "wireframe"]
    # _feature_2d_lists = ["doors", "inwalls", "outwalls", "firedoors", "elevators", "firelifts", "stairs", "grounds",
    #                      "escalators", "exits", "hazards", "wireframe", "firearea"]

    # feature 2d lists -- number = "0"
    _feature_2d_lists = ['inhydrants', 'fire_curtains', 'autoalarmsys', 'handalarmsys', 'pysys', 'sfsys', 'spraysys',
                         'broadcastsys']

    # _feature_2d_lists = ['inhydrants', 'pysys', 'sfsys', 'fire_curtains', 'spraysys', 'autoalarmsys', 'handalarmsys',
    #                      'broadcastsys', 'firedoors', 'fireregions', 'pumpadapter', 'videosys', 'outhydrant', 'roads',
    #                      'hazards', 'refuge_room', 'firepassage', 'control_room', 'fire_waterfeatures']

    _feature_type_lists = _feature_3d_lists if _number == '1' else _feature_2d_lists
    return _feature_type_lists


# Merge by type
def feature_merge_by_type(_ds_path, _out_path, _building_name, _type, shape_type=''):
    _ds_lists = _ds_path.split(';')
    _type_lists = []
    if len(shape_type) == 0:
        for ds in _ds_lists:
            env.workspace = ds
            _ft_lists = arcpy.ListFeatureClasses()
            # arcpy.AddMessage(_ft_lists)
            for ft in _ft_lists:
                if '_' + _type in ft:
                    arcpy.AddMessage(ft)
                    ft_path = ds + '\\' + ft
                    _type_lists.append(ft_path)
    else:
        for ds in _ds_lists:
            env.workspace = ds
            _ft_lists = arcpy.ListFeatureClasses()
            # arcpy.AddMessage(_ft_lists)
            for ft in _ft_lists:
                ft_prop = arcpy.Describe(ft)
                if '_' + _type in ft and ft_prop.shapeType == shape_type:
                    arcpy.AddMessage(ft)
                    ft_path = ds + '\\' + ft
                    _type_lists.append(ft_path)

    arcpy.AddMessage('The length of the {0} list is {1}'.format(_type_lists, len(_type_lists)))
    _ft_merge = _out_path + '\\' + '{0}_{1}_Merge'.format(_building_name, _type)
    if len(_type_lists) != 0:
        arcpy.Merge_management(_type_lists, _ft_merge)
    else:
        arcpy.AddMessage('The {} is not exited'.format(_type))


# Create a feature dataset
def dataset_create(_out_ds_path, _spatial_reference):
    # arcpy.AddMessage(_out_ds_path)
    _ds_name = _out_ds_path.split('\\')[-1]
    # arcpy.AddMessage(_ds_name)
    _out_gdb = _out_ds_path[0:len(_out_ds_path) - len(_ds_name) - 1]
    # arcpy.AddMessage(_out_gdb)
    arcpy.CreateFeatureDataset_management(_out_gdb, _ds_name, _spatial_reference)


# Execute Script Body
if MultipatchOrPolygon:
    shapeType = MultipatchOrPolygon
else:
    shapeType = ''

# Dataset Create
if SpatialReference:
    dataset_create(outPath, SpatialReference)
else:
    dataset_create(outPath, dataSetsPath)

ftTypeLists = type_lists_select(feature2Dor3D)
for ftType in ftTypeLists:
    arcpy.AddMessage(ftType + ' Start.')
    feature_merge_by_type(dataSetsPath, outPath, buildingName, ftType, shapeType)
    arcpy.AddMessage(ftType + ' End.')
    arcpy.AddMessage('        ')
