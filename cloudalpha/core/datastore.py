import sqlite3
import json

class DataStore(object):
    
    _DB_FILE = "datastore.db"
    _DB_TABLE_NAME = "datastore"
    
    _instance = None
    
    _db_conn = None
    _db_cur = None
    
    def _init_db_conn(self):
        self._db_conn = sqlite3.connect(self._DB_FILE)
        self._db_cur = self._db_conn.cursor()
        self._db_cur.execute("CREATE TABLE IF NOT EXISTS " + self._DB_TABLE_NAME 
                             + "(id INTEGER PRIMARY KEY AUTOINCREMENT, owner_unique_id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL)")
        
    def get_value(self, unique_id, key):
        self._db_cur.execute("SELECT value FROM " + self._DB_TABLE_NAME + " WHERE owner_unique_id = '" + json.dumps(unique_id) + "' AND key = '" + json.dumps(key) + "'")
        res = self._db_cur.fetchall()
        if len(res) > 0:
            return json.loads(res[0][0])
        else:
            return None
    
    def set_value(self, unique_id, key, value):
        if self.get_value(unique_id, key) == None:
            self._db_cur.execute("INSERT INTO " + self._DB_TABLE_NAME + "(id, owner_unique_id, key, value) VALUES(1, '" + json.dumps(unique_id) + "', '" 
                                 + json.dumps(key) + "', '" + json.dumps(value) + "')")
        else:
            self._db_cur.execute("UPDATE " + self._DB_TABLE_NAME + " SET value = '" + json.dumps(value) + "' WHERE owner_unique_id = '" 
                                 + json.dumps(unique_id) + "' AND key = '" + json.dumps(key) + "'")
        self._db_conn.commit()
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
            cls._instance._init_db_conn()
        return cls._instance