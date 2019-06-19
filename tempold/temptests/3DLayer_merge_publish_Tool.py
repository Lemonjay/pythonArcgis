"""
portal 服务发布流程第三次迭代，因为考虑到服务过多，需要对三维要素进行合并，按照每栋楼作为一个到2个三维要素标准进行合并，
合并完成后，进行发布。地板需要承载的信息比较多，因此需要单开一个服务。其他，诸如内墙外墙，都是而配合显示的，为了减少三维
服务个数，目前采用的方法。其合理性，仍有待进一步测试。
128个三维服务，每个三维服务需要内存120Mb 左右，32g内存理论上能支持100个gis服务。

"""

# !/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释

import arcpy, os
from arcpy import env

env.overwriteOutput = True
inPath = arcpy.GetParameterAsText(0)
env.workspace = inPath
dataSet = arcpy.GetParameterAsText(1)
# arcpy.AddMessage(dataSets, end='')
# arcpy.AddMessage(dataSets)
# arcpy.AddMessage(len(dataSets), end=" ")
# arcpy.AddMessage("Building" + "datasets")
dataSets_outPath = arcpy.GetParameterAsText(2)
# layerFullNumber = 0

arcpy.CreateFeatureDataset_management(dataSets_outPath, dataSet, dataSet)
env.workspace = inPath + "/" + dataSet
features = arcpy.ListFeatureClasses()
layerNumber = 0
featureTemp = []
for feature in features:
    arcpy.AddMessage(feature)
    # featureTemp.append(feature)
    if "grounds" not in feature:
        featureTemp.append(feature)
    else:
        featureCopy = dataSets_outPath + "/" + dataSet + "/" + feature
        arcpy.Copy_management(feature, featureCopy)
    layerNumber = layerNumber + 1
featureMerge = dataSets_outPath + "/" + dataSet + "/" + dataSet
featureMergeOld = featureMerge + "_Old"
arcpy.AddMessage(featureTemp)
arcpy.Merge_management(featureTemp, featureMergeOld)

# 添加防火分区字段
arcpy.AddField_management(featureMergeOld, 'function_type', 'TEXT')
arcpy.CalculateField_management(featureMergeOld, 'function_type', '!type!', "PYTHON_9.3")

arcpy.Merge_management([featureCopy, featureMergeOld], featureMerge)
arcpy.Delete_management(featureMergeOld)

arcpy.AddMessage('---------------------------------------------------')
arcpy.AddMessage(dataSet + " " + str(layerNumber) + " " + "features")
arcpy.AddMessage('---------------------------------------------------')
# layerFullNumber = layerFullNumber + layerNumber
env.workspace = inPath
arcpy.AddMessage('***************************************************')
arcpy.AddMessage('                                                   ')
arcpy.AddMessage('---------------------------------------------------')
arcpy.AddMessage(str(layerNumber) + " features")
