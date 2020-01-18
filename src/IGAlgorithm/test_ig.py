'''

@author: Wenquan Li
'''
from main_control import ig_main_control
from networkx.readwrite.gml import read_gml
import os
import networkx

if __name__ == '__main__':
    G = networkx.karate_club_graph()
    print ig_main_control(G)
     
            