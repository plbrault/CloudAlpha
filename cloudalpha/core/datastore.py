""" TODO: 

Implement a singleton DataStore class that provides methods
to set and get key-value persistent data associated to
the unique_id of a manager or an account.

The data must be saved to a file (e.g. datastore.bin), that
may be a sqlite database.

The file could be stored at the root of the project (beside cloudalpha.py).
It should be automatically created if missing, and added to the gitignore.
"""

import sqlite3

class DataStore(object):
    
    _instance = None
    
    def get_value(self, unique_id, key):
        pass
    
    def set_value(self, unique_id, key, value):
        pass
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
        return cls._instance