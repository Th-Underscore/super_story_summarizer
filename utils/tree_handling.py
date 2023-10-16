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
        obj (dict) -> the generation dictionary.\n
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

### TREE VIEW FUNCTIONS
import re
re.findall('....', '1234567890')
(_TREE_SPACE, _TREE_VERTICAL, _TREE_CONNECTOR, _TREE_CORNER) = [
    "    ",
    "│   ",
    "├── ",
    "└── "
]
def recursive_get_tree_string(obj: dict, indent: str = "") -> str:
    """Format all subjects in a parsed history dictionary as a tree string.

    Args:
        obj (dict): the parsed JSON history dictionary.
        indent (str, optional): recursive variable, leave empty.

    Returns:
        str: The tree representation as a string.
    """
    tree = ""
    length = len(obj)
    for index, (key, value) in enumerate(obj.items()):
        if index == length - 1:
            tree += f"{indent}{_TREE_CORNER}{key}\n"
            if isinstance(value, dict): tree += recursive_get_tree_string(value, indent + _TREE_SPACE)
        else:
            tree += f"{indent}{_TREE_CONNECTOR}{key}\n"
            if isinstance(value, dict): tree += recursive_get_tree_string(value, indent + _TREE_VERTICAL)
    return tree

placeholders = {
    "0-0": "characters",
    "1-0": "main",
    "2-0": "John Mush",
    "2-1": "submain",
    "3-0": "Paul Mush",
    "2-2": "Amy Harrison",
    "1-2": "misc",
    "2-3": "secondary",
    "2-4": "side",
    "0-1": "events",
    "1-1": "The First Incursion",
    "1-2": "The Second Incursion",
    "1-3": "The Mush Offensive",
    "4-0": "Whoa this is high",
    "5-0": "Wait, what are you doing?",
    "6-0": "I think this is enough...",
    "7-0": "Hello? What's going on?",
    "8-0": "I'm serious, this is extremely unnecessary.",
    "9-0": "Alright, cut it out.",
    "10-0": "Bro, we're at the tenth branch now.",
    "11-0": "Alright, I'm done.",
    "20-0": "Okay, you're crazy.",
    "0": "root",
    "1": "node",
    "2": "leaf"
}

def recursive_get_tree(obj: dict, level: int=0, branch_id: list[int]=[0], parent_html: str="") -> list:
    """Format all subjects in a parsed history dictionary as a tree string.

    Args:
        obj (dict): the parsed JSON history dictionary.
        level (int, optional): recursive variable, leave empty.
        branch_id (list[int], optional): recursive variable, leave empty.
        parent_html (str, optional): recursive variable, leave empty.

    Returns:
        list[str, list]: The tree representation as a string; the list of textboxes.
    """
    tree = ""
    current_branch_id = 0
    reading_properties = True
    for index, (key, value) in enumerate(obj.items()):
        tb = ""
        if isinstance(value, str):
            current_branch_id = current_branch_id or branch_id[level]
            tree += f'<div class="branch-part branch-property property-div"><textarea class="branch-property branch-text" id="property-branch-{level}-{index}-{current_branch_id}">{key}: {value}</textarea></div>'
            'NOT <LI>!!!!!'
        else:
            if (reading_properties):
                if level != 0: tree += "</div><details open><summary></summary><ul>"
            reading_properties = False
            print(branch_id)
            print(f"isdict {isinstance(value, dict)} | islist {isinstance(value, list)} | type {type(value)}")
            if level < (len(branch_id) - 1):
                branch_id[level] += 1
            else:
                branch_id.append(0)
            current_branch_id = branch_id[level]
            if isinstance(value, dict):
                with gr.Row():
                    tree += f'<li><div class="branch-part"><div class="tree-div"><textarea class="tree-branch branch-text" id="parent-branch-{level}-{index}-{current_branch_id}" placeholder="{placeholders[str(level%3)]}">{key}</textarea></div>{recursive_get_tree(value, level + 1, branch_id)}</ul></details></li>'
                    print("dict textbox created")
            elif isinstance(value, list):
                tree += f'<li><div class="branch-part"><div class="tree-div"><textarea class="tree-branch branch-text" id="parent-branch-{level}-{index}-{current_branch_id}" placeholder="{placeholders[str(level%3)]}">{key}</textarea></div></div></li>'
                print("list textbox created")
    return f'<ul class="tree">{tree}</ul>' if level == 0 else tree

_LIST_PATH = "extensions/super_story_summarizer/utils/examples/character_list.json"
with open(_LIST_PATH, "rt") as handle:
    sbj_list = json.load(handle)

def tree_view():
    tree = recursive_get_tree(sbj_list)
    _HTML_PATH = "extensions/super_story_summarizer/ui/test.html"
    with open(_HTML_PATH, "wt") as f:
        f.write(tree)
    print(f"result tree ::: {tree}")
    return tree