
import sys
import os


import inquirer
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from journal import prompts, schemas

"""
constants/globals
"""
YELLOW = "\033[33m"
RESET = "\033[0m"

question_mark = f"[{YELLOW}?{RESET}] "


kb = KeyBindings()

# Use Ctrl+n to exit text entry
@kb.add('c-n')
def _(event):
    event.app.exit(result=event.app.current_buffer.text)

session = PromptSession(multiline=True, key_bindings=kb)


"""
Helper functions
"""

def prompt_boolean(prompt_data):

    try:
        validate(prompt_data, schemas.boolean_schema)
    except ValidationError as e:
        raise e

        

    prompt = prompts.BooleanPrompt(**prompt_data)
    prompt_obj = prompts.adapter.validate_python(prompt)
    sys.stderr.write(prompt.description + "\n")
    answers = inquirer.prompt([
        inquirer.Confirm(
            name=prompt.name,
            message=prompt.prompt,
            default=prompt.default
        )
    ])
    user_input = answers[prompt.name]
    if type(user_input) is not bool:
        raise ValueError("journal.prompt_boolean expects user input to be a boolean (y/n)")
    return user_input
    #print(prompt_obj.prompt.model_dump_json(indent=2))

def prompt_choice(prompt_data):
    try:
        validate(prompt_data, schemas.choice_schema)
    except ValidationError as e:
        raise e

    prompt = prompts.ChoicePrompt(**prompt_data)
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
    

def prompt_multichoice(prompt_data):

    try:
        validate(prompt_data, schemas.multichoice_schema)
    except ValidationError as e:
        raise e

    prompt = prompts.MultiChoicePrompt(**prompt_data)
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


def prompt_text(prompt_data):

    try:
        validate(prompt_data, schemas.text_schema)
    except ValidationError as e:
        raise e


    prompt = prompts.TextPrompt(**prompt_data)
    sys.stderr.write(prompt.description + "\n")
    user_input = text_input(prompt.prompt)
    if type(user_input) is not str:
        raise TypeError("journal.prompt_text expects a str from user input.")
    return user_input


def prompt_singleline(prompt_data):

    try:
        validate(prompt_data, schemas.singleline_schema)
    except ValidationError as e:
        raise e


    
    prompt = prompts.SingleLinePrompt(**prompt_data)
    sys.stderr.write("\n\n" + prompt.description + "\n\n")
    sys.stderr.write(question_mark + prompt.prompt + "\n")
    user_input = input()
    # print("User input:")
    # print("   >'{0}'<".format(user_input))
    while user_input == "":
        sys.stderr.write("journal.py needs a non-trivial single-line input\n")
        user_input = input()
        
    # if user_input == "":
    #     raise ValueError("journal.prompt_singleline expects a non-trivial single-line input")
    return user_input

def prompt_multiline(prompt_data):
    try:
        validate(prompt_data, schemas.multiline_schema)
    except ValidationError as e:
        raise e


    
    prompt = prompts.SingleLinePrompt(**prompt_data)
    sys.stderr.write("\n\n" + prompt.description + "\n\n")
    sys.stderr.write(question_mark + prompt.prompt + "\n\n")
    sys.stderr.write("List answers (Empty answer ends input.):\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        else:
            lines.append(line)
    return lines


def get_belief(scale_label, reason_label):


    sys.stderr.write(" "*8 + question_mark + reason_label + "\n")
    reason = input()
    if reason == "":
        ValueError("journal.py: empty response")

    sys.stderr.write(" "*8 + question_mark + scale_label + "\n")
    
    belief_score = input()
    if belief_score == "":
        sys.stderr.write("journal.py needs a non-trivial belief score in the range (1 <=> 10)\n")
        raise ValueError("journal.py thinks you don't belief in journal.py")

        
    try:
        belief_score = int(belief_score)
    except ValueError as e:
        sys.stderr.write("\n\njournal.py: Invalid belief score. Your belief is invalid. /s\n\n")
        raise e

    if type(belief_score) is not int or (belief_score < 1 or belief_score > 10):
        raise ValueError("journal.prompt_belief expects a belief score in the range (1 <=> 10)")


        
    return (belief_score, reason)

def prompt_belief(prompt_data):

    try:
        validate(prompt_data, schemas.belief_schema)
    except ValidationError as e:
        raise e



    prompt = prompts.BeliefPrompt(**prompt_data)
    sys.stderr.write("\n\n" + prompt.description + "\n\n")
    
    sys.stderr.write(question_mark + prompt.prompt + "\n\n")

    
    belief_score, reason = get_belief(prompt.scale_label, prompt.reason_label)
    # print("HERE IS A BELIEF")
    # print(belief_score, reason)
    return (belief_score, reason)


def prompt_belief_list(prompt_data):
    try:
        validate(prompt_data, schemas.belief_schema)
    except ValidationError as e:
        raise e
    
    prompt = prompts.BeliefPrompt(**prompt_data)

    sys.stderr.write(question_mark + prompt.prompt + "\n\n")

    
    beliefs = []
    while True:
        try:
            belief_score, reason = get_belief(prompt.scale_label, prompt.reason_label)
            beliefs.append((belief_score, reason))
        except ValueError as e:
            if len(e.args) == 1 and "journal.py" in e.args[0]:
                break
            else:
                sys.stderr.write("Unknown error occurred. Try restating reason for belief")
                raise e

    print("These were the beliefs. I feel incredibly enthused.")
    print(beliefs)
    return beliefs
    

def text_input(prompt):
    sys.stderr.write(question_mark + prompt + "\n")
    text = session.prompt("Enter text (Ctrl+n to submit):\n")
    #print("Your text: \n{0}".format(text))
    return text
