from pydantic import BaseModel, Field, TypeAdapter, ValidationError
from typing import List, Literal, Union, Annotated, Optional



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
    Field(discriminator="type")
]
adapter = TypeAdapter(PromptType)
