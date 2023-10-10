import copy
import json
import pathlib
import pprint
from typing import Any, List, Tuple

import gradio as gr

import modules.shared as shared
from modules.chat import generate_chat_prompt
from modules.html_generator import fix_newlines

def get_readable_list(seq: List[Any]) -> str:
    # Return a grammatically correct human readable string (with an Oxford comma).
    # Ref: https://stackoverflow.com/a/53981846/
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return ' and '.join(seq)
    return ', '.join(seq[:-1]) + ', and ' + seq[-1]

def recursive_get_keys(obj, result, keys={}):
    # Recursively loop keys (i.e. "value=type") in JSON dictionary.
    if isinstance(obj, dict):
        for obj_key in obj.keys(): # i.e. main=type_of_character with 1 recursion
            # Looped value of current dictionary
            value = obj[obj_key]
            split_obj_key = obj_key.split("=")
            # If splitter doesn't exist (i.e. "type") and value is a list
            if (len(split_obj_key) == 1) & isinstance(value, list):
                for sbj in value: # i.e. main=type_of_character.character[0] with 2 recursions
                    # Get override strings.
                    overrides = sbj["overrides"]
                    for override_key in overrides.keys(): # i.e. main=type_of_character.character[0].overrides.character with 2 recursions
                        keys[override_key] = overrides[override_key]
                    keys[obj_key] = sbj["names"]
                    result.append(copy.deepcopy(keys))
            else:
                # Let key_value be the left side of splitter ("="), key_name be the right side.
                (key_value, key_name) = split_obj_key
                keys[key_name] = key_value
                # Recursive loop if value is a dictionary
                if isinstance(value, dict):
                    recursive_get_keys(value, result, copy.deepcopy(keys))
        
def parse_string(string, data):
    # Replace placeholders (i.e. "[key]") in string with formatted list.
    script = []
    for item in data:
        line = string
        for (key, value) in item.items():
            # Format value as English-readable string (i.e. "1, 2, and 3").
            formatted_list = get_readable_list(value) if isinstance(value, list) else value
            # Find placeholders in string and replace with formatted list.
            line = line.replace("{" + key + "}", formatted_list)
        script.append(line)
    return script

"""
subjects = {
    "characters=type_of_subject": {
        "$prompt=$prompt": "",
        "main=type_of_character": {
            "character": [
                {
                    "overrides": {},
                    "names": [ "char1", "char2" ],
                },
                {
                    "overrides": { "$prompt": "Hello, I am {character}, a {type_of_character} character." },
                    "names": [ "char0" ]
                }
            ]
        },
        "secondary=type_of_character": {
            "character": [{
                "overrides": {},
                "names": [ "char3", "char4", "char5", "char6" ]
            }]
        },
        "extra=type_of_character": {
            "sub=extra_list": {
                "character": [{
                    "overrides": {},
                    "names": [ "char7", "char8" ]
                }]
            },
            "sub2=extra_list": {
                "character": [{
                    "overrides": {},
                    "names": [ "char9", "char10" ]
                }]
            }
        }
    }
}

"This is an example. Type: {type_of_character}, name: {character}, extra list: {extra_list}" --- Output:
This is an example. Type: main, name: char 1 and char 2, extra list: {extra_list}
This is an example. Type: main, name: char 0, extra list: {extra_list}
This is an example. Type: secondary, name: char 3, char 4, char 5, and char 6, extra list: {extra_list}
This is an example. Type: extra, name: char 7 and char 8, extra list: sub
This is an example. Type: extra, name: char 9 and char 10, extra list: sub2
"""

def get_custom_prompts(tree):
    result = []
    recursive_get_keys(tree, result)

    string = "{character} is/are [a] {type_of_character} character(s). Please write a summary on {character}'s personality, relations, and overall actions in this story."
    return parse_string(string, result)