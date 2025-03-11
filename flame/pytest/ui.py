# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 22:43:04 2025

@author: Sam
"""
'''
from shiny import App, ui, render_text

# Define the user interface (UI)
app_ui = ui.page_fluid(
    ui.h1("Hello, Shiny Dashboard!"),  # A header with a title
    ui.output_text("text_output")  # A place to display text output
)

'''


from shiny import ui

# Define the user interface (UI)
app_ui = ui.page_fluid(
    ui.h1("Hello, Shiny Dashboard!"),  # A header with a title
    ui.output_text("text_output")  # A place to display text output
)


