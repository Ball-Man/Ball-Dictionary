"""Logical controller module."""
import os
import os.path as op
import json


class Controller:
    """The logical controller class.

    This class acts as a logical controller, loading/saving changes
    to/from the dictionary.
    """
    def __init__(self, dict_path):
        """Create a new controller, based on a dictionary path.

        If the said path doesn't exist, an empty dictionary will be
        created.
        """
        self._dictionary_path = None
        self._dictionary = None

        self.load(dict_path)

    def load(self, path):
        """Load a dictionary from a path, if exists.

        If the said path doesn't exist, an empty dictionary will be
        created.
        """
        if op.isfile(path):
            with open(path) as file:
                self._dictionary = json.load(file)

        self._dictionary_path = path

    def save(self, path=None):
        """Save the dictionary to the given path.

        If no path is given(default value None) the load path will be
        used(the previous dict, if exists, will be overwrited).
        If no load operation was executed before, an exception will
        rise.

        Missing directories will be created.
        """
        if path is None:
            path = self._dictionary_path

        os.makedirs(op.dirname(path), exist_ok=True)

        with open(path, 'w') as file:
            json.dump(self._dictionary, file)
