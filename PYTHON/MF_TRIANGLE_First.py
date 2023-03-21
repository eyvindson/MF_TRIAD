#DATA IMPORTATION -- and general model formulation
from __future__ import division
from pyomo.environ import *

from pyomo.opt import SolverStatus, TerminationCondition
import pandas
import pandas as pd
import time
import numpy
import pyutilib.services
import pickle
import random
import sqlite3
import numpy as np

#REQUIRES CBC TO BE INSTALLED ON THE MACHINE USED!!!  See https://github.com/coin-or/Cbc -- OTHER SOLVERS CAN BE USED -- 
#THEN CHANGE this line: "opt = SolverFactory('cbc') #Here we use the cbc solver -- open source software"

path = "/scratch/project_2000611/KYLE/REMI/"#ADJUST TO OWN PATH #"c:/mytemp/avohakkutpois/Files_for_optimization/temp/"
database_ROT = "simulated_RCP45_NEW_ROT.db" # SIMO DATABASE -- or whatever forest simulator used
database_CCF = "simulated_RCP45_NEW_CCF.db"
database_SA = "simulated_RCP45_NEW_SA.db"

#LOCATION OF DATABASE -- TOO LARGE FOR GIT
#url = 'https://a3s.fi/swift/v1/AUTH_d065f3b1e6d947c9bf986dce54e3d0ec/SIMULATED_DATA_ROOTROT/simulated_BAU_TEST.db'
#urllib.request.urlretrieve(url, path + database)

path2 = "/scratch/project_2000611/KYLE/AVO2/Files_for_optimization/"
pyutilib.services.TempfileManager.tempdir = path2

