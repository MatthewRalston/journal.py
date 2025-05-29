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
import sys

import datetime
import random
import copy

import tomllib
import yaml
#import json

import logging
import logging.config


from journal import helpers, affirmations



####################
# CONSTANTS
####################



PROMPTS_TOML = os.path.join(os.path.dirname(__file__), "prompts.toml")

SAMPLE_MULTILINE = 3

    
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
    
    with open(PROMPTS_TOML, 'rb') as ifile:
        prompts = tomllib.load(ifile)
        #print(prompts)
    answers = []
    affirmations.make_morning_affirmations()
    """
    Booleans
    """
    for name, prompt_data in prompts["bool"].items():
        bool_answer = helpers.prompt_boolean(prompt_data)
        #prompts["bool"][name]["answers"] = bool_answer
        answers.append([prompt_data["prompt"], bool_answer])
    """
    Choices (05/26/25: none)
    """
    # helpers.prompt_choice(choice_prompt_data)
    """
    Multichoice (05/26/25: none)
    """
    # multichoice_prompt_data = {
    #     "type": "multichoice",
    #     "name": "multichoice_ex",
    #     "prompt": "Select from the following",
    #     "description": "What languages do you like?",
    #     "default": ["Python"],
    #     "choices": ["Python", "Ruby", "Julia", "Javascript", "Rust", "R"]
    # }
    # helpers.prompt_multichoice(multichoice_prompt_data)
    """
    Text
    """
    for name, prompt_data in prompts["text"].items():
        text_answer = helpers.prompt_text(prompt_data)
        #prompts["text"][name]["answers"] = text_answer
        answers.append([prompt_data["prompt"], text_answer])
    """
    singleline
    """
    for name, prompt_data in prompts["singleline"].items():
        singleline_answer = helpers.prompt_singleline(prompt_data)
        #prompts["singleline"][name]["answers"] = singleline_answer
        answers.append([prompt_data["prompt"], singleline_answer])
    """
    multiline (05/26/25: random selection)
    """
    multiline_prompts = []
    multiline_names = []
    for name, prompt_data in prompts["multiline"].items():
        multiline_prompts.append(prompt_data)
        multiline_names.append(name)
    selected_prompts = random.sample(multiline_prompts, SAMPLE_MULTILINE) # randomly select n prompts from the 21 prompts (05/26/25)
    for i, p in enumerate(selected_prompts):
        multiline_answers = helpers.prompt_multiline(p)
        #prompts["multiline"][multiline_names[i]]["answers"] = multiline_answers
        answers.append([prompt_data["prompt"], multiline_answers])

    """
    belief
    """
    # for name, prompt_data in prompts["belief"].items():
    #     belief_answer = helpers.prompt_belief(prompt_data)
    #     answers.append([prompt_data["prompt"], belief_answer])

    """
    belieflist
    """
    scale_label = None
    reason_label = None
    for name, prompt_data in prompts["belieflist"].items():
        if "scale_label" in prompt_data.keys() and "reason_label" in prompt_data.keys():
            scale_label=prompt_data["scale_label"]
            reason_label=prompt_data["reason_label"]
        belieflist_answers = helpers.prompt_belief_list(prompt_data, scale_label=scale_label, reason_label=reason_label)
        #prompts["belieflist"][name]["answers"] = belieflist_answers
        answers.append([prompt_data["prompt"], belieflist_answers])

    today = str(datetime.date.today()).replace("-", "_")

    journal_metadata_file = "journal_metadata_{0}.yaml".format(today)
    affirmations.closing_thoughts()
    with open(journal_metadata_file, 'w') as ofile:
        yaml.dump(answers, ofile, sort_keys=False)
    sys.stderr.write("\n\nWrote journal metadata answers to '{0}'...\n\n".format(journal_metadata_file))

    #print(yaml.dump(answers))
        
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


