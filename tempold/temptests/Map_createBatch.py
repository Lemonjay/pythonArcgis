# encoding: utf-8

import arcpy, os
from arcpy import env

env.overwriteOutput = True
mxd_Path = r"D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\mxd"
env.workspace = mxd_Path
print(arcpy.ListFiles())

arcpy.AcceptConnections(r'D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\jscloud.sde', True)
sde_Path = r"D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\jscloud.sde"
env.workspace = sde_Path
sde_Datasets = arcpy.ListDatasets()

for sde_Dataset in sde_Datasets:
    print (sde_Dataset)
    print("********************************************")
    sde_DatasetName = sde_Dataset.replace('jscloud.sde.', '')  # 去除指定字符串“jscloud.sde.”
    mxdTemp = mxd_Path + "/" + "Temp.mxd"
    mxdNew = mxd_Path + "/" + sde_DatasetName + ".mxd"
    arcpy.Copy_management(mxdTemp, mxdNew)
    env.workspace = sde_Path + "/" + sde_Dataset
    # 读取 MXD 工程
    mxd = arcpy.mapping.MapDocument(mxdNew)
    layer = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # 图层添加位置
    print(layer.name)
    features = arcpy.ListFeatureClasses()
    for feature in features:
        print(feature)
        layerAdd = arcpy.mapping.Layer(feature)  # feature临时存储到 map.layer中
        print(layerAdd)
        print(layerAdd.datasetName)
        arcpy.mapping.AddLayer(layer, layerAdd, "AUTO_ARRANGE")  # 添加图层

    arcpy.RefreshActiveView()
    arcpy.RefreshTOC()
    mxd.save()
    # x = os.startfile(mxdNew)
    print("********************************************")
    print("--------------------------------------------")
    print("                                            ")
    print("                                            ")
    env.workspace = sde_Path

# 测试代码
# mxdPath = r'D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\lygCity_snS.mxd'
# mxd = arcpy.mapping.MapDocument(mxdPath)
#
# layer = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
# print(layer.name)
#
# layerNew = r'D:\myDocuments\Desktop\DataReorder\jsCloud_3D.gdb\ncCity_xlC\ncCity_xlC_doors'
# layerNewAdd = arcpy.mapping.Layer(layerNew)
#
# arcpy.mapping.AddLayer(layer, layerNewAdd, "AUTO_ARRANGE")
# arcpy.RefreshActiveView()
# arcpy.RefreshTOC()
#
# mxd.save()
# x = os.startfile(mxdPath)
#
# print mxd
