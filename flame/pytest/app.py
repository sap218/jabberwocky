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

# app.py
import shiny
from ui import ui  # Import the ui function from ui.py
from server import server  # Import the server function from server.py

# Create the app by passing the imported ui and server functions
app = shiny.App(ui=ui, server=server)

# Run the app
if __name__ == "__main__":
    app.run()
    #shiny.jupyter.run(app) 

####################################################

# End of script
