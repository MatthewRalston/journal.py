from pydantic import BaseModel, Field, TypeAdapter, ValidationError
from typing import List, Literal, Union, Annotated, Optional

class Goal(BaseModel):
    prompt_type: str
    name: str
    description: str
    priority: int
    effort: int
    date: str

class PromptBase(BaseModel):
    name: str
    prompt: str
    prompt_type: str
    description: str

class GoalPrompt(PromptBase):
    prompt_type: Literal["goal"]
    default: Optional[bool] = None
    choices: Optional[List[str]] = None

    def validate_selections(self, selections: str):
        for s in selections:
            if s not in self.choices:
                raise ValueError("journal.MultiChoicePrompt.validate_selection: Invalid selection '{0}'. Must be one of {1}".format(s, self.choices))

    desc_prompt_label: Optional[str] = "1. Describe the goal in detail"
    effort_label: Optional[str] = "2. Estimate the effort (in days | 1:7)"
    priority_label: Optional[str] = "3. What is the priority? (1:10)"

            
class BooleanPrompt(PromptBase):
    prompt_type: Literal["boolean"]
    default: Optional[bool] = None

class ChoicePrompt(PromptBase):
    prompt_type: Literal["choice"]
    choices: List[str]
    default: Optional[str] = None

    def validate_selection(self, selection: str):
        if selection not in self.choices:
            raise ValueError("journal.ChoicePrompt.validate_selection: Invalid selection '{0}'. Must be one of {1}".format(selection, self.choices))

class MultiChoicePrompt(PromptBase):
    prompt_type: Literal["multichoice"]
    choices: List[str]
    default: Optional[List[str]] = None

    def validate_selections(self, selections: str):
        for s in selections:
            if s not in self.choices:
                raise ValueError("journal.MultiChoicePrompt.validate_selection: Invalid selection '{0}'. Must be one of {1}".format(s, self.choices))

class TextPrompt(PromptBase):
    prompt_type: Literal["text"]
    default: Optional[str] = None

class SingleLinePrompt(PromptBase):
    prompt_type: Literal["singleline"]
    default: Optional[str] = None

class MultiLinePrompt(PromptBase):
    prompt_type: Literal["multiline"]
    default: Optional[str] = None

class BeliefPrompt(PromptBase):
    prompt_type: Literal["belief"]
    default: Optional[dict] = None

    # Custom validation
    scale_min: int = 1
    scale_max: int = 10
    scale_label: Optional[str] = "2. How strong is this belief? (1:10)    "
    reason_label: Optional[str] = "1. Why do you have this belief?    "

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
    Field(discriminator="prompt_type")
]
adapter = TypeAdapter(PromptType)
