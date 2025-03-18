# -*- coding: utf-8 -*-
"""
@date: 2025
@author: Samantha C Pendleton
@description: shiny dashboard
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://shiny.posit.co/py/docs/overview.html
"""

# server.py
import shiny
from shiny import reactive, render

def server(input, output, session):
    
    # Default test file
    testcorpus = "../../catch/test/social_media_posts.txt"
    
    # Reactive file input
    @reactive.Calc
    def reactiveFile():
        if input.corpus() is None:  # if NULL, use test data
            return testcorpus
        else:
            return input.corpus().datapath
    
    # Render file content
    @output
    @render.text
    def fileContent():
        corpus = reactiveFile()
        with open(corpus, 'r') as file:
            file_content = file.readlines()
        return ''.join(file_content)
