"""Extension that allows us to fetch and store memories from/to LTM."""

import json
import pathlib
import pprint
import subprocess
from typing import List, Tuple

import gradio as gr

import modules.shared as shared
from modules.chat import generate_chat_prompt
from modules.text_generation import generate_reply
from modules.html_generator import fix_newlines

from extensions.long_term_memory.core.memory_database import LtmDatabase
from extensions.long_term_memory.utils.chat_parsing import clean_character_message
from extensions.long_term_memory.utils.timestamp_parsing import (
    get_time_difference_message,
)

_JSON_PATH = "extensions/super_story_summarizer/utils/example.json"
with open(_JSON_PATH, "rt") as handle:
    _HISTORY = json.load(handle)

print("============ TEST HISTORY ============")
print(_HISTORY)

# === Internal constants (don't change these without good reason) ===
_CONFIG_PATH = "extensions/super_story_summarizer/sss_config.json"
_MIN_ROWS_TILL_RESPONSE = 5
_LAST_BOT_MESSAGE_INDEX = -3
_LTM_STATS_TEMPLATE = """{num_memories_seen_by_bot} memories are loaded in the bot
{num_memories_in_ram} memories are loaded in RAM
{num_memories_on_disk} memories are saved to disk"""
with open(_CONFIG_PATH, "rt") as handle:
    _CONFIG = json.load(handle)

"""# === Module-level variables ===
debug_texts = {
    "current_memory_text": "(None)",
    "num_memories_loaded": 0,
    "current_context_block": "(None)",
}
memory_database = LtmDatabase(
    pathlib.Path("./extensions/super_story_summarizer/user_data/summaries"),
    num_memories_to_fetch=_CONFIG["sss_reads"]["num_memories_to_fetch"],
)"""

print("----------")
print("SSS CONFIG")
print("----------")
print("change these values in sss_config.json")
pprint.pprint(_CONFIG)
print("----------")

def setup():
    print("Loaded Super Story Summarizer!")

def input_modifier(
    user_input,
    state
):
    bot_name = state["name1"]
    user_name = state["name2"]

    print("Context:")
    print(state["context"])

    print("Input:")
    print(user_input)

    print("========== STATE ==========")
    print(state)

    history = state["history"]["internal"]
    print("History:")
    print(f"{history} ::: {not history}")

    joinedHistory = ""
    if len(history) != 0:
        for el in history:
            print(f"el {el}")
            joinedHistory = f"{joinedHistory}\n\n\n{bot_name}: {el[0]}\n\n{user_name}: {el[1]}"

    print("Joined history:")
    print(joinedHistory)

    # generate_chat_prompt()

    return user_input


"""def custom_generate_chat_prompt(
    user_input,
    state,
    **kwargs,
):
    ""Main hook that allows us to fetch and store memories from/to LTM.""
    print("=" * 60)

    character_name = state["name2"].strip().lower().replace(" ", "_")
    memory_database.load_character_db_if_new(character_name)

    user_input = fix_newlines(user_input)

    # === Call oobabooga's original generate_chat_prompt ===
    augmented_context = state["context"]
    if memory_context is not None:
        augmented_context = _build_augmented_context(memory_context, state["context"])
    debug_texts["current_context_block"] = augmented_context

    kwargs["also_return_rows"] = True
    state["context"] = augmented_context
    (prompt, prompt_rows) = generate_chat_prompt(
        user_input,
        state,
        **kwargs,
    )

    bot_message = prompt_rows[_LAST_BOT_MESSAGE_INDEX]

    print("name:", state["name2"])
    print("message:", bot_message)

    print("name:", state["name1"])
    print("message:", user_input)
    print("-----------------------")

    return prompt
"""

print("Importing tree_handling.py...")
from extensions.super_story_summarizer.utils.tree_handling import get_custom_prompts
print("Imported!")


characters = {
    "main=type_of_character": {
        "character": [[
            { "name": "John Mush", }, 
            { "name": "Paul Mush" },
            { "name": "Amy Harrison" },
            { "name": "Angelina Washington" }
        ]]
    },
    "secondary=type_of_character": {
        "character": [[{ "name": "Sonya Lopez" }]]
    },
    "side=type_of_character": {
        "character": [[{ "name": "Harry Washington" }]]
    }
}

script = get_custom_prompts(characters)
for line in script:
    print(line)