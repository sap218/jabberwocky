#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2025
@author: Samantha C Pendleton
@description: shiny dashboard
@GitHub: github.com/sap218/jabberwocky

@useful links:
    # https://shiny.posit.co/py/docs/overview.html
"""

import threading

from shiny import App, ui, render_text

from ui import app_ui

from server import server

####################################################


# Create the Shiny app
app = App(app_ui, server)

####################################################

# Function to run the app in a separate thread
def run_app():
    app.run(port=8050)

# Run the app in a separate thread
if __name__ == "__main__":
    threading.Thread(target=run_app).start()


####################################################

# End of script
