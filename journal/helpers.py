import os
import sys

import datetime
import re



import inquirer

from pygments import highlight
from pygments.formatters import Terminal256Formatter

from pygments.lexers import TextLexer
from pygments.lexer import Lexer
from pygments.style import Style

from pygments.token import Token



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


class JournalPromptStyle(Style):
    default_style = ""
    styles = {
        Token.Text: "bg:#002200 #00ff00",
    }


class PlainGreenLexer(Lexer):
    def get_tokens_unprocessed(self, text):
        yield 0, Token.Text, text
    
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


    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    
    sys.stderr.write(highlighted)

    answers = inquirer.prompt([
        inquirer.Confirm(
            name=prompt.name,
            message=prompt.prompt,
            default=False
        )
    ])
    user_input = answers[prompt.name]
    #sys.stderr.write(">'{0}'<\n".format(user_input))
    if type(user_input) is not bool:
        sys.stderr.write(">'{0}'<\n".format(user_input))
        raise ValueError("journal.prompt_boolean expects user input to be a boolean (y/n)")
    return user_input
    #print(prompt_obj.prompt.model_dump_json(indent=2))

def prompt_choice(prompt_data):
    try:
        validate(prompt_data, schemas.choice_schema)
    except ValidationError as e:
        raise e

    prompt = prompts.ChoicePrompt(**prompt_data)

    
    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    
    sys.stderr.write(highlighted)


    
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

    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    
    sys.stderr.write(highlighted)

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

    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    
    sys.stderr.write(highlighted)

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

    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    
    sys.stderr.write(highlighted)

    sys.stderr.write(question_mark + prompt.prompt + "\n")
    user_input = input(">")
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


    
    prompt = prompts.MultiLinePrompt(**prompt_data)

    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    
    sys.stderr.write(highlighted)

    sys.stderr.write(question_mark + prompt.prompt + "\n\n")
    sys.stderr.write("List your answers below (Empty response terminates):\n")
    lines = []
    while True:
        line = input(">")
        if line == "":
            break
        else:
            lines.append(line)
    return lines

def get_goal(prompt, goal_prompt_description, desc_prompt_label, priority_label, effort_label):
    """
    This function prompts the user, with given labels, for a goal name, description, a priority, and a effort score (in # of days)
    """

    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(goal_prompt_description), goal_prompt_description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    sys.stderr.write(highlighted)
    sys.stderr.write(question_mark + prompt + "\n\n")
    goal_short_desc = input(">") # GET goal name

    
    sys.stderr.write(" "*8 + question_mark + desc_prompt_label + "\n")
    goal_desc = input(">") # GET goal description
    sys.stderr.write(" "*8 + question_mark + priority_label + "\n")
    priority = input("(1:10) >") # GET goal priority
    sys.stderr.write(" "*8 + question_mark + effort_label + "\n")
    effort = input("(1:60) >") # GET goal effort

    if goal_short_desc == "" and goal_desc == "" and priority == "" and effort == "":
        return None, None, None, None
    elif priority.isnumeric() and effort.isnumeric():
        priority = int(priority)
        effort = int(effort)
        pass
    else:
        raise ValueError("\n\njournal.py: Invalid goal, description, priority, or effort estimate. Inputs should be strings or integers\n\n")

    if priority > 10 or priority < 1 or effort < 1 or effort > 60:
        raise ValueError("\n\njournal.py: Invalid priority/effort. See scale above for priority/effort\n\n")
    return goal_short_desc, goal_desc, priority, effort
    

def get_belief(scale_label, reason_label):
    sys.stderr.write(" "*8 + question_mark + reason_label + "\n")
    reason = input(">")
    sys.stderr.write(" "*8 + question_mark + scale_label + "\n")
    
    belief_score = input("(0:10) >")

    if reason == "" and belief_score == "":
        return None, None
    elif re.match(r'^-?\d+(?:\.\d+)$', belief_score) is not None: # Catches float
        #sys.stderr.write("Belief score was a float\n")
        belief_score = float(belief_score)
        pass
    elif belief_score.isnumeric(): # Only catches int
        #sys.stderr.write("Belief score was a int\n")
        belief_score = int(belief_score)
        pass
    else:
        raise ValueError("\n\njournal.py: Invalid score/rating. Input should be a number on a scale of 0-10\n\n")

        # try:
        #     belief_score = int(belief_score)
        # except ValueError as e:
        #     sys.stderr.write("\n\njournal.py: Invalid belief score. Your belief is invalid. /s\n\n")
        #     raise e

    if (belief_score < 0 or belief_score > 10):
        raise ValueError("journal.prompt_belief expects a belief score in the range (0 <=> 10)")


        
    return (belief_score, reason)

def prompt_belief(prompt_data):

    try:
        validate(prompt_data, schemas.belief_schema)
    except ValidationError as e:
        raise e



    prompt = prompts.BeliefPrompt(**prompt_data)

    desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
    highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
    
    
    sys.stderr.write(highlighted)
    
    sys.stderr.write(question_mark + prompt.prompt + "\n\n")

    
    belief_score, reason = get_belief(prompt.scale_label, prompt.reason_label)
    # print("HERE IS A BELIEF")
    # print(belief_score, reason)
    return (belief_score, reason)


