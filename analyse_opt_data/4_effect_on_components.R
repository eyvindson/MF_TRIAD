####
#
# Effect on components
# 2022-03-03
#
####


library(dplyr)
library(tidyr)
library(ggplot2)



head(df.opt)




##################################################################################
##################################################################################

# effect on Indicators (normalized) at position were weight 1 of MF & NPV is highest 
# Fix position over weighting gradient - USED IN PUBLICATION


# round values -> otherwise no match when filtering (slight numarical changes after the comma) 
df.opt2 <- df.opt %>% 
  mutate_at( c("SA_O", "INT_O", "EXT_O"), ~round(.x , digits = 1)) 

# point of maximum Multifunctionality  
max_mf_pt <- df.opt2 %>% 
  select(NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
  filter(name %in% "MAX_MF_1.0") %>% 
  filter(MF == max(MF)) 

# point of maximum NPV
max_npv_pt <- df.opt2 %>% 
  select(NPV, MF, SA_O, INT_O, EXT_O, name) %>% 
  filter(name %in% "MAX_MF_0.0") %>% 
  filter(NPV == max(NPV)) 



## values of capercaillie and flying squirrel are identical at management shares where MF is maximum
df.opt2 %>% select(SA_O, INT_O, EXT_O, name, CAPERCAILLIE, SIBERIAN_FLYING_SQUIRREL) %>%
  filter(SA_O %in% 0.3 & INT_O %in% 0.2 & EXT_O %in% 0.5)







# list of all opt scenarios with different weights
ls.optscenario <- c("MAX_MF_0.0", "MAX_MF_0.1", "MAX_MF_0.2", "MAX_MF_0.3", "MAX_MF_0.4", "MAX_MF_0.5", "MAX_MF_0.6",
                    "MAX_MF_0.7", "MAX_MF_0.8", "MAX_MF_0.9", "MAX_MF_1.0" )



# -----------
# Non-wood ecosystems multi-functionality
# -----------

nonwood <- c("BILBERRY", "ALL_MARKETED_MUSHROOMS", "scenic")

nonwood.t <- NULL

for(i in ls.optscenario) {
  
  #i = ls.optscenario[1]
  
  df.mf <- df.opt2 %>% 
    select( NPV, MF, name, SA_O, INT_O, EXT_O, all_of(nonwood)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_mf_pt[,"SA_O"] & 
              INT_O %in%  max_mf_pt[,"INT_O"] & 
              EXT_O %in% max_mf_pt[,"EXT_O"]) %>% 
    mutate(AVG = mean(c_across(nonwood), na.rm = TRUE)) %>% 
    tidyr::gather("indicator", "value", 7:(7+length(nonwood)) ) %>% 
    mutate(name_p = "Optimized Triad zoning for MF")
  
  df.npv <- df.opt2 %>% 
    select(NPV, MF, name, SA_O, INT_O, EXT_O, all_of(nonwood)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_npv_pt[,"SA_O"] & 
              INT_O %in%  max_npv_pt[,"INT_O"] & 
              EXT_O %in% max_npv_pt[,"EXT_O"]) %>%
    mutate(AVG = mean(c_across(nonwood), na.rm = TRUE)) %>%
    tidyr::gather("indicator", "value", 7:(7+length(nonwood))  ) %>% 
    mutate(name_p = "Optimized Triad zoning for NPV")
  
  nonwood.t <- rbind(nonwood.t, df.mf, df.npv)
  
}

nonwood.t <- nonwood.t %>% mutate(component = "nonwood")




# -----------
# Climate mitigation multifunctionality
# -----------

carbon <- c("CARBON_SOIL_Update", "BM_total")

carbon.t <- NULL

for(i in ls.optscenario) {
  
  #i = ls.optscenario[1]
  
  df.mf <- df.opt2 %>% 
    select( NPV, MF, name, SA_O, INT_O, EXT_O, all_of(carbon)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_mf_pt[,"SA_O"] & 
              INT_O %in%  max_mf_pt[,"INT_O"] & 
              EXT_O %in% max_mf_pt[,"EXT_O"]) %>% 
    mutate(AVG = mean(c_across(carbon), na.rm = TRUE)) %>% 
    tidyr::gather("indicator", "value", 7:(7+length(carbon)) ) %>% 
    mutate(name_p = "Optimized Triad zoning for MF")
  
  df.npv <- df.opt2 %>% 
    select( NPV, MF, name, SA_O, INT_O, EXT_O, all_of(carbon)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_npv_pt[,"SA_O"] & 
              INT_O %in%  max_npv_pt[,"INT_O"] & 
              EXT_O %in% max_npv_pt[,"EXT_O"]) %>%
    mutate(AVG = mean(c_across(carbon), na.rm = TRUE)) %>% 
    tidyr::gather("indicator", "value", 7:(7+length(carbon)) ) %>% 
    mutate(name_p = "Optimized Triad zoning for NPV")
  
  carbon.t <- rbind(carbon.t, df.mf, df.npv)
  
}

carbon.t <- carbon.t %>% mutate(component = "carbon")




# -----------
# Vertebrate multifunctionality
# -----------

vertebrate <- c("LESSER_SPOTTED_WOODPECKER", "THREE_TOED_WOODPECKER", "SIBERIAN_FLYING_SQUIRREL", "LONG_TAILED_TIT", 
                "CAPERCAILLIE", "HAZEL_GROUSE")

vertebrate.t <- NULL

for(i in ls.optscenario) {
  
  #i = ls.optscenario[1]
  
  df.mf <- df.opt2 %>% 
    select( NPV, MF, name, SA_O, INT_O, EXT_O, all_of(vertebrate)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_mf_pt[,"SA_O"] & 
              INT_O %in%  max_mf_pt[,"INT_O"] & 
              EXT_O %in% max_mf_pt[,"EXT_O"]) %>% 
    mutate(MIN = min(c_across(vertebrate), na.rm = TRUE)) %>% 
    tidyr::gather("indicator", "value", 7:(7+length(vertebrate)) ) %>% 
    mutate(name_p = "Optimized Triad zoning for MF")
  
  df.npv <- df.opt2 %>% 
    select( NPV, MF, name, SA_O, INT_O, EXT_O, all_of(vertebrate)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_npv_pt[,"SA_O"] & 
              INT_O %in%  max_npv_pt[,"INT_O"] & 
              EXT_O %in% max_npv_pt[,"EXT_O"]) %>%
    mutate(MIN = min(c_across(vertebrate), na.rm = TRUE)) %>% 
    tidyr::gather("indicator", "value", 7:(7+length(vertebrate)) ) %>% 
    mutate(name_p = "Optimized Triad zoning for NPV")
  
  vertebrate.t <- rbind(vertebrate.t, df.mf, df.npv)
  
}

vertebrate.t <- vertebrate.t %>% mutate(component = "vertebrate")



# -----------
# Deadwood multi-functionality
# -----------

deadwood <- c("HSI_RL_S1", "HSI_RL_S2", "HSI_RL_S3", "HSI_RL_S4", "HSI_RL_S5","HSI_RL_S6", "HSI_RL_S7", "HSI_RL_S8","HSI_RL_S9","HSI_RL_S10",
              "HSI_RL_S11","HSI_RL_S12", "HSI_RL_S13","HSI_RL_S14","HSI_RL_S15", "HSI_RL_S16", "HSI_RL_S17","HSI_RL_S18","HSI_RL_S19","HSI_RL_S20",
              "HSI_RL_S21", "HSI_RL_S22","HSI_RL_S23","HSI_RL_S24","HSI_RL_S25","HSI_RL_S26","HSI_RL_S27")

deadwood.t <- NULL

for(i in ls.optscenario) {
  
  #i = ls.optscenario[1]
  
  df.mf <- df.opt2 %>% 
    select( NPV, MF, name, SA_O, INT_O, EXT_O, all_of(deadwood)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_mf_pt[,"SA_O"] & 
              INT_O %in%  max_mf_pt[,"INT_O"] & 
              EXT_O %in% max_mf_pt[,"EXT_O"]) %>% 
    mutate(MIN = min(c_across(deadwood), na.rm = TRUE)) %>% 
    tidyr::gather("indicator", "value", 7:(7+length(deadwood)) ) %>% 
    mutate(name_p = "Optimized Triad zoning for MF")
  
  df.npv <- df.opt2 %>% 
    select( NPV, MF, name, SA_O, INT_O, EXT_O, all_of(deadwood)) %>% 
    filter(name %in% i) %>% 
    filter( SA_O %in% max_npv_pt[,"SA_O"] & 
              INT_O %in%  max_npv_pt[,"INT_O"] & 
              EXT_O %in% max_npv_pt[,"EXT_O"]) %>%
    mutate(MIN = min(c_across(deadwood), na.rm = TRUE)) %>% 
    tidyr::gather("indicator", "value", 7:(7+length(deadwood)) ) %>% 
    mutate(name_p = "Optimized Triad zoning for NPV")
  
  deadwood.t <- rbind(deadwood.t, df.mf, df.npv)
  
}

deadwood.t <- deadwood.t %>% mutate(component = "deadwood")



# ------------
# Combine them
# ------------

df.mfcomp <- rbind(nonwood.t, vertebrate.t, deadwood.t, carbon.t) # , vertebrate.t, deadwood.t, carbon.t

head(df.mfcomp)


unique(df.mfcomp$indicator)

df.mfcomp[df.mfcomp$indicator %in% "BILBERRY",]$indicator <- "Bilberry"
df.mfcomp[df.mfcomp$indicator %in% "ALL_MARKETED_MUSHROOMS",]$indicator <- "Mushrooms"
df.mfcomp[df.mfcomp$indicator %in% "scenic",]$indicator <- "Scenic"

df.mfcomp[df.mfcomp$indicator %in% "LESSER_SPOTTED_WOODPECKER",]$indicator <- "Lesser spotted WP"
df.mfcomp[df.mfcomp$indicator %in% "THREE_TOED_WOODPECKER",]$indicator <- "Three Toed WP"
df.mfcomp[df.mfcomp$indicator %in% "SIBERIAN_FLYING_SQUIRREL",]$indicator <- "Flying Squirrel"
df.mfcomp[df.mfcomp$indicator %in% "LONG_TAILED_TIT",]$indicator <- "Long tailed tit"
df.mfcomp[df.mfcomp$indicator %in% "CAPERCAILLIE",]$indicator <- "Capercaillie"
df.mfcomp[df.mfcomp$indicator %in% "HAZEL_GROUSE",]$indicator <- "Hazel grouse"

df.mfcomp[df.mfcomp$indicator %in% "CARBON_SOIL_Update" ,]$indicator <- "Carbon soil & DW"
df.mfcomp[df.mfcomp$indicator %in% "BM_total",]$indicator <- "Carbon timber"






plotFunctionComp <- function( MFcomponent ) {
  
  #MFcomponent <- "vertebrate"
  
  if (MFcomponent == "nonwood"){
    TITLE <- "a) Nonwood ecosystem services"
  } else if (MFcomponent == "vertebrate"){
    TITLE <- "d) Vertebrate species habitat"
  } else if (MFcomponent == "deadwood" ) {
    TITLE <- "c) 27 deadwood species habitat"
  } else if (MFcomponent == "carbon" ) {
    TITLE <- "b) Climate change mitigation"
  }
    
  df <- df.mfcomp %>%
    filter(component %in% MFcomponent ) %>% 
    separate(name, c("MAX", "MF", "weight"), sep = "_") %>% 
    mutate( weight = as.numeric(weight)) #%>% 
  
  df2 <- df %>%  filter(indicator %in% c("MIN", "AVG"))
  
  plot <- df %>% 
    filter(!indicator %in% c("MIN", "AVG")) %>% 
    ggplot(aes(weight, value, color= factor(indicator),group=indicator)) +
    geom_line(alpha=.5, size = 1) + #
    
    geom_line(data = df2, aes(x= weight, y = value) , color = "black", lty = "dashed") +
    
    theme_bw() +
    #scale_color_brewer(palette="Dark2") +
    facet_grid(.~name_p) +
    scale_x_continuous(breaks=c(seq(0,1, by = 0.1) ))   +
    # ylab("normalized achievement") +
    # xlab("MF weight") +
    labs(linetype ="Point",col="Indicator") +
    expand_limits(y = c(0, 1))
    
  
    if(MFcomponent == "nonwood") {
      plot <- plot  +
        theme(axis.text.x = element_text(angle = 90,vjust = 0.5, hjust=1),
              axis.title.x=element_blank(),
              #panel.border = element_blank(), axis.line = element_line(color = "grey"),axis.ticks = element_line(color = "grey"),
              panel.grid = element_blank(),
              legend.position = "bottom") +
        ylab("normalized achievement") 
      
    } else if (MFcomponent == "carbon"){
      plot <- plot  +
        theme(axis.text.x = element_text(angle = 90,vjust = 0.5, hjust=1),
              axis.title.x=element_blank(),
              axis.title.y=element_blank(),
              #panel.border = element_blank(), axis.line = element_line(color = "grey"),axis.ticks = element_line(color = "grey"),
              panel.grid = element_blank(),
              legend.position = "bottom") 
       
    } else if (MFcomponent == "vertebrate"){
      plot <- plot  +
        theme(axis.text.x = element_text(angle = 90,vjust = 0.5, hjust=1),
              #axis.title.x=element_blank(),
              #panel.border = element_blank(), axis.line = element_line(color = "grey"),axis.ticks = element_line(color = "grey"),
              panel.grid = element_blank(),
              legend.position = "bottom") +
        ylab("normalized achievement") +
        xlab("weight for Multifunctionality (MF)") 
      
    } else if (MFcomponent == "deadwood") {
      
      plot <- plot  +
        theme(axis.text.x = element_text(angle = 90,vjust = 0.5, hjust=1),
              axis.title.y=element_blank(),
              #panel.border = element_blank(), axis.line = element_line(color = "grey"),axis.ticks = element_line(color = "grey"),
              panel.grid = element_blank(),
              legend.position = "none") +
        # ylab("normalized achievement") +
        xlab("weight for Multifunctionality (MF)")
      
    }
  
  # if(MFcomponent == "deadwood") {
  #   plot <- plot  +  
  #     theme(axis.text.x = element_text(angle = 90,vjust = 0.5, hjust=1),
  #           axis.title.x=element_blank(),
  #           #panel.border = element_blank(), axis.line = element_line(color = "grey"),axis.ticks = element_line(color = "grey"),
  #           panel.grid = element_blank(),
  #           legend.position = "none") 
  # } else {
  #   
  #   plot <- plot  +  
  #     theme(axis.text.x = element_text(angle = 90,vjust = 0.5, hjust=1),
  #           #axis.title.x=element_blank(),
  #           #panel.border = element_blank(), axis.line = element_line(color = "grey"),axis.ticks = element_line(color = "grey"),
  #           panel.grid = element_blank(),
  #           legend.position = "bottom")
  #   
  # }
  
  
  plot <- plot + ggtitle(TITLE)
  plot
  
  return(plot)
  
}


plot.vertebrate <- plotFunctionComp(MFcomponent = "vertebrate")
#ggsave(plot = plot.vertebrate, paste0(path,"cb/plot.vertebrate.jpeg"), width=8, height=6)

plot.carbon <- plotFunctionComp(MFcomponent = "carbon")

plot.nonwood <- plotFunctionComp(MFcomponent = "nonwood")
#ggsave(plot = plot.nonwood, paste0(path,"cb/plot.nonwood.jpeg"), width=8, height=6)

plot.deadwood <- plotFunctionComp(MFcomponent = "deadwood")
#ggsave(plot = plot.deadwood, paste0(path,"cb/plot.deadwood.jpeg"), width=8, height=6)


#
plot.combined1 <- egg::ggarrange(plot.nonwood, plot.carbon,
                                 plot.vertebrate ,  plot.deadwood, 
                                    nrow = 2, ncol=2)
ggsave(plot = plot.combined1, paste0(path,"analyse_opt_data/plot.components.jpeg"), width=10, height=7)
ggsave(plot = plot.combined1, paste0(path,"analyse_opt_data/plot.components.pdf"), width=10, height=7)



### get values shwon in manuscript
getval <- df.mfcomp %>%
  # filter(component %in% MFcomponent ) %>% 
  separate(name, c("MAX", "MF", "weight"), sep = "_") %>% 
  mutate( weight = as.numeric(weight)) %>% 
  filter(indicator %in% c("MIN", "AVG")) %>% 
  filter(weight %in% 0.0 | weight %in% 1.0) %>% 
  arrange(name_p) %>% 
  select(name_p, component, weight, indicator, value)










##########################################################################################
##########################################################################################





# # effect on Indicators (normalized) at varying max values over weighting gradient
# # Position is not fixed  - NOT USED FOR PUBLICATION
# 
# 
# ls.optscenario <- c("MAX_MF_0", "MAX_MF_0.1", "MAX_MF_0.2", "MAX_MF_0.3", "MAX_MF_0.4", "MAX_MF_0.5", "MAX_MF_0.6",
#                     "MAX_MF_0.7", "MAX_MF_0.8", "MAX_MF_0.9", "MAX_MF_1" )
# 
# # -----------
# # Nonwood ecosystems multifunctionality
# # -----------
# 
# nonwood <- c("BILBERRY", "ALL_MARKETED_MUSHROOMS")
# 
# nonwood.t <- NULL
# 
# for(i in ls.optscenario) {
#   
#   #i = ls.optscenario[1]
#   
#   df.mf <- df.opt %>% 
#     select(nonwood, NPV, MF, name, SA_O, INT_O, EXT_O,) %>% 
#     filter(name %in% i) %>% 
#     filter(MF == max(MF)) %>% 
#     tidyr::gather("indicator", "value", 1:length(nonwood)) %>% 
#     mutate(name_p = "max_MF")
#   
#   df.npv <- df.opt %>% 
#     select(nonwood, NPV, MF, name, SA_O, INT_O, EXT_O,) %>% 
#     filter(name %in% i) %>% 
#     filter(NPV == max(NPV)) %>% 
#     tidyr::gather("indicator", "value", 1:length(nonwood)) %>% 
#     mutate(name_p = "max_NPV")
#   
#   nonwood.t <- rbind(nonwood.t, df.mf, df.npv)
#   
# }
# nonwood.t <- nonwood.t %>% mutate(component = "nonwood")
# 
# 
# # -----------
# # vertebrate multifunctionality
# # -----------
# 
# vertebrate <- c("LESSER_SPOTTED_WOODPECKER", "THREE_TOED_WOODPECKER", "SIBERIAN_FLYING_SQUIRREL", "LONG_TAILED_TIT", 
#                 "CAPERCAILLIE", "HAZEL_GROUSE")
# 
# vertebrate.t <- NULL
# 
# for(i in ls.optscenario) {
#   
#   #i = ls.optscenario[1]
#   
#   df.mf <- df.opt %>% 
#     select(all_of(vertebrate), NPV, MF, name, SA_O, INT_O, EXT_O,) %>% 
#     filter(name %in% i) %>% 
#     filter(MF == max(MF)) %>% 
#     tidyr::gather("indicator", "value", 1:length(vertebrate)) %>% 
#     mutate(name_p = "max_MF")
#   
#   df.npv <- df.opt %>% 
#     select(all_of(vertebrate), NPV, MF, name, SA_O, INT_O, EXT_O,) %>% 
#     filter(name %in% i) %>% 
#     filter(NPV == max(NPV)) %>% 
#     tidyr::gather("indicator", "value", 1:length(vertebrate)) %>% 
#     mutate(name_p = "max_NPV")
#   
#   vertebrate.t <- rbind(vertebrate.t, df.mf, df.npv) 
#   
# }
# vertebrate.t <- vertebrate.t %>% mutate(component = "vertebrate")
# 
# 
# # -----------
# # Deadwood habitat multifuntionality
# # -----------
# 
# names(df.opt)
# 
# 
# deadwood <- c("HSI_RL_S1", "HSI_RL_S2", "HSI_RL_S3", "HSI_RL_S4", "HSI_RL_S5","HSI_RL_S6", "HSI_RL_S7", "HSI_RL_S8","HSI_RL_S9","HSI_RL_S10",
#               "HSI_RL_S11","HSI_RL_S12", "HSI_RL_S13","HSI_RL_S14","HSI_RL_S15", "HSI_RL_S16", "HSI_RL_S17","HSI_RL_S18","HSI_RL_S19","HSI_RL_S20",
#               "HSI_RL_S21", "HSI_RL_S22","HSI_RL_S23","HSI_RL_S24","HSI_RL_S25","HSI_RL_S26","HSI_RL_S27")
# 
# deadwood.t <- NULL
# 
# for(i in ls.optscenario) {
#   
#   #i = ls.optscenario[1]
#   
#   df.mf <- df.opt %>% 
#     select(all_of(deadwood), NPV, MF, name, SA_O, INT_O, EXT_O,) %>% 
#     filter(name %in% i) %>% 
#     filter(MF == max(MF)) %>% 
#     tidyr::gather("indicator", "value", 1:length(deadwood)) %>% 
#     mutate(name_p = "max_MF")
#   
#   df.npv <- df.opt %>% 
#     select(all_of(deadwood), NPV, MF, name, SA_O, INT_O, EXT_O,) %>% 
#     filter(name %in% i) %>% 
#     filter(NPV == max(NPV)) %>% 
#     tidyr::gather("indicator", "value", 1:length(deadwood)) %>% 
#     mutate(name_p = "max_NPV")
#   
#   deadwood.t <- rbind(deadwood.t, df.mf, df.npv)
#   
# }
# deadwood.t <- deadwood.t %>% mutate(component = "deadwood")
# 
# 
# 
# # ------------
# # Combine them
# # ------------
# 
# df.mfcomp <- rbind(deadwood.t, nonwood.t, vertebrate.t)
# 
# head(df.mfcomp)
# 
# 
# plotFunctionComp <- function( MFcomponent ) {
#   
#   # MFcomponent <- "vertebrate"
#   
#   plot <- df.mfcomp %>%
#     filter(component %in% MFcomponent ) %>% 
#     separate(name, c("MAX", "MF", "weight"), sep = "_") %>% 
#     mutate( weight = as.numeric(weight)) %>% 
#     
#     ggplot(aes(weight, value)) +
#     
#     geom_line(aes(color = indicator, linetype = name_p)) +
#     theme_minimal() +
#     theme(axis.text.x = element_text(angle = 90,vjust = 0.5, hjust=1),
#           #axis.title.x=element_blank(),
#           panel.border = element_blank(), axis.line = element_line(color = "grey"),axis.ticks = element_line(color = "grey"),
#           panel.grid = element_blank(),
#           legend.position = "right"
#     ) +
#     #scale_color_brewer(palette="Dark2") +
#     scale_x_continuous(breaks=c(seq(0,1, by = 0.1) )) +
#     ylab("normalized achievement") +
#     xlab("MF weight") +
#     labs(linetype ="Point",col="Indicator") +
#     expand_limits(y = c(0, 1)) 
#   
#   return(plot)
#   
# }
# 
# 
# plot.vertebrate <- plotFunctionComp(MFcomponent = "vertebrate")
# ggsave(plot = plot.vertebrate, paste0(path,"cb/plot.vertebrate.jpeg"), width=8, height=6)
# 
# plot.nonwood <- plotFunctionComp(MFcomponent = "nonwood")
# ggsave(plot = plot.nonwood, paste0(path,"cb/plot.nonwood.jpeg"), width=8, height=6)
# 
# plot.deadwood <- plotFunctionComp(MFcomponent = "deadwood")
# ggsave(plot = plot.deadwood, paste0(path,"cb/plot.deadwood.jpeg"), width=8, height=6)
# 
# 
# # plot.combined1 <- ggpubr::ggarrange(plot.vertebrate , plot.nonwood, plot.deadwood,
# #                                     nrow = 1, ncol=3)






