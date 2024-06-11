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
    graph = "Yes"
    cm = "Set3"
    grep_format = True # if False, posts with have tags
    not_annotated = False # if True, posts will be the inverted grep
    output_name = "../catch/test/catch_output"
    stats_output_name = "../catch/test/catch_output_stats"
    plot_output_name = "../catch/test/catch_output_wordcloud"
    
else:
    corpus = ""
    annotation_file = ""
    
    graph = "Yes"
    if graph == "Yes":
        cm = ""
    
    grep_format = ""
    not_annotated = ""
    
    output_name = "catch_output"
    stats_output_name = "catch_output_stats"
    plot_output_name = "catch_output_wordcloud"

####################################################

# End of script
