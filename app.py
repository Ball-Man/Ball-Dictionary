"""GUI manager module."""
import json
import os.path as op
from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox as messagebox

import controller


# Configuration default file path(relative to this file)
CONFIG_FILE = 'config.json'
CONFIG_WORD_LANG_KEY = 'word_lang'
CONFIG_TRANS_LANG_KEY = 'trans_lang'

# Dictionary default path(json file, relative to this file)
DICTIONARY_PATH = 'dict/dictionary.json'

# Icon default path(relative to this file)
ICON_PATH = 'icon.ico'

# Default search threshold
SEARCH_THRESHOLD = 0.6


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
        # Load configuration
        self._config_dict = None
        self._load_config()

        lang1 = self._config_dict.get(CONFIG_WORD_LANG_KEY,
                                      CONFIG_WORD_LANG_KEY)
        lang2 = self._config_dict.get(CONFIG_TRANS_LANG_KEY,
                                      CONFIG_TRANS_LANG_KEY)

        # Setup window
        self._window = Tk()
        self._window.geometry("%dx%d" % (500, 600))
        self._window.title('Dictionary')
        self._window.iconbitmap(_abspath(ICON_PATH))

        # Setup window notebook
        self._notebook = Notebook(self._window)
        self._notebook.pack(fill=BOTH, expand=1)

        # Tabs
        self._tab_search = Frame(self._notebook, padding=10)
        self._tab_insert = Frame(self._notebook, padding=10)

        self._notebook.add(self._tab_search, text='search')
        self._notebook.add(self._tab_insert, text='insert')

        # Setup search frame
        frame_search = Labelframe(self._tab_search, text='Search', padding=5)
        frame_search.pack(fill=X)

        self._entry_search = Entry(frame_search)
        lbl_keyword = Label(frame_search, text='keyword: ')
        self._btn_search = Button(frame_search, text='Search')

        lbl_keyword.pack(side=LEFT)
        self._entry_search.pack(side=LEFT)
        self._btn_search.pack(side=LEFT, padx=(10, 0))

        self._lst_search = Listbox(self._tab_search, borderwidth=0,
                                   highlightthickness=0)
        self._lst_search.pack(fill=BOTH, expand=True)

        # Setup insert frame
        frame_lang1 = Frame(self._tab_insert)
        frame_lang1.pack(fill=X, pady=(0, 5))

        lbl_lang_1 = Label(frame_lang1, text=f'{lang1}: ')
        lbl_lang_1.pack(side=LEFT)
        self._entry_word = Entry(frame_lang1)
        self._entry_word.pack(side=LEFT)

        frame_lang2 = Frame(self._tab_insert)
        frame_lang2.pack(fill=X)

        lbl_lang_2 = Label(frame_lang2, text=f'{lang2}: ')
        lbl_lang_2.pack(side=LEFT)
        self._entry_trans = Entry(frame_lang2)
        self._entry_trans.pack(side=LEFT, anchor=N)

        self._btn_insert = Button(self._tab_insert, text='Add')
        self._btn_insert.pack(anchor=W, pady=(5, 0))

        # Event bindings
        self._btn_search.bind('<Button-1>', self._btn_search_click)
        self._entry_search.bind('<Return>', self._btn_search_click)
        self._btn_search.bind('<Return>', self._btn_search_click)

        self._btn_insert.bind('<Button-1>', self._btn_insert_click)
        self._entry_trans.bind('<Return>', self._btn_insert_click)
        self._entry_word.bind('<Return>', self._btn_insert_click)
        self._btn_insert.bind('<Return>', self._btn_insert_click)

        # Create a new logical controller
        self._controller = None
        try:
            self._controller = controller.Controller(_abspath(DICTIONARY_PATH))
        except Exception as e:
            messagebox.showerror('Error loading dictionary :(', str(e))
            self._window.destroy()

    def start(self):
        """Start the application's main loop."""
        self._window.mainloop()

    # Private instance methods
    def _load_config(self):
        """Load config from a default json file."""
        self._config_dict = {}

        if op.isfile(_abspath(CONFIG_FILE)):
            with open(_abspath(CONFIG_FILE)) as file:
                self._config_dict = json.load(file)
        else:
            print(f'Config file not found: {CONFIG_FILE}.')

    def _btn_search_click(self, event):
        """Event for the search button."""
        # Clear listbox
        self._lst_search.delete(0, END)

        result = self._controller.search_entries(
            keyword=self._entry_search.get(), threshold=SEARCH_THRESHOLD)

        for entry in result:
            self._lst_search.insert(END, f'{entry[controller.WORD]}: '
                                    + f'{entry[controller.TRANS]}')

    def _btn_insert_click(self, event):
        """Event for the insert button."""
        w = self._entry_word.get()
        t = self._entry_trans.get()

        # Focus on the first textbox for fast insertion
        self._entry_word.focus()
        self._entry_word.selection_range(0, END)

        # Clean textboxes
        self._entry_word.delete(0, END)
        self._entry_trans.delete(0, END)

        if not w or w.isspace() or not t or t.isspace():
            messagebox.showerror('Oops', 'Empty words are not allowed.')
            return

        ok = self._controller.add_entry(w, t)

        if not ok:
            messagebox.showerror('Oops', 'This word was already in your '
                                + 'dictionary.')
            return

        self._controller.save()
