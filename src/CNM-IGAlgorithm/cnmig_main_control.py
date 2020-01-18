# -*- coding: utf-8 -*-
'''
Created on 2018.6.3
@author: Administrator
'''


from init_solution import agglomgreedytk, modularity, local_search
import time
from destruction import destruction
import random
import math

__TIMES = 5
__THRESHOLD = 0.000005
__T_FINAL = 0.000005
K_INLoop = 10
__alpha = 0.9
__Init_CP = 0.01

def cnmig_main_control(G):
    init_solution = agglomgreedytk(G)
    cur_solution = local_search(G, init_solution, weight='weight', resolution=1.,randomize= True)
    cur_mod = modularity(cur_solution, G, weight='weight')
    best_solution = cur_solution.copy()
    best_mod = cur_mod
    
    print 'initial solution completed'
    iterations_count = 0
    acworse_count = 0 
    k_inner = 0
    destroy_rate = 0.40
    __T_INIT = __Init_CP * best_mod
    temp = __T_INIT
    last_bm = best_mod
    t0 = time.time()
    ig_rl = []
    
    while time.time() - t0 < 2400:
            #         扰动
        while k_inner < K_INLoop:
            temp_solution = cur_solution.copy()
            destruction_re =  destruction(temp_solution, G, destroy_rate,weight='weight')
            new_dict = {}
            for k, v in destruction_re[1].items():
                new_dict.setdefault(v, []).append(k)
            forced_cluster = [set(values) for values in new_dict.values()]
            construct_re = agglomgreedytk(G,forced_cluster)
            
            new_solution = local_search(G, construct_re, weight='weight', resolution=1.,randomize= True)
            new_mod = modularity(new_solution,G,weight='weight')
            if new_mod > cur_mod :
                cur_solution = new_solution
                cur_mod = new_mod
                if cur_mod > best_mod:
                    best_solution = cur_solution
                    best_mod = cur_mod
            elif random.uniform(0, 1) < math.exp((new_mod - cur_mod) / temp) and (new_mod - cur_mod != 0) :
                cur_solution = new_solution
                cur_mod = new_mod
                acworse_count = acworse_count + 1
                
            k_inner = k_inner + 1
            iterations_count = iterations_count + 1
            ig_rl.append(cur_mod)
        temp = __alpha * temp
        k_inner = 0
        if iterations_count % 100 == 0 :
            if acworse_count < 3 and (best_mod - last_bm < __THRESHOLD):
                break
            last_bm = best_mod
            acworse_count = 0 
    print 'opitimal solution completed'
    return best_solution