class optimization:
    def __init__(self):
        c = 0
        for datab in ["simulated_RCP45_NEW_CCF_4.db","simulated_RCP45_NEW_ROT.db","simulated_RCP45_NEW_SA.db"]:
            con = sqlite3.connect(path+datab)
            create_table_max_v = 'CREATE TABLE max_v AS    SELECT comp_unit.id AS id,   MAX(comp_unit.V) AS max_v    FROM comp_unit    GROUP BY comp_unit.id'
            create_table_OPERS2 ='CREATE TABLE OPERS2 AS SELECT t.id,t.branch,t.iteration, t.op_date, br.branching_group, case when t.op_name = "clearcut" OR t.op_name = "clearcut_nature_scene" then 1 else 0 end as bool,t.op_name,  (SELECT sum(op_res.income) FROM op_res WHERE t.op_id = op_res.op_id )/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS income,   (SELECT sum(op_res.cash_flow) FROM op_res WHERE t.op_id = op_res.op_id )/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS cash_flow,  (SELECT sum(op_res.income) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =1 )/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS income_log,  (SELECT sum(op_res.income) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =2 )/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS income_pulp,  (SELECT sum(op_res.income_biomass) FROM op_res WHERE t.op_id = op_res.op_id )/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS income_biomass,  (SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =1)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_log,(SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =2)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_pulp,(SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V,  (SELECT sum(op_res.Biomass) FROM op_res WHERE t.op_id = op_res.op_id)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Biomass,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =1 and op_res.sp = 1),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_log_pine,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =2 and op_res.sp = 1),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_pulp_pine,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =1 and op_res.sp = 2),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_log_spruce,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =2 and op_res.sp = 2),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_pulp_spruce,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =1 and (op_res.sp = 3 or op_res.sp = 4)),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_log_birch,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =2 and (op_res.sp = 3 or op_res.sp = 4)),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_pulp_birch,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and (op_res.assortment =2 or op_res.assortment =1) and op_res.sp > 4),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_others,   case when t.op_name = "thinning" OR t.op_name = "first_thinning" then t.op_date else 0 end as THIN,  ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =1 and op_res.sp > 4),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_log_others,    ifnull((SELECT sum(op_res.Volume) FROM op_res WHERE t.op_id = op_res.op_id and op_res.assortment =2 and op_res.sp > 4),0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Harvested_V_pulp_others,    ifnull((SELECT sum(op_res.Biomass) FROM op_res WHERE t.op_id = op_res.op_id and op_res.sp = 1)*0.420,0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Biomass_Ton_pine,  ifnull((SELECT sum(op_res.Biomass) FROM op_res WHERE t.op_id = op_res.op_id and op_res.sp = 2)*0.380,0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Biomass_Ton_spruce,  ifnull((SELECT sum(op_res.Biomass) FROM op_res WHERE t.op_id = op_res.op_id and op_res.sp = 3)*0.510,0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Biomass_Ton_birch_pub,  ifnull((SELECT sum(op_res.Biomass) FROM op_res WHERE t.op_id = op_res.op_id and op_res.sp = 4)*0.485,0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Biomass_Ton_birch_pen,  ifnull((SELECT sum(op_res.Biomass) FROM op_res WHERE t.op_id = op_res.op_id and op_res.sp > 4)*0.420,0)/((select count(*) from (select  * from op_res where t.op_id = op_res.op_id) x)/(select count(*) from (select distinct * from op_res where t.op_id = op_res.op_id ) x)  ) AS Biomass_Ton_others,  (CASE WHEN t.op_name is "clearcut" THEN 55 WHEN t.op_name is "clearcut_nature_scene" THEN 55 WHEN t.op_name is "first_thinning" THEN 40 WHEN t.op_name is "thinning" THEN 50 WHEN t.op_name is "selection_cut" THEN 50 WHEN t.op_name is "selection_cut_with_little_open_areas" THEN 50 WHEN t.op_name is "remove_seedtrees" THEN 55 WHEN t.op_name is "seedtree_position" THEN 55 WHEN t.op_name is "seedtree_position_nature_scene" THEN 55 ELSE 9999 END) as P_PINE_LOG,  (CASE WHEN t.op_name is "clearcut" THEN 17 WHEN t.op_name is "clearcut_nature_scene" THEN 17 WHEN t.op_name is "first_thinning" THEN 11 WHEN t.op_name is "thinning" THEN 13 WHEN t.op_name is "selection_cut" THEN 13 WHEN t.op_name is "selection_cut_with_little_open_areas" THEN 13 WHEN t.op_name is "remove_seedtrees" THEN 17 WHEN t.op_name is "seedtree_position" THEN 17 WHEN t.op_name is "seedtree_position_nature_scene" THEN 17 ELSE 9999 END) as P_PINE_PULP,  (CASE WHEN t.op_name is "clearcut" THEN 55 WHEN t.op_name is "clearcut_nature_scene" THEN 55 WHEN t.op_name is "first_thinning" THEN 42 WHEN t.op_name is "thinning" THEN 50 WHEN t.op_name is "selection_cut" THEN 50 WHEN t.op_name is "selection_cut_with_little_open_areas" THEN 50 WHEN t.op_name is "remove_seedtrees" THEN 55 WHEN t.op_name is "seedtree_position" THEN 55 WHEN t.op_name is "seedtree_position_nature_scene" THEN 55 ELSE 9999 END) as P_SPRUCE_LOG,  (CASE WHEN t.op_name is "clearcut" THEN 25 WHEN t.op_name is "clearcut_nature_scene" THEN 25 WHEN t.op_name is "first_thinning" THEN 19 WHEN t.op_name is "thinning" THEN 21 WHEN t.op_name is "selection_cut" THEN 21 WHEN t.op_name is "selection_cut_with_little_open_areas" THEN 21 WHEN t.op_name is "remove_seedtrees" THEN 25 WHEN t.op_name is "seedtree_position" THEN 25 WHEN t.op_name is "seedtree_position_nature_scene" THEN 25 ELSE 9999 END) as P_SPRUCE_PULP,  (CASE WHEN t.op_name is "clearcut" THEN 43 WHEN t.op_name is "clearcut_nature_scene" THEN 43 WHEN t.op_name is "first_thinning" THEN 35 WHEN t.op_name is "thinning" THEN 38 WHEN t.op_name is "selection_cut" THEN 38 WHEN t.op_name is "selection_cut_with_little_open_areas" THEN 38 WHEN t.op_name is "remove_seedtrees" THEN 43 WHEN t.op_name is "seedtree_position" THEN 43 WHEN t.op_name is "seedtree_position_nature_scene" THEN 43 ELSE 9999 END) as P_BIRCH_LOG,  (CASE WHEN t.op_name is "clearcut" THEN 15 WHEN t.op_name is "clearcut_nature_scene" THEN 15 WHEN t.op_name is "first_thinning" THEN 10 WHEN t.op_name is "thinning" THEN 11 WHEN t.op_name is "selection_cut" THEN 11 WHEN t.op_name is "selection_cut_with_little_open_areas" THEN 11 WHEN t.op_name is "remove_seedtrees" THEN 15 WHEN t.op_name is "seedtree_position" THEN 15 WHEN t.op_name is "seedtree_position_nature_scene" THEN 15 ELSE 9999 END) as P_BIRCH_PULP,  (CASE WHEN t.op_name is "clearcut" THEN 10 WHEN t.op_name is "clearcut_nature_scene" THEN 10 WHEN t.op_name is "first_thinning" THEN 7 WHEN t.op_name is "thinning" THEN 8 WHEN t.op_name is "selection_cut" THEN 8 WHEN t.op_name is "selection_cut_with_little_open_areas" THEN 8 WHEN t.op_name is "remove_seedtrees" THEN 10 WHEN t.op_name is "seedtree_position" THEN 10 WHEN t.op_name is "seedtree_position_nature_scene" THEN 10 ELSE 9999 END) as P_OTHER,  (CASE WHEN t.op_group is "soil_preparation" THEN 1 WHEN t.op_group is "harrowing" THEN 1 WHEN t.op_group is "mounding" THEN 1 ELSE 0 END) as SCAR,  (CASE WHEN t.op_name is "planting" THEN 1 ELSE 0 END) as PLANTING,  (CASE WHEN t.op_name is "seedtree_position" THEN 1 WHEN t.op_group is "seedtree_position_nature_scene" THEN 1 WHEN t.op_group is "natural_regeneration" THEN 1 ELSE 0 END) as SEEDING   FROM op_link t  LEFT OUTER JOIN branch_desc br ON br.branch = t.branch AND t.id = br.id  and t.iteration = br.iteration WHERE cash_flow is not null' 
            create_table_OPERS3 ='CREATE TABLE OPERS3 AS SELECT distinct id, branch,iteration, op_date, branching_group, sum(income) as income,  sum(Harvested_V_pulp) as Harvested_V_pulp,sum(Harvested_V_log) as Harvested_V_log,sum(Harvested_V) as Harvested_V, case when sum(bool) > 0 then 1 else 0 end as clearcut,  sum(income_log) as income_log, sum(income_pulp) as income_pulp,  sum(income_biomass) as income_biomass, sum(Biomass) as Biomass,  sum(Harvested_V_log_pine* P_PINE_LOG + Harvested_V_log_spruce* P_SPRUCE_LOG+ Harvested_V_log_birch* P_BIRCH_LOG) as income_log_change,  sum(Harvested_V_pulp_pine* P_PINE_PULP+ Harvested_V_pulp_spruce* P_SPRUCE_PULP+ Harvested_V_pulp_birch* P_BIRCH_PULP+ Harvested_v_others* P_OTHER)as income_pulp_change,  sum(cash_flow) as cash_flow, thin,  SCAR, PLANTING,SEEDING,  sum(Harvested_V_log_pine*0.88 +Harvested_V_log_spruce*0.898 +Harvested_V_log_birch*0.885+Harvested_V_log_others*0.874) as Harvested_V_log_under_bark,  sum(Harvested_V_pulp_pine*0.863 +Harvested_V_pulp_spruce*0.864 +Harvested_V_pulp_birch*0.862+Harvested_V_pulp_others*0.862) as Harvested_V_pulp_under_bark,  sum(Biomass_Ton_pine +Biomass_Ton_spruce+ Biomass_Ton_birch_pub+ Biomass_Ton_birch_pen+Biomass_Ton_others) as Harvested_biomass_Ton  FROM OPERS2  group by id, branch, op_date, iteration'
            create_table_UNIT ='Create Table UNIT AS SELECT u.*,(1-u.PEAT)*u.Carbon_soil+sum(ifnull( u.CARBON_STORAGE_Ojanen,0)) OVER (PARTITION BY u.id, b.branching_group ORDER BY u.year)+u.PEAT*300000 as CARBON_SOIL_Update,(4.471+0.0645*COALESCE((select max(stratum.D_gm) From stratum where stratum.data_id = u.data_id),0)-0.0001745*u.N + (select case when  COALESCE((select max(stratum.H_dom) From stratum where stratum.data_id = u.data_id),0) >= 10 THEN 1 else 0 end as dummy_h_dom from comp_unit u)*0.006439 + 0.005733*(u.V_penbirch+u.V_pubbirch)*(select case when COALESCE((select max(stratum.H_dom) From stratum where stratum.data_id = u.data_id),0) >= 10 THEN 1 else 0 end as dummy_h_dom from comp_unit u)) as scenic,(select max(stratum.H_dom) From stratum where stratum.data_id = u.data_id) as H_dom,   (select max(stratum.D_gm) From stratum where stratum.data_id = u.data_id) as D_gm,   (select sum(stratum.N) From stratum where stratum.data_id = u.data_id and D_gm >40) as N_where_D_gt_40,  (select sum(stratum.N) From stratum where stratum.data_id = u.data_id and D_gm <=40 and D_gm > 35) as N_where_D_gt_35_lt_40,  (select sum(stratum.N) From stratum where stratum.data_id = u.data_id and D_gm <=35 and D_gm > 30) as N_where_D_gt_30_lt_35,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and D_gm >40) as V_where_D_gt_40,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and D_gm <=40 and D_gm > 35) as V_where_D_gt_35_lt_40,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and D_gm <=35 and D_gm > 30) as V_where_D_gt_30_lt_35,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 5) as V_populus,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 6) as V_Alnus_incana,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 7) as V_Alnus_glutinosa,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 8) as V_o_coniferous,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 9) as V_o_decidious,    l.data_date,l.iteration, l.branch, b.branch_desc, b.branching_group, o.income/u.AREA as income, o.cash_flow/u.AREA as cash_flow,  o.clearcut, o.Harvested_V_log/u.AREA as Harvested_V_log,   o.Harvested_V_pulp/u.AREA as Harvested_V_pulp,  o.Harvested_V/u.AREA as Harvested_V,m.max_v, o.income_log/u.AREA as income_log, o.income_pulp/u.AREA as income_pulp,  o.income_log_change/u.AREA as income_log_change,o.income_pulp_change/u.AREA as income_pulp_change, o.income_biomass, o.Biomass/u.AREA as Biomass, o.thin,  (case when o.cash_flow > 0 then 0 else o.cash_flow end) as costs,  o.Harvested_biomass_Ton/u.AREA as Biomass_ton,  o.Harvested_V_pulp_under_bark/u.AREA as Harvested_V_pulp_under_bark,  o.Harvested_V_log_under_bark/u.AREA as Harvested_V_log_under_bark,  ((o.income_log_change/u.AREA + o.income_pulp_change/u.AREA - (case when o.cash_flow > 0 then 0 else o.cash_flow/u.AREA end))) as NPV_period_1,  ((o.income_log_change/u.AREA + o.income_pulp_change/u.AREA - (case when o.cash_flow > 0 then 0 else o.cash_flow/u.AREA end))) as NPV_period_2,  ((o.income_log_change/u.AREA + o.income_pulp_change/u.AREA - (case when o.cash_flow > 0 then 0 else o.cash_flow/u.AREA end))) as NPV_period_3,  ((o.income_log_change/u.AREA + o.income_pulp_change/u.AREA - (case when o.cash_flow > 0 then 0 else o.cash_flow/u.AREA end))) as NPV_period_4,  (CASE WHEN u.age >= 100 THEN 1 ELSE 0 END) as OLD_FOREST,  (CASE WHEN u.age <= 40 THEN 1 ELSE 0 END) as YOUNG_FOREST,  (CASE WHEN u.Main_sp is 1 THEN 1 ELSE 0 END) as SP_DOM,  (CASE WHEN u.Main_sp is 2 THEN 1 ELSE 0 END) as Ns_DOM,  (CASE WHEN u.Main_sp is 3 THEN 1 ELSE 0 END) as Bpend_DOM,  (CASE WHEN u.Main_sp is 4 THEN 1 ELSE 0 END) as Bpub_DOM,  (CASE WHEN u.Main_sp is 6 THEN 1 ELSE 0 END) as Alnus_DOM,  o.SCAR,o.PLANTING,o.SEEDING,  u.BM_total*0.5 + u.Carbon_soil+ifnull(u.CARBON_STORAGE_Ojanen,0)+u.PEAT*300000 as CARBON_STORAGE_Update    FROM comp_unit u, data_link l  left outer join branch_desc b on l.branch = b.branch and l.id = b.id and l.iteration = b.iteration cross join max_v m on l.id = m.id  left outer join OPERS3 o on o.branch = b.branch and o.id = b.id and o.iteration =b.iteration and o.op_date= l.data_date  WHERE u.data_id=l.data_id  ORDER BY u.id,  l.branch,l.iteration, l.data_date'
            create_table_UNIT_SA ='Create Table UNIT AS SELECT u.*,(1-u.PEAT)*u.Carbon_soil+sum(ifnull( u.CARBON_STORAGE_Ojanen,0)) OVER (PARTITION BY u.id, b.branching_group ORDER BY u.year)+u.PEAT*300000 as CARBON_SOIL_Update,(4.471+0.0645*COALESCE((select max(stratum.D_gm) From stratum where stratum.data_id = u.data_id),0)-0.0001745*u.N + (select case when  COALESCE((select max(stratum.H_dom) From stratum where stratum.data_id = u.data_id),0) >= 10 THEN 1 else 0 end as dummy_h_dom from comp_unit u)*0.006439 + 0.005733*(u.V_penbirch+u.V_pubbirch)*(select case when COALESCE((select max(stratum.H_dom) From stratum where stratum.data_id = u.data_id),0) >= 10 THEN 1 else 0 end as dummy_h_dom from comp_unit u)) as scenic, (select max(stratum.H_dom) From stratum where stratum.data_id = u.data_id) as H_dom,   (select max(stratum.D_gm) From stratum where stratum.data_id = u.data_id) as D_gm,   (select sum(stratum.N) From stratum where stratum.data_id = u.data_id and D_gm >40) as N_where_D_gt_40,  (select sum(stratum.N) From stratum where stratum.data_id = u.data_id and D_gm <=40 and D_gm > 35) as N_where_D_gt_35_lt_40,  (select sum(stratum.N) From stratum where stratum.data_id = u.data_id and D_gm <=35 and D_gm > 30) as N_where_D_gt_30_lt_35,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and D_gm >40) as V_where_D_gt_40,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and D_gm <=40 and D_gm > 35) as V_where_D_gt_35_lt_40,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and D_gm <=35 and D_gm > 30) as V_where_D_gt_30_lt_35,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 5) as V_populus,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 6) as V_Alnus_incana,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 7) as V_Alnus_glutinosa,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 8) as V_o_coniferous,  (select sum(stratum.V) From stratum where stratum.data_id = u.data_id and SP = 9) as V_o_decidious,    l.data_date,l.iteration, l.branch, b.branch_desc, b.branching_group, 0 as income, 0 as cash_flow,  0 as clearcut, 0 as Harvested_V_log,  0 as Harvested_V_pulp,  0 as Harvested_V,m.max_v, 0 as income_log, 0 as income_pulp, 0 as income_log_change,0 as income_pulp_change, 0 as income_biomass, 0 as Biomass, 0 as thin,  0 as costs,  0 as Biomass_ton,  0 as Harvested_V_pulp_under_bark,  0 as Harvested_V_log_under_bark,  0 NPV_period_1,  0 as NPV_period_2, 0 as NPV_period_3,  0 as NPV_period_4,  (CASE WHEN u.age >= 100 THEN 1 ELSE 0 END) as OLD_FOREST,  (CASE WHEN u.age <= 40 THEN 1 ELSE 0 END) as YOUNG_FOREST,  (CASE WHEN u.Main_sp is 1 THEN 1 ELSE 0 END) as SP_DOM,  (CASE WHEN u.Main_sp is 2 THEN 1 ELSE 0 END) as Ns_DOM,  (CASE WHEN u.Main_sp is 3 THEN 1 ELSE 0 END) as Bpend_DOM,  (CASE WHEN u.Main_sp is 4 THEN 1 ELSE 0 END) as Bpub_DOM,  (CASE WHEN u.Main_sp is 6 THEN 1 ELSE 0 END) as Alnus_DOM,  0 as Scar,0 as PLANTING,0 as SEEDING,  u.BM_total*0.5 + u.Carbon_soil+ifnull(u.CARBON_STORAGE_Ojanen,0)+u.PEAT*300000 as CARBON_STORAGE_Update    FROM comp_unit u, data_link l  left outer join branch_desc b on l.branch = b.branch and l.id = b.id and l.iteration = b.iteration cross join max_v m on l.id = m.id   WHERE u.data_id=l.data_id  ORDER BY u.id,  l.iteration, l.data_date'
            #IF TABLES EXIST IN DB, DROP AND TRY AGAIN
            #try:
            #    con.execute("drop table max_v")
            #    con.execute("drop table UNIT")
            #    con.execute("drop table OPERS2")
            #    con.execute("drop table OPERS3")               
            #except:
            #    print("NO need to drop tables")
            #con.execute(create_table_max_v)
            #try:
            #    con.execute("drop table UNIT")
            #except:
            #    print("NO need to drop tables")
            #    
            #if c != 2:
            #    con.execute(create_table_OPERS2)
            #    con.execute(create_table_OPERS3)
            #    con.execute(create_table_UNIT)
            #else:
            #    con.execute(create_table_UNIT_SA)
            
            if c == 1:
                self.data_rot = pd.read_sql_query("SELECT * from UNIT",con)
                self.data_rot = self.data_rot[self.data_rot['branch'] != 0]
                c = 2
            elif c== 0:
                self.data_ccf = pd.read_sql_query("SELECT * from UNIT",con)
                self.data_ccf = self.data_ccf[self.data_ccf['branch'] != 0]
                self.data_ccf['branch'] = self.data_ccf['branch'] +40
                c = 1
            elif c == 2:
                self.data_sa = pd.read_sql_query("SELECT * from UNIT",con)  
        
        self.data = pd.concat([self.data_sa,self.data_ccf,self.data_rot])
        self.data['branching_group'] = self.data['branching_group']+self.data["branch_desc"]
        self.data['branching_group'] = self.data['branching_group'].str.replace("+","")
        self.data['branching_group'] = self.data['branching_group'].str.replace("-","m")
        self.data['branching_group'] = self.data['branching_group'].str.replace(" ","")
        self.data['branching_group'] = self.data['branching_group'].str.replace("_","")
        self.data['branching_group'] = self.data['branching_group'].str.replace("_","")
        self.data['branching_group'] = self.data['branching_group'].str.replace("|","")
        self.data['branching_group'].replace({"00": "SA"}, inplace=True)
        self.data['branching_group'] = self.data['branching_group'].fillna("SA")
        
        #n = int(len(set(self.data["id"].values))/10)
        #stand_sample = np.random.choice(list(set(self.data["id"].values)),n,replace=False)
        #  self.origData = self.data
        
        #self.data = self.data[self.data["id"].isin(stand_sample)]
        
        self.data_opt = self.data[['id',"iteration",'branch',"year","V","income_log_change","income_pulp_change","Harvested_V",'Harvested_V_log','Harvested_V_pulp',"AREA",'branching_group',"PV",'HSI_RL_S1','HSI_RL_S2','HSI_RL_S3','HSI_RL_S4','HSI_RL_S5','HSI_RL_S6','HSI_RL_S7','HSI_RL_S8','HSI_RL_S9','HSI_RL_S10','HSI_RL_S11','HSI_RL_S12','HSI_RL_S13','HSI_RL_S14','HSI_RL_S15','HSI_RL_S16','HSI_RL_S17','HSI_RL_S18','HSI_RL_S19','HSI_RL_S20','HSI_RL_S21','HSI_RL_S22','HSI_RL_S23','HSI_RL_S24','HSI_RL_S25','HSI_RL_S26','HSI_RL_S27','BILBERRY','ALL_MARKETED_MUSHROOMS','LESSER_SPOTTED_WOODPECKER','THREE_TOED_WOODPECKER','SIBERIAN_FLYING_SQUIRREL','LONG_TAILED_TIT','CAPERCAILLIE','HAZEL_GROUSE','COWBERRY','CARBON_SOIL_Update','BM_total','DEAD_WOOD_DIVERSITY',"scenic"]]
        self.data_opt['income'] = self.data_opt['income_pulp_change']+self.data_opt['income_log_change']
        self.combinations = 1
        
        #CREATE replicates with varying iterations
        
        #ONE WAY
        #self.df4=pd.DataFrame(columns=self.data_opt.keys())
        #self.dat_id = self.data['id'].drop_duplicates()#[['id','iteration','branch']]
        #self.df5=pd.DataFrame(columns=self.data_opt.keys())
        #for k in range(0,self.combinations):
        #    self.df4=pd.DataFrame(columns=self.data_opt.keys())
        #    self.ran_id = [[self.dat_id.iloc[i],random.randrange(10)] for i in range(0,len(self.dat_id))]
        #    for i, it in enumerate(self.ran_id): 
        #        #_id = it[0]
        #        #rint(it)
        #        self.df2 = self.data_opt[self.data_opt["id"]==it[0]]
        #        self.df3 = self.df2[self.df2["iteration"]==it[1]]
        #        self.df4 = pd.concat([self.df4, self.df3],ignore_index=True)
        #    self.df4['iteration']=k
        #    self.df5 = pd.concat([self.df5,self.df4])        
        self.all_data = self.data_opt#df5
        
        INT = ["Selectioncut2Selectioncut", "Selectioncut1Selectioncut", "TapiothinningThinningTapio",  "Longrotationharvest5Longrotationclearcut", "TapioharvestnaturesceneTapioclearcutwithnaturescene", "TapioharvestTapioclearcut", "Shortrotationthinning5Thinninglongrotation", "Shortrotationharvest5shortrotationclearcut"]
        EXT = ["Selectioncut4Selectioncut", "Selectioncut3Selectioncut", "Longrotationharvest15Longrotationclearcut", "Longrotationharvest10Longrotationclearcut", "Tapioharvestwithoutthinningsm20Tapioclearcut", "TapioharvestwithoutthinningsTapioclearcut", "Tapioharvestwithoutthinnings10Tapioclearcut", "Longrotationthinning30Thinninglongrotation", "Longrotationharvest30Longrotationclearcut", "Longrotationthinning15Thinninglongrotation", "Longrotationthinning10Thinninglongrotation", "TapiothinningnatureThinningTapio", "Longrotationthinning5Thinninglongrotation"]
        
        
        SA = ["SA"]
        
        self.Index_values = self.all_data.set_index(['id','branch']).index.unique()
        self.all_data = self.all_data.set_index(['id','branch','year'])
        
        
        self.INTENSE = self.all_data.loc[(slice(None),slice(None),slice(None)),['branching_group']]
        self.INTENSE = self.INTENSE[self.INTENSE['branching_group'].isin(INT)]
        self.INTENSE = self.INTENSE.reset_index()
        self.INTENSE = self.INTENSE.drop(["year"],axis = 1)
        self.INTENSE = self.INTENSE.drop_duplicates()
        self.INTENSE.set_index(["id","branch"],inplace=True)
        self.INTENSE = self.INTENSE.index.unique()
        
        self.EXTENSE = self.all_data.loc[(slice(None),slice(None),slice(None)),['branching_group']]
        self.EXTENSE = self.EXTENSE[self.EXTENSE['branching_group'].isin(EXT)]
        self.EXTENSE = self.EXTENSE.reset_index()
        self.EXTENSE = self.EXTENSE.drop(["year"],axis = 1)
        self.EXTENSE = self.EXTENSE.drop_duplicates()
        self.EXTENSE.set_index(["id","branch"],inplace=True)
        self.EXTENSE = self.EXTENSE.index.unique()
        
        self.SA = self.all_data.loc[(slice(None),slice(None),slice(None)),['branching_group']]
        self.SA = self.SA[self.SA['branching_group'].isin(SA)]
        self.SA = self.SA.reset_index()
        self.SA = self.SA.drop(["year"],axis = 1)
        self.SA = self.SA.drop_duplicates()
        self.SA.set_index(["id","branch"],inplace=True)
        self.SA = self.SA.index.unique()
        
        self.AREA = self.all_data.loc[slice(None),0,2016]['AREA']
        self.all_data = self.all_data.fillna(0)
        
        #INDEX = t1.all_data.set_index(["id","branch"]).index.unique()
        self.createModel()
        
    def createModel(self):
        # Declare sets - These used to recongnize the number of stands, regimes and number of periods in the analysis.
        self.model1 = ConcreteModel()
        
        self.model1.stands = Set(initialize = list(set(self.all_data.index.get_level_values(0))))
        self.model1.year = Set(initialize = list(set(self.all_data.index.get_level_values(2))))
        self.model1.regimes = Set(initialize = list(set(self.all_data.index.get_level_values(1))))
        self.model1.scen_index = Set(initialize= [i for i in range(0,self.combinations)])
        self.model1.Index_values = self.Index_values
        self.model1.Index_SA = self.SA
        self.model1.Index_INT = self.INTENSE
        self.model1.Index_EXT = self.EXTENSE
        
        # Indexes (stand, regime)-- excludes those combinations that have no regimes simulated
        
        def index_rule(model1):
            index = []
            for (s,r) in model1.Index_values: #stand_set
                index.append((s,r))
            return index            
        self.model1.index1 = Set(dimen=2, initialize=index_rule)
              
        def index_rule_EXT(model1):
            index = []
            for (s,r,) in model1.Index_EXT:
                index.append((s,r))
            return index
        self.model1.index1EXT = Set(dimen=2, initialize=index_rule_EXT)
        
        def index_rule_INT(model1):
            index = []
            for (s,r)  in model1.Index_INT:
                index.append((s,r))
            return index
        self.model1.index1INT= Set(dimen=2, initialize=index_rule_INT)
        
        def index_rule_SA(model1):
            index = []
            for (s,r)  in model1.Index_SA:
                index.append((s,r))
            return index
        self.model1.index1SA = Set(dimen=2, initialize=index_rule_SA)
        
        def index_rule_MULTIPLE(model1):
            index = []
            for (s,r) in model1.Index_values: #stand_set
                for k in range(0,50):
                    index.append((s,r,k))
            return index            
        self.model1.indexMULTIPLE = Set(dimen=3, initialize=index_rule_MULTIPLE)
        
        self.model1.X1 = Var(self.model1.index1, within=NonNegativeReals, bounds=(0,1), initialize=1)
        self.model1.X2 = Var(self.model1.indexMULTIPLE, within=NonNegativeReals, bounds=(0,1), initialize=1)
        
        self.all_data['year'] = self.all_data.index.get_level_values(2)
        
        #objective function:
        def outcome_rule(model1):
            return sum((self.all_data.Harvested_V.loc[(s,r,k)]*self.all_data.AREA.loc[(s,r,k)]* self.model1.X1[(s,r)])/((1+0.03)**(2.5+self.all_data.year[(s,r,k)]))  for (s,r) in self.model1.index1 for k in self.model1.year)
        self.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
        
        def regime_rule(model1, s):
            row_sum = sum(model1.X1[(s,r)] for r in [x[1] for x in model1.index1 if x[0] == s])
            return row_sum == 1
        self.model1.regime_limit = Constraint(self.model1.stands, rule=regime_rule)
        
    def solve(self):
        opt = SolverFactory('cbc') #Here we use the cbc solver -- open source software
        #results = opt.solve(self.model1,tee=False) #We solve a problem, but do not show the solver output
        self.results = opt.solve(self.model1,tee=False) #We solve a problem, but do not show the solver output

