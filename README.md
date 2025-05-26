# README

## journal.py

journal is a Python command line tool for creating prompts according to different prompt response requirements. My goal is to list a number of prompts in a configurable `.toml` file and produce simplified metadata/answers to add to my journal file in the mornings. By cutting boiler-plate prompts/descriptions and niceties (mantras, quotes, reminders, etc.), I can simplify my journaling and journal parsing experiences. 

## Prompt Types

1. boolean: (y/n) true or false. Uses inquirer.
2. choice: choice from list. Uses inquirer.
3. multichoice: choices from list. Uses inquirer.
4. text: multi-line input.
5. singleline: single, one-line response to question
6. multiline: multiple one-line responses to question
7. belief: make a statement and a confidence score in the statement

```bash
>git clone https://github.com/MatthewRalston/journal.py.git && cd journal.py
>pip install .
>journal # answer questions. Ctrl-n exits text entry, empty/newline terminates multiline capture
                                                        
                                                         
In the last week, have you called or texted your friends? 
                                                         
                                                         
[?] Are you talking to your friends? (y/N): N
                                                             
                                                             
What is your plan for groceries, mealprep, and cooking today?
                                                             
                                                             
[?] Are you cooking today? (y/N): y

                                          
                                          
Are you going to walk, run, or lift today?
                                          
                                          
[?] Are you exercising today? (y/N): N

```
