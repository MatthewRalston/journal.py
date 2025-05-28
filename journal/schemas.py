from jsonschema import validate


boolean_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
        "default": {"type": "string"}
    },
    "required": ["type", "name", "prompt", "description" ]
}


choice_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
        "default": {"type": "string"},
        "choices": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["type", "name", "prompt", "description", "default", "choices"]
}

multichoice_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
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
    "required": ["type", "name", "prompt", "description", "default", "choices"]
}


text_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["type", "name", "prompt", "description"]
}



singleline_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["type", "name", "prompt", "description"]
}





multiline_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
    },
    "required": ["type", "name", "prompt", "description"]
}


belief_schema = {
    "type": "object",
    "properties": {
        "type": {"type": "string"},
        "name": {"type": "string"},
        "prompt": {"type": "string"},
        "description": {"type": "string"},
        "scale_label": {"type": "string"},
        "reason_label": {"type": "string"},
    },
    "required": ["type", "name", "prompt", "description"]
}

