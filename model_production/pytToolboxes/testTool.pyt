# -- coding: cp936 --
# ! usr/bin/python
# coding = utf-8

import arcpy
from arcpy import env
import time
import os


# Create log file
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


# gdb_backup
def gdb_backup(_in_gdb):
    folder_bk = r'D:\myDocuments\Desktop\DataReorder\data_backup'
    _gdb = arcpy.Describe(_in_gdb).name
    _gdb_name = _gdb.replace('.gdb', '')
    print(_gdb_name)
    _time_bk = time.strftime('%Y%m%d', time.localtime(time.time()))
    _out_gdb_name = _gdb_name + '_' + _time_bk + '.gdb'
    _out_gdb = folder_bk + '/' + _out_gdb_name
    print(_out_gdb)
    arcpy.Copy_management(_in_gdb, _out_gdb)
    log_write(_gdb, 'The {0} was copy.   The backup file : {1}'.format(_gdb, _out_gdb_name))

    # Print the lists of the gdb database

    env.workspace = _in_gdb
    arcpy.AddMessage(arcpy.ListDatasets())
    log_write(_gdb, 'There are {0} buildings in the {1} datasets.'.format(len(arcpy.ListDatasets()), _gdb))
    log_write(_gdb, '{}'.format(arcpy.ListDatasets()))
    arcpy.AddMessage('           ')


# # Execute Script Tool Body
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Database Operation"
        self.alias = "pytTests"

        # List of tool classes associated with this toolbox
        self.tools = [GdbBackup]


class GdbBackup(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "gdb_backup"
        self.description = "gdb backup"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        # Input Features parameter
        in_gdb_path = arcpy.Parameter(
            displayName="Input gdb",
            name="in_features",
            datatype="DEType",
            parameterType="Required",
            multiValue='True',
            direction="Input")
        params = [in_gdb_path]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        env.overwriteOutput = True
        gdb_path_lists = parameters[0].valueAsText

        # Execute Script Body
        gdb_path = gdb_path_lists.split(';')
        for gp in gdb_path:
            env.workspace = gp
            arcpy.AddMessage(arcpy.ListDatasets())
            dsp = arcpy.ListDatasets()
            for ds in dsp:
                env.workspace = ds
                ftp = arcpy.ListFeatureClasses()
                for ft in ftp:
                    arcpy.AddMessage(ft)
                    ft_cursor = arcpy.SearchCursor(ft)
                    for row in ft_cursor:
                        if row.getValue('type') == '室内消火栓':
                            arcpy.AddMessage(row.getValue('type'))
        return
