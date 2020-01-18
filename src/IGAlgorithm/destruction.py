# -*- coding: utf-8 -*-
'''

@author: Wenquan Li
'''
from __future__ import division
import operator
from random import choice
from community_status import Status


def node_contribution(partition, graph, weight='weight'):
    indegree = dict([])
    contribution = dict([])
    links = graph.size(weight=weight)
    newstatus = Status()
    newstatus.init(graph, weight, partition)
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")
        
    for node in graph:
        com = partition[node]
       
        for neighbor, datas in graph[node].items():
            edge_weight = datas.get(weight, 1)
            if partition[neighbor] == com:
                if neighbor != node:
                    indegree[node] = indegree.get(node, 0.) + float(edge_weight)
        contribution[node] = round(indegree[node] - (0.5*newstatus.gdegrees[node] * newstatus.degrees[com])/links,4)
    
    return contribution
def __neighcom(node, graph, status, weight_key):
    """
    Compute the communities in the neighborhood of node in the graph given
    with the decomposition node2com
    """
    weights = {}
    for neighbor, datas in graph[node].items():
        if neighbor != node:
            edge_weight = datas.get(weight_key, 1)
            neighborcom = status.node2com[neighbor]
            weights[neighborcom] = weights.get(neighborcom, 0) + edge_weight

    return weights
def contribution_nodeneighbor(partition, graph, weight='weight'):
  
    contribution = dict([])
    participation = dict([])
    node_neighbor = dict([])
    newstatus = Status()
    newstatus.init(graph, weight, partition)
    links = newstatus.total_weight
    if links == 0:
        raise ValueError("A graph without link has an undefined modularity")
        
    for node in graph:
        com_node = newstatus.node2com[node]
        deg_node = newstatus.gdegrees.get(node,0.)
        deg_com = newstatus.degrees.get(com_node,0.)
        
        neigh_communities = __neighcom(node, graph, newstatus, weight_key=weight)
        if neigh_communities:
            contribution[node] = round(neigh_communities.get(com_node,0) - (0.5*deg_node * deg_com)/links,4)
            for com, dnc in neigh_communities.items():
                participation[node] = participation.get(node,1) - (dnc / deg_node) ** 2
                if com != com_node:
                    if node_neighbor.has_key(node):
                        node_neighbor[node].append(com)
                    else:
                        node_neighbor[node] = [com]
            if node_neighbor.has_key(node):
                pass
            else:
                node_neighbor[node] = [com_node]
    return contribution,participation,node_neighbor

def destruction(partition, graph,rate,weight='weight'):
   
    contribution,participation,node_nrighbor = contribution_nodeneighbor(partition, graph, weight)
    count = max(partition.values())    
    sorted_nc = sorted(contribution.items(),key=operator.itemgetter(1),reverse=False)
#     print sorted_nc
    order_sequence = []
    for index in range(0,sorted_nc.__len__()):
#            
        order_sequence.append(sorted_nc[index][0])
       
    for index in range(0,int(rate *order_sequence.__len__())):
#         partition[sorted_nc[index][0]] = choice(node_nrighbor[order_sequence[index]])
        if participation[order_sequence[index]] > 0.05:
            partition[sorted_nc[index][0]] = choice(node_nrighbor[order_sequence[index]])
        else:
            partition[sorted_nc[index][0]] = ++count
            count = count + 1
    return order_sequence,partition