"""GUI manager module."""
import json
import os.path as op
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as messagebox

import controller


# Configuration default file path(relative to this file)
config_file = 'config.json'
CONFIG_WORD_LANG_KEY = 'word_lang'
CONFIG_TRANS_LANG_KEY = 'word_trans'


def _abspath(path):
    """Compute an absolute path.

    The path will be calculated between this module's file and a
    relative path(relative to this module's file).
    """
    return op.join(op.dirname(__file__), path)


class App:
    """GUI manager class.

    This class will create the tkinter window and manage the tkinter
    events, wrapping on the logical controller(from module
    'controller').
    """

    def __init__(self):
        """Create a new app window."""
        self._window = Tk()

        # Setup window
        self._window.geometry("%dx%d" % (500, 600))
        self._window.title('Dictionary')
        # self._window.overrideredirect(True)

        # Load configuration
        self._config_dict = None
        self._load_config()

        lang1 = self._config_dict.get(CONFIG_WORD_LANG_KEY,
                                      CONFIG_WORD_LANG_KEY)
        lang2 = self._config_dict.get(CONFIG_TRANS_LANG_KEY,
                                      CONFIG_TRANS_LANG_KEY)

        # Setup window notebook
        self._notebook = Notebook(self._window)
        self._notebook.pack(fill=BOTH, expand=1)

        # Tabs
        self._tab_search = Frame(self._notebook, padding=10)
        self._tab_insert = Frame(self._notebook, padding=10)

        self._notebook.add(self._tab_search, text='search')
        self._notebook.add(self._tab_insert, text='insert')

        # Setup insert frame
        frame_lang1 = Frame(self._tab_insert)
        frame_lang1.pack(fill=X, pady=(0, 5))

        lbl_lang_1 = Label(frame_lang1, text=f'{lang1}: ')
        lbl_lang_1.pack(side=LEFT)
        self._entry_word = Entry(frame_lang1)
        self._entry_word.pack(side=LEFT)

        frame_lang2 = Frame(self._tab_insert)
        frame_lang2.pack(fill=X)

        lbl_lang_2 = Label(frame_lang2, text=f'{lang1}: ')
        lbl_lang_2.pack(side=LEFT)
        self._entry_trans = Entry(frame_lang2)
        self._entry_trans.pack(side=LEFT, anchor=N)

    def start(self):
        """Start the application's main loop."""
        self._window.mainloop()

    # Private instance methods
    def _load_config(self):
        """Load config from a default json file."""
        self._config_dict = {}

        if op.isfile(_abspath(config_file)):
            with open(_abspath(config_file)) as file:
                self._config_dict = json.load(file)
