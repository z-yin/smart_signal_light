# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:07:21 2017

@author: Lios
"""

import data_process as dp
import random  
import copy  
import adapt_func as adp
  
birds = 1000  # 种群数，如果报错，可以把初始化的1000放大
pos = []  
speed = []  
bestpos = []  
birdsbestpos = []
result = []  # 存和为周期长的几个随机数，二维列表
best_location = []
phase_result = []
w = 0.8  
c1 = 2   
c2 = 2  
r1 = 0.6  
r2 = 0.3  
C = 200    # 周期时长，可修改
phase = [4, 4, 3, 5, 3, 4, 3]
minu = [[35, 8, 10, 35], [8, 35, 8, 35], [10, 35, 35], [10, 35, 10, 8, 35], [10, 35, 35], [10, 35, 10, 35], [10, 35, 35]]

a = dp.DataProcess()
a.process()

print("a over")


def generate_rand(lst):
    k = 0
    list1 = []
    list2 = []
    for j in range(10000):
        mark = 0
        list1.append([])
        list2.append([])
        count = 0
        for i in range(phase[k]):
            count = count + 1
            if count == phase[k]:
                break
            num = random.randint(minu[k][i], 200)
            list1[j].append(num)
        list1[j].sort()
        list2[j].append(list1[j][0])
        num = phase[k] - 2
        for i in range(num):
            list2[j].append(list1[j][i + 1] - list1[j][i])
        list2[j].append(200 - list1[j][num])
        while mark == 0:
            if len(list2[j]) != 5:
                list2[j].append(0)
            else:
                mark = 1
    for j in range(10000):
        count = 0
        for i in range(4):
            if list2[j][i] >= minu[k][i]:
                count = count + 1
        if count == 4:
            lst.append(list2[j])


def generate_rand_vec(lst):
    num = random.randint(0, len(result) - 1)
    lst.append(result[num])


def cal_dis(t):
    dis = adp.delay(a, t)
    return dis


def FindBirdsMostPos():
    best = cal_dis(bestpos[0])
    index = 0
    for i in range(birds):
        temp = cal_dis(bestpos[i])
        if temp < best:
            best = temp
            index = i
    best_location.append(index)
    return bestpos[index]


def NumMulVec(num,lst):
    for i in range(len(lst)):
        lst[i] *= num
    return lst


def VecSubVec(list1,list2):
    for i in range(len(list1)):
        list1[i] -= list2[i]
    return list1


def VecAddVec(list1,list2):
    for i in range(len(list1)):
        list1[i] += list2[i]
    return list1


def UpdateSpeed():
    for i in range(birds):
        temp1 = NumMulVec(w,speed[i][:])
        temp2 = VecSubVec(bestpos[i][:],pos[i])
      #  r1=random.random()
        temp2 = NumMulVec(c1*r1,temp2[:])
        temp1 = VecAddVec(temp1[:],temp2)
        temp2 = VecSubVec(birdsbestpos[:],pos[i])
      #  r2=random.random()
        temp2 = NumMulVec(c2*r2,temp2[:])
        speed[i] = VecAddVec(temp1,temp2)


def UpdatePos():
    global bestpos, birdsbestpos
    for i in range(birds):
        VecAddVec(pos[i],speed[i])
        if cal_dis(pos[i])<cal_dis(bestpos[i]):
            bestpos[i] = copy.deepcopy(pos[i])
    birdsbestpos = FindBirdsMostPos()

generate_rand(result)
print(len(result))
for i in range(birds):
    generate_rand_vec(pos)
    generate_rand_vec(speed)
    bestpos.append([])
    bestpos[i] = copy.deepcopy(pos[i])

print(bestpos[0])
birdsbestpos = FindBirdsMostPos()

for i in range(100):   # 迭代次数，可修改
    print("i = ", i)
    Dis = cal_dis(birdsbestpos)
    phase_result.append(Dis)
    UpdateSpeed()
    UpdatePos()

i = phase_result.index(min(phase_result))
print(pos[best_location[i]])
# 如果第i次结果最优，结果在pos[j]:j = best_location[i]