def prompt_belief_list(prompt_data, scale_label:str=None, reason_label:str=None):
    if scale_label is not None and reason_label is not None:
        alt_labels = True
    else:
        alt_labels = False
        
    try:
        validate(prompt_data, schemas.belief_schema)
    except ValidationError as e:
        raise e
    
    prompt = prompts.BeliefPrompt(**prompt_data)

    sys.stderr.write(question_mark + prompt.prompt + "\n\n")

    
    beliefs = []
    while True:
        try:
            if alt_labels == True:
                belief_score, reason = get_belief(scale_label, reason_label)
            else:
                belief_score, reason = get_belief(prompt.scale_label, prompt.reason_label)
            if belief_score is None and reason is None:
                break
            else:
                beliefs.append([belief_score, reason])
        except ValueError as e:
            raise e
            if len(e.args) == 1 and "journal.py" in e.args[0]:
                break
            else:
                sys.stderr.write("Unknown error occurred. Try restating reason for belief")
                raise e

    return beliefs
    

def text_input(prompt):
    sys.stderr.write(question_mark + prompt + "\n")
    text = session.prompt("Enter text (Ctrl+n to submit):\n")
    #print("Your text: \n{0}".format(text))
    return text


def create_goal_list(goals):
    no_goals = False

    if type(goals) is not list:
        raise TypeError("journal.helpers.create_goal_list expects a list as its first positional argument")
    elif len(goals) == 0:
        no_goals = True
    elif not all([type(g) is dict for g in goals]):
        raise TypeError("journal.helpers.create_goal_list expects a list of dictionaries as its first positional argument")
    
    today = str(datetime.datetime.today())
    existing_goals_list = []
    new_goals_list = []
    existing_goals_prompt_data = {
        "prompt_type": "goal",
        "name": "existing_goals",
        "prompt": "Which goals should you continue to pursue?",
        "description": "Select existing goals below to focus"
    }
    
    new_goals_prompt_data = {
        "prompt_type": "goal",
        "name": "goal_list",
        "prompt": "Create a goal (short description, long description, priority, and effort)",
        "description": "Focus on habits, work, and deliverables",
        "priority_label": "What is the priority?",
        "effort_label": "Estimate the effort (in days)",
        "desc_prompt_label": "Describe the goal. Be verbose for me.",
    }
    try:
        if no_goals is False:
            validate(goals, schemas.goal_schema)
            sys.stderr.write("\n\nExisting goals read and validated successfully...\n\n")
        validate(new_goals_prompt_data, schemas.goal_prompt_schema)
    except ValidationError as e:
        raise e



    """
    Custom code to re-select existing goals read from the goals.json file
    """
    # [TODO] HERE the 'choices' option is populated with the goal name

    if no_goals is False:
        existing_goals_prompt_data["choices"] = list(map(lambda g: g["name"], goals))
        prompt = prompts.GoalPrompt(**existing_goals_prompt_data)

    
        desc = "{0}\n{0}\n{1}\n{0}\n{0}".format(" "*len(prompt.description), prompt.description)
        highlighted = highlight(desc, PlainGreenLexer(), Terminal256Formatter(style=JournalPromptStyle))
        sys.stderr.write(highlighted)

    
        answers = inquirer.prompt([
            inquirer.Checkbox(
                name=prompt.name,
                message=prompt.prompt,
                choices=prompt.choices,
                default=prompt.default
            )
        ])
        try:
            existing_goal_names = answers[prompt.name]
            prompt.validate_selections(existing_goal_names)
            # print("Selections:")
            # print(user_input)
        except ValidationError as e:
            raise e
        sys.stderr.write("\n\nRe-selected goals: {0}\n\n".format(existing_goal_names))

        existing_goals_list = [g for g in goals if g["name"] in existing_goal_names]
        sys.stderr.write("\n\nFinished assessing existing goals...\n\n\n")

    """
    New goals
    """
    #print(new_goals_prompt_data)
    prompt = prompts.GoalPrompt(**new_goals_prompt_data)

    name = new_goals_prompt_data["name"]
    description = new_goals_prompt_data["description"]
    prompt = new_goals_prompt_data["prompt"]
    priority_label = new_goals_prompt_data["priority_label"]
    effort_label = new_goals_prompt_data["effort_label"]
    desc_prompt_label = new_goals_prompt_data["desc_prompt_label"]

    """
    Hoisted code to get additional goal descriptions, priorities, efforts.
    """
    while True:
        try:
            name, goal_desc, priority, effort = get_goal(prompt, description, desc_prompt_label, priority_label, effort_label)
            if goal_desc is None and priority is None and effort is None:
                break
            else:
                new_goals_list.append({
                    "prompt_type": "goal",
                    "name": name,
                    "description": goal_desc,
                    "priority": priority,
                    "effort": effort,
                    "date": today
                })
        except ValueError as e:
            raise e
            if len(e.args) == 1 and "journal.py" in e.args[0]:
                break
            else:
                sys.stderr.write("Unknown error occurred.")
                raise e
    final_goals_list = new_goals_list + existing_goals_list
    return final_goals_list
