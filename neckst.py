from lib.db.Database import Database
import os

def get_db(path='~/.neckstdb'):
    db_config = {"path":os.path.expanduser(path)}
    return Database(db_config)

if __name__ == '__main__':
    db = get_db()
    print(db)
