library(shiny)

library(reticulate)
use_python("../../catch/")

#ui <- source("ui.R")
#server <- source("server.R")

shinyApp(ui = ui.R, server = server.R)

#runApp("app")
