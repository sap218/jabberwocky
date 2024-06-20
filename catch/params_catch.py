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
    filter_level = "light" # "heavy"
    grep_format = True # if False, posts with have tags
    not_annotated = False # if True, posts will be the inverted grep
    graph = True
    cm = "Set3"
    output_name = "../catch/test/catch_output"
    stats_output_name = "../catch/test/catch_output_stats"
    plot_output_name = "../catch/test/catch_output_wordcloud"
    
else:
    corpus = ""
    annotation_file = ""
    filter_level = "light"
    
    grep_format = True
    not_annotated = False
    
    graph = True
    cm = "Set3"
        
    output_name = "catch_output"
    stats_output_name = "catch_output_stats"
    plot_output_name = "catch_output_wordcloud"

####################################################

# End of script
