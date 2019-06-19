import os
import arcpy
from arcpy import env

folderPath = arcpy.GetParameterAsText(0)
buildingAbbre = arcpy.GetParameterAsText(1)
gdbNameStr = arcpy.GetParameterAsText(2)
gdbNameLists = gdbNameStr.split(';')

folderNew = ''
# Create a new folder
env.workspace = folderPath
for i in range(0, 10):
    if i == 0:
        if 'results' not in arcpy.ListFiles():
            arcpy.CreateFolder_management(folderPath, 'results')
            folderNew = 'results'
            break
    else:
        if 'results' + str(i) not in arcpy.ListFiles():
            arcpy.CreateFolder_management(folderPath, 'results' + str(i))
            folderNew = 'results' + str(i)
            break
arcpy.AddMessage('{} folder was created.'.format(folderNew))

# Create GDB
for gn in gdbNameLists:
    gName = buildingAbbre + '_' + gn
    arcpy.CreateFileGDB_management(os.path.join(folderPath, folderNew), '{}.gdb'.format(gName))
    arcpy.AddMessage('{}.gdb was created.'.format(gName))
