###
#
# Plot triangles
# 2022-03-02
#
###


library(dplyr)
library(ggtern)
library(viridis)
library(ggpubr)


### 
unique(df.opt$name)
names(df.opt)



### just use the necessary columns
df.plot <- df.opt %>% 
  # filter(name %in% c("MAX_MF_0", "MAX_MF_1")) %>% 
  select(NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
  mutate_at(c("SA_O","INT_O", "EXT_O"), round, 2) %>% 
  mutate(NPV = NPV / 1000000) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O)



################################################################################
################################################################################




# ----------------
# Plot MF and NPV, each for weight 1 and its counterpart 
# ----------------


# ----------------
# Plot corresponding Multifunctionality value
# ----------------

# point of max MF
maxMF_MF <- df.plot %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  filter(MF == max(MF))

# point of max NPV
maxNPV_NPV <- df.plot %>%
  filter(name %in% c("MAX_MF_0.0")) %>%
  filter(NPV == max(NPV))


# defin min and max value for ranges
minMF <- min(df.plot$MF)
maxMF <- max(df.plot$MF)

# Plot when maximize MF - "MAX_MF_1.0"
plot.MF_MF <- df.plot %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  ggtern(aes(INT, EXT, RES, value = MF)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"#,
    #show.legend = FALSE
  ) +
  scale_fill_viridis(name = "MF\n(index)", limits = c(minMF,maxMF)) +
  theme_bvbg() +
  theme_legend_position("topright") +
  theme_gridsontop() +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("c) Maximize Multifunctionality (MF)") +
  
  geom_mask() +
  geom_point(data = maxMF_MF, aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5) +
  geom_point(data = maxNPV_NPV, aes(INT, EXT, RES),fill="green", shape=21, size = 5,stroke = 1.5 )
plot.MF_MF


# plot when maximize NPV - "MAX_MF_0.0"
plot.NPV_MF <- df.plot %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  ggtern(aes(INT,EXT, RES, value = MF)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"# ,
    #show.legend = FALSE
  ) +
  scale_fill_viridis(name = "MF\n(index)", limits = c(minMF,maxMF)) +
  theme_bvbg() +
  theme_legend_position("topright") +
  theme_gridsontop() +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("b) MF when maximizing for NPV") + 
  
  geom_mask() +
  geom_point(data = maxMF_MF, aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5) +
  geom_point(data = maxNPV_NPV, aes(INT, EXT, RES),fill="green", shape=21, size = 5 , stroke = 1.5)
plot.NPV_MF



# ----------------
# Plot corresponding NPV value
# ----------------

# defin min and max value for ranges
minNPV <- min(df.plot$NPV)
maxNPV <- max(df.plot$NPV)

