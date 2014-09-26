import sqlite3
import json
from threading import Lock

class DataStore(object):
    
    _DB_FILE = "datastore.db"
    _DB_TABLE_NAME = "datastore"
    
    _instance = None
    
    _lock = Lock()    
    _db_conn = None
    _db_cur = None
    
    def get_value(self, unique_id, key):
        sql = "SELECT value FROM " + self._DB_TABLE_NAME + " WHERE owner_unique_id = '" + json.dumps(unique_id) + "' AND key = '" + json.dumps(key) + "'"
        with self._lock:
            self._db_cur.execute(sql)
            res = self._db_cur.fetchall()
        if len(res) > 0:
            return json.loads(res[0][0])
        else:
            return None
    
    def set_value(self, unique_id, key, value):
        sql_select = "SELECT COUNT(value) FROM " + self._DB_TABLE_NAME + " WHERE owner_unique_id = '" + json.dumps(unique_id) + "' AND key = '" + json.dumps(key) + "'"
        sql_insert = "INSERT INTO " + self._DB_TABLE_NAME + "(id, owner_unique_id, key, value) VALUES(1, '" + json.dumps(unique_id) + "', '"  + json.dumps(key) + "', '" + json.dumps(value) + "')"
        sql_update = "UPDATE " + self._DB_TABLE_NAME + " SET value = '" + json.dumps(value) + "' WHERE owner_unique_id = '" + json.dumps(unique_id) + "' AND key = '" + json.dumps(key) + "'"        
        with self._lock:
            self._db_cur.execute(sql_select)
            res = self._db_cur.fetchone()
            if res[0] == 0:
                self._db_cur.execute(sql_insert)
            else:
                self._db_cur.execute(sql_update)
            self._db_conn.commit()
    
    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(DataStore, cls).__new__(cls, *args, **kwargs)
                cls._instance._db_conn = sqlite3.connect(cls._DB_FILE)
                cls._instance._db_cur = cls._instance._db_conn.cursor()
                cls._instance._db_cur.execute("CREATE TABLE IF NOT EXISTS " + cls._DB_TABLE_NAME 
                                     + "(id INTEGER PRIMARY KEY AUTOINCREMENT, owner_unique_id INTEGER NOT NULL, key TEXT NOT NULL, value TEXT NOT NULL)")                
        return cls._instance