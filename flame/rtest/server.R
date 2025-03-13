# SERVER ---------

server <- function(input, output) {

# Corpus ------------------------------------------------------------------

  # Default corpus (test data)
  testcorpus <- "../../catch/test/social_media_posts.txt"
  
  reactiveFile <- reactive({
    if (is.null(input$corpus)) {
      return(testcorpus)
    } else {
      return(input$corpus$datapath)
    }
  })
  
  # output$whatFile <- renderText({
  #   reactiveFile()
  # })
  
  # Render data for user to see
  output$fileContent <- renderPrint({
    corpus <- reactiveFile()
    file_lines <- readLines(corpus, n=3)
    file_lines # print
  })

# Next Section ------------------------------------------------------------
  
} # end of server