t1 = optimization()
import copy
t2 = copy.deepcopy(t1)

#MAX NPV
t2 = copy.deepcopy(t1)
t2.model1.flow_SA = Param(default=.2, mutable=True)
t2.model1.flow_INT = Param(default=.2, mutable=True)
t2.model1.flow_EXT = Param(default=.2, mutable=True)
t2.model1.SA_p= Var(within=NonNegativeReals)
t2.model1.SA_n= Var(within=NonNegativeReals)
t2.model1.EXT_p= Var(within=NonNegativeReals)
t2.model1.EXT_n= Var(within=NonNegativeReals)
t2.model1.INT_p= Var(within=NonNegativeReals)
t2.model1.INT_n= Var(within=NonNegativeReals)
t2.model1.NPV= Var(within=NonNegativeReals)

def regime_rule_SA(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1SA)
    return t2.model1.flow_SA*sum(t2.AREA) - row_sum - t2.model1.SA_p +t2.model1.SA_n ==0
t2.model1.SA_limit= Constraint(rule=regime_rule_SA)

def regime_rule_INT(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1INT)
    return t2.model1.flow_INT*sum(t2.AREA) - row_sum - t2.model1.INT_p +t2.model1.INT_n ==0
t2.model1.INT_limit= Constraint(rule=regime_rule_INT)

