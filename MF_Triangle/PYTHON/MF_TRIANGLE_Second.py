from __future__ import division
from pyomo.environ import *
import argparse
from pyomo.opt import SolverStatus, TerminationCondition
import pandas as pd
import time
import pyutilib.services
import pickle
import random
import sqlite3
import itertools
import copy
import matplotlib.pyplot as plt
import numpy as np
#from samternary.ternary import Ternary
import multiprocessing as mp
#import pathos as pmp
#import dill
#from pathos.multiprocessing import ProcessingPool as Pool

path_output = "./opt_data/"

def regime_rule_SA(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1SA)
    return t2.model1.flow_SA*sum(t2.AREA) - row_sum - t2.model1.SA_p +t2.model1.SA_n ==0
#t2.model1.SA_limit= Constraint(rule=regime_rule_SA)

def regime_rule_INT(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1INT)
    return t2.model1.flow_INT*sum(t2.AREA) - row_sum - t2.model1.INT_p +t2.model1.INT_n ==0
#t2.model1.INT_limit= Constraint(rule=regime_rule_INT)

def regime_rule_EXT(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1EXT)
    return t2.model1.flow_EXT*sum(t2.AREA) - row_sum - t2.model1.EXT_p +t2.model1.EXT_n ==0

def extract_data(t2):
    b1 = t2.all_data.HSI_RL_S1.groupby(["id","branch"]).sum()
    b2 = t2.all_data.HSI_RL_S2.groupby(["id","branch"]).sum()
    b3 = t2.all_data.HSI_RL_S3.groupby(["id","branch"]).sum()
    b4 = t2.all_data.HSI_RL_S4.groupby(["id","branch"]).sum()
    b5 = t2.all_data.HSI_RL_S5.groupby(["id","branch"]).sum()
    b6 = t2.all_data.HSI_RL_S6.groupby(["id","branch"]).sum()
    b7 = t2.all_data.HSI_RL_S7.groupby(["id","branch"]).sum()
    b8 = t2.all_data.HSI_RL_S8.groupby(["id","branch"]).sum()
    b9 = t2.all_data.HSI_RL_S9.groupby(["id","branch"]).sum()
    b10 = t2.all_data.HSI_RL_S10.groupby(["id","branch"]).sum()
    b11 = t2.all_data.HSI_RL_S11.groupby(["id","branch"]).sum()
    b12 = t2.all_data.HSI_RL_S12.groupby(["id","branch"]).sum()
    b13 = t2.all_data.HSI_RL_S13.groupby(["id","branch"]).sum()
    b14 = t2.all_data.HSI_RL_S14.groupby(["id","branch"]).sum()
    b15 = t2.all_data.HSI_RL_S15.groupby(["id","branch"]).sum()
    b16 = t2.all_data.HSI_RL_S16.groupby(["id","branch"]).sum()
    b17 = t2.all_data.HSI_RL_S17.groupby(["id","branch"]).sum()
    b18 = t2.all_data.HSI_RL_S18.groupby(["id","branch"]).sum()
    b19 = t2.all_data.HSI_RL_S19.groupby(["id","branch"]).sum()
    b20 = t2.all_data.HSI_RL_S20.groupby(["id","branch"]).sum()
    b21 = t2.all_data.HSI_RL_S21.groupby(["id","branch"]).sum()
    b22 = t2.all_data.HSI_RL_S22.groupby(["id","branch"]).sum()
    b23 = t2.all_data.HSI_RL_S23.groupby(["id","branch"]).sum()
    b24 = t2.all_data.HSI_RL_S24.groupby(["id","branch"]).sum()
    b25 = t2.all_data.HSI_RL_S25.groupby(["id","branch"]).sum()
    b26 = t2.all_data.HSI_RL_S26.groupby(["id","branch"]).sum()
    b27 = t2.all_data.HSI_RL_S27.groupby(["id","branch"]).sum()
        
    relative_S1 = (sum(b1[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S1) / (t2.max_HSI_RL_S1-t2.min_HSI_RL_S1)
    relative_S2 = (sum(b2[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S2) / (t2.max_HSI_RL_S2-t2.min_HSI_RL_S2)
    relative_S3 = (sum(b3[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S3) / (t2.max_HSI_RL_S3-t2.min_HSI_RL_S3)
    relative_S4 = (sum(b4[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S4) / (t2.max_HSI_RL_S4-t2.min_HSI_RL_S4)
    relative_S5 = (sum(b5[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S5) / (t2.max_HSI_RL_S5-t2.min_HSI_RL_S5)
    relative_S6 = (sum(b6[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S6) / (t2.max_HSI_RL_S6-t2.min_HSI_RL_S6)
    relative_S7 = (sum(b7[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S7) / (t2.max_HSI_RL_S7-t2.min_HSI_RL_S7)
    relative_S8 = (sum(b8[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S8) / (t2.max_HSI_RL_S8-t2.min_HSI_RL_S8)
    relative_S9 = (sum(b9[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S9) / (t2.max_HSI_RL_S9-t2.min_HSI_RL_S9)
    relative_S10 = (sum(b10[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S10) / (t2.max_HSI_RL_S10-t2.min_HSI_RL_S10)
    relative_S11 = (sum(b11[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S11) / (t2.max_HSI_RL_S11-t2.min_HSI_RL_S11)
    relative_S12 = (sum(b12[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S12) / (t2.max_HSI_RL_S12-t2.min_HSI_RL_S12)
    relative_S13 = (sum(b13[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S13) / (t2.max_HSI_RL_S13-t2.min_HSI_RL_S13)
    relative_S14 = (sum(b14[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S14) / (t2.max_HSI_RL_S14-t2.min_HSI_RL_S14)
    relative_S15 = (sum(b15[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S15) / (t2.max_HSI_RL_S15-t2.min_HSI_RL_S15)
    relative_S16 = (sum(b16[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S16) / (t2.max_HSI_RL_S16-t2.min_HSI_RL_S16)
    relative_S17 = (sum(b17[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S17) / (t2.max_HSI_RL_S17-t2.min_HSI_RL_S17)
    relative_S18 = (sum(b18[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S18) / (t2.max_HSI_RL_S18-t2.min_HSI_RL_S18)
    relative_S19 = (sum(b19[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S19) / (t2.max_HSI_RL_S19-t2.min_HSI_RL_S19)
    relative_S20 = (sum(b20[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S20) / (t2.max_HSI_RL_S20-t2.min_HSI_RL_S20)
    relative_S21 = (sum(b21[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S21) / (t2.max_HSI_RL_S21-t2.min_HSI_RL_S21)
    relative_S22 = (sum(b22[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S22) / (t2.max_HSI_RL_S22-t2.min_HSI_RL_S22)
    relative_S23 = (sum(b23[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S23) / (t2.max_HSI_RL_S23-t2.min_HSI_RL_S23)
    relative_S24 = (sum(b24[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S24) / (t2.max_HSI_RL_S24-t2.min_HSI_RL_S24)
    relative_S25 = (sum(b25[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S25) / (t2.max_HSI_RL_S25-t2.min_HSI_RL_S25)
    relative_S26 = (sum(b26[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S26) / (t2.max_HSI_RL_S26-t2.min_HSI_RL_S26)
    relative_S27 = (sum(b27[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S27) / (t2.max_HSI_RL_S27-t2.min_HSI_RL_S27)
    
    a1 = t2.all_data.BILBERRY.groupby(["id","branch"]).sum()
    a2 = t2.all_data.ALL_MARKETED_MUSHROOMS.groupby(["id","branch"]).sum()
    a3 = t2.all_data.scenic.groupby(["id","branch"]).sum()
    relative_1a = (sum(a1[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_BILBERRY) / (t2.max_BILBERRY-t2.min_BILBERRY)
    relative_1b = (sum(a2[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_ALL_MARKETED_MUSHROOMS) / (t2.max_ALL_MARKETED_MUSHROOMS-t2.min_ALL_MARKETED_MUSHROOMS)
    relative_1c = (sum(a3[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_scenic) / (t2.max_scenic-t2.min_scenic)
    
    c1 = t2.all_data.CARBON_SOIL_Update.groupby(["id","branch"]).sum()
    c2 = t2.all_data.BM_total.groupby(["id","branch"]).sum()
    c3 = t2.all_data.DEAD_WOOD_DIVERSITY.groupby(["id","branch"]).sum()
    relative_2a = (sum(c1[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_CARBON_SOIL_Update) / (t2.max_CARBON_SOIL_Update-t2.min_CARBON_SOIL_Update)
    relative_2b = (sum(c2[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_BM_total) / (t2.max_BM_total-t2.min_BM_total)
    relative_2c = (sum(c3[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_DEAD_WOOD_DIVERSITY) / (t2.max_DEAD_WOOD_DIVERSITY-t2.min_DEAD_WOOD_DIVERSITY)
    
    d1 = t2.all_data.LESSER_SPOTTED_WOODPECKER.groupby(["id","branch"]).sum()
    d2 = t2.all_data.THREE_TOED_WOODPECKER.groupby(["id","branch"]).sum()
    d3 = t2.all_data.SIBERIAN_FLYING_SQUIRREL.groupby(["id","branch"]).sum()
    d4 = t2.all_data.LONG_TAILED_TIT.groupby(["id","branch"]).sum()
    d5 = t2.all_data.CAPERCAILLIE.groupby(["id","branch"]).sum()
    d6 = t2.all_data.HAZEL_GROUSE.groupby(["id","branch"]).sum()
    
    relative_3a = (sum(d1[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_LESSER_SPOTTED_WOODPECKER) / (t2.max_LESSER_SPOTTED_WOODPECKER-t2.min_LESSER_SPOTTED_WOODPECKER)
    relative_3b = (sum(d2[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_THREE_TOED_WOODPECKER) / (t2.max_THREE_TOED_WOODPECKER-t2.min_THREE_TOED_WOODPECKER)
    relative_3c = (sum(d3[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_SIBERIAN_FLYING_SQUIRREL) / (t2.max_SIBERIAN_FLYING_SQUIRREL-t2.min_SIBERIAN_FLYING_SQUIRREL)
    relative_3d = (sum(d4[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_LONG_TAILED_TIT) / (t2.max_LONG_TAILED_TIT-t2.min_LONG_TAILED_TIT)
    relative_3e = (sum(d5[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_CAPERCAILLIE) / (t2.max_CAPERCAILLIE-t2.min_CAPERCAILLIE)
    relative_3f = (sum(d6[s,r] * t2.model1.X1[(s,r)].value for (s,r) in t2.model1.index1)-t2.min_HAZEL_GROUSE) / (t2.max_HAZEL_GROUSE-t2.min_HAZEL_GROUSE)
    
    return [relative_1a,relative_1b,relative_1c,relative_2a,relative_2b,relative_2c,relative_3a,relative_3b,relative_3c,relative_3d,relative_3e,relative_3f,relative_S1,relative_S2,relative_S3,relative_S4,relative_S5,relative_S6,relative_S7,relative_S8,relative_S9,relative_S10,relative_S11,relative_S12,relative_S13,relative_S14,relative_S15,relative_S16,relative_S17,relative_S18,relative_S19,relative_S20,relative_S21,relative_S22,relative_S23,relative_S24,relative_S25,relative_S26,relative_S27]


import pandas as pd

payoff = pd.read_csv(path_output+"payoff.csv")
min_max_Da = [min([float(i) for i in list(payoff.iloc[0])]),max([float(i) for i in list(payoff.iloc[0])])]
min_max_Db = [min([float(i) for i in list(payoff.iloc[1])]),max([float(i) for i in list(payoff.iloc[1])])]
min_max_Dc = [min([float(i) for i in list(payoff.iloc[2])]),max([float(i) for i in list(payoff.iloc[2])])]
min_max_Dd = [min([float(i) for i in list(payoff.iloc[3])]),max([float(i) for i in list(payoff.iloc[3])])]


DATA_EXTRACT = []
MF_var = ['BILBERRY','ALL_MARKETED_MUSHROOMS','LESSER_SPOTTED_WOODPECKER','THREE_TOED_WOODPECKER','SIBERIAN_FLYING_SQUIRREL','LONG_TAILED_TIT','CAPERCAILLIE','HAZEL_GROUSE','COWBERRY','CARBON_SOIL_Update','BM_total','DEAD_WOOD_DIVERSITY',"scenic"]
for i in [0,1,12,9,10,11,2,3,4,5,6,7]:
    DATA_EXTRACT = DATA_EXTRACT+[MF_var[i]]
for i in range(1,28):
    DATA_EXTRACT=DATA_EXTRACT+["HSI_RL_S"+str(i)]
DATA_EXTRACT = DATA_EXTRACT + ["NPV","MF","SA_O","INT_O","EXT_O"]


import itertools

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--v',type=float,dest='val',help='MF_value')
    
    args = parser.parse_args()
    val = args.val
    
    import cloudpickle
    #path = "/scratch/project_2000611/KYLE/REMI/"
    with open(path_output+"MODEL_1_MF.pkl",mode = "rb") as file:
        t2 = cloudpickle.load(file)
    
    options = list(set(t2.all_data.loc[(slice(None),slice(None),2016),['branching_group']]['branching_group']))
    DATA_EXTRACT = DATA_EXTRACT + options
    
    def outcome_rule(model1):
        NPV = (t2.model1.NPV-t2.model1.MIN_NPV_v)/(t2.model1.MAX_NPV_v-t2.model1.MIN_NPV_v)
        MF = ((t2.model1.Da-min_max_Da[0])/(min_max_Da[1]-min_max_Da[0])+(t2.model1.Db-min_max_Db[0])/(min_max_Db[1]-min_max_Db[0])+(t2.model1.Dc-min_max_Dc[0])/(min_max_Dc[1]-min_max_Dc[0])+(t2.model1.Dd-min_max_Dd[0])/(min_max_Dd[1]-min_max_Dd[0])-10* (t2.model1.SA_p +t2.model1.SA_n+ t2.model1.EXT_p +t2.model1.EXT_n +t2.model1.INT_p +t2.model1.INT_n))
        return NPV*t2.model1.MF_NPV_flow + (1-t2.model1.MF_NPV_flow)*MF-(t2.model1.SA_p +t2.model1.SA_n+t2.model1.EXT_p +t2.model1.EXT_n+t2.model1.INT_p +t2.model1.INT_n)*1000+(MF+NPV)/100
    t2.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
    
    #for val in [0, .10, .20, .30, .40, .50, .60, .70, .80, .90, 1.00]:
    #curr_arr = [0, .10, .20, .80, .90, 1.00]
    curr_arr = [0, .10, .20, .30, .40, .50, .60, .70, .80, .90, 1.00]
    t2.model1.MF_NPV_flow = val
    comb_input = [a for a in itertools.combinations_with_replacement(curr_arr, 3) if sum(a) == 1]
    comb_input = [set(itertools.permutations(a)) for a in comb_input]
    
    finish = []
    for a in comb_input:
        finish += list(a)
    t1aa = []
    t1bb = []
    t1cc= []
    t1dd= []
    t1ee = []
    t1_alla = {}
    
    for (a,b,c) in finish:
        t2.model1.flow_SA = a
        t2.model1.flow_INT = b
        t2.model1.flow_EXT = c
        try:
            t2.model1.del_component(t2.model1.EXT_limit)
            t2.model1.del_component(t2.model1.INT_limit)
            t2.model1.del_component(t2.model1.SA_limit)
        except:
            print("first")
        t2.model1.EXT_limit= Constraint(rule=regime_rule_EXT)
        t2.model1.SA_limit= Constraint(rule=regime_rule_SA)
        t2.model1.INT_limit= Constraint(rule=regime_rule_INT)
        t2.solve()
        t1aa= t1aa+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1SA)/sum(t2.AREA)]
        t1bb= t1bb+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1INT)/sum(t2.AREA)]
        t1cc= t1cc+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1EXT)/sum(t2.AREA)]
        t1dd= t1dd+[t2.model1.MF.value]
        t1ee = t1ee+[t2.model1.NPV.value]
        temp_data = extract_data(t2)
        
        for kk in range(0,len(temp_data)):
            if DATA_EXTRACT[kk] in t1_alla.keys():
                t1_alla[DATA_EXTRACT[kk]] = t1_alla[DATA_EXTRACT[kk]] +[temp_data[kk]]
            else:
                t1_alla[DATA_EXTRACT[kk]] = [temp_data[kk]]
        XX = [t2.model1.NPV.value,t2.model1.MF.value,sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1SA)/sum(t2.AREA),sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1INT)/sum(t2.AREA),sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1EXT)/sum(t2.AREA)]
        print(XX)
        
        options = list(set(t2.all_data.loc[(slice(None),slice(None),2016),['branching_group']]['branching_group']))
        
        kkk=0
        for kk in range(len(temp_data),len(DATA_EXTRACT)-len(options)):
            if DATA_EXTRACT[kk] in t1_alla.keys():
                t1_alla[DATA_EXTRACT[kk]] = t1_alla[DATA_EXTRACT[kk]] + [XX[kkk]]
            else:
                t1_alla[DATA_EXTRACT[kk]] = [XX[kkk]]
            kkk=kkk+1
        
        options = list(set(t2.all_data.loc[(slice(None),slice(None),2016),['branching_group']]['branching_group']))
        opt_dict = {options[0]:0}
        for k in range(1,len(options)):
            opt_dict[options[k]] = 0
        
        for (t,p) in t2.model1.index1:
            if t2.model1.X1[(t,p)].value > 0:
                opt_dict[t2.all_data.loc[(t,p,2016),['branching_group']]['branching_group']] = opt_dict[t2.all_data.loc[(t,p,2016),['branching_group']]['branching_group']]+t2.model1.X1[(t,p)].value*t2.AREA[t]
        
        for kk in range(len(DATA_EXTRACT)-len(options),len(DATA_EXTRACT)):
            if DATA_EXTRACT[kk] in t1_alla.keys():
                t1_alla[DATA_EXTRACT[kk]] = t1_alla[DATA_EXTRACT[kk]] + [opt_dict[DATA_EXTRACT[kk]]]
            else:
                t1_alla[DATA_EXTRACT[kk]] = [opt_dict[DATA_EXTRACT[kk]]]
        
        pd.DataFrame.from_dict(t1_alla).to_csv(path_output+"MAX_NPV_"+str(val)+".csv")
