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



import inquirer
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings
from pydantic import BaseModel, Field, TypeAdapter, ValidationError
from typing import List, Literal, Union, Annotated, Optional

####################
# CONSTANTS
####################

kb = KeyBindings()

prompts_toml = os.path.join(os.path.dirname(__file__), "prompts.toml")



@kb.add('c-n')
def _(event):
    event.app.exit(result=event.app.current_buffer.text)

session = PromptSession(multiline=True, key_bindings=kb)
    
####################
# DATATYPES
####################

class PromptBase(BaseModel):
    name: str
    prompt: str
    type: str
    description: str

class BooleanPrompt(PromptBase):
    type: Literal["boolean"]
    default: Optional[bool] = None

class ChoicePrompt(PromptBase):
    type: Literal["choice"]
    choices: List[str]
    default: Optional[str] = None

    def validate_selection(self, selection: str):
        if selection not in self.choices:
            raise ValueError("journal.ChoicePrompt.validate_selection: Invalid selection '{0}'. Must be one of {1}".format(selection, self.choices))

class MultiChoicePrompt(PromptBase):
    type: Literal["multichoice"]
    choices: List[str]
    default: Optional[List[str]] = None

    def validate_selections(self, selections: str):
        for s in selections:
            if s not in self.choices:
                raise ValueError("journal.MultiChoicePrompt.validate_selection: Invalid selection '{0}'. Must be one of {1}".format(s, self.choices))

class TextPrompt(PromptBase):
    type: Literal["text"]
    default: Optional[str] = None

class SingleLinePrompt(PromptBase):
    type: Literal["singleline"]
    default: Optional[str] = None

class MultiLinePrompt(PromptBase):
    type: Literal["multiline"]
    default: Optional[str] = None

class BeliefPrompt(PromptBase):
    type: Literal["belief"]
    default: Optional[dict] = None

    # Custom validation
    scale_min: int = 1
    scale_max: int = 10
    scale_label: Optional[str] = "How strong is this belief?"
    reason_label: Optional[str] = "Why?"

PromptType = Annotated[
    Union[
        BooleanPrompt,
        ChoicePrompt,
        MultiChoicePrompt,
        TextPrompt,
        SingleLinePrompt,
        MultiLinePrompt,
        BeliefPrompt
    ],
    Field(discriminator="type")
]
adapter = TypeAdapter(PromptType)


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

def prompt_boolean():
    prompt_data = {
        "type": "boolean",
        "name": "bool_ex",
        "prompt": "Do you enjoy programeing",
        "description": "If you like programming please input True or False",
        "default": "False"
    }

    prompt = BooleanPrompt(**prompt_data)
    prompt_obj = adapter.validate_python(prompt)
    sys.stderr.write(prompt.description + "\n")
    answers = inquirer.prompt([
        inquirer.Confirm(
            name=prompt.name,
            message=prompt.prompt,
            default=prompt.default
        )
    ])
    try:
        user_input = answers[prompt.name]
    except ValidationError as e:
        raise e
    return user_input
    #print(prompt_obj.prompt.model_dump_json(indent=2))

def prompt_choice():
    prompt_data = {
        "type": "choice",
        "name": "choice_ex",
        "prompt": "Do you enjoy programeing?",
        "description": "If you like programming please input True, False, or maybe",
        "default": "False",
        "choices": ["True", "False", "Maybe"]
    }

    prompt = ChoicePrompt(**prompt_data)
    sys.stderr.write(prompt.description + "\n")
    answers = inquirer.prompt([
        inquirer.List(
            name=prompt.name,
            message=prompt.prompt,
            choices=prompt.choices,
            default=prompt.default
        )])
    try:
        user_input = answers[prompt.name]
        prompt.validate_selection(user_input)
    except ValidationError as e:
        raise e
    return user_input
    

def prompt_multichoice():
    prompt_data = {
        "type": "multichoice",
        "name": "multichoice_ex",
        "prompt": "Select from the following",
        "description": "What languages do you like?",
        "default": ["Python"],
        "choices": ["Python", "Ruby", "Julia", "Javascript", "Rust", "R"]
    }
    prompt = MultiChoicePrompt(**prompt_data)
    sys.stderr.write(prompt.description + "\n")
    answers = inquirer.prompt([
        inquirer.Checkbox(
            name=prompt.name,
            message=prompt.prompt,
            choices=prompt.choices,
            default=prompt.default
        )
    ])

    try:
        user_input = answers[prompt.name]
        prompt.validate_selections(user_input)
        # print("Selections:")
        # print(user_input)
    except ValidationError as e:
        raise e
    return user_input


def prompt_text():
    prompt_data = {
        "type": "text",
        "name": "text_ex",
        "prompt": "Describe what you enjoy about programming",
        "description": "Do you like programming?",
    }
    prompt = TextPrompt(**prompt_data)
    sys.stderr.write(prompt.description + "\n")
    user_input = text_input(prompt.prompt)
    if type(user_input) is not str:
        raise TypeError("journal.prompt_text expects a str from user input.")
    return user_input
        

def get_multiline(prompts):
    if not all(type(p) is str for p in prompts):
        raise TypeError("multiline expects a list of str as its first positional argument")

    answers = []
    for p in prompts:
        lines = []
        sys.stderr.write(p + " : (One line at a time)\n")
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        print(lines)
        answers.append(lines)
    return answers

def text_input(prompt):

    sys.stderr.write(prompt + "\n")
    text = session.prompt("Enter text (Ctrl+n to submit):\n")
    #print("Your text: \n{0}".format(text))
    return text

def main():
    with open(prompts_toml, 'rb') as ifile:
        prompts = tomllib.load(ifile)
        print(prompts)
        #first = text_input("foo")
    prompt_boolean()
    prompt_choice()
    prompt_multichoice()
    prompt_text()

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


