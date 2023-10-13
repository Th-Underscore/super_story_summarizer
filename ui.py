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

print("Importing history_parser.py...")
from extensions.super_story_summarizer.utils.history_parser import *
print("Finished importing history_parser.py!")

def ui():
    generate_tree({})

    with gr.Tab('Summary'):
        ''


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

def generate_tree(data: dict):
    with gr.Tab('Subjects'):
        tree: list[list[str]] = []
        with open(_JSON_PATH, "rt") as handle:
            _HISTORY = json.load(handle)
        with gr.Row():
            with gr.Column(scale=0, min_width=600, variant="compact"):
                # Get current subjects separately from other branches
                print("Getting tree...")
                recursive_get_tree(_HISTORY["current"])
                print(tree)
                print("Finished getting tree!")
                # for node in tree:
                #     with gr.Row():
                #         for branch in node[:-1]:
                #             gr.Button(branch)
                #         gr.Textbox(label=node[-1])