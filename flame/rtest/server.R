# SERVER ---------

server <- function(input, output) {
  
  output$exampleplot <- renderPlot({
    hist(faithful$waiting, col = "#007bc2", border = "white",
         xlab = "Waiting time to next eruption (in mins)",
         main = "Histogram of waiting times")
  })
  
} # end of server