### plot when maximize NPV - "MAX_MF_0.0"
plot.NPV_NPV <- df.plot %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  ggtern(aes(INT, EXT, RES, value = NPV)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis(name = "NPV\n(M.Euro)", limits = c(minNPV,maxNPV)
                     ,option="plasma"
                     ) +
  theme_bvbg() +
  theme_gridsontop() +
  theme(tern.axis.arrow = element_line(size = 2))+
  theme_legend_position("topright") +
  ggtitle("a) Maximize Net Present Value (NPV)") + 
  geom_mask() +
  geom_point(data = maxMF_MF, aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5) +
  geom_point(data = maxNPV_NPV, aes(INT, EXT, RES),fill="green", shape=21, size = 5 , stroke = 1.5)
plot.NPV_NPV


### plot when maximize MF - "MAX_MF_1.0"
plot.MF_NPV <- df.plot %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  ggtern(aes(INT, EXT, RES, value = NPV)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"#,
    #show.legend = FALSE
  ) +
  scale_fill_viridis(name = "NPV\n(M.Euro)", limits = c(minNPV,maxNPV),
                     option="plasma") +
  theme_bvbg() +
  #theme_arrowlarge() +
  #theme_bvbw() +
  #theme_rgbg() +
  #theme_classic() + 
  theme_legend_position("topright") +
  theme_gridsontop() +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("d) NPV when maximizing for MF") +
  
  geom_mask() +
  geom_point(data = maxMF_MF, aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5) +
  geom_point(data = maxNPV_NPV, aes(INT, EXT, RES),fill="green", shape=21, size = 5 , stroke = 1.5)
plot.MF_NPV


## plot all
plot.all  <- ggtern::grid.arrange(plot.NPV_NPV, plot.NPV_MF,
                                  plot.MF_MF, plot.MF_NPV, ncol = 2, nrow = 2) 
ggsave(plot = plot.all, paste0(path,"analyse_opt_data/plot_npv_mf_max_counterpart.jpeg"), width=10, height=10)
ggsave(plot = plot.all, paste0(path,"analyse_opt_data/plot_npv_mf_max_counterpart.pdf"), width=10, height=10)


# ## plot just NPV under max NPV & MF under max MF
# plot.NPV_NPV_MF_MF <- ggtern::grid.arrange(plot.NPV_NPV, plot.MF_MF, ncol = 2, nrow = 1)
# ggsave(plot = plot.NPV_NPV_MF_MF, paste0(path,"analyse_opt_data/plot_NPV_MF_max.tiff"), width=12, height=5)
# ggsave(plot = plot.NPV_NPV_MF_MF, paste0(path,"analyse_opt_data/plot_NPV_MF_max.pdf"), width=12, height=5)



## GET percentage values of difference

# when maximize MF
maxMF_MF <- df.plot %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  filter(MF == max(MF))
maxNPV_MF <- df.plot %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  filter(RES == maxMF_MF$RES & INT == maxMF_MF$INT & EXT == maxMF_MF$EXT)

# when maximize NPV
maxNPV_NPV <- df.plot %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  filter(NPV == max(NPV))
maxMF_NPV <- df.plot %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  filter(RES == 0.03 & INT == 0.77 & EXT == 0.2) # comes closest with this shares

# get values to the plots
getval <- rbind(maxMF_MF, maxNPV_MF, maxNPV_NPV, maxMF_NPV) %>% 
  mutate(maxMF = max(MF),
         prcOfMaxMF = MF / maxMF * 100,
         maxNPV = max(NPV),
         prcOfMaxNPV = NPV / maxNPV * 100) %>% 
  select(NPV, prcOfMaxNPV, MF, prcOfMaxMF, RES, INT, EXT, name)




################################################################################
################################################################################



# ---------------
# Individual components of Multifunctionality
# when "MF is optimized"
# ---------------

names(df.opt)

# for nonwood ES
nonwoodCol <- c("BILBERRY", "ALL_MARKETED_MUSHROOMS", "scenic")

nw <- df.opt %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  select(all_of(nonwoodCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "nonwood")
nw$AVG <- apply(nw[,nonwoodCol], 1, mean, na.rm = TRUE)


# for climate mitigation
carbonCol <- c("CARBON_SOIL_Update", "BM_total")

carbon <- df.opt %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  select(all_of(carbonCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "carbon")
carbon$AVG <- apply(carbon[,carbonCol], 1, mean, na.rm = TRUE)


# for vertebrate species habitat
vertebrateCol <- c("LESSER_SPOTTED_WOODPECKER", "THREE_TOED_WOODPECKER", "SIBERIAN_FLYING_SQUIRREL", "LONG_TAILED_TIT", 
                   "CAPERCAILLIE", "HAZEL_GROUSE")

vertebrate <- df.opt %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  select(all_of(vertebrateCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "vertebrate")
vertebrate$MIN <- apply(vertebrate[,vertebrateCol], 1, min, na.rm = TRUE)


# for 27 deadwood species habitat
deadwoodCol <- c("HSI_RL_S1", "HSI_RL_S2", "HSI_RL_S3", "HSI_RL_S4", "HSI_RL_S5","HSI_RL_S6", "HSI_RL_S7", "HSI_RL_S8","HSI_RL_S9","HSI_RL_S10",
                 "HSI_RL_S11","HSI_RL_S12", "HSI_RL_S13","HSI_RL_S14","HSI_RL_S15", "HSI_RL_S16", "HSI_RL_S17","HSI_RL_S18","HSI_RL_S19","HSI_RL_S20",
                 "HSI_RL_S21", "HSI_RL_S22","HSI_RL_S23","HSI_RL_S24","HSI_RL_S25","HSI_RL_S26","HSI_RL_S27")

dw <- df.opt %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  select(all_of(deadwoodCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "deadwood")
dw$MIN <- apply(dw[,deadwoodCol], 1, min, na.rm = TRUE)




### get values for manuscript text
a <- nw %>% 
  select(RES, INT, EXT, es, AVG) %>% 
  mutate_at(c("RES","INT", "EXT"), round, 2) %>% 
  filter(RES %in% maxMF_MF$RES & INT %in% maxMF_MF$INT & EXT %in% maxMF_MF$EXT | AVG == max(nw$AVG) | AVG == min(nw$AVG)) %>% 
  rename(value = AVG) %>% 
  mutate(prcOfMax = value / max(value) * 100) %>% 
  mutate(aggregation = "AVG")

b <- carbon %>% 
  select(RES, INT, EXT, es, AVG) %>% 
  mutate_at(c("RES","INT", "EXT"), round, 2) %>% 
  filter(RES %in% maxMF_MF$RES & INT %in% maxMF_MF$INT & EXT %in% maxMF_MF$EXT | AVG == max(carbon$AVG) | AVG == min(carbon$AVG)) %>%
  rename(value = AVG) %>% 
  mutate(prcOfMax = value / max(value) * 100) %>% 
  mutate(aggregation = "AVG")

c <- vertebrate %>% 
  select(RES, INT, EXT, es, MIN) %>% 
  mutate_at(c("RES","INT", "EXT"), round, 2) %>% 
  filter(RES %in% maxMF_MF$RES & INT %in% maxMF_MF$INT & EXT %in% maxMF_MF$EXT | MIN == max(vertebrate$MIN) | MIN == min(vertebrate$MIN)) %>% 
  rename(value = MIN) %>% 
  mutate(prcOfMax = value / max(value) * 100) %>% 
  mutate(aggregation = "MIN")

d <- dw %>% 
  select(RES, INT, EXT, es, MIN) %>% 
  mutate_at(c("RES","INT", "EXT"), round, 2) %>% 
  filter(RES %in% maxMF_MF$RES & INT %in% maxMF_MF$INT & EXT %in% maxMF_MF$EXT | MIN == max(dw$MIN) | MIN == min(dw$MIN)) %>% 
  rename(value = MIN) %>% 
  mutate(prcOfMax = value / max(value) * 100) %>% 
  mutate(aggregation = "MIN")

getval2 <- rbind(a,b,d,c)





# ---------------
# Plot components of Multifunctionality
# when MF is optimized
# ---------------

# # define overall min and max for plot limit (getting same legend scale) --> use different scales for better illustration of patterns
# minComp <- min( min(nw$AVG) , min(dw$MIN), min(vertebrate$MIN), min(carbon$AVG)) 
# maxComp <- max( max(nw$AVG) , max(dw$MIN), max(vertebrate$MIN), max(carbon$AVG)) 


### point of maximize MF
maxMF_MF <- df.plot %>% 
  filter(name %in% c("MAX_MF_1.0")) %>% 
  filter(MF == max(MF))

# nonwood ES
plot.nw <- nw %>%  ggtern(aes(INT, EXT, RES, value  = AVG)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
    
    #,show.legend = FALSE
  
    ) +
  scale_fill_viridis(name = "value\n(AVG)") + # , limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("a) Nonwood ecosystem services") +
  geom_mask() +
  geom_point(data = maxMF_MF %>% rename(AVG = MF), aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5) 
plot.nw


# climate mitigation
plot.carbon <- carbon %>%  ggtern(aes(INT, EXT, RES, value  = AVG)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
    
    #,show.legend = FALSE
    
  ) +
  scale_fill_viridis(name = "value\n(AVG)") + # , limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("b) Climate mitigation")+
  geom_mask() +
  geom_point(data = maxMF_MF %>% rename(AVG = MF), aes(INT, EXT, RES),fill="red", shape=21,size = 5, stroke = 1.5) 
plot.carbon


# vertebrate species
plot.vertebrate <- vertebrate %>%  ggtern(aes(INT, EXT, RES, value  = MIN)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
    
    #,show.legend = FALSE
  
    ) +
  scale_fill_viridis(name = "value\n(MIN)") + #, limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("c) Vertebrate species habitat") +
  geom_mask() +
  geom_point(data = maxMF_MF %>% rename(MIN = MF), aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5)
plot.vertebrate


# 27 deadwood species
plot.dw <- dw %>%  ggtern(aes(INT, EXT, RES, value  = MIN)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis(name = "value\n(MIN)") + #, limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("d) 27 deadwood species habitat") +
  geom_mask() +
  geom_point(data = maxMF_MF %>% rename(MIN = MF), aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5)
plot.dw

components <- ggtern::grid.arrange(plot.nw, plot.carbon,plot.vertebrate, plot.dw,  ncol = 4, nrow = 1)
ggsave(plot = components, paste0(path,"analyse_opt_data/plot_MF_components_1.tiff"), width=16, height=5)
ggsave(plot = components, paste0(path,"analyse_opt_data/plot_MF_components_1.pdf"), width=16, height=5)

components2 <- ggtern::grid.arrange(plot.nw, plot.carbon,plot.vertebrate, plot.dw,  ncol = 2, nrow = 2)
ggsave(plot = components2, paste0(path,"analyse_opt_data/plot_MF_components_2.tiff"), width=10, height=10)
ggsave(plot = components2, paste0(path,"analyse_opt_data/plot_MF_components_2.pdf"), width=10, height=10) 




################################################################################
################################################################################




# ---------------
# Individual components of Multifunctionality
# when "NPV is optimized"
# ---------------


# for nonwood ES
nonwoodCol <- c("BILBERRY", "ALL_MARKETED_MUSHROOMS", "scenic")

nw2 <- df.opt %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  select(all_of(nonwoodCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "nonwood")
nw2$AVG <- apply(nw[,nonwoodCol], 1, mean, na.rm = TRUE)


# for climate mitigation
carbonCol <- c("CARBON_SOIL_Update", "BM_total")

carbon2 <- df.opt %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  select(all_of(carbonCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "carbon")
carbon2$AVG <- apply(carbon[,carbonCol], 1, mean, na.rm = TRUE)


# for vertebrate species habitat
vertebrateCol <- c("LESSER_SPOTTED_WOODPECKER", "THREE_TOED_WOODPECKER", "SIBERIAN_FLYING_SQUIRREL", "LONG_TAILED_TIT", 
                   "CAPERCAILLIE", "HAZEL_GROUSE")

vertebrate2 <- df.opt %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  select(all_of(vertebrateCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "vertebrate")
vertebrate2$MIN <- apply(vertebrate[,vertebrateCol], 1, min, na.rm = TRUE)


# for 27 deadwood species habitat
deadwoodCol <- c("HSI_RL_S1", "HSI_RL_S2", "HSI_RL_S3", "HSI_RL_S4", "HSI_RL_S5","HSI_RL_S6", "HSI_RL_S7", "HSI_RL_S8","HSI_RL_S9","HSI_RL_S10",
                 "HSI_RL_S11","HSI_RL_S12", "HSI_RL_S13","HSI_RL_S14","HSI_RL_S15", "HSI_RL_S16", "HSI_RL_S17","HSI_RL_S18","HSI_RL_S19","HSI_RL_S20",
                 "HSI_RL_S21", "HSI_RL_S22","HSI_RL_S23","HSI_RL_S24","HSI_RL_S25","HSI_RL_S26","HSI_RL_S27")

dw2 <- df.opt %>% 
  filter(name %in% c("MAX_MF_0.0")) %>% 
  select(all_of(deadwoodCol), NPV, MF, name, SA_O, INT_O, EXT_O) %>% 
  rename(RES = SA_O, INT = INT_O, EXT = EXT_O) %>% 
  mutate(es = "deadwood")
dw2$MIN <- apply(dw[,deadwoodCol], 1, min, na.rm = TRUE)



# ---------------
# Plot components of Multifunctionality
# when "NPV" is optimized
# ---------------

# # define overall min and max for plot limit (getting same legend scale) --> use different scales for better illustration of patterns
# minComp <- min( min(nw$AVG) , min(dw$MIN), min(vertebrate$MIN), min(carbon$AVG)) 
# maxComp <- max( max(nw$AVG) , max(dw$MIN), max(vertebrate$MIN), max(carbon$AVG)) 


### point of maximize NPV
maxNPV_NPV <- df.plot %>%
  filter(name %in% c("MAX_MF_0.0")) %>%
  filter(NPV == max(NPV))

# nonwood ES
plot.nw2 <- nw2 %>%  ggtern(aes(INT, EXT, RES, value  = AVG)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
    
    #,show.legend = FALSE
    
  ) +
  scale_fill_viridis(name = "value\n(AVG)") + # , limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("a) Nonwood ecosystem services") +
  geom_mask() +
  geom_point(data = maxNPV_NPV %>% rename(AVG = MF), aes(INT, EXT, RES),fill="red", shape=21,size = 5, stroke = 1.5) 
plot.nw2

# climate mitigation
plot.carbon2 <- carbon2 %>%  ggtern(aes(INT, EXT, RES, value  = AVG)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
    
    #,show.legend = FALSE
    
  ) +
  scale_fill_viridis(name = "value\n(AVG)") + # , limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("b) Climate mitigation")+
  geom_mask() +
  geom_point(data = maxNPV_NPV %>% rename(AVG = MF), aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5) 
plot.carbon2


# Vertebrate species
plot.vertebrate2 <- vertebrate2 %>%  ggtern(aes(INT, EXT, RES, value  = MIN)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
    
    #,show.legend = FALSE
    
  ) +
  scale_fill_viridis(name = "value\n(MIN)") + #, limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("c) Vertebrate species habitat") +
  geom_mask() +
  geom_point(data = maxNPV_NPV %>% rename(MIN = MF), aes(INT, EXT, RES),fill="red", shape=21,size = 5, stroke = 1.5)
plot.vertebrate2


# 27 deadwood species
plot.dw2 <- dw2 %>%  ggtern(aes(INT, EXT, RES, value  = MIN)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis(name = "value\n(MIN)") + #, limits = c(minComp,maxComp)
  theme_bvbg() +
  theme_gridsontop() +
  theme_legend_position("topright") +
  theme(tern.axis.arrow = element_line(size = 2))+
  ggtitle("d) 27 deadwood species habitat") +
  geom_mask() +
  geom_point(data = maxNPV_NPV %>% rename(MIN = MF), aes(INT, EXT, RES),fill="red", shape=21, size = 5, stroke = 1.5)
plot.dw2

components3 <- ggtern::grid.arrange(plot.nw2, plot.carbon2, plot.vertebrate2, plot.dw2,  ncol = 4, nrow = 1)
ggsave(plot = components3, paste0(path,"analyse_opt_data/plot_MF_components_underMaxNPV_1.tiff"), width=16, height=5)
ggsave(plot = components3, paste0(path,"analyse_opt_data/plot_MF_components_underMaxNPV_1.pdf"), width=16, height=5)

components4 <- ggtern::grid.arrange(plot.nw2, plot.carbon2 ,plot.vertebrate2, plot.dw2,  ncol = 2, nrow = 2)
ggsave(plot = components4, paste0(path,"analyse_opt_data/plot_MF_components_underMaxNPV_2.tiff"), width=10, height=10) 
ggsave(plot = components4, paste0(path,"analyse_opt_data/plot_MF_components_underMaxNPV_2.pdf"), width=10, height=10) 




################################################################################
################################################################################




# ----------------
# Plot Values for NPV and MF JOINTLY along different weightings for MF
# and highlight the point (red dot) of the maximum values
# ----------------


plot.triangleFct <- function(df, optscenario){
  
  # df = df.plot
  # optscenario = "MAX_MF_0.3"
  
  minValue_NPV <- min(df$NPV)
  maxValue_NPV <- max(df$NPV)
  
  minValue_MF <- min(df$MF)
  maxValue_MF <- max(df$MF)
  
  ### NPV
  maxNPV <- df %>% 
    filter(name %in% optscenario) %>% 
    filter(NPV == max(NPV))
  
  plot.NPV <- df.plot %>% 
    filter(name %in% optscenario) %>% 
    ggtern(aes(INT, EXT, RES, value = NPV)) +
    geom_hex_tern(
      stat = "hex_tern",
      fun = "mean",
      na.rm = TRUE,
      binwidth = 0.1, # depends on your data granularity 
      colour = "grey"
    ) +
    scale_fill_viridis(name = "NPV\n(MEuro)", limits = c( minValue_NPV,maxValue_NPV),
                       option="plasma") +
    theme_bvbg() +
    theme_gridsontop() +
    #ggtitle("Net Present Value (NPV)") + 
    
    geom_mask() +
    geom_point(data = maxNPV, aes(INT, EXT, RES),fill="red", shape=21, size = 5) 
  plot.NPV
  
  ### MF
  maxMF <- df.plot %>% 
    filter(name %in% optscenario) %>% 
    filter(MF == max(MF))
  
  plot.MF <- df.plot %>% 
    filter(name %in% optscenario) %>% 
    ggtern(aes(INT, EXT, RES, value = MF)) +
    geom_hex_tern(
      stat = "hex_tern",
      fun = "mean",
      na.rm = TRUE,
      binwidth = 0.1, # depends on your data granularity 
      colour = "grey"
    ) +
    scale_fill_viridis(name = "MF\n(index)", limits = c(minValue_MF,maxValue_MF)) +
    theme_bvbg() +
    theme_gridsontop() +
    #ggtitle("Multifunctionality (MF)") + 
    
    geom_mask() +
    geom_point(data = maxMF, aes(INT, EXT, RES),fill="red", shape=21, size = 5) 
  plot.MF
  
  plot.both <- ggtern::grid.arrange(plot.NPV, plot.MF, ncol = 2, nrow = 1)
  
  return(plot.both)
}



#ls.optscenario <- c("MAX_MF_0.0", "MAX_MF_0.1", "MAX_MF_0.2", "MAX_MF_0.3", "MAX_MF_0.4", "MAX_MF_0.5", "MAX_MF_0.6", 
#                    "MAX_MF_0.7", "MAX_MF_0.8", "MAX_MF_0.9", "MAX_MF_1.0" )

ls.optscenario <- c("MAX_MF_0.0", "MAX_MF_0.3", "MAX_MF_0.7","MAX_MF_1.0" )


for( i in ls.optscenario) {

  # i = ls.optscenario[1]

  plot <- plot.triangleFct(df.plot, i )
  plot <- annotate_figure(plot, top = text_grob(paste0("Optimization scenario: ,",i), face = "bold", size = 12))
  ggsave(plot = plot, paste0(path,"analyse_opt_data/plot_",i,".tiff"), width=12, height=6)

}
  

# plot.1 <- plot.triangleFct(df.plot, "MAX_MF_1.0")
# plot.1 <- annotate_figure(plot.1,left = text_grob(paste0("MAX_MF_1"), rot = 90, face = "bold", size = 12))
# ggsave(plot = plot.1, paste0(path,"analyse_opt_data/plot_MAX_MF_1.tiff"), width=12, height=6)
 
# plot.0.8 <- plot.triangleFct(df.plot, "MAX_MF_0.8")
# plot.0.8 <- annotate_figure(plot.0.8, top = text_grob(paste0("Optimization scenario: MAX_MF_0.8"), face = "bold", size = 12))
# ggsave(plot = plot.0.8, paste0(path,"analyse_opt_data/plot_MAX_MF_0.8.tiff"), width=12, height=6)
# 
# plot.0.6 <- plot.triangleFct(df.plot, "MAX_MF_0.6")
# plot.0.6 <- annotate_figure(plot.0.6, top = text_grob(paste0("Optimization scenario: MAX_MF_0.6"), face = "bold", size = 12))
# ggsave(plot = plot.0.6, paste0(path,"analyse_opt_data/plot_MAX_MF_0.6.tiff"), width=12, height=6)
# 
# plot.0.4 <- plot.triangleFct(df.plot, "MAX_MF_0.4")
# plot.0.4 <- annotate_figure(plot.0.4, top = text_grob(paste0("Optimization scenario: MAX_MF_0.4"), face = "bold", size = 12))
# ggsave(plot = plot.0.4, paste0(path,"analyse_opt_data/plot_MAX_MF_0.4.tiff"), width=12, height=6)
# 
# plot.0.2 <- plot.triangleFct(df.plot, "MAX_MF_0.2")
# plot.0.2 <- annotate_figure(plot.0.2, top = text_grob(paste0("Optimization scenario: MAX_MF_0.2"), face = "bold", size = 12))
# ggsave(plot = plot.0.2, paste0(path,"analyse_opt_data/plot_MAX_MF_0.2.tiff"), width=12, height=6)
# 
# plot.0 <- plot.triangleFct(df.plot, "MAX_MF_0.0")
# plot.0 <- annotate_figure(plot.0, top = text_grob(paste0("Optimization scenario: MAX_MF_0"), face = "bold", size = 12))
# ggsave(plot = plot.0, paste0(path,"analyse_opt_data/plot_MAX_MF_0.tiff"), width=12, height=6)




################################################################################
################################################################################




### Two separate plot functions for the Triangle of MF and NPV

# # function for NPV triangle
# 
# plot.triangleFctNPV <- function(df, optscenario){
#   
#   # df = df.plot
#   # optscenario = "MAX_MF_0.3"
#   
#   minValue_NPV <- min(df$NPV)
#   maxValue_NPV <- max(df$NPV)
#   
#   ### NPV
#   maxNPV <- df %>% 
#     filter(name %in% optscenario) %>% 
#     filter(NPV == max(NPV))
#   
#   plot <- df.plot %>%
#     filter(name %in% optscenario) %>%
#     ggtern(aes(x=INT, y=EXT, z=RES, value = NPV)) +
#     geom_hex_tern(
#       stat = "hex_tern",
#       fun = "mean",
#       na.rm = TRUE,
#       binwidth = 0.1, # depends on your data granularity
#       colour = "grey"
#       #,show.legend = FALSE
#     ) +
#     scale_fill_viridis(name = "NPV\n(MEuro)", limits = c( minValue_NPV,maxValue_NPV),
#                        option="plasma") +
#     theme_bvbg() +
#     theme_gridsontop() +
#     #ggtitle(optscenario) + 
#     
#     geom_mask() +
#     geom_point(data = maxNPV, aes(INT, EXT, RES),fill="red", shape=21, size = 4)
#   
#   if(optscenario == "MAX_MF_1.0"){
#     
#     plot <- plot + 
#       theme_legend_position("topright")  
#     
#     
#   } 
#   
#   return(plot)
#   
# }
# 
# 
# 
# # function for MF triangle
# 
# plot.triangleFctMF <- function(df, optscenario){
#   
#   # df = df.plot
#   # optscenario = "MAX_MF_0.3"
#   
#   minValue_MF <- min(df$MF)
#   maxValue_MF <- max(df$MF)
#   
#   ### NPV
#   maxMF <- df %>% 
#     filter(name %in% optscenario) %>% 
#     filter(MF == max(MF))
#   
#   plot <- df.plot %>% 
#     filter(name %in% optscenario) %>% 
#     ggtern(aes(x=INT, y=EXT, z=RES, value = MF)) +
#     geom_hex_tern(
#       stat = "hex_tern",
#       fun = "mean",
#       na.rm = TRUE,
#       binwidth = 0.1, # depends on your data granularity 
#       colour = "grey"
#       ,show.legend = FALSE
#     ) +
#     scale_fill_viridis(name = "MF\n(index)", limits = c(minValue_MF,maxValue_MF)) +
#     theme_bvbg() +
#     theme_gridsontop() +
#     #ggtitle(optscenario) + 
#     
#     geom_mask() +
#     #theme_legend_position("topright") +
#     geom_point(data = maxMF, aes(INT, EXT, RES),fill="red", shape=21, size = 4) 
#   
#   if(optscenario == "MAX_MF_1.0"){
#     
#     plot <- plot +
#       theme_legend_position("topright")
#     
#   } 
#  
#   return(plot)
# }


# Function for NPV
plot.triangleFctNPV <- function(df, optscenario){
  
  # df = df.plot
  # optscenario = "MAX_MF_0.3"
  
  minValue_NPV <- min(df$NPV)
  maxValue_NPV <- max(df$NPV)
  
  ### NPV
  maxNPV <- df %>% 
    filter(name %in% optscenario) %>% 
    filter(NPV == max(NPV))
  
  if(optscenario == "MAX_MF_1.0"){
    
    plot <- df.plot %>%
      filter(name %in% optscenario) %>%
      ggtern(aes(x=INT, y=EXT, z=RES, value = NPV)) +
      geom_hex_tern(
        stat = "hex_tern",
        fun = "mean",
        na.rm = TRUE,
        binwidth = 0.1, # depends on your data granularity
        colour = "grey"
        #,show.legend = FALSE
      ) +
      scale_fill_viridis(name = "NPV\n(MEuro)", limits = c( minValue_NPV,maxValue_NPV),
                         option="plasma") +
      theme_bvbg() +
      theme_gridsontop() +
      #ggtitle(optscenario) + 
      
      geom_mask() +
      theme_legend_position("topright") +
      geom_point(data = maxNPV, aes(INT, EXT, RES),fill="red", shape=21, size = 4)
    
  } else {
    
    plot <- df.plot %>% 
      filter(name %in% optscenario) %>% 
      ggtern(aes(x=INT, y=EXT, z=RES, value = NPV)) +
      geom_hex_tern(
        stat = "hex_tern",
        fun = "mean",
        na.rm = TRUE,
        binwidth = 0.1, # depends on your data granularity 
        colour = "grey"
        ,show.legend = FALSE
      ) +
      scale_fill_viridis(name = "NPV\n(MEuro)", limits = c( minValue_NPV,maxValue_NPV),
                         option="plasma") +
      theme_bvbg() +
      theme_gridsontop() +
      #ggtitle(optscenario) + 
      
      geom_mask() +
      #theme_legend_position("topright") +
      geom_point(data = maxNPV, aes(INT, EXT, RES),fill="red", shape=21, size = 4) 
    
    
  }  
  
  return(plot)
  
}

# Function for MF
plot.triangleFctMF <- function(df, optscenario){
  
  # df = df.plot
  # optscenario = "MAX_MF_0.3"
  
  minValue_MF <- min(df$MF)
  maxValue_MF <- max(df$MF)
  
  ### NPV
  maxMF <- df %>% 
    filter(name %in% optscenario) %>% 
    filter(MF == max(MF))
  
  if(optscenario == "MAX_MF_1.0"){
    
    plot <- df.plot %>%
      filter(name %in% optscenario) %>%
      ggtern(aes(x=INT, y=EXT, z=RES, value = MF)) +
      geom_hex_tern(
        stat = "hex_tern",
        fun = "mean",
        na.rm = TRUE,
        binwidth = 0.1, # depends on your data granularity
        colour = "grey"
        #,show.legend = FALSE
      ) +
      scale_fill_viridis(name = "MF\n(index)", limits = c(minValue_MF,maxValue_MF)) +
      theme_bvbg() +
      theme_gridsontop() +
      #ggtitle(optscenario) + 
      
      geom_mask() +
      theme_legend_position("topright") +
      geom_point(data = maxMF, aes(INT, EXT, RES),fill="red", shape=21, size = 4)
    
  } else {
    
    plot <- df.plot %>% 
      filter(name %in% optscenario) %>% 
      ggtern(aes(x=INT, y=EXT, z=RES, value = MF)) +
      geom_hex_tern(
        stat = "hex_tern",
        fun = "mean",
        na.rm = TRUE,
        binwidth = 0.1, # depends on your data granularity 
        colour = "grey"
        ,show.legend = FALSE
      ) +
      scale_fill_viridis(name = "MF\n(index)", limits = c(minValue_MF,maxValue_MF)) +
      theme_bvbg() +
      theme_gridsontop() +
      #ggtitle(optscenario) + 
      
      geom_mask() +
      #theme_legend_position("topright") +
      geom_point(data = maxMF, aes(INT, EXT, RES),fill="red", shape=21, size = 4) 
    
  }  
  
  return(plot)
  
}



plot.1npv <- plot.triangleFctNPV(df.plot, "MAX_MF_1.0")
plot.03npv <- plot.triangleFctNPV(df.plot, "MAX_MF_0.3")
plot.06npv <- plot.triangleFctNPV(df.plot, "MAX_MF_0.6")
plot.00npv <- plot.triangleFctNPV(df.plot, "MAX_MF_0.0")


plot.1mf <- plot.triangleFctMF(df.plot, "MAX_MF_1.0")
plot.03mf <- plot.triangleFctMF(df.plot, "MAX_MF_0.3")
plot.06mf <- plot.triangleFctMF(df.plot, "MAX_MF_0.6")
plot.00mf <- plot.triangleFctMF(df.plot, "MAX_MF_0.0")

plot.1 <- ggtern::grid.arrange(plot.1npv, plot.1mf, ncol = 2, nrow = 1)
plot.1 <- annotate_figure(plot.1,left = text_grob(paste0("MAX_MF_1.0"), rot = 90, face = "bold", size = 12))

plot.03 <- ggtern::grid.arrange(plot.03npv, plot.03mf, ncol = 2, nrow = 1)
plot.03 <- annotate_figure(plot.03,left = text_grob(paste0("MAX_MF_0.3"), rot = 90, face = "bold", size = 12))

plot.06 <- ggtern::grid.arrange(plot.06npv, plot.06mf, ncol = 2, nrow = 1)
plot.06 <- annotate_figure(plot.06,left = text_grob(paste0("MAX_MF_0.6"), rot = 90, face = "bold", size = 12))

plot.00 <- ggtern::grid.arrange(plot.00npv, plot.00mf, ncol = 2, nrow = 1)
plot.00 <- annotate_figure(plot.00,left = text_grob(paste0("MAX_MF_0.0"), rot = 90, face = "bold", size = 12))


plot.all <- ggtern::grid.arrange(plot.1,  plot.06, plot.03, plot.00, ncol = 1, nrow = 4)
ggsave(plot = plot.all, paste0(path,"analyse_opt_data/plot_triangle_all.tiff"), width=8, height=14)
ggsave(plot = plot.all, paste0(path,"analyse_opt_data/plot_triangle_all.pdf"), width=8, height=14)

plot.all <- ggtern::grid.arrange(plot.1, plot.03,
                                 plot.06, plot.00, ncol = 2, nrow = 2)
ggsave(plot = plot.all, paste0(path,"analyse_opt_data/plot_triangle_all_2.tiff"), width=16, height=8)
ggsave(plot = plot.all, paste0(path,"analyse_opt_data/plot_triangle_all_2.pdf"), width=16, height=8)

#rm(list = ls(pattern = "plot"))
rm(list = ls(pattern = "max" ))
rm(list = ls(pattern = "min" ))





###################
















