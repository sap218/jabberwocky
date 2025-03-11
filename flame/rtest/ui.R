# UI ---------

library(shinythemes)

ui <- fluidPage(
  theme = shinytheme("paper"), # list of nice themes: cosmo, flatly, paper, yeti
  
  titlePanel("Jabberwocky"),
  
  fluidRow(
    column(2,
           helpText("Data"),
           
           # Data filtering parameters ----
           sliderInput(inputId="rangeage", label="Age range:",
                       value=c(0,100),
                       min=0, max=100)
           
    ), # end of col2 (left panel)
    
    column(10,

           navbarPage("Navigation",
                      
                      tabPanel("Numerical",
                               sidebarLayout(
                                 position = "right",
                                 sidebarPanel(
                                   helpText("Features"),
                                   textInput(inputId="xaxis", label="Feature (x):", placeholder="AGE"),    
                                   textInput(inputId="yaxis", label="Feature (y):", placeholder="HEIGHT"), 
                                 ),
                                 mainPanel(
                                   plotOutput("exampleplot")
                                 ) # end of main panel
                               ) # end of panel layout
                      ), # end of numeric panel
                      
                      
                      tabPanel("Other panel",
                      ) # end of other tab panel
                      
           ) # end of navbar
    ) # end of col10 (centre panel)
  ) # end of fluid rows
) # end of fluid page