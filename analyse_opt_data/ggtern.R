#####
#
# First try to plot the triangle MF data from Kyle
#
# 15.09.2021
#
#####



#library(tidyverse)
library(ggtern)
library(viridis)






### Set the working path to this R-project
path <- paste0(getwd(),"/")

inputpath <- paste0(path,"input_data/")



### read example data

maxnpv <- read_csv(paste0(inputpath,"MAX_NPV.csv")) %>% 
  select(NPV, MF, SA, INT, EXT) %>% 
  mutate_at(c("SA","INT", "EXT"), round, 1) %>% 
  mutate(opt = "maxnpv")

maxmf <- read_csv(paste0(inputpath,"MAX_MF.csv")) %>% 
  select(NPV, MF, SA, INT, EXT) %>% 
  mutate_at(c("SA","INT", "EXT"), round, 1) %>% 
  mutate(opt = "maxmf")

df.max <- rbind(maxnpv, maxmf)



# -----------
# with test data from Kyle
# -----------

# -----------
# values for multifunctionality
# -----------

max <- max(df.max$MF)
min <- min(df.max$MF)

# when MF is optimized
plot1 <- ggtern(df.max[ df.max$opt %in% "maxmf",], 
       aes(INT, EXT,SA, value = MF)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis(limits = c(min,max)) + #limits = c(0,4)
  theme_bvbg( ) + 
  theme(legend.position = "right")+
  theme_gridsontop() +
  labs(fill = 'MF') +
  ggtitle("Maximise MF")
plot1


# when NPV is optimized
plot2 <- ggtern(df.max[ df.max$opt %in% "maxnpv",], 
                aes(INT, EXT,SA, value = MF)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis(limits = c(min,max)) + #limits = c(0,4)
  theme_bvbg( ) + 
  theme(legend.position = "right")+
  theme_gridsontop() +
  labs(fill = 'MF') +
  ggtitle("Maximise NPV")
plot2



# -----------
# values for NPV
# -----------

df.max <- df.max %>% mutate(NPV2 = NPV / 1000000)

max <- max(df.max$NPV2)
min <- min(df.max$NPV2)

# when MF is optimized
plot3 <- ggtern(df.max[ df.max$opt %in% "maxmf",], 
                aes(INT, EXT,SA, value = NPV2)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis(limits = c(min,max), option = "plasma") + #limits = c(0,4)
  theme_bvbg( ) + 
  theme(legend.position = "right")+
  theme_gridsontop() +
  labs(fill = 'NPV\n(mil. Euro)') +
  ggtitle("Maximise MF")
plot3


# when NPV is optimized
plot4 <- ggtern(df.max[ df.max$opt %in% "maxnpv",], 
                aes(INT, EXT,SA, value = NPV2)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis(limits = c(min,max), option = "plasma") + #limits = c(0,4)
  theme_bvbg( ) + 
  theme(legend.position = "right")+
  theme_gridsontop() +
  labs(fill = 'NPV\n(mil. Euro)') +
  ggtitle("Maximise NPV")
plot4


library(ggpubr)

plot.combined <- grid.arrange(plot1, plot3, plot2, plot4,
                                   #common.legend = TRUE,legend = "bottom,
                                   ncol = 2, nrow= 2)

ggsave(plot = plot.combined, paste0(path,"first_combined.tiff"), width=10, height=8)







################################################################################
################################################################################



ggtern(maxnpv,aes(INT, EXT, SA)) + 
  geom_point(aes(color=MF), size=18) + 
  #scale_colour_gradient(low = "yellow", high = "blue") +
  scale_colour_viridis() +
  theme_rgbw()+
  theme(tern.panel.grid.ontop = TRUE) +
  labs(title = "MAXNPV - value MF",
       fill = "MF")

ggtern(maxnpv,aes(INT, EXT, SA)) + 
  geom_point(aes(color=NPV), size=18) + 
  #scale_colour_gradient(low = "yellow", high = "blue") +
  scale_colour_viridis() +
  theme_rgbw()+
  theme(tern.panel.grid.ontop = TRUE)+ 
  labs(title = "MAXNPV - value NPV",
       fill = "NPV")

##################

ggtern(maxnpv,aes(INT, EXT, SA)) + 
  #stat_confidence_tern(geom='polygon', aes(fill= ..level..), color = 'white')+
  geom_point_swap(aes(fill=MF),  size = 5) + 
  theme_rgbw()+
  theme(tern.panel.grid.ontop = TRUE)


plot <- ggtern(maxnpv,aes(INT, EXT, SA), fill = NPV)
plot + stat_density_tern(geom = 'polygon',
                         n         = 200,
                         aes(fill =..level.. ,alpha = ..level..),
                         #bdl = 0,
                         bdl.val = NA) +
  geom_point() +
  theme_rgbw() +
  labs(title = "Example Density/Contour Plot")    +
  scale_fill_gradient(low = "blue",high = "red")  +
  guides(color = "none", fill = "none", alpha = "none")







##################

plotnpv <- ggtern(maxnpv,aes(INT, EXT, SA, value=NPV)) +
  stat_interpolate_tern(geom="polygon",
                        formula = value~x+y,
                        method= lm, n= 100,
                        breaks=seq(0, max(maxnpv$NPV), length.out = 9),
                        aes(fill = ..level..), expand = 1.1)+
  scale_fill_viridis()+
  #geom_point(aes(colour = NPV/1000)) +
  labs(title = "MAXNPV - value NPV",
       fill = "NPV") +
  theme_rgbw() +
  theme(tern.panel.grid.ontop = TRUE)
plotnpv

ggsave(plot = plotnpv, paste0(path, "outp/maxNPV_npv.jpg"), width = 8, height = 7)


plotmf <- ggtern(maxnpv, aes(INT, EXT,SA, value = MF)) +
  stat_interpolate_tern(geom="polygon",
                        formula = value~y+x,
                        method = lm,
                        n = 100,
                        #breaks = seq(0, 2.5, length.out = 8),
                        breaks = seq(0, max(maxnpv$MF)+(max(maxnpv$MF)/100)*30, length.out = 9), # 25%
                        #breaks = seq(0, max(maxnpv$MF), length.out = 9), # max value
                        aes(fill = ..level..),
                        expand = 1.1) +
  #scale_fill_gradient(low = "green", high = "red")+
  scale_fill_viridis()+
  #geom_point(aes(colour = MF)) +
  labs(title = "MAXNPV - value MF",
       fill = "MultiF.") +
  theme_rgbw() +
  theme(tern.panel.grid.ontop = TRUE)
plotmf

ggsave(plot = plotmf, paste0(path, "outp/maxNPV_mf.jpg"), width = 8, height = 7)

grid.arrange(plotmf,plotnpv, ncol = 2, nrow= 1)




### example data for stack overflow

#round(maxnpv$SA, digits = 1)
#round(maxnpv$INT, digits = 1)
#round(maxnpv$EXT, digits = 1)
#round(maxnpv$MF, digits = 3)

a <- c(1.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.9, 0.1, 0.1, 0.8, 0.0, 0.0, 0.2, 0.2, 0.8, 0.3, 0.7, 0.0, 0.0, 0.3, 0.7, 0.0, 0.4, 0.0, 0.6, 0.6, 0.4, 0.5, 0.0, 0.5, 0.1, 0.1, 0.8, 0.7, 0.1, 0.2, 0.1, 0.7,
       0.2, 0.6, 0.1, 0.1, 0.6, 0.3, 0.3, 0.1, 0.5, 0.1, 0.4, 0.5, 0.4, 0.6, 0.2, 0.2, 0.3, 0.5, 0.2, 0.5, 0.2, 0.3, 0.4, 0.4, 0.2, 0.3, 0.3, 0.4)
b <- c(0.0, 0.0, 1.0, 0.1, 0.9, 0.0, 0.1, 0.9, 0.0, 0.0, 0.8, 0.2, 0.8, 0.0, 0.2, 0.0, 0.3, 0.7, 0.3, 0.7, 0.0, 0.6, 0.0, 0.4, 0.0, 0.4, 0.6, 0.5, 0.5, 0.0, 0.1, 0.8, 0.1, 0.1, 0.2, 0.7, 0.7, 0.2,
       0.1, 0.1, 0.3, 0.6, 0.3, 0.6, 0.1, 0.4, 0.1, 0.5, 0.1, 0.4, 0.5, 0.2, 0.6, 0.2, 0.5, 0.3, 0.3, 0.2, 0.5, 0.2, 0.4, 0.2, 0.4, 0.4, 0.3, 0.3)
c <- c(0.0, 1.0, 0.0, 0.9, 0.1, 0.1, 0.0, 0.0, 0.9, 0.2, 0.2, 0.8, 0.0, 0.8, 0.0, 0.7, 0.0, 0.3, 0.7, 0.0, 0.3, 0.4, 0.6, 0.6, 0.4, 0.0, 0.0, 0.0, 0.5, 0.5, 0.8, 0.1, 0.1, 0.2, 0.7, 0.1, 0.2, 0.1,
       0.7, 0.3, 0.6, 0.3, 0.1, 0.1, 0.6, 0.5, 0.4, 0.4, 0.5, 0.1, 0.1, 0.2, 0.2, 0.6, 0.2, 0.2, 0.5, 0.3, 0.3, 0.5, 0.2, 0.4, 0.4, 0.3, 0.4, 0.3)
value <- c(1.433, 0.251, 0.000, 0.176, 0.000, 1.556, 1.490, 0.087, 0.522, 1.718, 0.000, 0.098, 0.347, 0.772, 1.642, 1.093, 1.762, 0.000, 0.052, 0.713, 1.857, 0.000, 1.367, 0.022, 1.814,
           1.726, 1.043, 1.424, 0.001, 1.722, 0.428, 0.122, 1.656, 1.798, 0.330, 0.384, 0.138, 1.777, 0.661, 1.763, 0.271, 0.166, 1.733, 0.753, 0.984, 0.236, 1.574, 0.204, 1.232, 1.471,
           1.086, 1.748, 0.409, 0.568, 0.790, 1.505, 0.520, 1.552, 0.451, 0.884, 1.094, 1.180, 0.484, 0.831, 0.859, 1.123)
df <- data.frame(a,b,c,value)
library(ggtern)
ggtern(df,aes(a, b, c)) +
  geom_point(size=2, aes(color=value)) +
  theme_rgbw() 


# answer to first question - was closed to early
# https://stackoverflow.com/questions/69191949/ggtern-fill-smooth-area-between-values-of-triangulation-points

library(ggtern)
library(ggtern)
ggtern(df, aes(a, b, c, value = value)) +
  geom_point(size = 2, shape = 21, aes(fill = value)) +
  stat_interpolate_tern(geom="polygon",
                        formula = value~x+y,
                        method = lm,
                        n = 100,
                        breaks = seq(0, 2.5, length.out = 50),
                        aes(fill = ..level..),
                        expand = 1,
                        alpha = 0.5) +
  scale_fill_gradient(low = "green", high = "red") +
  theme_rgbw()


library(ggtern)
ggtern(df, aes(a, b, c, value = value)) +
  stat_interpolate_tern(geom="polygon",
                        formula = value~y+x,
                        method = lm,
                        n = 100,
                        breaks = seq(0, 2.5, length.out = 8),
                        aes(fill = ..level..),
                        expand = 1) +
  scale_fill_gradient(low = "green", high = "red")+
  geom_point()




### answer to secons question 
# https://stackoverflow.com/questions/69218262/ggtern-create-contoured-ternary-plot


SA <- c(1.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.9, 0.1, 0.1, 0.8, 0.0, 0.0, 0.2, 0.2, 0.8, 0.3, 0.7, 0.0, 0.0, 0.3, 0.7, 0.0, 0.4, 0.0, 0.6, 0.6, 0.4, 0.5, 0.0, 0.5, 0.1, 0.1, 0.8, 0.7, 0.1, 0.2, 0.1, 0.7,
        0.2, 0.6, 0.1, 0.1, 0.6, 0.3, 0.3, 0.1, 0.5, 0.1, 0.4, 0.5, 0.4, 0.6, 0.2, 0.2, 0.3, 0.5, 0.2, 0.5, 0.2, 0.3, 0.4, 0.4, 0.2, 0.3, 0.3, 0.4)
INT <- c(0.0, 0.0, 1.0, 0.1, 0.9, 0.0, 0.1, 0.9, 0.0, 0.0, 0.8, 0.2, 0.8, 0.0, 0.2, 0.0, 0.3, 0.7, 0.3, 0.7, 0.0, 0.6, 0.0, 0.4, 0.0, 0.4, 0.6, 0.5, 0.5, 0.0, 0.1, 0.8, 0.1, 0.1, 0.2, 0.7, 0.7, 0.2,
         0.1, 0.1, 0.3, 0.6, 0.3, 0.6, 0.1, 0.4, 0.1, 0.5, 0.1, 0.4, 0.5, 0.2, 0.6, 0.2, 0.5, 0.3, 0.3, 0.2, 0.5, 0.2, 0.4, 0.2, 0.4, 0.4, 0.3, 0.3)
EXT <- c(0.0, 1.0, 0.0, 0.9, 0.1, 0.1, 0.0, 0.0, 0.9, 0.2, 0.2, 0.8, 0.0, 0.8, 0.0, 0.7, 0.0, 0.3, 0.7, 0.0, 0.3, 0.4, 0.6, 0.6, 0.4, 0.0, 0.0, 0.0, 0.5, 0.5, 0.8, 0.1, 0.1, 0.2, 0.7, 0.1, 0.2, 0.1,
         0.7, 0.3, 0.6, 0.3, 0.1, 0.1, 0.6, 0.5, 0.4, 0.4, 0.5, 0.1, 0.1, 0.2, 0.2, 0.6, 0.2, 0.2, 0.5, 0.3, 0.3, 0.5, 0.2, 0.4, 0.4, 0.3, 0.4, 0.3)
MF <- c(1.433, 0.251, 0.000, 0.176, 0.000, 1.556, 1.490, 0.087, 0.522, 1.718, 0.000, 0.098, 0.347, 0.772, 1.642, 1.093, 1.762, 0.000, 0.052, 0.713, 1.857, 0.000, 1.367, 0.022, 1.814,
        1.726, 1.043, 1.424, 0.001, 1.722, 0.428, 0.122, 1.656, 1.798, 0.330, 0.384, 0.138, 1.777, 0.661, 1.763, 0.271, 0.166, 1.733, 0.753, 0.984, 0.236, 1.574, 0.204, 1.232, 1.471,
        1.086, 1.748, 0.409, 0.568, 0.790, 1.505, 0.520, 1.552, 0.451, 0.884, 1.094, 1.180, 0.484, 0.831, 0.859, 1.123)
df <- data.frame(SA,INT,EXT,MF)

library(ggtern)
library(viridis)


# With ggtern, I had some difficulties as well providing the right interpolation. Especially, the polygons are a bit tricky.
# When you switch to stat = "InterpolateTern" instead of stat = "polygon", you could reproduce your example, 
# together with the important changes in base = "identity" and method = "auto":

ggtern(df,
       aes(INT, EXT,SA, value = MF)) +
  geom_interpolate_tern(
    stat = "InterpolateTern",
    method = "auto",
    na.rm = TRUE,
    formula = value ~ x + y,
    expand = 0,
    base = "identity",
    aes(
      colour = after_stat(level)
    ),
    breaks = seq(0,1.75, length.out = 9),
    size = 2
  ) + scale_colour_viridis() +
  theme_rgbw()


# I was not able to generate a polygon based plot to deliver the desired output as the polygons are usually truncated.
# I helped myself with a workaround:

ggtern(df, 
       aes(INT, EXT,SA, value = MF)) +
  geom_interpolate_tern(
    stat = "InterpolateTern",
    method = "auto",
    na.rm = TRUE,
    formula = value ~ x + y,
    expand = 0,
    base = "identity",
    aes(
      colour = after_stat(level)
    ),
    breaks = seq(0,1.8, length.out = 500),
    size = 5
    # ) +
    # geom_interpolate_tern(
    #   stat = "InterpolateTern",
    #   method = "auto",
    #   na.rm = TRUE,
    #   formula = value ~ x + y,
    #   expand = 0,
    #   base = "identity",
    #   aes(
    #     colour = after_stat(level)
    #   ),
    #   breaks = seq(0, 1.75, length.out = 9),
    #   size = 1,
    #   colour = "white"
  )+  scale_colour_viridis() +
  theme_rgbw() + 
  theme_gridsontop()


# You have to play a bit with breaks and size to colour the whole area. 
# Probably, it is worth to calculate a model first and plot this extrapolated to the triangle corners.


# Another alternative:

ggtern(df, 
       aes(INT, EXT,SA, value = MF)) +
  geom_hex_tern(
    stat = "hex_tern",
    fun = "mean",
    na.rm = TRUE,
    binwidth = 0.1, # depends on your data granularity 
    colour = "grey"
  ) +
  scale_fill_viridis() +
  #theme_rgbw() +
  
  theme_bvbg() +
  #theme_arrowlarge() +
  #theme_bvbw() +
  #theme_rgbg() +
  #theme_classic() + 
  theme_gridsontop()











