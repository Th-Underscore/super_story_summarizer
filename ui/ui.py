import json
import pathlib
import pprint
import subprocess
import tkinter as tk
from tkinter import ttk
from typing import List, Tuple

import gradio as gr

import modules.shared as shared
from modules.chat import generate_chat_prompt
from modules.text_generation import generate_reply
from modules.html_generator import fix_newlines
from modules.ui import list_interface_input_elements
from modules.ui import gather_interface_values

right_symbol = '\U000027A1'
left_symbol = '\U00002B05'
refresh_symbol = '\U0001f504'  # 🔄

_JSON_PATH = "extensions/super_story_summarizer/utils/examples/post_apocalyptic.json"
with open(_JSON_PATH, "rt") as handle:
    _HISTORY = json.load(handle)

print("Importing tree_handling.py...")
from extensions.super_story_summarizer.utils.tree_handling import *
print("Finished importing tree_handling.py!")


_LIST_PATH = "extensions/super_story_summarizer/utils/examples/character_list.json"
with open(_LIST_PATH, "rt") as handle:
    sbj_list = json.load(handle)

_HTML_PATH = "extensions/super_story_summarizer/ui/ui.html"
with open(_HTML_PATH, "rt") as f:
    html = f.read()

print(recursive_get_tree_string(sbj_list))

_JS_PATH = "extensions/super_story_summarizer/ui/ui.js"
with open(_JS_PATH) as f:
    js = f.read()

def custom_js():
    return js

def ui():
    generate_tree({})

    with gr.Tab('Summary'):
        with gr.Column(scale=0, min_width=150, variant="compact", elem_classes="subject-tree"):
            gr.HTML(html)


    # with gr.Row():
    #     text1 = gr.Textbox(label="t1")
    #     slider2 = gr.Textbox(label="s2")
    #     drop3 = gr.Dropdown(["a", "b", "c"], label="d3")
    # with gr.Row():
    #     with gr.Column(scale=1, min_width=600):
    #         text1 = gr.Textbox(label="prompt 1")
    #         text2 = gr.Textbox(label="prompt 2")
    #         inbtw = gr.Button("Between")
    #         text4 = gr.Textbox(label="prompt 1")
    #         text5 = gr.Textbox(label="prompt 2")
    #     with gr.Column(scale=2, min_width=600):
    #         btn = gr.Button("Go")

from extensions.super_story_summarizer.test import *

def get_inputs_from_tree(tree: dict) -> list:


    return

(_TREE_SPACE, _TREE_VERTICAL, _TREE_CONNECTOR, _TREE_CORNER) = [
    "    ",
    "│   ",
    "├── ",
    "└── "
]

def generate_tree(data: dict):
    with gr.Tab('Subjects'):
        with open(_JSON_PATH, "rt") as handle:
            _HISTORY = json.load(handle)
        with gr.Row():
            with gr.Column(scale=1, min_width=450, variant="compact", elem_classes="subject-tree") as tree:
                inputs = []
                output = gr.HTML(elem_classes="horizontal-scroll")
                btn = gr.Button("Test", elem_id="subject-button")
                # Get current subjects separately from other branches
            print("Getting tree...")
            state = gr.State()
            btn.click(tree_view, inputs, output)
            tree_view()
            print(tree)
            print("Finished getting tree!")
                
                # # for node in tree:
                # #     with gr.Row():
                # #         for branch in node[:-1]:
                # #             gr.Button(branch)
                # #         gr.Textbox(label=node[-1])
            # with gr.Column(scale=0, min_width=150, variant="compact"):
            #     foo_input = gr.Textbox(label="Enter foo", elem_classes="foo", show_label=False)
            #     bar_input = gr.Textbox(label="Enter bar", show_label=False)
            #     baz_input = gr.Textbox(label="Enter baz", show_label=False)
            #     gr.HTML(f"<style>{css}</style>")
            #     inputs = [
            #         gr.HTML(f'<div>{foo_input}</div>', elem_classes="foo"),
            #         gr.HTML(f'<div style="margin-left: 20px;">{bar_input}</div>', elem_classes="foo"),
            #         gr.HTML(f'<div style="margin-left: 40px;">{baz_input}</div>', elem_classes="foo")
            #     ]
            #     output = gr.Textbox()
            #     btn = gr.Button("Test")
            #     # Get current subjects separately from other branches
            #     print("Getting tree...")
            #     btn.click(tree_view, inputs, output)
            #     # # Initial tree
            #     # tree = {
            #     #     "Key 1": "Value 1",
            #     #     "Key 2": "Value 2",
            #     #     "Key 3": "Value 3"
            #     # }

            #     # # Launch the tree editor
            #     # tree_editor(tree, btn)
            #     # # btn.click(create_tree_view, [foo_input, bar_input, baz_input], output)
            #     print(tree)
            #     print("Finished getting tree!")