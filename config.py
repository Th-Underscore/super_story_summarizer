import copy
import json
import os
from typing import Any, List, Tuple

import gradio as gr

import modules.shared as shared
from modules.chat import generate_chat_prompt
from modules.html_generator import fix_newlines

global textboxes
textboxes: list[gr.Textbox] = []

global current_character
current_character: str = shared.settings["character"]
print(f"current character {current_character}")

_CONFIG_PATH = f"extensions/super_story_summarizer/user_data/config/{current_character}.json"
with open(_CONFIG_PATH, "rt") as handle:
    sbj_tree: dict = json.load(handle)

def updateConfig() -> bool:
    """Update the current config state based on the current selected generation character.

    Returns:
        bool: True if updated, false if not.
    """
    global current_character
    if shared.settings["character"] != current_character:
        current_character = shared.settings["character"]
        global sbj_tree
        with open(f"extensions/super_story_summarizer/user_data/config/{current_character}") as handle:
            sbj_tree = json.load(handle)


        return True
    return False