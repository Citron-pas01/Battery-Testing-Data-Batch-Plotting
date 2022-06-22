# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 18:16:28 2020

@author: bfn5081
"""

from cycling import data_process, cycle_stat
import os
import re
import time


def convertPath(path):
    sep = os.path.sep
    if sep != '/':
        path = path.replace(os.path.sep, '/')
    return path


def sorted_aphanumeric(data):
    def convert(text): return int(text) if text.isdigit() else text.lower()
    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def file_list1(root):
    papers = []
    filename = []
    try:
        for d in sorted_aphanumeric(os.listdir(root)):
            new_d = convertPath(root)
            name = d.replace('.csv', '')
            filename.append(name)
            # this is to make sure it is a end file path instead of sub folder
            if os.path.isfile(new_d + '/' + d) and d.endswith('.csv') :
                papers.append(new_d + '/' + d)
        return sorted_aphanumeric(papers),filename
    except:
        pass


def create_db(paper_root, start=0, end=None, end_cycle = None):
    # set up the database

    file_l,file_name = file_list1(paper_root)
    file_l = file_l[int(start):int(end)]
    file_name = file_name[int(start):int(end)]

    cycle_dict = dict()
    for i in range(len(file_l)):
        print(file_l[i], file_name[i])

        # to draw the charge-discharge curve
        cycle_stat_i = data_process(file_l[i], file_name[i], end_cycle)
        cycle_dict[file_name[i]] = cycle_stat_i
        print('--------------------------------the next file-----------------------------------')
    
    # this is to draw the cyclic curve
    cycle_stat(cycle_dict, end_cycle)

    return
# this file is debugged over

if __name__ == '__main__':
    start_time = time.time()
    file_root = r'C:\Users\Bo_Ni\Desktop\btd'

    # change the file read numbers and cycling numbers 
    create_db(file_root, start=0, end=3, end_cycle = 4)

    elapsed_time = (time.time() - start_time)
    print('-------------------','%.2f' % round(elapsed_time, 2),'Seconds -----------------------')
