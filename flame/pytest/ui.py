# -*- coding: utf-8 -*-
"""
@date: 2025
@author: Samantha C Pendleton
@description: shiny dashboard
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://shiny.posit.co/py/docs/overview.html
"""

# ui.py
import shiny
from shiny import ui

# ui.py
import shiny
from shiny import ui

def ui():
    return ui.page_fluid(
        ui.theme('cosmo'),  # theme like in R Shiny
        ui.panel_title("Jabberwocky"),
        
        ui.layout_sidebar(
            ui.panel_sidebar(
                ui.help_text("Data"),
                ui.input_file("corpus", "Upload corpus", accept=".txt"),
                ui.input_radio_buttons("filter_level", "Stopword filtering", choices=["light", "heavy"]),
                ui.input_radio_buttons("output_format", "Output format", choices=["wtags", "grep", "invertedgrep"]),
            ),
            
            ui.panel_main(
                ui.navbar_page(
                    "Navigation",
                    
                    ui.nav_panel("Corpus", 
                                 ui.layout_sidebar(
                                     ui.panel_sidebar(
                                         ui.help_text("Features"),
                                         ui.input_radio_buttons("cm", "Wordcloud scheme", choices=["Set3", "viridis"]),
                                         ui.input_colour_picker("highlightcolour", "Highlighter", value="#00bcd4")
                                     ),
                                     ui.panel_main(
                                         ui.output_text("fileContent")
                                         #ui.div(style="max-height:200px; overflow-y:scroll; border:0.5px solid #ccc; padding:0px;", 
                                         #       ui.output_text("fileContent"))
                                     )
                                 )
                    )
                )
            )
        )
    )
