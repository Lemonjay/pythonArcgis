#!/usr/bin/python
# -*- coding: utf-8 -*-
# 中文注释
# UnicodeEncodeError: 'ascii' codec can't encode character u'\xa0'in position
# problem solved
import sys
from collections import OrderedDict

reload(sys)
sys.setdefaultencoding('utf-8')

_building_id = 'zc001'
_name = '涵月楼'
_city = '南京市'
_province = '江苏省'
field_dict = {'building_id': _building_id, 'name': _name, 'city': _city, 'province': _province}
print field_dict['name'] == _name
print(field_dict)

print(_name)
for key in field_dict.keys():
    print key, field_dict[key]
    print(type(key))

fieldOrder = ['building_id', 'type', 'floor', 'floor_z', 'status', 'fire_area', 'function_type', 'door_aspect',
              'area_type', 'name',
              'z', 'city', 'province']

fieldAlias = ['建筑ID', '类型', '楼层', '层高', '状态', "防火分区", "功能类型", '门_方向', '分区类型', '建筑名称', '显示高度', '市', '省']

for i in range(len(fieldOrder)):
    print "('{0}','{1}'),".format(fieldOrder[i], fieldAlias[i]),
print '         '
_field_lists = [('building_id', '建筑ID'), ('type', '类型'), ('floor', '楼层'), ('floor_z', '层高'), ('status', '状态'),
                ('fire_area', '防火分区'), ('function_type', '功能类型'), ('door_aspect', '门_方向'), ('area_type', '分区类型'),
                ('name', '建筑名称'), ('z', '显示高度'), ('city', '市'), ('province', '省')]

_field_order = OrderedDict(_field_lists)
print(_field_order)
# Field Copy
for key in _field_order.keys():
    print key, _field_order[key]

_feature_3d_lists = ["inwalls", "outwalls", "grounds", "doors", "firedoors", "elevators", "firelifts", "stairs",
                     "escalators", "firearea", "wireframe"]
_feature_3d_lists = ['inhydrants', 'fire_curtains', 'autoalarmsys', 'handalarmsys', 'pysys', 'sfsys', 'spraysys',
                         'broadcastsys']

def name(x):
    return '_' + x


_ft_lists = list(map(name, _feature_3d_lists))
print(_ft_lists)
