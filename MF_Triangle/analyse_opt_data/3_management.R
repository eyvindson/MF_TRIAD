####
#
# Effect on management
# 2022-03-03
#
####


library(dplyr)
library(tidyr)
library(ggplot2)
library(viridis)
library(RColorBrewer)



namesRegimes <- read.csv(paste0(path, "analyse_opt_data/regimes.txt"),sep = ";",header = TRUE,stringsAsFactors = FALSE)




# ---------------------
# percent shares of regime classes
# ---------------------

names(df.opt)

column <- c("EXT_BAUwT_10" ,  "EXT_BAUwT_GTR",  "EXT_BAU_30" ,    "EXT_BAUwT_15" ,  "EXT_BAUwT_30",   "EXT_BAUwoT" ,    "EXT_BAUwT_5",    "EXT_BAUwoT_m20", "EXT_CCF_4",      "EXT_CCF_3",     
            "EXT_BAUwoT_10",  "EXT_BAU_10",     "INT_CCF_1" ,     "INT_BAU" ,       "INT_BAU_m5",     "INT_BAU_5" ,     "EXT_BAU_15",     "INT_CCF_2"  ,    "INT_BAUwT"  ,    "INT_BAUwT_m5",  
            "INT_BAUwGTR" ,   "SA"  )  

df.regime <- df.opt %>% 
  mutate(row_sum = rowSums(.[,column])) %>% 
  #mutate_at( column, ~round((.x / row_sum * 100), digits = 3)) %>% 
  mutate_at( column, ~(.x / row_sum * 100)) %>% 
  mutate(row_sum_prc = rowSums(.[,column]))



# ---------------------
# Management regimes at the highest point
# ---------------------

head(df.regime)

