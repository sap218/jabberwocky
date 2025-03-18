#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@date: 2024
@author: Samantha C Pendleton
@GitHub: github.com/sap218/jabberwocky
"""

####################################################
#
# PARAMETERS FOR CATCH
#
####################################################

is_this_a_test = True

####################################################

if is_this_a_test:
    corpus = "../catch/test/social_media_posts"
    annotation_file = "../bandersnatch/test/snatch_output"
    
    filter_level = "light" # or "none" or "heavy"
    output_format = "wtags" # ["wtags","grep","invertedgrep"]
    
    output_name = "../catch/test/catch_output"
    stats_output_name = "../catch/test/catch_output_stats"
    
    plotWORDCLOUD = False
    if plotWORDCLOUD:
        plot_output_name = "../catch/test/catch_output_wordcloud"
        cm = "Set3" # default
        
    plotCYANNOTATOR = True
    if plotCYANNOTATOR:
        cyannotator_output_name = "../catch/test/catch_output_cyannotator"
        highlightcolour = "#00bcd4" # default = cyan
    
else:
    corpus = ""
    annotation_file = ""
    
    filter_level = ""
    output_format = ""
    
    output_name = "catch_output"
    stats_output_name = "catch_output_stats"
    
    plotWORDCLOUD = True
    if plotWORDCLOUD:
        plot_output_name = "catch_output_wordcloud"
        cm = ""
        
    plotCYANNOTATOR = True
    if plotCYANNOTATOR:
        cyannotator_output_name = "catch_output_cyannotator"
        highlightcolour = "" 

####################################################

# End of script
