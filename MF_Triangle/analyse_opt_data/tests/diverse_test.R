

# https://rpubs.com/tskam/ternary_plot

# packages = c('ggtern', 'plotly', 'readr', 'dplyr', 'tidyr')
# 
# for(p in packages){
#   if(!require(p, character.only = T)){
#     install.packages(p)
#   }
#   library(p, character.only = T)
# }

library(ggplot2)
library(ggtern)
library(plotly)
library(readr)
library(dplyr)
library(tidyr)


#https://stackoverflow.com/questions/10879361/ternary-plot-and-filled-contour

#Orignal Data as per Question
a <- c(0.1, 0.5,0.5, 0.6, 0.2, 0          , 0         , 0.004166667, 0.45) 
b <- c(0.75,0.5,0  , 0.1, 0.2, 0.951612903,0.918103448, 0.7875     , 0.45)
c <- c(0.15,0  ,0.5, 0.3, 0.6, 0.048387097,0.081896552, 0.208333333, 0.10) 
d <- c(500,2324.90,2551.44,1244.50, 551.22,-644.20,-377.17,-100, 2493.04) 
df <- data.frame(a, b, c, d)

#For labelling each point.
df$id <- 1:nrow(df)

#Build Plot
ggtern(data=df,aes(x=c,y=a,z=b),aes(x,y,z)) + 
  
  # geom_point(size=2, aes(color=d)) +
  # theme_bw() +
  # scale_color_gradient2(low = "green", mid = "yellow", high = "red")
  
  stat_(geom="polygon",
                 n=400,
                 aes(fill=..level..,
                     weight=d,
                     alpha=abs(..level..)),
                 binwidth=100) + 
  geom_density2d(aes(weight=d,color=..level..),
                 n=400,
                 binwidth=100) +
  geom_point(aes(fill=d)) + 
  #geom_text(aes(label=id),size=3) + 
  scale_fill_gradient(low="yellow",high="red") + 
  scale_color_gradient(low="yellow",high="red") + 
  #theme_ggtern() +
  #theme_rgbw() +
  theme_rgbg() +
  #theme_tropical()+
  theme(legend.justification=c(0,1), legend.position=c(0,1)) + 
  guides(fill = guide_colorbar(order=1),
         alpha= guide_legend(order=2),
         color="none") + 
  labs(  title= "Ternary Plot and Filled Contour",
         fill = "Value, V",alpha="|V - 0|")

#Save Plot
ggsave("TernFilled.png")








df <- data.frame(a, b, c, d)
ggtern(df,aes(a,c,b)) + 
  # geom_interpolate_tern(aes(value=d,fill=..level..),
  #                       binwidth=500,
  #                       colour="white") +
  geom_point(aes(fill=d),color="black",shape=21,size=3) + 
  scale_fill_gradient(low="yellow",high="red") +
  theme(legend.position=c(0,1),legend.justification=c(0,1)) + 
  labs(fill="Value, d")


#######################################################################################

# https://cran.r-project.org/web/packages/Ternary/vignettes/Ternary.html

#install.packages('Ternary')
#Ternary::TernaryApp()
library('Ternary')
TernaryPlot()

par(mar = rep(0.2, 4))
TernaryPlot(alab = 'a', blab = 'b', clab = 'c')

FunctionToContour <- function (a, b, c) {
  a - c + (4 * a * b) + (27 * a * b * c)
}

values <- TernaryPointValues(FunctionToContour, resolution = 24L)
ColourTernary(values)
TernaryContour(FunctionToContour, resolution = 36L)



######################################################################################


#https://www.geo.fu-berlin.de/en/v/soga/Introduction-to-R/Plotting-Data/ternary-diagrams/index.html

library(ggtern)
library(ggplot2)
set.seed(1)
plot <- ggtern(data = data.frame(x = runif(100),
                                 y = runif(100),
                                 z = runif(100)),
               aes(x, y, z))
plot + stat_density_tern(geom = 'polygon',
                         n         = 200,
                         aes(fill  = ..level..,
                         alpha = ..level..),
                         bdl = 0,
                         bdl.val = 0.01
                         ) +
  geom_point() +
  theme_rgbw() +
  labs(title = "Example Density/Contour Plot")    +
  scale_fill_gradient(low = "blue",high = "red")  +
  guides(color = "none", fill = "none", alpha = "none")



################################################




# https://cran.r-project.org/web/packages/Ternary/Ternary.pdf

coords <- list(A = c(1, 0, 2),B = c(1, 1, 1),C = c(1.5, 1.5, 0),D = c(0.5, 1.5, 1))
TernaryPlot()
AddToTernary(lines, coords, col='darkgreen', lty='dotted', lwd=3)
TernaryLines(coords, col='darkgreen')
TernaryArrows(coords[1], coords[2:4], col='orange', length=0.2, lwd=1)
TernaryText(coords, cex=0.8, col='red', font=2)
TernaryPoints(coords, pch=1, cex=2, col='blue')
AddToTernary(points, coords, pch=1, cex=3)



#https://plotly.com/r/ternary-plots/

library(plotly)

journalist <- c(75,70,75,5,10,10,20,10,15,10,20)
developer <- c(25,10,20,60,80,90,70,20,5,10,10)
designer <- c(0,20,5,35,10,0,10,70,80,80,70)
label <- c('point 1','point 2','point 3','point 4','point 5','point 6',
           'point 7','point 8','point 9','point 10','point 11')


df <- data.frame(journalist,developer,designer,label)

# axis layout
axis <- function(title) {
  list(
    title = title,
    titlefont = list(
      size = 20
    ),
    tickfont = list(
      size = 15
    ),
    tickcolor = 'rgba(0,0,0,0)',
    ticklen = 5
  )
}


fig <- df %>% plot_ly()
fig <- fig %>% add_trace(
  type = 'scatterternary',
  mode = 'markers',
  a = ~journalist,
  b = ~developer,
  c = ~designer,
  text = ~label,
  marker = list( 
    symbol = 100,
    color = '#DB7365',
    size = 14,
    line = list('width' = 2)
  )
)
fig <- fig %>% layout(
  title = "Simple Ternary Plot with Markers",
  ternary = list(
    sum = 100,
    aaxis = axis('Journalist'),
    baxis = axis('Developer'),
    caxis = axis('Designer')
  )
)

fig


#############################

# Set plot margins
par(mfrow=c(1, 1), mar=rep(.3, 4))

# Make ternary plot grid
TernaryPlot(alab="% Sand \u2192", blab="% Silt \u2192", clab="\u2190 % Clay ",
            lab.col=c('red', 'green3', 'blue'),
            point='up', lab.cex=1.5, grid.minor.lines=1, axis.cex=1.5,
            grid.lty='solid', col=rgb(0.9, 0.9, 0.9), grid.col='white', 
            axis.col=rgb(0.6, 0.6, 0.6), ticks.col=rgb(0.6, 0.6, 0.6),
            padding=0.08)

# Define colors for the background
cols <- TernaryPointValues(rgb)

# Add colors to Ternary plot
ColourTernary(cols, spectrum = NULL, resolution=45)




TernaryPlot(atip = "Top", btip = "Bottom", ctip = "Right", axis.col = "red", 
            col = rgb(0.8, 0.8, 0.8))
HorizontalGrid(grid.lines = 2, grid.col = 'blue', grid.lty = 1) 