df.max_mf <- df.regime %>% 
  select(all_of(column), NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
  filter(name %in% "MAX_MF_1.0") %>% 
  filter(MF == max(MF)) %>% 
  tidyr::gather("regime", "prc", EXT_BAUwT_10:SA) %>% 
  mutate(name_p = "max_MF")

df.max_npv <- df.regime %>% 
  select(all_of(column), NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
  filter(name %in% "MAX_MF_0.0") %>% 
  filter(NPV == max(NPV)) %>% 
  tidyr::gather("regime", "prc", EXT_BAUwT_10:SA) %>% 
  mutate(name_p = "max_NPV")


## combine and adjust factor level

df.max <- rbind(df.max_mf, df.max_npv)

df.max$regime <- factor(df.max$regime,
                        levels = c(
                                 "INT_BAU","INT_BAU_m5","INT_BAU_5","INT_BAUwT","INT_BAUwT_m5","INT_BAUwGTR",
                                 "INT_CCF_1", "INT_CCF_2",
                                 "EXT_CCF_3" ,"EXT_CCF_4", 
                                 "EXT_BAUwoT","EXT_BAUwoT_m20","EXT_BAUwT_GTR","EXT_BAUwT_5","EXT_BAU_10", "EXT_BAUwT_10","EXT_BAUwoT_10","EXT_BAUwT_15","EXT_BAU_15","EXT_BAU_30","EXT_BAUwT_30",
                                 "SA"))





### plot regimes for MF and NPV max

plot.regime_max <- df.max %>% 
  mutate(prc = round(prc, digits = 1)) %>% 
  filter(prc > 0) %>% 
  ggplot(aes(x = name_p, y = prc, fill=regime )) +
  geom_bar(stat="identity") +
  theme_minimal()+
  theme(axis.title.x=element_blank() )+
  
  scale_fill_manual(values = c(colorRampPalette(rev(brewer.pal(9,"Blues")[2:9]))(3),
                               colorRampPalette(rev(brewer.pal(9,"Oranges")[2:8]))(4),
                               #colorRampPalette(brewer.pal(9,"Blues"))(2),
                               colorRampPalette(rev(brewer.pal(9,"Greens")[2:9]))(8),
                               colorRampPalette(rev((brewer.pal(9,"BrBG") )))(1)
                               #colorRampPalette(brewer.pal(9,"Greys"))(2)
  ))
  #scale_fill_manual(values = colorRampPalette(brewer.pal(8, "Set2"))(colourCount)) 
  #scale_fill_viridis_d(option = "cividis" ,direction = -1)
  #scale_fill_brewer("Paired")
plot.regime_max

ggsave(plot = plot.regime_max, paste0(path,"analyse_opt_data/regime_max.tiff"), width=4, height=5)
ggsave(plot = plot.regime_max, paste0(path,"analyse_opt_data/regime_max.pdf"), width=4, height=5)



# ### groups or regimes
# 
# # regime length and color setting
# col <- rbind(max_mf, max_npv) %>% 
#   mutate(prc = round(prc, digits = 1)) %>% 
#   filter(prc > 0) %>% 
#   left_join(namesRegimes, by = "regime")
# colourCount = length(unique(col$regime_gr))
# 
# plot.regime_max <- rbind(max_mf, max_npv) %>% 
#   mutate(prc = round(prc, digits = 1)) %>% 
#   filter(prc > 0) %>% 
#   left_join(namesRegimes, by = "regime") %>% 
#   ggplot(aes(x = name_p, y = prc, fill=regime_gr )) +
#   geom_bar(stat="identity") +
#   theme_minimal()+
#   theme(axis.title.x=element_blank() )+
#   scale_fill_manual(values = colorRampPalette(brewer.pal(12, "Set3"))(colourCount)) 
# #scale_fill_viridis_d(option = "cividis" ,direction = -1)
# #scale_fill_brewer("Paired")
# plot.regime_max
# 
# ggsave(plot = plot.regime_max, paste0(path,"analyse_opt_data/regime_max_gr.tiff"), width=4, height=5)





# ---------------------
# Management regimes over the weighting gradient - With fixed highest point
# ---------------------


# round values -> otherwise no match when filtering 
df.regime <- df.regime %>% 
  mutate_at( c("SA_O", "INT_O", "EXT_O"), ~round(.x , digits = 1)) 

# point of maximum Multifunctionality  
max_mf_pt <- df.regime %>% 
  select(NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
  filter(name %in% "MAX_MF_1.0") %>% 
  filter(MF == max(MF)) 

# point of maximum NPV
max_npv_pt <- df.regime %>% 
  select(NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
  filter(name %in% "MAX_MF_0.0") %>% 
  filter(NPV == max(NPV)) 



ls.optscenario <- c("MAX_MF_0.0", "MAX_MF_0.1", "MAX_MF_0.2", "MAX_MF_0.3", "MAX_MF_0.4", "MAX_MF_0.5", "MAX_MF_0.6",
                    "MAX_MF_0.7", "MAX_MF_0.8", "MAX_MF_0.9", "MAX_MF_1.0" )

  
regimeAtMax.t <- NULL

for(i in ls.optscenario) {
  
  #i = ls.optscenario[1]
  
  mf.t <- df.regime %>% 
    select(column, NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_mf_pt[,"SA_O"] & 
              INT_O %in%  max_mf_pt[,"INT_O"] & 
              EXT_O %in% max_mf_pt[,"EXT_O"]) %>% 
    tidyr::gather("regime", "prc", EXT_BAUwT_10:SA) %>% 
    mutate(name_p = "Optimized Triad zoning for MF")
  
  npv.t <- df.regime %>% 
    select(column, NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_npv_pt[,"SA_O"] & 
              INT_O %in%  max_npv_pt[,"INT_O"] & 
              EXT_O %in% max_npv_pt[,"EXT_O"]) %>% 
    tidyr::gather("regime", "prc", EXT_BAUwT_10:SA) %>% 
    mutate(name_p = "Optimized Triad zoning for NPV")
  
  regimeAtMax.t <- rbind(regimeAtMax.t, mf.t , npv.t)
  
}


# col <- regimeAtMax.t  %>% 
#   mutate(prc = round(prc, digits = 1)) %>% 
#   filter(prc > 0) 
# colourCount = length(unique(col$regime))


unique(regimeAtMax.t$regime)

regimeAtMax.t$regime <- factor(regimeAtMax.t$regime, 
                               levels = c(
                                 "INT_BAU","INT_BAU_m5","INT_BAU_5","INT_BAUwT","INT_BAUwT_m5","INT_BAUwGTR",
                                 "INT_CCF_1", "INT_CCF_2",
                                 "EXT_CCF_3" ,"EXT_CCF_4", 
                                 "EXT_BAUwoT","EXT_BAUwoT_m20","EXT_BAUwT_GTR","EXT_BAUwT_5","EXT_BAU_10", "EXT_BAUwT_10","EXT_BAUwoT_10","EXT_BAUwT_15","EXT_BAU_15","EXT_BAU_30","EXT_BAUwT_30",
                                 "SA"))
       
plot.regimeAtMax_gradient <- regimeAtMax.t %>% 
  mutate(prc = round(prc, digits = 1)) %>% 
  filter(prc > 0) %>% 
  
  separate(name, c("MAX", "MF", "weight"), sep = "_") %>% 
  mutate( weight = as.numeric(weight)) %>% 
  
  ggplot(aes(x = weight, y = prc, fill=regime )) +
  geom_bar(stat="identity") +
  
  # geom_bar(data=test,        # filter
  #          aes(x = weight, y = prc, fill=regime ), stat="stack", alpha=0, size=1, color="black") +
  
  theme_minimal()+
  #theme_bw() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
  #scale_fill_manual(values = colorRampPalette(brewer.pal(8, "Set2"))(colourCount)) +
  
  # scale_fill_manual(values = c(colorRampPalette(brewer.pal(9,"Blues") )(8),
  #                              colorRampPalette(brewer.pal(9,"Reds") )(4),
  #                              #colorRampPalette(brewer.pal(9,"Blues"))(2),
  #                              colorRampPalette(brewer.pal(9,"Greens") )(10) #,
  #                              #colorRampPalette((brewer.pal(9,"Greys") ))(1)
  #                              #colorRampPalette(brewer.pal(9,"Greys"))(2)
  #                              ))+
  
  scale_fill_manual(values = c(colorRampPalette(rev(brewer.pal(9,"Blues")[2:9]))(6),
                               colorRampPalette(rev(brewer.pal(9,"Oranges")[2:8]))(4),
                               #colorRampPalette(brewer.pal(9,"Blues"))(2),
                               colorRampPalette(rev(brewer.pal(9,"Greens")[2:9]))(9),
                               colorRampPalette(rev((brewer.pal(9,"BrBG") )))(1)
                               #colorRampPalette(brewer.pal(9,"Greys"))(2)
  ))+
  
  
  facet_grid(name_p ~ .) +
  scale_x_continuous(breaks=c(seq(0,1, by = 0.1) )) +
  ylab("management regime share [%]") +
  xlab("Weight for Multifunctionality (MF)") #+
  #ggtitle( "Regime combination over gradient - fixed position")
plot.regimeAtMax_gradient

ggsave(plot = plot.regimeAtMax_gradient, paste0(path,"analyse_opt_data/regimeAtMax_gradient.tiff"), width=9, height=6)
ggsave(plot = plot.regimeAtMax_gradient, paste0(path,"analyse_opt_data/regimeAtMax_gradient.pdf"), width=9, height=6)



### get values shown in figure 
getval_pointMaxMF <- regimeAtMax.t %>% 
  mutate(prc = round(prc, digits = 1)) %>% 
  filter(prc > 0) %>% 
  separate(name, c("MAX", "MF", "weight"), sep = "_") %>% 
  mutate( weight = as.numeric(weight)) %>% 
  filter(name_p %in% "point of max MF") %>% 
  filter(weight %in% 0 | weight %in% 1) %>% 
  select(regime, prc, weight, name_p)

getval_pointMaxNPV <- regimeAtMax.t %>% 
  mutate(prc = round(prc, digits = 1)) %>% 
  filter(prc > 0) %>% 
  separate(name, c("MAX", "MF", "weight"), sep = "_") %>% 
  mutate( weight = as.numeric(weight)) %>% 
  filter(name_p %in% "point of max NPV") %>% 
  filter(weight %in% 0 | weight %in% 1) %>% 
  select(regime, prc, weight, name_p)



#display.brewer.all() 


rm(list=ls(pattern="plot"))



# # ---------------------
# # Management regimes over the weighting gradient - each at highest point
# # ---------------------
# 
# 
# 
# ls.optscenario <- c("MAX_MF_0", "MAX_MF_0.1", "MAX_MF_0.2", "MAX_MF_0.3", "MAX_MF_0.4", "MAX_MF_0.5", "MAX_MF_0.6",
#                     "MAX_MF_0.7", "MAX_MF_0.8", "MAX_MF_0.9", "MAX_MF_1" )
# 
# max_mf.t <- NULL
# 
# for(i in ls.optscenario) {
#   
#   #i = ls.optscenario[1]
#   
#   max_mf <- df.regime %>% 
#     select(column, NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
#     filter(name %in% i) %>% 
#     filter(MF == max(MF)) %>% 
#     tidyr::gather("regime", "prc", EXT_BAUwT_10:SA) %>% 
#     mutate(name_p = "max_MF")
#   
#   max_mf.t <- rbind(max_mf.t, max_mf)
#   
# }
# 
# 
# max_npv.t <- NULL
# 
# for(i in ls.optscenario) {
#   
#   #i = ls.optscenario[1]
#   
#   max_npv <- df.regime %>% 
#     select(column, NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
#     filter(name %in% i) %>% 
#     filter(NPV == max(NPV)) %>% 
#     tidyr::gather("regime", "prc", EXT_BAUwT_10:SA) %>% 
#     mutate(name_p = "max_NPV")
#   
#   max_npv.t <- rbind(max_npv.t, max_npv)
#   
# }
# 
# 
# ### regimes along weighting of MF/NPV
# 
# # regime length and color setting
# col <- rbind(max_mf.t, max_npv.t) %>% 
#   mutate(prc = round(prc, digits = 1)) %>% 
#   filter(prc > 0) 
# colourCount = length(unique(col$regime))
# 
# plot.max_mfnpv_0to1 <- rbind(max_mf.t, max_npv.t) %>% 
#   mutate(prc = round(prc, digits = 1)) %>% 
#   filter(prc > 0) %>% 
#   ggplot(aes(x = name, y = prc, fill=regime )) +
#   geom_bar(stat="identity") +
#   theme_minimal()+
#   theme(axis.title.x=element_blank(),
#         axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))+
#   scale_fill_manual(values = colorRampPalette(brewer.pal(8, "Set2"))(colourCount)) +
#   facet_grid(name_p ~ .) +
#   ggtitle( "Regime combination where MF and NPV are maximum")
# plot.max_mfnpv_0to1
# 
# ggsave(plot = plot.max_mfnpv_0to1, paste0(path,"analyse_opt_data/regime_max_mfnpv_0to1.tiff"), width=10, height=8)








