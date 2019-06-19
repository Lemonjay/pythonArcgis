# -- coding: utf-8 --
# ! usr/bin/python
# coding = utf-8

import arcpy
from arcpy import env

env.overwriteOutput = True
env.workspace = r"D:\myDocuments\Desktop\jscloud.gdb\Building_Label"
fieldLists = arcpy.ListFields("jscloud_label")

# fieldTemp = []
#
# for field in fieldLists:
#     print field.name
#     print field.type
#     print field.precision
#     print field.scale
#     print field.length
#     fieldTemp.append(field.name)

fieldOrder = ['building_id', 'building_name', 'type', 'adress', 'telphone', 'structure', 'height', 'elevation',
              'floors_up', 'floor_down', 'refuge_storey', 'covered_area', 'total_area']

fieldAlias = ['建筑ID', '建筑名称', '类型', '地址', '电话', '结构', '地面高度', '高程',
              '地上楼层', '地下楼层', '避难层', '占地面积', '建筑面积']

for i in range(len(fieldOrder)):
    for field in fieldLists:
        fieldList = fieldOrder[i]
        if fieldList == field.name:
            fieldNew = fieldList + "_1"
            arcpy.AddField_management("jscloud_label", fieldNew, field.type, field.precision, field.scale,
                                      field.length)
            expression = '!{}!'.format(fieldList)  # 字符串无法直接变成变量名，需要加一个转换
            print expression
            arcpy.CalculateField_management("jscloud_label", fieldNew, expression, "PYTHON_9.3")
            arcpy.DeleteField_management("jscloud_label", fieldList)
            print (fieldList + "_Deleted")

fieldLists = arcpy.ListFields("jscloud_label")
for i in range(len(fieldOrder)):
    for field in fieldLists:
        fieldNew = fieldOrder[i]
        if fieldNew + "_1" == field.name:
            print (field.name + "_Start")
            arcpy.AddField_management("jscloud_label", fieldNew, field.type, field.precision, field.scale,
                                      field.length, fieldAlias[i])
            expression = '!{}!'.format(field.name)  # 字符串无法直接变成变量名，需要加一个转换
            print expression
            arcpy.CalculateField_management("jscloud_label", fieldNew, expression, "PYTHON_9.3")
            arcpy.DeleteField_management("jscloud_label", field.name)
            print (field.name + "_Deleted")
