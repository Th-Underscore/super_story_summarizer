import copy
import json
import pathlib
import pprint
from typing import Any, List, Tuple

import gradio as gr

import modules.shared as shared
from modules.chat import generate_chat_prompt
from modules.html_generator import fix_newlines

_JSON_PATH = "extensions/super_story_summarizer/utils/examples/post_apocalyptic.json"
with open(_JSON_PATH, "rt") as handle:
    _HISTORY = json.load(handle)

print("============ TEST HISTORY ============")
print(_HISTORY)

def read_history():
    """Stringify Super Story Summarizer subject list.
    
    Returns:
        str: Each subject history 
    """
    subjects = {}
    with open(_JSON_PATH, "rt") as handle:
        _HISTORY = json.load(handle)
    # Get current subjects separately from other branches
    recursive_get_subjects(subjects, _HISTORY["current"])

    string = ""
    keys = subjects.keys()
    print(f"keys {keys}")
    for key in keys:
        string += '\n'.join(subjects[key]) + "\n\n"
        print("added \\n\\n")

    return string

def recursive_get_subjects(result: dict, obj: dict):
    """Retrieve all subjects in a parsed history dictionary.

    Args:
        result (dict) -> the result dictionary reference (is modified recursively)

        obj (dict) -> the parsed JSON history dictionary
    """
    print(f"obj {obj}")
    if isinstance(obj, dict):
        print("is dict")
        for value in obj.values():
            print(f"value {value}")
            if isinstance(value, list):
                print(f"is list | old result {result}")
                result.update(obj)
                print(f"new result {result}")
            else:
                print("is not list")
                recursive_get_subjects(result, value)