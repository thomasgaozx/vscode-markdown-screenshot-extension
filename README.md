# VSCode Markdown Image Screenshot Extension

## What is this?

This is an "extension" of VSCode that allows you to screenshot crop anything into **markdown** document image with simple shortcut keys.

1. Press the hotkey
2. Screenshot overlay prompts you to crop an area of the screen
3. On mouse release, an autofocus textbox pops up so you can enter img name
4. Image is saved locally, and a line will be added to your document referencing that image.

## Prerequisite

Python packages including PIL, tkinter, numpy.
An anaconda full installation should suffice.

## Installation

Firstly, clone this repo (goes without saying).

Secondly, open VSCode, go to `tasks.json`, and add the following to the task list, replacing `<path-to-crop.py>` with full path to `crop.py` in this repo:

```json
{
    "label": "crop",
    "type": "process",
    "command": "${config:python.pythonPath}",
    "args": ["<path-to-crop.py>", "${file}"]
}
```

Thirdly and lastly, go to `keybindings.json`, and add the following, replacing `ctrl+alt+p` your preferred hotkey:

```json
{
    "key": "ctrl+alt+p",
    "command": "workbench.action.tasks.runTask",
    "args": "crop"
}
```

Enjoy!

## Credit

Since I have zero experience with GUI or tkinter.
The script relies heavily on external snippets.
The reference to the links are commented in code.
