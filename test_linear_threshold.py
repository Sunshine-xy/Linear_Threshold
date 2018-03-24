#!/usr/bin/env python
# coding=UTF-8                 #支持中文字符需要添加  coding=UTF-8
from nose.tools import *
from networkx import *
from linear_threshold import *
import time
"""Test Diffusion Models
----------------------------
"""
if __name__=='__main__':
    start=time.clock()
    datasets=[]
    f=open("Wiki-Vote.txt","r")        #读取文件数据（边的数据）
    data=f.read()
    rows=data.split('\n')
    for row in rows:
      split_row=row.split('\t')
      name=(int(split_row[0]),int(split_row[1]))
      datasets.append(name)            #将边的数据以元组的形式存放到列表中

    G=networkx.DiGraph()               #建立一个空的有向图G
    G.add_edges_from(datasets)         #向有向图G中添加边的数据列表
    layers=linear_threshold(G,[25],2)     #调用LT线性阈值算法，返回子节点集和该子节点集的最大激活节点集
    del layers[-1]
    length=0
    for i in range(len(layers)):
        length =length+len(layers[i])
    lengths=length-len(layers[0])       #获得子节点的激活节点的个数（长度）
    end=time.clock()
    #测试数据输出结果
    print(layers)  #[[25], [33, 3, 6, 8, 55, 80, 50, 19, 54, 23, 75, 28, 29, 30, 35]]
    print(lengths) #15
    print('Running time: %s Seconds'%(end-start))  #输出代码运行时间




