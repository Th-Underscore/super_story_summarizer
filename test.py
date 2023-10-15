import gradio as gr

def update_tree(*args):
    tree = {}
    for i, arg in enumerate(args):
        if i % 2 == 0:
            last_arg = arg
        else:
            tree.update({ last_arg: arg })
    # Update the tree with the new key-value pairs
    # You can implement your own logic here

    # Print the updated tree for demonstration purposes
    print(f"Updated Tree: {tree}")

def tree_editor(tree: dict, btn: gr.Button):
    # Display the current tree
    print(f"Current Tree: {tree}")

    # Create editable text boxes for each key-value pair
    inputs = []
    for key, value in tree.items():
        key_input = gr.Textbox(label=f"Key: {key}", default=key)
        value_input = gr.Textbox(label=f"Value: {value}", default=value)
        inputs.extend([key_input, value_input])

    # Update the tree when any of the text boxes are edited
    btn.click(update_tree, inputs=inputs, outputs=None)

print(len([1, 2, 3]))