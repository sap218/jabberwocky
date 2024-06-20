#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@GitHub: github.com/sap218/jabberwocky
"""

####################################################
#
# PARAMETERS FOR BITE
#
####################################################

is_this_a_test = True

####################################################

if is_this_a_test:
    corpus = "../catch/test/catch_output_invert"
    concepts_to_remove = "../bandersnatch/test/snatch_output"
    filter_level = "light" # "heavy"
    graph = True   
    cm = "mediumseagreen"
    limit = 30 # default is top 30 words
    output_name = "../bite/test/bite_output"
    stats_output_name = "../bite/test/bite_output_stats"
    plot_output_name = "../bite/test/bite_output_plot"
    
else:
    corpus = ""
    concepts_to_remove = ""
    filter_level = "light"
    
    graph = True
    cm = "mediumseagreen"
    limit = 30
    
    output_name = "bite_output"
    stats_output_name = "bite_output_stats"
    plot_output_name = "bite_output_plot"

####################################################

# End of script
