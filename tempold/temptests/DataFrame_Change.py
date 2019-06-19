# encoding: utf-8

import arcpy, os
from arcpy import env

env.overwriteOutput = True
mxd_Path = r"D:\myDocuments\Documents\ArcGIS\Projects\Features_3dPublish\mxd"
env.workspace = mxd_Path
mxdfileList_existed = arcpy.ListFiles()
print(mxdfileList_existed)

for mxdFile in mxdfileList_existed:
    if mxdFile != "Temp.mxd":
        mxdFile_Path = mxd_Path + "/" + mxdFile
        mxd = arcpy.mapping.MapDocument(mxdFile_Path)
        layer = arcpy.mapping.ListDataFrames(mxd)[0]
        layer.name = mxdFile.replace(".mxd", "")  # 对layer的name的属性直接更改名字，就可以改变图层数值，可能是python默认的规定
        print(layer.name)
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        mxd.save()
