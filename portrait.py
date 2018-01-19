# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 23:28:29 2017

@author: wyl
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import math
import data_process
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

plt.close()  # clf() # 清图  cla() # 清坐标轴 close() # 关窗口
fig = plt.figure()
fig.set_size_inches(2, 18)
print fig.get_size_inches()
ax = fig.add_subplot(1, 1, 1)
# ax.axis("equal")  # 设置图像显示的时候XY轴比例
plt.grid(True)  # 添加网格
plt.ion()  # interactive mode on

xmajorLocator = MultipleLocator(200)  # 将x主刻度标签设置为20的倍数

ymajorLocator = MultipleLocator(200)  # 将y轴主刻度标签设置为0.5的倍数

ax.xaxis.set_major_locator(xmajorLocator)

ax.yaxis.set_major_locator(ymajorLocator)

plt.xlim(520955.0, 521920.0)
plt.ylim(53380.0, 58715.0)
print('开始仿真')
a = data_process.DataProcess()
a.process()

try:
    intersection = data_process.InterSection()
    for i in intersection.dict_location:
        ax.scatter(intersection.dict_location[i][0], intersection.dict_location[i][1], c='r', marker='+')  # 散点图

    # for i in a.vehicles:
    for j in a.vehicles['2c974ed99d80730b41779ec813498646'].tr_info:
        for x in a.vehicles['2c974ed99d80730b41779ec813498646'].tr_info[j]:
        # for y in a.vehicles[i].tr_info:
        #     for x in a.vehicles[i].tr_info[y]:
            ax.scatter(x.x_coordinate, x.y_coordinate, s=3, c='b', marker='.')  # 散点图
            # 下面的图,两船的距离
            plt.pause(0.01)
            # ax.lines.pop(1)  # 删除轨迹
except Exception as err:
    print(err)
