# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 22:43:20 2025

@author: Sam
"""

'''
from shiny import App, ui, render_text

# Define server logic
def server(input, output, session):
    # Define what text should be rendered in the output
    @output
    @render_text
    def text_output():
        return "Welcome to your first Shiny dashboard in Python!"
'''

'''
from shiny import render_text

# Define server logic
def server(input, output, session):
    # Render text in the UI
    @output
    @render_text
    def text_output():
        return "Welcome to your first Shiny dashboard in Python!"
'''

from shiny import render_text

# Define server logic
def server(input, output, session):
    # The @output decorator links the function to the UI component
    # The @render_text decorator makes the function return text output dynamically
    @output
    @render_text
    def text_output():
        return "Welcome to your first Shiny dashboard in Python!"

