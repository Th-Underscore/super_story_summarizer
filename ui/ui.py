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

import extensions.super_story_summarizer.config as config

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

_JS_PATH = "extensions/super_story_summarizer/ui/ui.js"
with open(_JS_PATH) as f:
	js = f.read()

url = f"{shared.args.listen_host or '127.0.0.1'}:{shared.args.listen_port or '7860'}"
js = js.replace("LISTEN_HOST", f'"{url}"')

def custom_js():
	return js

global test_state

def ui():
	generate_subjects_tab()

	with gr.Tab('Summary'):
		with gr.Column(scale=0, min_width=150, variant="compact", elem_classes="subject-tree"):
			gr.HTML(html)
	from gradio_client import Client
	test_box = gr.Textbox(placeholder="Write here")
	global test_state
	test_state = gr.State({})
	js = """
() => {
	let superStorySummarizer = window.superStorySummarizer;
	console.log(superStorySummarizer);
	return superStorySummarizer;
}
"""
	test_box.input(fn=None, inputs=test_box, outputs=test_state, _js=js).then(fn=return_fn(), _js="() => console.log(`Yo`)") # Have to use button.click() in JS to force function??

def return_fn():
	print("return fn")
	return print_state

def print_state():
	print("??????????????")
	global test_state
	print(f"============= test state!!! =============")
	print(f"state {test_state.value}")

def set_value():
	return

with open("extensions/super_story_summarizer/utils/getTreeBranches.js", "rt") as f:
	tree_js = f.read()

def generate_subjects_tab():
	with gr.Tab('Subjects'):
		with gr.Row():
			with gr.Column(scale=1, min_width=850, variant="compact", elem_classes="subject-tree") as tree:
				inputs = []
				output = gr.HTML(elem_classes="horizontal-scroll")
				btn = gr.Button("Test", elem_id="subject-button")
			create_tree_textboxes()
			tree.update()
			test_state = gr.State("")
			print("Getting tree...")
			btn.click(tree_view, inputs, output).then(fn=None, _js=tree_js)
			print("Finished getting tree!")

def create_tree_textboxes():
	config.textboxes = []
	for i in range(100):
		textbox = gr.Textbox(value=f"{i}", visible=True, elem_id=f"textbox-placeholder-{i}", show_label=False, interactive=True, max_lines=1)
		textbox.submit(fn=None, _js="")
		textbox.blur(fn=None, _js="")
		textbox.elem_classes = []
		config.textboxes.append(textbox)

def tree_view():
	(tree, n_branches) = generate_tree(config.sbj_tree)
	# Loop remaining textboxes
	for i in range(n_branches, 100):
		config.textboxes[i].visible = False
	_HTML_PATH = "extensions/super_story_summarizer/ui/test.html"
	with open(_HTML_PATH, "wt") as f:
		f.write(tree)
	# print(f"result tree ::: {tree}")
	return tree

def get_inputs_from_tree(tree: dict) -> list:

	return