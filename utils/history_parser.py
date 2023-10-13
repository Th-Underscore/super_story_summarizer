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
    recursive_get_subjects(_HISTORY["current"], subjects)

    string = ""
    keys = subjects.keys()
    print(f"keys {keys}")
    for key in keys:
        string += '\n'.join(subjects[key]) + "\n\n"
        print("added \\n\\n")

    return string

def recursive_get_subjects(obj: dict, result: dict):
    """Retrieve all subject histories in a parsed history dictionary.

    Args:
        obj (dict) -> the parsed JSON history dictionary.\n
        result (dict) -> the result dictionary reference (modified recursively).
    """
    if isinstance(obj, dict):
        for (key, value) in obj.items():
            if isinstance(value, list):
                result.update(obj)
            else:
                recursive_get_subjects(value, result)

import re
re.findall('....', '1234567890')
(_TREE_SPACE, _TREE_VERTICAL, _TREE_CONNECTOR, _TREE_CORNER) = [
    "    ",
    "│   ",
    "├── ",
    "└── "
]

def recursive_get_tree(obj: dict, indent: str = "") -> str:
    """Format all subjects in a parsed history dictionary as a tree.

    Args:
        obj (dict): the parsed JSON history dictionary.
        indent (str, optional): recursive variable, leave empty.

    Returns:
        str: The tree representation as a string.
    """
    tree = ""
    length = len(obj)
    for index, (key, value) in enumerate(obj.items()):
        if isinstance(value, dict):
            if index == length - 1:
                tree += f"{indent}{_TREE_CORNER}{key}\n"
                tree += recursive_get_tree(value, indent + _TREE_SPACE)
            else:
                tree += f"{indent}{_TREE_CONNECTOR}{key}\n"
                tree += recursive_get_tree(value, indent + _TREE_VERTICAL)
        else:
            if index == length - 1:
                tree += f"{indent}{_TREE_CORNER}{key}\n"
            else:
                tree += f"{indent}{_TREE_CONNECTOR}{key}\n"
    return tree

def edit_tree(obj: dict) -> dict:
    return obj

def display_tree_and_edit(obj: dict) -> dict:
    tree = "test"
    return { "tree": tree, "edited_tree": edit_tree(obj) }

def create_tree_view(foo: str, bar: str, baz: str):
    # for arg in args:
    #     tree.update(arg)
    tree = { foo: { bar: { baz: "qux" } } }
    tree_string = recursive_get_tree(tree)
    print(tree_string)
    return tree_string

    # if isinstance(obj, dict):
    #     items = obj.items()
    #     length = len(items)
    #     print(f"length {length} | range {range(0, length-1)}")
    #     for i, (key, value) in enumerate(items):
    #         new_indent = [ *indent, key ]
    #         print(f"i {i}")
    #         with gr.Row():
    #             if i != length:
    #                 print(f"i {i} != length {length}")
    #                 gr.Markdown("├")
    #             else:
    #                 print(f"i {i} == length {length}")
    #                 gr.Markdown("└")
    #         if isinstance(value, dict):
    #             recursive_get_tree(value, new_branch)
    #         else:
    #             ''