def regime_rule_EXT(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1EXT)
    return t2.model1.flow_EXT*sum(t2.AREA) - row_sum - t2.model1.EXT_p +t2.model1.EXT_n ==0
t2.model1.EXT_limit= Constraint(rule=regime_rule_EXT)

def NPV_INVENTORY(model1):
    row_sum = sum((t2.all_data.income.loc[(s,r,k)]*t2.all_data.AREA.loc[(s,r,k)]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+t2.all_data.year[(s,r,k)]-2016))  for (s,r) in t2.model1.index1 for k in t2.model1.year) +sum((t2.all_data.PV.loc[(s,r,max(t2.all_data.year[(s,r,slice(None))]))]* t2.all_data.AREA.loc[(s,r,max(t2.all_data.year[(s,r,slice(None))]))]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+max(t2.all_data.year[(s,r,slice(None))])-2016))  for (s,r) in t2.model1.index1)
    return t2.model1.NPV==row_sum
t2.model1.NPV_INV= Constraint(rule=NPV_INVENTORY)

def outcome_rule(model1):
    return t2.model1.NPV - 100000*(t2.model1.SA_p +t2.model1.SA_n+ t2.model1.EXT_p +t2.model1.EXT_n +t2.model1.INT_p +t2.model1.INT_n)
