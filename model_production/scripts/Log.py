import os
import time


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

