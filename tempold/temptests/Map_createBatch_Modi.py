# encoding: utf-8

import arcpy
from arcpy import env

env.overwriteOutput = True
mxd_Path = r"D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\mxd"
env.workspace = mxd_Path
mxdList_existed = arcpy.ListFiles()
print(mxdList_existed)

arcpy.AcceptConnections(r'D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\jscloud.sde', True)
sde_Path = r"D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\jscloud.sde"
env.workspace = sde_Path
sde_Datasets = arcpy.ListDatasets()
print(sde_Datasets)

for sde_Dataset in sde_Datasets:
    print (sde_Dataset)
    print("********************************************")
    sde_DatasetName = sde_Dataset.replace('jscloud.sde.', '')  # 去除指定字符串“jscloud.sde.”
    mxdTemp = mxd_Path + "/" + "Temp.mxd"
    mxdNew = mxd_Path + "/" + sde_DatasetName + ".mxd"
    # 如果文件夹中已经存在此工程，直接跳过
    if sde_DatasetName + ".mxd" not in mxdList_existed:
        arcpy.Copy_management(mxdTemp, mxdNew)
        sde_featurePath = sde_Path + "/" + sde_Dataset
        env.workspace = sde_featurePath
        # 读取 MXD 工程
        mxd = arcpy.mapping.MapDocument(mxdNew)
        layer = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]  # 图层添加位置
        layer.name = sde_DatasetName  # layers名称修改
        print(layer.name)
        features = arcpy.ListFeatureClasses()
        for feature in features:
            print(feature)
            layerAdd = arcpy.mapping.Layer(
                sde_featurePath + "/" + feature)  # feature临时存储到 map.layer中,加路径和不加路径，layerAdd的名称是不一样的，不加路径出来的是简称（不全的）
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