t2.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
t2.solve()

import itertools

curr_arr = [0, .10, .20, .30, .40, .50, .60, .70, .80, .90, 1.00]

comb_input = [a for a in itertools.combinations_with_replacement(curr_arr, 3) if sum(a) == 1]
comb_input = [set(itertools.permutations(a)) for a in comb_input]

finish = []
for a in comb_input:
    finish += list(a)
t1a = []
t1b = []
t1c= []
t1d= []

for (a,b,c) in finish:
    t2.model1.flow_SA = a
    t2.model1.flow_INT = b
    t2.model1.flow_EXT = c
    t2.model1.del_component(t2.model1.EXT_limit)
    t2.model1.del_component(t2.model1.INT_limit)
    t2.model1.del_component(t2.model1.SA_limit)
    t2.model1.EXT_limit= Constraint(rule=regime_rule_EXT)
    t2.model1.SA_limit= Constraint(rule=regime_rule_SA)
    t2.model1.INT_limit= Constraint(rule=regime_rule_INT)
    t2.solve()
    t1a= t1a+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1SA)/sum(t2.AREA)]
    t1b= t1b+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1INT)/sum(t2.AREA)]
    t1c= t1c+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1EXT)/sum(t2.AREA)]
    t1d= t1d+[t2.model1.NPV.value]

#SCRATCH
t2 = copy.deepcopy(t1)
t2str = "t2"
VAR_i = "1"

rar = []
for i in range(1,28):
    rar.append(str(i))
for VAR_i in rar:
    print(VAR_i)
    t2.model1.del_component(t2.model1.OBJ)    
    # Define the objective
    def outcome_rule(model1):
        value = str("sum(sum("+str(t2str)+".all_data.HSI_RL_S"+VAR_i+".loc[s,r,k] for k in "+str(t2str)+".model1.year) * "+str(t2str)+".model1.X1[(s,r)] for (s,r) in "+str(t2str)+".model1.index1)")
        setattr(t2,"out",eval(value))
        return t2.out
    t2.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
    t2.solve()
    print("SOLVED")
    value_VAR_i = "sum(sum("+str(t2str)+".all_data.HSI_RL_S"+VAR_i+".loc[s,r,k] for k in "+str(t2str)+".model1.year) * "+str(t2str)+".model1.X1[(s,r)].value for (s,r) in "+str(t2str)+".model1.index1)"
    
    setattr(t2,"max_HSI_RL_S"+VAR_i, eval(value_VAR_i ))
    t2.model1.del_component(t2.model1.OBJ)    
    t2.model1.OBJ = Objective(rule=outcome_rule, sense=minimize)
    t2.solve()
    value_VAR_i = "sum(sum("+str(t2str)+".all_data.HSI_RL_S"+VAR_i+".loc[s,r,k] for k in "+str(t2str)+".model1.year) * "+str(t2str)+".model1.X1[(s,r)].value for (s,r) in "+str(t2str)+".model1.index1)"
    setattr(t2,"min_HSI_RL_S"+VAR_i, eval(value_VAR_i))
MF_var = ['BILBERRY','ALL_MARKETED_MUSHROOMS','LESSER_SPOTTED_WOODPECKER','THREE_TOED_WOODPECKER','SIBERIAN_FLYING_SQUIRREL','LONG_TAILED_TIT','CAPERCAILLIE','HAZEL_GROUSE','COWBERRY','CARBON_SOIL_Update','BM_total','DEAD_WOOD_DIVERSITY',"scenic"]
for VAR_i in MF_var:
    print(VAR_i)
    t2.model1.del_component(t2.model1.OBJ)    
    # Define the objective
    def outcome_rule(model1):
        value = str("sum(sum("+str(t2str)+".all_data."+VAR_i+".loc[s,r,k] for k in "+str(t2str)+".model1.year) * "+str(t2str)+".model1.X1[(s,r)] for (s,r) in "+str(t2str)+".model1.index1)")
        setattr(t2,"out",eval(value))
        return t2.out
    t2.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
    t2.solve()
    value_VAR_i = " sum(sum("+str(t2str)+".all_data."+VAR_i +".loc[s,r,k] for k in "+str(t2str)+".model1.year) * "+str(t2str)+".model1.X1[(s,r)].value for (s,r) in "+str(t2str)+".model1.index1)"
    
    
    setattr(t2,"max_"+VAR_i, eval(value_VAR_i ))
    t2.model1.del_component(t2.model1.OBJ)    
    t2.model1.OBJ = Objective(rule=outcome_rule, sense=minimize)
    t2.solve()
    value_VAR_i = " sum(sum("+str(t2str)+".all_data."+VAR_i +".loc[s,r,k] for k in "+str(t2str)+".model1.year) * "+str(t2str)+".model1.X1[(s,r)].value for (s,r) in "+str(t2str)+".model1.index1)"
    setattr(t2,"min_"+VAR_i, eval(value_VAR_i))

#ORGANIZING THE MF OBJECTIVE
a1 = 0
a2 = 0
a3 = 1
a4 = 1

MF_var1 = list( MF_var[i] for i in [0,1,12] )
MF_var2 = list( MF_var[i] for i in [9,10])#,11] )
MF_var3 = list( MF_var[i] for i in [2,3,4,5,6,7] )
name = str(a1)+"_"+str(a2)+"_"+str(a3)+"_"+str(a4)

calc_MAX = 1

#ADD CONSTRAINTS   

t2.model1.Da = Var(within=NonNegativeReals)
t2.model1.Db = Var(within=NonNegativeReals)
t2.model1.Dc = Var(within=NonNegativeReals)
t2.model1.Dd = Var(within=NonNegativeReals)
t2.model1.Dc1 = Var(within=NonNegativeReals)
t2.model1.Dd1 = Var(within=NonNegativeReals)

value_VAR_i = " sum(sum("+str(t2str)+".all_data."+VAR_i +".loc[s,r,k] for k in "+str(t2str)+".model1.year) * "+str(t2str)+".model1.X1[(s,r)].value for (s,r) in "+str(t2str)+".model1.index1)"

code = """for VAR_i in MF_var1:
    start = time.time()
    def objA_rule(model1,i):
        relative_a = eval("(sum(sum(t2.all_data."+VAR_i+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+VAR_i+") / (t2.max_"+VAR_i+"-t2.min_"+VAR_i+")")
        return t2.model1.Da <= relative_a
    exec("t2.model1.obj"+VAR_i+" = Constraint(t2.model1.periods,rule=objA_rule)")
    end = time.time()
    print(end-start)
    print(VAR_i)
"""
start = time.time()
if a1 == 0:
    def objA1_rule(model1):
        relative_a = eval("(sum(sum(t2.all_data."+MF_var1[0]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var1[0]+") / (t2.max_"+MF_var1[0]+"-t2.min_"+MF_var1[0]+")")
        relative_b = eval("(sum(sum(t2.all_data."+MF_var1[1]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var1[1]+") / (t2.max_"+MF_var1[1]+"-t2.min_"+MF_var1[1]+")")
        relative_c = eval("(sum(sum(t2.all_data."+MF_var1[2]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var1[2]+") / (t2.max_"+MF_var1[2]+"-t2.min_"+MF_var1[2]+")")
        return t2.model1.Da <= (relative_a+relative_b+relative_c)/3
        #return t2.model1.Da <= (relative_a+relative_b)/2
    t2.model1.objBundle1 = Constraint(rule=objA1_rule)
    end = time.time()
