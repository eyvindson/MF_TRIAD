# MF_Triangle

This git is for the development of a forest management planning optimization trade-off analysis. The purpose of this code will be to formulate an optimization problem that systematically explores the trade-off between forest management by assisgning management into thirds (extensive, intensive and protective management).

There are four  folders -- 

1: PYTHON: contains a callable python script, it is called through tehe RUN_MF_TRI.sh script.
2: DATA: contains a database (or set of databases) used as input data for the analysis. This is ignored by the git, as the file will be large - the data is availble from: XXXX. Currently located on PUHTI: /scratch/project_2000611/KYLE/REMI/, three files simulated_RCP_NEW_ROT.db, simulated_RCP_NEW_CCF.db, simulated_RCP_NEW_SA.db
3: opt_data: folder where optimization solution is moved to. We have placed a sample set of solutions to this folder.
4: analyse_opt_data: A folder containing r-script codes to generate figures for the manuscript.

Additionally, to conduct the optimizations, an opensource linear programming solving software is needed. We opted to use CBC, which should be available here: https://github.com/coin-or/Cbc

To run: You will need to install a variety of packages. We have uploaded the latest environment MF_Triangle.yml as a guide for what is needed.