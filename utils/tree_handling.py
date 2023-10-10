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
    # Recursively loop keys ("value=type") in JSON dictionary.
    if isinstance(obj, dict):
        for key in obj.keys():
            # Looped value of current dictionary
            value = obj[key]
            split_key = key.split("=")
            # If splitter doesn't exist ("type") and value is a list
            if (len(split_key) == 1) & isinstance(value, list):
                for sbj in value:
                    keys[key] = sbj
                    result.append(copy.deepcopy(keys))
            # Recursive loop if value is a dictionary
            elif isinstance(value, dict):
                # Let key_value be left side of splitter ("="), key_name be right side.
                (key_value, key_name) = split_key
                keys[key_name] = key_value
                recursive_get_keys(value, result, copy.deepcopy(keys))
        
def parse_string(string, data):
    # Replace placeholders ("[key]") in string with formatted list.
    script = []
    for item in data:
        line = string
        for (key, value) in item.items():
            # Format value as English-readable string ("1, 2, and 3").
            formatted_list = get_readable_list(value) if isinstance(value, list) else value
            # Find placeholders in string and replace with formatted list.
            line = line.replace("{" + key + "}", formatted_list)
        script.append(line)
    return script

"""
characters = {
    "$prompt_override": "",
    "main=type_of_character": {
        "character": [["char1", "char2"], ["char0"]] # { "name": "char1", "$prompt_override": "...", "type_of_character_override": "..." }
    },
    "secondary=type_of_character": {
        "character": [["char3", "char4", "char5", "char6"]]
    },
    "extra=type_of_character": {
        "sub=extra_list": {
            "character": [["char7", "char8"]]
        },
        "sub2=extra_list": {
            "character": [["char9", "char10"]]
        }
    }
}

"This is an example. Type: [type_of_character], name: {character}, extra list: [extra_list]" --- Output:
This is an example. Type: main, name: char 1 and char 2, extra list: [extra_list]
This is an example. Type: main, name: char 0, extra list: [extra_list]
This is an example. Type: secondary, name: char 3, char 4, char 5, and char 6, extra list: [extra_list]
This is an example. Type: extra, name: char 7 and char 8, extra list: sub
This is an example. Type: extra, name: char 9 and char 10, extra list: sub2
"""

def get_custom_prompts(tree):
    result = []
    recursive_get_keys(tree, result)

    string = "{character} is/are [a] {type_of_character} character(s). Please write a summary on {character}'s personality, relations, and overall actions in this story."
    return parse_string(string, result)