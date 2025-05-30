from jsonschema import validate


boolean_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
        "default": {"type": "string"}
    },
    "required": ["prompt_type", "name", "prompt", "description" ]
}


choice_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
        "default": {"type": "string"},
        "choices": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["prompt_type", "name", "prompt", "description", "default", "choices"]
}

multichoice_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
        "default": {
            "type": "array",
            "items": {"type": "string"}
        },
        "choices": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["prompt_type", "name", "prompt", "description", "default", "choices"]
}


text_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["prompt_type", "name", "prompt", "description"]
}



singleline_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["prompt_type", "name", "prompt", "description"]
}





multiline_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["prompt_type", "name", "prompt", "description"]
}


belief_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
        "scale_label": {"type": "string"},
        "reason_label": {"type": "string"},
    },
    "required": ["prompt_type", "name", "prompt", "description"]
}

goal_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "prompt_type": {"type": "string"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "priority": {"type": "number"},
            "effort": {"type": "number"},
            "date": {"type": "string"}
        },
        "required": ["prompt_type", "name", "description", "priority", "effort", "date"]
    }
}


goal_prompt_schema = {
    "type": "object",
    "properties": {
        "prompt_type": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "prompt": {"type": "string"},
        "priority_label": {"type": "string"},
        "effort_label": {"type": "string"},
        "desc_prompt_label": {"type": "string"},
    },
    "required": ["prompt_type", "name", "description", "prompt", "priority_label", "effort_label", "desc_prompt_label"]
}


