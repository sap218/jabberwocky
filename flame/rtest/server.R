# Server ------------------------------------------------------------------

server <- function(input, output) {

# Input files -------------------------------------------------------------

  testcorpus <- "../../catch/test/social_media_posts.txt"
  testconcepts <- "../../bandersnatch/test/snatch_output.txt"
    
  reactiveCorpus <- reactive({
    if (is.null(input$corpus)) { # if NULL, use test
      return(testcorpus)
    } else {
      return(input$corpus$datapath)
    }
  })
  
  reactiveConcepts <- reactive({
    if (is.null(input$concepts)) { # if NULL, use test
      return(testconcepts)
    } else {
      return(input$concepts$datapath)
    }
  })
  
  # output$whatFile <- renderText({
  #   reactiveCorpus()
  # }) # this was the script to show filepath

  output$corpusContent <- renderText({
    corpus <- reactiveCorpus()
    file_content <- readLines(corpus)
    paste(file_content, collapse="\n")
  })
  
  output$conceptsContent <- renderText({
    concepts <- reactiveConcepts()
    file_content <- readLines(concepts)
    paste(file_content, collapse=", ")
  })
  
# Next Section ------------------------------------------------------------
 
#

# End ---------------------------------------------------------------------

}