elif a1 == 1:
    code1 = """for VAR_i in MF_var1:
    start = time.time()
    def objA1_rule(model1):
        relative_a = eval("(sum(sum(t2.all_data.all_data."+VAR_i+".loc[s,r,k] for k in t2.model1.year) * t1.model1.X1[(s,r)] for (s,r) in t1.model1.index1)-t1.min_"+VAR_i+") / (t1.max_"+VAR_i+"-t1.min_"+VAR_i+")")
        return t1.model1.Da <= relative_a
    exec("t1.model1.obj"+VAR_i+" = Constraint(rule=objA1_rule)")
    end = time.time()
    print(end-start)
    print(VAR_i)
    """
    exec(code1.replace("t1", t2str))
print(end-start)

start = time.time()
if a2 == 0:
    def objA2_rule(model1):
        relative_a = eval("(sum(sum(t2.all_data."+MF_var2[0]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var2[0]+") / (t2.max_"+MF_var2[0]+"-t2.min_"+MF_var2[0]+")")
        relative_b = eval("(sum(sum(t2.all_data."+MF_var2[1]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var2[1]+") / (t2.max_"+MF_var2[1]+"-t2.min_"+MF_var2[1]+")")
        #relative_c = eval("(sum(sum(t2.all_data."+MF_var2[2]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var2[2]+") / (t2.max_"+MF_var2[2]+"-t2.min_"+MF_var2[2]+")")
        #return t2.model1.Db <= (relative_a+relative_b+relative_c)/3
        return t2.model1.Db <= (relative_a+relative_b)/2
    t2.model1.objBundle2 = Constraint(rule=objA2_rule)
    end = time.time()
elif a2 == 1:
    code2 = """for VAR_i in MF_var2:
    start = time.time()
    def objA2_rule(model1):
        relative_a = eval("(sum(sum(t2.all_data."+VAR_i+".loc[s,r,k] for k in t2.model1.year) * t1.model1.X1[(s,r)] for (s,r) in t1.model1.index1)-t1.min_"+VAR_i+") / (t1.max_"+VAR_i+"-t1.min_"+VAR_i+")")
        return t1.model1.Db <= relative_a
    exec("t1.model1.obj"+VAR_i+" = Constraint(rule=objA2_rule)")
    end = time.time()
    print(end-start)
    print(VAR_i)
    """
    exec(code2.replace("t1", t2str))
print(end-start)

start = time.time()
if a3 == 0:
    def objA3_rule(model1):
        relative_a = eval("(sum(sum(t2.all_data."+MF_var3[0]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var3[0]+") / (t2.max_"+MF_var3[0]+"-t2.min_"+MF_var3[0]+")")
        relative_b = eval("(sum(sum(t2.all_data."+MF_var3[1]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var3[1]+") / (t2.max_"+MF_var3[1]+"-t2.min_"+MF_var3[1]+")")
        relative_c = eval("(sum(sum(t2.all_data."+MF_var3[2]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var3[2]+") / (t2.max_"+MF_var3[2]+"-t2.min_"+MF_var3[2]+")")
        relative_d = eval("(sum(sum(t2.all_data."+MF_var3[3]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var3[3]+") / (t2.max_"+MF_var3[3]+"-t2.min_"+MF_var3[3]+")")
        relative_e = eval("(sum(sum(t2.all_data."+MF_var3[4]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var3[4]+") / (t2.max_"+MF_var3[4]+"-t2.min_"+MF_var3[4]+")")
        relative_f = eval("(sum(sum(t2.all_data."+MF_var3[5]+".loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r)] for (s,r) in t2.model1.index1)-t2.min_"+MF_var3[5]+") / (t2.max_"+MF_var3[5]+"-t2.min_"+MF_var3[5]+")")
        return t2.model1.Dc <= (relative_a+relative_b+relative_c +relative_d+relative_e+relative_f)/6
    t2.model1.objBundle3 = Constraint(rule=objA3_rule)
elif a3 == 1:
    code3 = """for VAR_i in MF_var3:
    start = time.time()
    def objA3_rule(model1):
        relative_a = eval("(sum(sum(t1.all_data."+VAR_i+".loc[s,r,k] for k in t2.model1.year) * t1.model1.X1[(s,r)] for (s,r) in t1.model1.index1)-t1.min_"+VAR_i+") / (t1.max_"+VAR_i+"-t1.min_"+VAR_i+")")
        return t1.model1.Dc <= relative_a
    exec("t1.model1.obj"+VAR_i+" = Constraint(rule=objA3_rule)")
    end = time.time()
    print(end-start)
    print(VAR_i)
    """
    exec(code3.replace("t1", t2str))
end = time.time()
print(end-start)

start = time.time()
if a4 == 0:

    def objA4_rule(model1):
        relative_S1 = eval("(sum(sum(t2.all_data.HSI_RL_S1.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S1) / (t2.max_HSI_RL_S1-t2.min_HSI_RL_S1)")
        relative_S2 = eval("(sum(sum(t2.all_data.HSI_RL_S2.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S2) / (t2.max_HSI_RL_S2-t2.min_HSI_RL_S2)")
        relative_S3 = eval("(sum(sum(t2.all_data.HSI_RL_S3.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S3) / (t2.max_HSI_RL_S3-t2.min_HSI_RL_S3)")
        relative_S4 = eval("(sum(sum(t2.all_data.HSI_RL_S4.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S4) / (t2.max_HSI_RL_S4-t2.min_HSI_RL_S4)")
        relative_S5 = eval("(sum(sum(t2.all_data.HSI_RL_S5.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S5) / (t2.max_HSI_RL_S5-t2.min_HSI_RL_S5)")
        relative_S6 = eval("(sum(sum(t2.all_data.HSI_RL_S6.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S6) / (t2.max_HSI_RL_S6-t2.min_HSI_RL_S6)")
        relative_S7 = eval("(sum(sum(t2.all_data.HSI_RL_S7.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S7) / (t2.max_HSI_RL_S7-t2.min_HSI_RL_S7)")
        relative_S8 = eval("(sum(sum(t2.all_data.HSI_RL_S8.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S8) / (t2.max_HSI_RL_S8-t2.min_HSI_RL_S8)")
        relative_S9 = eval("(sum(sum(t2.all_data.HSI_RL_S9.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S9) / (t2.max_HSI_RL_S9-t2.min_HSI_RL_S9)")
        relative_S10 = eval("(sum(sum(t2.all_data.HSI_RL_S10.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S10) / (t2.max_HSI_RL_S10-t2.min_HSI_RL_S10)")
        relative_S11 = eval("(sum(sum(t2.all_data.HSI_RL_S11.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S11) / (t2.max_HSI_RL_S11-t2.min_HSI_RL_S11)")
        relative_S12 = eval("(sum(sum(t2.all_data.HSI_RL_S12.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S12) / (t2.max_HSI_RL_S12-t2.min_HSI_RL_S12)")
        relative_S13 = eval("(sum(sum(t2.all_data.HSI_RL_S13.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S13) / (t2.max_HSI_RL_S13-t2.min_HSI_RL_S13)")
        relative_S14 = eval("(sum(sum(t2.all_data.HSI_RL_S14.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S14) / (t2.max_HSI_RL_S14-t2.min_HSI_RL_S14)")
        relative_S15 = eval("(sum(sum(t2.all_data.HSI_RL_S15.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S15) / (t2.max_HSI_RL_S15-t2.min_HSI_RL_S15)")
        relative_S16 = eval("(sum(sum(t2.all_data.HSI_RL_S16.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S16) / (t2.max_HSI_RL_S16-t2.min_HSI_RL_S16)")
        relative_S17 = eval("(sum(sum(t2.all_data.HSI_RL_S17.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S17) / (t2.max_HSI_RL_S17-t2.min_HSI_RL_S17)")
        relative_S18 = eval("(sum(sum(t2.all_data.HSI_RL_S18.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S18) / (t2.max_HSI_RL_S18-t2.min_HSI_RL_S18)")
        relative_S19 = eval("(sum(sum(t2.all_data.HSI_RL_S19.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S19) / (t2.max_HSI_RL_S19-t2.min_HSI_RL_S19)")
        relative_S20 = eval("(sum(sum(t2.all_data.HSI_RL_S20.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S20) / (t2.max_HSI_RL_S20-t2.min_HSI_RL_S20)")
        relative_S21 = eval("(sum(sum(t2.all_data.HSI_RL_S21.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S21) / (t2.max_HSI_RL_S21-t2.min_HSI_RL_S21)")
        relative_S22 = eval("(sum(sum(t2.all_data.HSI_RL_S22.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S22) / (t2.max_HSI_RL_S22-t2.min_HSI_RL_S22)")
        relative_S23 = eval("(sum(sum(t2.all_data.HSI_RL_S23.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S23) / (t2.max_HSI_RL_S23-t2.min_HSI_RL_S23)")
        relative_S24 = eval("(sum(sum(t2.all_data.HSI_RL_S24.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S24) / (t2.max_HSI_RL_S24-t2.min_HSI_RL_S24)")
        relative_S25 = eval("(sum(sum(t2.all_data.HSI_RL_S25.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S25) / (t2.max_HSI_RL_S25-t2.min_HSI_RL_S25)")
        relative_S26 = eval("(sum(sum(t2.all_data.HSI_RL_S26.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S26) / (t2.max_HSI_RL_S26-t2.min_HSI_RL_S26)")
        relative_S27 = eval("(sum(sum(t2.all_data.HSI_RL_S27.loc[s,r,k] for k in t2.model1.year) * t2.model1.X1[(s,r,)] for (s,r) in t2.model1.index1)-t2.min_HSI_RL_S27) / (t2.max_HSI_RL_S27-t2.min_HSI_RL_S27)")
        return t2.model1.Dd <= (relative_S1+relative_S2+relative_S3 +relative_S4+relative_S5+relative_S6+relative_S7+relative_S8+relative_S9+relative_S10+relative_S10+relative_S11+relative_S12+relative_S13+relative_S14+relative_S15+relative_S16+relative_S17+relative_S18+relative_S19+relative_S20+relative_S20+relative_S21+relative_S22+relative_S23+relative_S24+relative_S25+relative_S26+relative_S27)/27
    t2.model1.objBundle4 = Constraint(rule=objA4_rule)
