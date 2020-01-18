'''

@author: Wenquan Li
'''
from cnmig_main_control import cnmig_main_control
from networkx.readwrite.gml import read_gml
import os
import networkx

if __name__ == '__main__':
    G = networkx.karate_club_graph()
    print cnmig_main_control(G)
     
            