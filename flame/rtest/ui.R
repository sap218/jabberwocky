# UI ---------

library(shinythemes) # theme
library(colourpicker) # cyan

ui <- fluidPage(
  theme = shinytheme("cosmo"), # list of nice themes: cosmo, flatly, paper, yeti
  
  titlePanel("Jabberwocky"),
  
  fluidRow(
    column(3,
           helpText("Data"),
      
           #textInput("corpus", "Corpus"),
           fileInput("corpus", "Upload corpus", accept = ".txt"),
           
           #textInput("annotation_file", "Annotation file"),
           #fileInput("corpus", "Upload corpus", accept = ".txt"),
           
           # selectInput("filter_level", "Stopword filtering", c("light","heavy")),
           radioButtons("filter_level", "Stopword filtering", c("light","heavy")),
           radioButtons("output_format", "Output format", c("wtags","grep","invertedgrep")),

           #output_name, stats_output_name, plot_output_name, cyannotator_output_name
           
    ), # end of left panel
    
    column(9,

           navbarPage("Navigation",
                      
                      tabPanel("Numerical",
                               sidebarLayout(
                                 position = "right",
                                 sidebarPanel(
                                   helpText("Features"),
                                   radioButtons("cm", "Wordcloud scheme", c("Set3","viridis")),
                                   colourInput("highlightcolour", "Highlighter", value="#00bcd4")
                                 ), # end of right panel
                                 
                                 mainPanel(
                                   
                                   #textOutput("whatFile")
                                   verbatimTextOutput("fileContent")
                                   
                                 ) # end of main panel
                               ) # end of panel layout
                      )#, # end of numeric panel
                      
                      # tabPanel("Other panel",
                      # ) # end of other tab panel
                      
           ) # end of navbar
    ) # end of centre panel
  ) # end of fluid rows
) # end of fluid page