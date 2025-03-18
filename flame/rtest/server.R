# Server ------------------------------------------------------------------

server <- function(input, output) {

# Corpus ------------------------------------------------------------------

  # Default corpus (test data)
  testcorpus <- "../../catch/test/social_media_posts.txt"
  
  reactiveFile <- reactive({
    if (is.null(input$corpus)) { # if NULL, use test data
      return(testcorpus)
    } else {
      return(input$corpus$datapath)
    }
  })
  
  # output$whatFile <- renderText({
  #   reactiveFile()
  # }) # this was the script to show filepath

  output$fileContent <- renderText({
    corpus <- reactiveFile()
    file_content <- readLines(corpus)
    paste(file_content, collapse="\n")
  })

# Next Section ------------------------------------------------------------
 
#

# End ---------------------------------------------------------------------

}
