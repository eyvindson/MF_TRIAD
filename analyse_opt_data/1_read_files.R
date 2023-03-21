###
#
# Read the optimization outcome 
# https://jyu.sharepoint.com/:f:/s/BERG359/Ei7hzZ3TR0BGvdJ1Id8_40gBpEMg-jxA9lMTmhDMzyRDwA?e=qqM44d 
# 2022-03-03
#
###


library(dplyr)


### Set the working path to this R-project
path <- paste0(getwd(),"/")



# ----------------
# Read all files and combine
# ----------------

filename <- list.files(paste0(path, "opt_data/"), pattern = "MAX_MF_")
filename <- gsub(".csv", "", filename)

df.t <- NULL

for(i in filename) {
  # test loop
  #i = filename[1]
  
    df <- read.csv(paste0(path, "opt_data/", i ,".csv"), 
                       sep = ","  ,
                       header = TRUE, 
                      stringsAsFactors = FALSE)
  # Add column indicating the filename 
  df$name <- i 
  
  df.t <- rbind(df.t, df)
}

df.opt <- df.t
rm(df.t, df)



# ----------------
# rename columns for management regimes
# ----------------
names(df.opt)

# "SA"
df.opt <- df.opt %>% 
  
  # rename individual regimes
  rename(EXT_BAUwT_5 = Longrotationthinning5Thinninglongrotation,
         EXT_BAUwT_10 = Longrotationthinning10Thinninglongrotation,
         EXT_BAUwT_15 = Longrotationthinning15Thinninglongrotation,
         EXT_BAUwT_30 = Longrotationthinning30Thinninglongrotation,
         
         INT_BAU_5 = Longrotationharvest5Longrotationclearcut,
         EXT_BAU_10 = Longrotationharvest10Longrotationclearcut,
         EXT_BAU_15 = Longrotationharvest15Longrotationclearcut,
         EXT_BAU_30 = Longrotationharvest30Longrotationclearcut, 
         
         INT_BAU = TapioharvestTapioclearcut, 
         INT_BAUwT = TapiothinningThinningTapio,
         EXT_BAUwoT = TapioharvestwithoutthinningsTapioclearcut,
         
         EXT_BAUwT_GTR = TapiothinningnatureThinningTapio,
         INT_BAUwGTR = TapioharvestnaturesceneTapioclearcutwithnaturescene, 
         
         INT_BAUwT_m5 = Shortrotationthinning5Thinninglongrotation,
         INT_BAU_m5 = Shortrotationharvest5shortrotationclearcut,
         
         EXT_BAUwoT_10 = Tapioharvestwithoutthinnings10Tapioclearcut,
         EXT_BAUwoT_m20 = Tapioharvestwithoutthinningsm20Tapioclearcut,
         
         INT_CCF_1 = Selectioncut1Selectioncut,
         INT_CCF_2 = Selectioncut2Selectioncut, 
         EXT_CCF_3 = Selectioncut3Selectioncut,
         EXT_CCF_4 = Selectioncut4Selectioncut)

names(df.opt)

df.opt <- df.opt %>% select(-X)


# ----------------
# Grouping of management regimes into INT, EXT (, SA)
# ----------------

## SA
# 
## INT = 
#   ["Selectioncut2Selectioncut", 
#    "Selectioncut1Selectioncut", 
#    "TapiothinningThinningTapio",  
#    "Longrotationharvest5Longrotationclearcut", 
#    "TapioharvestnaturesceneTapioclearcutwithnaturescene", 
#    "TapioharvestTapioclearcut", 
#    "Shortrotationthinning5Thinninglongrotation", 
#    "Shortrotationharvest5shortrotationclearcut"]
## EXT = 
#   ["Selectioncut4Selectioncut", 
#    "Selectioncut3Selectioncut", 
#    "Longrotationharvest15Longrotationclearcut", 
#    "Longrotationharvest10Longrotationclearcut", 
#    "Tapioharvestwithoutthinningsm20Tapioclearcut", 
#    "TapioharvestwithoutthinningsTapioclearcut", 
#    "Tapioharvestwithoutthinnings10Tapioclearcut", 
#    "Longrotationthinning30Thinninglongrotation", 
#    "Longrotationharvest30Longrotationclearcut", 
#    "Longrotationthinning15Thinninglongrotation", 
#    "Longrotationthinning10Thinninglongrotation", 
#    "TapiothinningnatureThinningTapio", 
#    "Longrotationthinning5Thinninglongrotation"]






















