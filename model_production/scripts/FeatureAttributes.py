#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释
# UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0'in position
# problem solved
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import arcpy
from arcpy import env
from collections import OrderedDict

arcpy.env.overwriteOutput = True


def field_name(x):
    return x.name


class FieldOperation(object):
    def __init__(self, _feature):
        self._feature = _feature

    # Field Add and Delete
    def feature_field_op(self):
        _fld_names = ['building_id', 'type', 'floor', 'floor_z', 'z', 'floor_d', 'name', 'city', 'province', 'status']
        _fld_types = ['TEXT', 'TEXT', 'SHORT', 'FLOAT', 'FLOAT', 'FLOAT', 'TEXT', 'TEXT', 'TEXT', 'TEXT']
        _fld_alias = ['建筑Id', '类型', '楼层', '层高', '显示高度', '层差', '建筑名称', '市', '省', '状态']

        # Existed fields
        _ft_field_names = list(map(field_name, arcpy.ListFields(self._feature)))
        for fld_i in range(len(_fld_names)):
            if _fld_names[fld_i] in _ft_field_names:
                arcpy.AddMessage("The '{0}' field of the {1} was existed".format(_fld_names[fld_i], self._feature))
            else:
                arcpy.AddField_management(self._feature, _fld_names[fld_i], _fld_types[fld_i],
                                          field_alias=_fld_alias[fld_i])
                arcpy.AddMessage("The '{0}' field of the {1} was added.".format(_fld_names[fld_i], self._feature))

        # Ground fields
        if 'grounds' in self._feature:
            if 'function_type' not in _ft_field_names:
                arcpy.AddField_management(self._feature, 'function_type', 'TEXT', field_alias='功能类型')
                arcpy.AddMessage("The '{0}' field of the {1} was added.".format('function_type', self._feature))

        # Delete fields
        _fld_names_add = ['function_type', 'refname', 'text']
        _fld_names_add.extend(_fld_names)
        for fld in arcpy.ListFields(self._feature):
            if fld.name.lower() in _fld_names_add:
                arcpy.AddMessage("The '{0}' field of the {1} was used".format(fld.name, self._feature))
            else:
                try:
                    arcpy.DeleteField_management(self._feature, fld.name)
                    arcpy.AddMessage("The '{0}' field of the {1} was deleted".format(fld.name, self._feature))
                except:
                    arcpy.AddMessage("The '{0}' field of the {1} cannot be deleted".format(fld.name, self._feature))

    # Filled value in the field ('building_id', 'name', 'city', 'province')
    def constant_value_fill(self, _building_id='', _name='', _city='', _province=''):
        _field_dict = {'building_id': _building_id, 'name': _name, 'city': _city, 'province': _province}
        for _key in _field_dict.keys():
            if len(_field_dict[_key]) != 0:
                arcpy.CalculateField_management(self._feature, _key, "'{}'".format(_field_dict[_key]), "PYTHON_9.3")
                arcpy.AddMessage('The value {1} was added in the {0} field'.format(_key, _field_dict[_key]))

    # Filled value in the type field (not include ['autoalarmsys','pysys','sfsys','escalators'])
    def type_value_fill(self):
        # featureTypes = ["inwalls", "outwalls", "grounds", "doors", "firedoors", "elevators", "firelifts", "stairs",
        #                 "firearea", "wireframe", "inhydrants", "fire_curtains", "handalarmsys"]
        #
        # typeValue = ['内墙', '外墙', '地板', '门', '防火门', '客用电梯', '消防电梯', '疏散楼梯', '防火分区', '线框', '室内消火栓', '防火卷帘', '手动报警器']

        type_field_dict = {'inwalls': '内墙', 'outwalls': '外墙', 'grounds': '地板', 'doors': '门', 'firedoors': '防火门',
                           'elevators': '客用电梯', 'firelifts': '消防电梯', 'stairs': '疏散楼梯', 'firearea': '防火分区',
                           'wireframe': '线框', 'inhydrants': '室内消火栓', 'fire_curtains': '防火卷帘', 'handalarmsys': '手动报警器'}
        for _key in type_field_dict.keys():
            if '_' + _key in self._feature:
                arcpy.CalculateField_management(self._feature, 'type', "'{}'".format(type_field_dict[_key]),
                                                "PYTHON_9.3")
                arcpy.AddMessage(
                    'The value {0} was added in the {1} feature'.format(type_field_dict[_key], self._feature))

    # Filled value in the status field
    def status_value_fill(self):
        _type_lists = ['pysys', 'sfsys', 'handalarmsys']
        for _type in _type_lists:
            if _type in self._feature:
                arcpy.CalculateField_management(self._feature, "status", "'运行'", "PYTHON_9.3")

        _type_lists = ['inhydrants', 'autoalarmsys', 'broadcastsys', 'spraysys', 'fire_curtains']
        for _type in _type_lists:
            if _type in self._feature:
                arcpy.CalculateField_management(self._feature, "status", "'正常'", "PYTHON_9.3")

    # Field reorder
    def field_reorder(self):
        _field_lists = [('building_id', '建筑ID'), ('type', '类型'), ('floor', '楼层'), ('floor_z', '层高'), ('status', '状态'),
                        ('fire_area', '防火分区'), ('function_type', '功能类型'), ('door_aspect', '门_方向'),
                        ('area_type', '分区类型'), ('name', '建筑名称'), ('z', '显示高度'), ('floor_d', '层差'), ('city', '市'),
                        ('province', '省')]
        _field_order_lists = OrderedDict(_field_lists)  # 按照输入的顺序，输出字典的key和value
        # Field Copy
        for _key in _field_order_lists.keys():
            # arcpy.AddMessage(_key)
            for fld in arcpy.ListFields(self._feature):
                if fld.name == _key:
                    _field_new = _key + '_1'
                    arcpy.AddField_management(self._feature, _field_new, fld.type, fld.precision, fld.scale, fld.length)
                    expression = '!{}!'.format(_key)  # 字符串无法直接变成变量名，需要加一个转换
                    # arcpy.AddMessage(expression)
                    arcpy.CalculateField_management(self._feature, _field_new, expression, "PYTHON_9.3")
                    arcpy.DeleteField_management(self._feature, _key)
                    # arcpy.AddMessage("The {0} was deleted.".format(_key))
        # Field Reorder
        for _key in _field_order_lists.keys():
            for fld in arcpy.ListFields(self._feature):
                if fld.name == _key + '_1':
                    arcpy.AddField_management(self._feature, _key, fld.type, fld.precision, fld.scale, fld.length,
                                              _field_order_lists[_key])
                    expression = '!{}!'.format(fld.name)  # 字符串无法直接变成变量名，需要加一个转换
                    # arcpy.AddMessage(expression)
                    arcpy.CalculateField_management(self._feature, _key, expression, "PYTHON_9.3")
                    arcpy.DeleteField_management(self._feature, fld.name)
                    # arcpy.AddMessage("The {0} was deleted.".format(fld.name))
        arcpy.SetLogHistory(True)
