"""Logical controller module."""
import os
import os.path as op
import json
from difflib import SequenceMatcher
import locale
import functools

# Constants
WORD = 'w'
TRANS = 't'


def _similar(a, b):
    """Find the similarity between two strings."""
    return SequenceMatcher(None, a, b).ratio()


class Controller:
    """The logical controller class.

    This class acts as a logical controller, loading/saving changes
    to/from the dictionary.
    """

    def __init__(self, dict_path, locale_code):
        """Create a new controller, based on a dictionary path.

        If the said path doesn't exist, an empty dictionary will be
        created.
        locale_code is used for alphabetical order(special characters
        from different countries).
        """
        self._dictionary_path = None
        # It's called dictionary but in reality it's a list
        self._dictionary = None

        self.load(dict_path)

        locale.setlocale(locale.LC_ALL, locale_code)

    def load(self, path):
        """Load a dictionary from a path, if exists.

        If the said path doesn't exist, an empty dictionary will be
        created.
        """
        if op.isfile(path):
            with open(path) as file:
                self._dictionary = json.load(file)
        else:
            self._dictionary = []

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

    def add_entry(self, word, trans):
        """Add an entry in the dict.

        word is the new word you want to remember, trans is the
        translation in your main language.

        Returns True if the operation succeded, False if the word was
        already present inside the dict(no action is taken in this
        case).
        """
        found = any(word == dic[WORD] for dic in self._dictionary)
        if not found:
            self._dictionary.append({WORD: word, TRANS: trans})

        return not found

    def remove_entry(self, word):
        """Remove the word entry from the dictionary."""
        removed = [entry for entry in self._dictionary if entry[WORD] == word]
        self._dictionary = [entry for entry in self._dictionary
                            if entry not in removed]

    def search_entries(self, keyword=None, threshold=0):
        """Search entries.

        keyword will be used as search parameter. If the similarity
        between keyword and w or t(from the entry key's "w" and "t") is
        greater than the given threshold, the selected pair will be
        added to the output.

        Return a list of dicts matching the research. If keyword is None
        return all the entries. The entries are sorted so that the
        higher similarities come first.
        """

        def _max_ratio(kw, entry):
            """Return the maximum similarity ratio.

            The ratio is calculated between the keyword and w, and
            between the keyword and t. The maximum is returned.
            """
            return max(_similar(keyword, entry[WORD]),
                       _similar(keyword, entry[TRANS]))

        if keyword is None:
            keyword = ''

        # Obtain a tuple structured as follows: ( (ratio, w, t), * )
        ratios_dict = map(lambda x: (_max_ratio(keyword, x), x),
                          self._dictionary)
        filtered_ratios = filter(lambda x: x[0] >= threshold, ratios_dict)
        sorted_ratios = sorted(filtered_ratios, key=lambda x: x[0],
                               reverse=True)

        # Go back to the canonical entry format
        entries = map(lambda x: x[1], sorted_ratios)

        return tuple(entries)

    def get_entries_sorted(self, target, reverse=False):
        """Get a tuple containing all the entries, sorted.

        target defines which word from the two "sides"("w" and "t" from
        the entries dicts) should be used for sorting. target can be
        WORD or TRANS (constants from this module).

        The default order is alphabetical. Reverse simply reverts the
        alphabetical order.
        """

        compare = lambda a, b: locale.strcoll(a[target], b[target])

        return tuple(sorted(self._dictionary,
                            key=functools.cmp_to_key(compare),
                            reverse=reverse))
