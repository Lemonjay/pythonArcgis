import os
import arcpy
from arcpy import env

folderPath = arcpy.GetParameterAsText(0)
gdbName = arcpy.GetParameterAsText(1) if arcpy.GetParameterAsText(1) else 'result'
arcpy.AddMessage(gdbName)
dsNameStr = arcpy.GetParameterAsText(2)
spatialReference = arcpy.GetParameterAsText(3)

arcpy.AddMessage(os.path.join(folderPath, gdbName + '.gdb'))
if not os.path.exists(os.path.join(folderPath, gdbName + '.gdb')):
    arcpy.CreateFileGDB_management(folderPath, gdbName)

dsNameLists = dsNameStr.split(';')
arcpy.AddMessage(dsNameLists)
for dsName in dsNameLists:
    arcpy.AddMessage(dsName)
    try:
        arcpy.CreateFeatureDataset_management(os.path.join(folderPath, gdbName + '.gdb'), dsName, spatialReference)
    except:
        arcpy.AddMessage('The {1} dataset of {0} was existed.'.format(gdbName + '.gdb', dsName))
