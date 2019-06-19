# encoding: utf-8

import arcpy
from Log import log_write


def ly_name(x):
    return x.name


def map_create(_dataset, _sde_path, _mxd_folder):
    arcpy.AcceptConnections(_sde_path, True)
    _dataset_name = _sde_path.split('\\')[-1] + '.' + _dataset
    _dataset_path = _sde_path + '/' + _dataset_name
    print(_dataset_path)
    arcpy.env.workspace = _mxd_folder
    mxd_list = arcpy.ListFiles()
    mxd_temp = _mxd_folder + "/" + "Temp.mxd"
    mxd_new = _mxd_folder + "/" + _dataset + ".mxd"
    if _dataset + '.mxd' not in mxd_list:
        log_write(_dataset, "{}.mxd was created".format(_dataset))
        arcpy.Copy_management(mxd_temp, mxd_new)
        # Read MXD file
        _mxd = arcpy.mapping.MapDocument(mxd_new)
        # Read Layers sets
        _layers = arcpy.mapping.ListDataFrames(_mxd, "Layers")[0]
        _layers.name = _dataset  # Layers sets rename
        print(_layers.name)
        # Read feature lists
        arcpy.env.workspace = _dataset_path
        for ft in arcpy.ListFeatureClasses():
            print(ft)
            layer_add = arcpy.mapping.Layer(
                _dataset_path + '/' + ft)  # This operation need to add full path in order to keeping the full name of the layer.
            print(layer_add)
            print(layer_add.datasetName)
            arcpy.mapping.AddLayer(_layers, layer_add, "AUTO_ARRANGE")  # Add layer
            log_write(_dataset, "{1} was added in {0}.mxd".format(_dataset, ft))
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        _mxd.save()
    else:
        _mxd = arcpy.mapping.MapDocument(mxd_new)
        log_write(_dataset, "{}.mxd was Exited".format(_dataset))
        print(arcpy.mapping.ListLayers(_mxd))
        layer_lists = list(map(ly_name, arcpy.mapping.ListLayers(_mxd)))
        print(layer_lists)
        # Read feature lists
        arcpy.env.workspace = _dataset_path
        print(arcpy.ListFeatureClasses())
        for ft in arcpy.ListFeatureClasses():
            if ft not in layer_lists:
                print(ft)
                layer_add = arcpy.mapping.Layer(
                    _dataset_path + '/' + ft)  # This operation need to add full path in order to keeping the full name of the layer.
                print(layer_add)
                print(layer_add.datasetName)
                _layers = arcpy.mapping.ListDataFrames(_mxd, _dataset)[0]
                arcpy.mapping.AddLayer(_layers, layer_add, "AUTO_ARRANGE")  # Add layer
                log_write(_dataset, "{1} was added in {0}.mxd".format(_dataset, ft))
        arcpy.RefreshActiveView()
        arcpy.RefreshTOC()
        _mxd.save()



