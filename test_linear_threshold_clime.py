#!/usr/bin/env python
# coding=UTF-8
from nose.tools import *
from networkx import *
from linear_threshold_clime import *
import time
"""Test Diffusion Models
----------------------------
"""
#贪心算法
def _linear_clime(G,k):      #参数k-表示要获取的子节点的个数
    allnodes = G.nodes()     #获取图中所有节点数
    seed_nodes = []          #该列表存储选取的子节点集
    for m in range(k):
        all_nodes = list(allnodes)   #将所有的节点存储在all_nodes列表里
        layers_activite = []    # 存储每个节点的激活节点列表
        lengths = []         # 存储每个节点的激活列表长度
        datas = []
        for i in all_nodes:   #遍历所有的节点，分别求出每个节点对应的激活节点集以及激活节点集的长度
            data = []
            data.append(i)
            datas.append(i)
            data_test=seed_nodes+data
            layers = linear_threshold(G,data_test)
            data.pop()
            del layers[-1]
            length = 0
            layer_data = []
            for j in range(len(layers)):
                length = length + len(layers[j])
                layer_data = layer_data + layers[j]
            length_s = length - len(layers[0])
            for s in range(len(layers[0])):
                del layer_data[0]
            layers_activite.append(layer_data)
            lengths.append(length_s)
      # length_max = max(lengths)  # 获取激活节点最多的节点数
        layers_max = layers_activite[lengths.index(max(lengths))]  # 获取被激活节点数最多的列表
        seed_nodes.append(datas[lengths.index(max(lengths))])      # 获取被激活节点最多的子节点
        for i in all_nodes:       #该循环是删除所有节点中seed_nodes节点集
            if i in seed_nodes:
                del all_nodes[all_nodes.index(i)]
        allnodes=all_nodes
    return seed_nodes,layers_max     #返回值是贪心算法求得的子节点集和该子节点集激活的最大节点集

#测试算法
if __name__=='__main__':
    start=time.clock()
    datasets=[]
    f=open("Wiki-Vote.txt")
    data=f.read()
    rows=data.split('\n')
    for row in rows:
      split_row=row.split('\t')
      name=(int(split_row[0]),int(split_row[1]))
      datasets.append(name)
    G=networkx.DiGraph()
    G.add_edges_from(datasets)   #根据数据集创建有向图

    n=input('Please input the number of seeds: k=')
    k=int(n)
    seed_nodes, layers_max=_linear_clime(G,k)   #调用贪心算法获取节点子集和节点子集的最大激活节点集
    lenth=len(layers_max)
    end=time.clock()
    print(seed_nodes)
    print(layers_max)
    print(lenth)
    print('Running time: %s Seconds'%(end-start))