elif a4 == 1:
    code4 = """for VAR_i in rar:
    start = time.time()
    def objA4_rule(model1):
        relative_a = eval("(sum(sum(t2.all_data.HSI_RL_S"+VAR_i+".loc[s,r,k] for k in t2.model1.year) * t1.model1.X1[(s,r)] for (s,r) in t1.model1.index1)-t1.min_HSI_RL_S"+VAR_i+") / (t1.max_HSI_RL_S"+VAR_i+"-t1.min_HSI_RL_S"+VAR_i+")")
        return t1.model1.Dd <= relative_a
    exec("t1.model1.obj_HSI_RL_S"+VAR_i+" = Constraint(rule=objA4_rule)")
    end = time.time()
    print(end-start)
    print(VAR_i)
    """
    rar = []
    for i in range(1,28):
        rar.append(str(i))
    exec(code4.replace("t1", t2str))
end = time.time()
print("TIME",str(end-start))

#Constructing a payoff table between the different components of multifunctionality    
def Payoff_table(t2):
    import copy
    t4 = copy.deepcopy(t2)
    #With NPV constraints
    t4.model1.del_component(t4.model1.OBJ)    
    
    def outcome_rule(model1):
        #ADJUST TO BECOME MF
        return t4.model1.Da+(t4.model1.Db+t4.model1.Dc+t4.model1.Dd)/1000
    t4.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
    t4.solve()
    
    NPV = sum((t4.all_data.income.loc[(s,r,k)]*t4.all_data.AREA.loc[(s,r,k)]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+t4.all_data.year[(s,r,k)]-2016))  for (s,r) in t2.model1.index1 for k in t2.model1.year) +sum((t4.all_data.PV.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]*t4.all_data.AREA.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+max(t4.all_data.year[(s,r,slice(None))])-2016))  for (s,r) in t2.model1.index1)
    a1 = [t4.model1.Da.value,t4.model1.Db.value,t4.model1.Dc.value,t4.model1.Dd.value,NPV]
    t4.model1.del_component(t4.model1.OBJ)    
    
    def outcome_rule(model1):
        #ADJUST TO BECOME MF
        return t4.model1.Db+(t4.model1.Da+t4.model1.Dc+t4.model1.Dd)/1000
    t4.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
    t4.solve()
    
    NPV = sum((t4.all_data.income.loc[(s,r,k)]*t4.all_data.AREA.loc[(s,r,k)]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+t4.all_data.year[(s,r,k)]-2016))  for (s,r) in t2.model1.index1 for k in t2.model1.year) +sum((t4.all_data.PV.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]*t4.all_data.AREA.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+max(t4.all_data.year[(s,r,slice(None))])-2016))  for (s,r) in t2.model1.index1)
    a2 = [t4.model1.Da.value,t4.model1.Db.value,t4.model1.Dc.value,t4.model1.Dd.value,NPV]
    t4.model1.del_component(t4.model1.OBJ)    
    
    def outcome_rule(model1):
        #ADJUST TO BECOME MF
        return t4.model1.Dc+(t4.model1.Db+t4.model1.Da+t4.model1.Dd)/1000
    t4.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
    t4.solve()
    
    NPV = sum((t4.all_data.income.loc[(s,r,k)]*t4.all_data.AREA.loc[(s,r,k)]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+t4.all_data.year[(s,r,k)]-2016))  for (s,r) in t2.model1.index1 for k in t2.model1.year) +sum((t4.all_data.PV.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]*t4.all_data.AREA.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+max(t4.all_data.year[(s,r,slice(None))])-2016))  for (s,r) in t2.model1.index1)
    a3 = [t4.model1.Da.value,t4.model1.Db.value,t4.model1.Dc.value,t4.model1.Dd.value,NPV]
    t4.model1.del_component(t4.model1.OBJ)    
    
    def outcome_rule(model1):
        #ADJUST TO BECOME MF
        return t4.model1.Dd+(t4.model1.Db+t4.model1.Dc+t4.model1.Da)/1000
    t4.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
    t4.solve()
    
    NPV = sum((t4.all_data.income.loc[(s,r,k)]*t4.all_data.AREA.loc[(s,r,k)]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+t4.all_data.year[(s,r,k)]-2016))  for (s,r) in t2.model1.index1 for k in t2.model1.year) +sum((t4.all_data.PV.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]*t4.all_data.AREA.loc[(s,r,max(t4.all_data.year[(s,r,slice(None))]))]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+max(t4.all_data.year[(s,r,slice(None))])-2016))  for (s,r) in t2.model1.index1)
    a4 = [t4.model1.Da.value,t4.model1.Db.value,t4.model1.Dc.value,t4.model1.Dd.value,NPV]
    
    payoff = pandas.DataFrame({"MF_a_NPV":a1,"MF_b_NPV":a2,"MF_c_NPV":a3,"MF_d_NPV":a4})
    return payoff

payoff = Payoff_table(t2)
payoff.to_csv("/users/keyvinds/ROOT_ROT/Figs/payoff.csv")
min_max_Da = [min(payoff.iloc[0]),max(payoff.iloc[0])]
min_max_Db = [min(payoff.iloc[1]),max(payoff.iloc[1])]
min_max_Dc = [min(payoff.iloc[2]),max(payoff.iloc[2])]
min_max_Dd = [min(payoff.iloc[3]),max(payoff.iloc[3])]

#t2 = copy.deepcopy(t1)
try:
    t2.model1.del_component(t2.model1.flow_SA)
    t2.model1.del_component(t2.model1.flow_INT)
    t2.model1.del_component(t2.model1.flow_EXT)
    t2.model1.del_component(t2.model1.EXT_n)
    t2.model1.del_component(t2.model1.INT_p)
    t2.model1.del_component(t2.model1.INT_n)
    t2.model1.del_component(t2.model1.NPV)
    t2.model1.del_component(t2.model1.MF)
    t2.model1.del_component(t2.model1.MF_INV)
    t2.model1.del_component(t2.model1.SA_limit)
    t2.model1.del_component(t2.model1.INT_limit)
    t2.model1.del_component(t2.model1.EXT_limit)
    t2.model1.del_component(t2.model1.OBJ)
    t2.model1.del_component(t2.model1.SA_n)
    t2.model1.del_component(t2.model1.SA_p)
    t2.model1.del_component(t2.model1.EXP_p)
except:
    print("NO need")

t2.model1.flow_SA = Param(default=.2, mutable=True)
t2.model1.flow_INT = Param(default=.2, mutable=True)
t2.model1.flow_EXT = Param(default=.2, mutable=True)
t2.model1.SA_p= Var(within=NonNegativeReals)
t2.model1.SA_n= Var(within=NonNegativeReals)
t2.model1.EXT_p= Var(within=NonNegativeReals)
t2.model1.EXT_n= Var(within=NonNegativeReals)
t2.model1.INT_p= Var(within=NonNegativeReals)
t2.model1.INT_n= Var(within=NonNegativeReals)
t2.model1.NPV= Var(within=NonNegativeReals)
t2.model1.MF= Var(within=NonNegativeReals)


