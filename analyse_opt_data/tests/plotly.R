####
# based on plotly
#
####


# https://xang1234.github.io/ternary/


library(ggplot2)
library(plotly)
library(tidyverse)

# # we filter out data with zero %
# tern %>%filter(`% Young`!=0 & `% Old`!=0 & `% Economically Active`!=0 & !is.na(`Planning Region`))%>%
#   filter(Year>=2010)
# tern2017<-tern %>% filter(Year=='2017')
# 
# # we create the ternary plot using plotly
# p1<- plot_ly(
#   tern2017, a = ~`% Economically Active`, b = ~`% Young`, c = ~`% Old`,
#   color = ~`Planning Region`, type = "scatterternary", colors=~colors,
#   size = ~Total,
#   text = ~paste('Young:',sep='', round(`% Young`,1),'%',
#                 '<br>Economically Active:',
#                 round(`% Economically Active`,1),'%', '<br>Old:',
#                 round(`% Old`,1),'%','<br>Subzone:', Subzone, hoverinfo="text",
#                 '<br>Planning Area:', `Planning Area`),
#   marker = list(symbol = 'circle', opacity=0.55, sizemode="diameter", sizeref=1.5,
#                 line = list(width = 2, color = '#FFFFFF')))
# 
# p1


### Set the working path to this R-project
path <- paste0(getwd(),"/")
inputpath <- paste0(path,"input_data/")


maxnpv <- read_csv(paste0(inputpath,"MAX_NPV.csv")) %>% 
  select(NPV, MF, SA, INT, EXT) 

p1<- plot_ly(
    maxnpv, a = ~`SA`, b = ~`INT`, c = ~`EXT`,
    color = ~`MF`, 
    type = "scatterternary", 
    colors=~colors,
    # size = ~Total,
    # text = ~paste('Young:',sep='', round(`% Young`,1),'%',
    #               '<br>Economically Active:',
    #               round(`% Economically Active`,1),'%', '<br>Old:',
    #               round(`% Old`,1),'%','<br>Subzone:', Subzone, hoverinfo="text",
    #               '<br>Planning Area:', `Planning Area`),
    marker = list(symbol = 'circle', opacity=0.55, sizemode="diameter", sizeref=1.5,
                  line = list(width = 2, color = '#FFFFFF'))
    )

  p1
  
  
