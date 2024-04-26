import logging
from dict2file import write_dict_to_file, read_dict_from_file
from utils import get_logger

class FireDict(dict):
    """
    A dictionary with additional features:
    * easy access to nested dictionaries with default variables
    * Save the dictionary to a file on changes
    """

    def __init__(self, *args, **kwargs):
        """
        Initialize a new FireDict.

        All arguments are the same as the built-in dict, with one additional
        argument:
        filename: str, optional
            If provided, the dict is initialized with data from this file and changes are persisted to it.
        """
        logger = get_logger("FireDict.__init__", logging.INFO)
        self._file = kwargs.pop('filename', None)
        super().__init__(*args, **kwargs)
        if self._file:
            try:
                file_data = read_dict_from_file(full_filename=self._file)
                self.update(file_data)
            except FileNotFoundError:
                logger.warning(f"File {self._file} not found. Creating a new one.")
                
    def get(self, *keys):
        current = self
        for key in keys:
            current = super().get(key)
            if current is None:
                return None
        return current

    def _save_to_file(self):
        if self._file:
            write_dict_to_file(dictionary=self, full_filename=self._file)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self._save_to_file()

    def __delitem__(self, key):
        super().__delitem__(key)
        self._save_to_file()


    def clear(self):
        super().clear()
        self._save_to_file()


    def pop(self, key, default=None):
        result = super().pop(key, default)
        self._save_to_file()
        return result
    
    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self._save_to_file()

    def popitem(self):
        result = super().popitem()
        self._save_to_file()
        return result

    def setdefault(self, key, default=None):
        result = super().setdefault(key, default)
        self._save_to_file()
        return result