def regime_rule_SA(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1SA)
    return t2.model1.flow_SA*sum(t2.AREA) - row_sum - t2.model1.SA_p +t2.model1.SA_n ==0
t2.model1.SA_limit= Constraint(rule=regime_rule_SA)

def regime_rule_INT(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1INT)
    return t2.model1.flow_INT*sum(t2.AREA) - row_sum - t2.model1.INT_p +t2.model1.INT_n ==0
t2.model1.INT_limit= Constraint(rule=regime_rule_INT)

def regime_rule_EXT(model1):
    row_sum = sum(t2.model1.X1[(t,p)]*t2.AREA[t] for (t,p) in t2.model1.index1EXT)
    return t2.model1.flow_EXT*sum(t2.AREA) - row_sum - t2.model1.EXT_p +t2.model1.EXT_n ==0
t2.model1.EXT_limit= Constraint(rule=regime_rule_EXT)

def MF_INVENTORY(model1):
    row_sum = (t2.model1.Da-min_max_Da[0])/(min_max_Da[1]-min_max_Da[0])+(t2.model1.Db-min_max_Db[0])/(min_max_Db[1]-min_max_Db[0])+(t2.model1.Dc-min_max_Dc[0])/(min_max_Dc[1]-min_max_Dc[0])+(t2.model1.Dd-min_max_Dd[0])/(min_max_Dd[1]-min_max_Dd[0])
    return t2.model1.MF==row_sum
t2.model1.MF_INV= Constraint(rule=MF_INVENTORY)

def NPV_INVENTORY(model1):
    row_sum = sum((t2.all_data.income.loc[(s,r,k)]*t2.all_data.AREA.loc[(s,r,k)]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+t2.all_data.year[(s,r,k)]-2016))  for (s,r) in t2.model1.index1 for k in t2.model1.year) +sum((t2.all_data.PV.loc[(s,r,max(t2.all_data.year[(s,r,slice(None))]))]*t2.all_data.AREA.loc[(s,r,max(t2.all_data.year[(s,r,slice(None))]))]* t2.model1.X1[(s,r)])/((1+0.03)**(2.5+max(t2.all_data.year[(s,r,slice(None))])-2016))  for (s,r) in t2.model1.index1)
    return t2.model1.NPV==row_sum
t2.model1.NPV_INV= Constraint(rule=NPV_INVENTORY)

def outcome_rule(model1):
    return t2.model1.NPV /10000000 + (t2.model1.Da-min_max_Da[0])/(min_max_Da[1]-min_max_Da[0])+(t2.model1.Db-min_max_Db[0])/(min_max_Db[1]-min_max_Db[0])+(t2.model1.Dc-min_max_Dc[0])/(min_max_Dc[1]-min_max_Dc[0])+(t2.model1.Dd-min_max_Dd[0])/(min_max_Dd[1]-min_max_Dd[0])-10* (t2.model1.SA_p +t2.model1.SA_n+ t2.model1.EXT_p +t2.model1.EXT_n +t2.model1.INT_p +t2.model1.INT_n)
t2.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)
t2.solve()



###START OPTIMIZATIONS:

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

import itertools
def outcome_rule(model1):
    return t2.model1.NPV /10000000 + (t2.model1.Da-min_max_Da[0])/(min_max_Da[1]-min_max_Da[0])+(t2.model1.Db-min_max_Db[0])/(min_max_Db[1]-min_max_Db[0])+(t2.model1.Dc-min_max_Dc[0])/(min_max_Dc[1]-min_max_Dc[0])+(t2.model1.Dd-min_max_Dd[0])/(min_max_Dd[1]-min_max_Dd[0])-10* (t2.model1.SA_p +t2.model1.SA_n+ t2.model1.EXT_p +t2.model1.EXT_n +t2.model1.INT_p +t2.model1.INT_n)
t2.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)

DATA_EXTRACT = []
for i in [0,1,12,9,10,11,2,3,4,5,6,7]:
    DATA_EXTRACT = DATA_EXTRACT+[MF_var[i]]
for i in range(1,28):
    DATA_EXTRACT=DATA_EXTRACT+["HSI_RL_S"+str(i)]
DATA_EXTRACT = DATA_EXTRACT + ["NPV","MF","SA","INT","EXT"]


curr_arr = [0, .10, .20, .30, .40, .50, .60, .70, .80, .90, 1.00]

comb_input = [a for a in itertools.combinations_with_replacement(curr_arr, 3) if sum(a) == 1]
comb_input = [set(itertools.permutations(a)) for a in comb_input]

finish = []
for a in comb_input:
    finish += list(a)
t1a = []
t1b = []
t1c= []
t1d= []
t1e = []
t1_all = {}

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
    t1a= t1a+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1SA)/sum(t2.AREA)]
    t1b= t1b+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1INT)/sum(t2.AREA)]
    t1c= t1c+[sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1EXT)/sum(t2.AREA)]
    t1d= t1d+[t2.model1.MF.value]
    t1e = t1e+[t2.model1.NPV.value]
    temp_data = extract_data(t2)
    for kk in range(0,len(temp_data)):
        if DATA_EXTRACT[kk] in t1_all.keys():
            t1_all[DATA_EXTRACT[kk]] = t1_all[DATA_EXTRACT[kk]] +[temp_data[kk]]
        else:
            t1_all[DATA_EXTRACT[kk]] = [temp_data[kk]]
    XX = [t2.model1.NPV.value,t2.model1.MF.value,sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1SA)/sum(t2.AREA),sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1INT)/sum(t2.AREA),sum(t2.model1.X1[(t,p)].value*t2.AREA[t] for (t,p) in t2.model1.index1EXT)/sum(t2.AREA)]
    print(XX)
    kkk=0
    for kk in range(len(temp_data),len(DATA_EXTRACT)):
        if DATA_EXTRACT[kk] in t1_all.keys():
            t1_all[DATA_EXTRACT[kk]] = t1_all[DATA_EXTRACT[kk]] + [XX[kkk]]
        else:
            t1_all[DATA_EXTRACT[kk]] = [XX[kkk]]
        kkk=kkk+1

pd.DataFrame.from_dict(t1_all).to_csv("/users/keyvinds/ROOT_ROT/Figs/MAX_MF.csv")

def outcome_rule(model1):
    return t2.model1.NPV + 10000*((t2.model1.Da-min_max_Da[0])/(min_max_Da[1]-min_max_Da[0])+(t2.model1.Db-min_max_Db[0])/(min_max_Db[1]-min_max_Db[0])+(t2.model1.Dc-min_max_Dc[0])/(min_max_Dc[1]-min_max_Dc[0])+(t2.model1.Dd-min_max_Dd[0])/(min_max_Dd[1]-min_max_Dd[0])-10* (t2.model1.SA_p +t2.model1.SA_n+ t2.model1.EXT_p +t2.model1.EXT_n +t2.model1.INT_p +t2.model1.INT_n))
t2.model1.OBJ = Objective(rule=outcome_rule, sense=maximize)

curr_arr = [0, .10, .20, .30, .40, .50, .60, .70, .80, .90, 1.00]

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
    #print("1")
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
    kkk=0
    for kk in range(len(temp_data),len(DATA_EXTRACT)):
        if DATA_EXTRACT[kk] in t1_alla.keys():
            t1_alla[DATA_EXTRACT[kk]] = t1_alla[DATA_EXTRACT[kk]] + [XX[kkk]]
        else:
            t1_alla[DATA_EXTRACT[kk]] = [XX[kkk]]
        kkk=kkk+1

pd.DataFrame.from_dict(t1_alla).to_csv("/users/keyvinds/ROOT_ROT/Figs/MAX_NPV.csv")        

max_NPV = max(t1ee)
min_NPV = min(t1e)
max_MF = max(t1d)
min_MF = min(t1dd)

t2.model1.MF_NPV_flow = Param(default=0, mutable=True)
t2.model1.MAX_NPV_v = Param(default=max_NPV)
t2.model1.MIN_NPV_v = Param(default=min_NPV)


import cloudpickle
with open(path+"MOD/MODEL_1_MF.pkl",mode = "wb") as file:
    cloudpickle.dump(t2, file)
