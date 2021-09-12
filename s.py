# -*- coding: utf-8 -*-
from main import *
with tqdm(ip_list, ascii=False, ncols=75) as bar:
    for i in ip_list:
        start_ping(i, 16802, bar)

number -= 1
if print_result():
    print('SSH Server is online.')
with tqdm(ip_list, ascii=False, ncols=75) as bar:
    for i in ip_list:
        start_ping(i, 8006, bar)

number -= 1
if print_result():
    print('PVE Server is online.')
with tqdm(ip_list, ascii=False, ncols=75) as bar:
    for i in ip_list:
        start_ping(i, 16803, bar)

number -= 1
if print_result():
    print('Minecraft Server is online.')

os.system('pause')
