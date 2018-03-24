#!/usr/bin/env python
# coding=UTF-8
from nose.tools import *
from networkx import *
from linear_threshold_clime import *
from linear_threshold  import *
import math
import time

#计算图中边的权重
def Buv_calculate(G,u,v):
    out_deg_all = G.out_degree()  # 获取所有节点的出度
    in_edges_all = G.in_edges()  # 获取所有的入边
    out_deg = out_deg_all[u]  # 获取节点e[0]的出度
    in_edges = in_edges_all._adjdict[v]  # 获取节点e[1]的所有的入边
    edges_dict = dict(in_edges)
    in_all_edges = list(edges_dict.keys())  # 获取节点e[1]的所有入边节点并存入列表
    out_deg_sum = 0
    for i in in_all_edges:  # 求节点e[1]所有入边节点的出度和
        out_deg_sum = out_deg_sum + out_deg_all[i]
    return out_deg / out_deg_sum

#计算每个节点AP的值
def AP_calculate(node):
    data = []
    data.append(node)
    layer_two_nodes = linear_threshold(G, data, 2)  # 获取每个节点的两层出度节点数
    data.pop()
    del layer_two_nodes[-1]
    length = 0
    for i in range(len(layer_two_nodes)):
        length = length + len(layer_two_nodes[i])
    lengths = length - len(layer_two_nodes[0])

    out_edges = out_edges_all._adjdict[node]  # 获得节点的出边
    edges_dict = dict(out_edges)
    out_all_edges = list(edges_dict.keys())  # 将节点的所有出边存入列表
    Buv_sum = 0
    for out_edge in out_all_edges:   # 计算该节点所有出边的Buv的值
        Buv = Buv_calculate(G, node, out_edge)
        Buv_sum = Buv_sum + Buv
    cha_sum = 1 + math.e ** (-Buv_sum)
    AP = lengths + cha_sum
    return AP

def select_layers(G,node_list_sorted,k1):   #选择前k/2个节点的算法实现
    seed_nodes = []  # 存贮种子节点
    for i in range(k1):
        data = []
        data.append(node_list_sorted[0][0])
        seed_nodes.append(node_list_sorted[0][0])
        layers = linear_threshold(G, data)        # 使用LT算法
        data.pop()
        del layers[-1]
        layers_activate = []
        for i in layers:  # 将种子节点和激活的节点存入layers_activate列表
            for j in i:
                layers_activate.append(j)

        for m in node_list_sorted:  # 删除node_list_sorted中的layers_activate
            for n in layers_activate:
                if m[0] == n:
                    node_list_sorted.remove(m)

    return seed_nodes,node_list_sorted

def _select_others(seed_nodes, other_nodes,k2):     #贪心算法选择剩余k/2个节点
    for m in range(k2):
        all_nodes = list(other_nodes)   #将所有的节点存储在all_nodes列表里
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
        layers_max = layers_activite[lengths.index(max(lengths))]  # 获取被激活节点数最多的列表
        seed_nodes.append(datas[lengths.index(max(lengths))])      # 获取被激活节点最多的子节点
        for i in all_nodes:       #该循环是删除所有节点中seed_nodes节点集
            if i in seed_nodes:
                del all_nodes[all_nodes.index(i)]
        other_nodes=all_nodes
    return seed_nodes,layers_max     #返回值是贪心算法求得的子节点集和该子节点集激活的最大节点集


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
    allnodes=G.nodes()           #获取图中所有的节点
    all_nodes=list(allnodes)
    out_edges_all = G.out_edges() # 获取所有节点的出边
    node_dict={}               #将节点和节点对应的AP值存入字典
    for node in all_nodes:        #遍历所有节点获得每个节点的AP值
        AP=AP_calculate(node)
        node_dict[node]=AP
    node_list_sorted=sorted(node_dict.items(),key=lambda d:d[1],reverse=True)  #对字典按AP值进行由大到小排序
    k=input('Please input inter of k=')
    seed_nodes, node_list_sorted=select_layers(G,node_list_sorted,k/2)
    other_nodes=[]
    '''
    for i in range(len(node_list_sorted)):
        other_nodes.append(node_list_sorted[i][0])
    '''
    for i in seed_nodes:
        if i in all_nodes:
            all_nodes.remove(i)
    other_nodes=all_nodes

    seed_nodes, layers_max=_select_others(seed_nodes,other_nodes,k/2)
    lenth=len(layers_max)
    end = time.clock()
    print(seed_nodes)
    print(layers_max)
    print(lenth)
    print('Running time: %s Seconds'%(end-start))













