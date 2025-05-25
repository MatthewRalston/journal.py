#!/bin/env python
#   Copyright 2025 Matthew Ralston
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# Author: Matt Ralston
# Date: 05/24/25
# Description:

####################
# PACKAGES
####################
import os
#import argparse
import copy
import sys
import tomllib
#from typeclass import *
#import ConfigParser
import logging
import logging.config


from journal import helpers



####################
# CONSTANTS
####################



prompts_toml = os.path.join(os.path.dirname(__file__), "prompts.toml")



    
####################
# DATATYPES
####################



"""
Types of questions:

boolean : inquirer.Confirm (y/n)
choice : inquirer.List
multichoice : inquirer.Checkbox, select more than one option from choice
text : multiline_input, produce multiline text input
singleline : single line of input
multiline: multiple lines as input
belief : dual prompt: 1:10 and single line explanation

"""

####################
# FUNCTIONS
####################


def main():
    with open(prompts_toml, 'rb') as ifile:
        prompts = tomllib.load(ifile)
        print(prompts)
        #first = text_input("foo")

    bool_prompt_data  = {
        "type": "boolean",
        "name": "bool_ex",
        "prompt": "Do you enjoy programeing",
        "description": "If you like programming please input True or False",
        "default": "False"
    }

        
    helpers.prompt_boolean(bool_prompt_data)

    choice_prompt_data = {
        "type": "choice",
        "name": "choice_ex",
        "prompt": "Do you enjoy programeing?",
        "description": "If you like programming please input True, False, or maybe",
        "default": "False",
        "choices": ["True", "False", "Maybe"]
    }

    helpers.prompt_choice(choice_prompt_data)
    
    multichoice_prompt_data = {
        "type": "multichoice",
        "name": "multichoice_ex",
        "prompt": "Select from the following",
        "description": "What languages do you like?",
        "default": ["Python"],
        "choices": ["Python", "Ruby", "Julia", "Javascript", "Rust", "R"]
    }

    
    
    helpers.prompt_multichoice(multichoice_prompt_data)

    text_prompt_data = {
        "type": "text",
        "name": "text_ex",
        "prompt": "Describe what you enjoy about programming",
        "description": "Do you like programming?",
    }

    helpers.prompt_text(text_prompt_data)

    singleline_prompt_data = {
        "type": "singleline",
        "name": "singleline_ex",
        "prompt": "Describe what you like about programming in one line",
        "description": "Do you really like programming?"
    }

    helpers.prompt_singleline(singleline_prompt_data)

    multiline_prompt_data = {
        "type": "singleline",
        "name": "singleline_ex",
        "prompt": "Describe 2 things you like about programming ",
        "description": "Do you really REALLY like programming?"
    }
    helpers.prompt_multiline(multiline_prompt_data)


    belief_prompt_data = {
        "type": "belief",
        "name": "belief_ex",
        "prompt": "Describe one thing you like about programming ",
        "description": "Do you really REALLY like programming?"
    }

    helpers.prompt_belief(belief_prompt_data)

    belieflist_prompt_data = {
        "type": "belief",
        "name": "belieflist_ex",
        "prompt": "What are a few healthy beliefs about a programming career?",
        "description": "Do you really REALLY REALLY like programming?"
    }

    
    helpers.prompt_belief_list(belieflist_prompt_data)
    
def cli():
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--required', help="Required argument",required=True)
    # parser.add_argument('--flag', help="This is a flag",action="store_true")
    # parser.add_argument('-v, --verbose', help="Prints warnings to console by default",default=0, action="count")
    # args = parser.parse_args()
    # Main routine
    main()


####################
# OPTIONS AND MAIN
####################

if __name__ == '__main__':
    cli()


