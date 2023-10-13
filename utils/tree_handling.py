import copy
import json
import pathlib
import pprint
from typing import Any, List, Tuple

import gradio as gr

import modules.shared as shared
from modules.chat import generate_chat_prompt
from modules.html_generator import fix_newlines

def get_readable_list(seq: list) -> str:
    """Return a grammatically correct human readable string (with an Oxford comma)
    Ref: https://stackoverflow.com/a/53981846/

    Args:
        seq (list) -> the list to stringify.

    Returns:
        str -> the list as a readable string.
    """
    
    seq = [str(s) for s in seq]
    if len(seq) < 3:
        return ' and '.join(seq)
    return ', '.join(seq[:-1]) + ', and ' + seq[-1]

test_subjects = {
    "main": [ { "name": "", "properties": { 1, 2, 3, 4, 5 } }, {} ],
    "gen1": [ { "name": "" }, {} ],
    "secondary": [ { "name": "" }, {} ]
}

def recursive_get_keys(obj: dict, result: dict, properties: list={}):
    """Get all keys of each branch in the generation dictionary.

    Args:
        obj (dict) -> the generation dictionary\n
        result (list) -> the list reference to be modified.\n
        generations (dict) -> the generation order of each subject.\n
        properties (list, optional) -> recursive variable, leave empty.
    """
    # Recursively loop keys (i.e. "value=type") in dictionary.
    for (obj_key, obj_value) in obj.items(): # i.e. main with 1 recursion
        if isinstance(obj_value, list):
            for sbj in obj_value: # i.e. main.character[0] with 2 recursions
                # Create copy of current properties for each subject.
                sbj_properties = copy.copy(properties)
                # Get generation key of subject, default to last property.
                generation_key = sbj.get("generation_key", [*sbj_properties.values()][-1])
                # Get all subject properties.
                for (sbj_key, sbj_value) in sbj.items(): # i.e. main.character[0].prompt with 2 recursions
                    # Get name of subject.
                    if sbj_key == "name":
                        name = sbj_value
                    # Exclude "name" key from properties.
                    else:
                        sbj_properties[sbj_key] = sbj_value
                print(f"generation key {generation_key} | name {name}")
                # Add subject name and properties to result using generation key.
                result.setdefault(generation_key, []).append({"name": name, "properties": sbj_properties})
        elif isinstance(obj_value, str):
            properties[obj_key] = obj_value
        elif isinstance(obj_value, dict):
            # Loop recursively if value is a dictionary.
            recursive_get_keys(obj_value, result, copy.copy(properties))
        
def parse_prompts(data: list):
    """Replace placeholders (i.e. "[key]") in string with formatted list.

    Args:
        string (str): The prompt string
        data (list): The generation prompts and properties.

    Returns:
        list: The list of prompts to use for generation.
    """
    
    print(data)
    prompts = []
    for generation in data: # i.e. main or gen1
        # Total dictionary of prompts for current generation
        generation_prompt = {}
        for sbj in generation:
            sbj_properties = sbj["properties"]
            sbj_prompt = sbj_properties["prompt"]
            for (key, property) in sbj_properties.items(): # i.e. type_of_character
                # Find placeholders in string and replace with property value.
                sbj_prompt = sbj_prompt.replace("{" + key + "}", property)
            # Add subject name to list with prompt as key.
            generation_prompt.setdefault(sbj_prompt, []).append(sbj["name"])
        # Loop all collected prompts.
        generation_prompts = ""
        for (prompt, names) in generation_prompt.items():
            # Format value as English-readable string (i.e. "1, 2, and 3").
            formatted_list = get_readable_list(names)
            prompt = prompt.replace("{name}", formatted_list)
            generation_prompts += f"{prompt}\n"
        prompts.append(generation_prompts)
    return prompts

"""
Please make a summary for each of these {type_of_character} characters:
...
...

example_summary_config = {
    "characters": {
        "type_of_subject": "characters",
        "prompt": "This is an example. Type: {type_of_character}, name: {character}, extra list: {extra_list}",
        "main": {
            "type_of_character": "main",
            "values": [
                { "name": "char1" },
                { "name": "char2" },
                { "name": "char0", "prompt": "Hello, I am {character}, a {type_of_character} character.", "generation_key": "gen1" }
            ]
        },
        "secondary": {
            "type_of_character": "secondary",
            "values": [
                { "name": "char3" },
                { "name": "char4", "generation_key": "gen1" },
                { "name": "char5" },
                { "name": "char6" },
            ]
        },
        "extra": {
            "type_of_character": "extra",
            "sub": {
                "extra_list": "sub",
                "values": [
                    { "name": "char7" },
                    { "name": "char8" }
                ]
            },
            "sub2": {
                "extra_list": "sub2",
                "values": [
                    { "name": "char9" },
                    { "name": "char10" }
                ]
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
    result = {}
    recursive_get_keys(tree, result)

    string = "{character} is/are [a] {type_of_character} character(s). Please write a summary on {character}'s personality, relations, and overall actions in this story."
    return parse_prompts(result.values())