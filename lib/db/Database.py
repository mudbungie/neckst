# Abstraction layer. To be consumed only by child classes
# Provides database portability. 

import os
import sqlalchemy as sqla

class Database:
    tableNames = [
    ]

    def __init__(self, databaseConfig):
        # Calling micromethod to allow mobility for child classes
        self.initDB(databaseConfig)

    def initDB(self, config):
        self.config = config
        self.connect()

    def constructConnectionString(self):
        # Connection string construction from config dict
        return 'sqlite://' + self.config['path']

    def connect(self):
        self.connection = sqla.create_engine(self.constructConnectionString())
        self.metadata = sqla.MetaData(self.connection)

        # Initialize things.
        self.initTables(self.tableNames) # Should be defined in child class
        self.inspector = sqla.engine.reflection.Inspector
        return self.connection

    def initTable(self, tableName, autoload=True):
        table = sqla.Table(tableName, self.metadata, autoload=autoload,
            autoload_with=self.connection)
        return table

    def initTables(self, tableNames):
        self.tables = {}
        for tableName in tableNames:
            self.tables[tableName] = self.initTable(tableName)

    # 
    # The following methods are just shorthand, and some abstraction for 
    # children.
    # 
    def execute(self, query):
        return self.connection.execute(query)

    def insert(self, table, values):
        return self.execute(table.insert(values))
    def update(self, table, values, pkey=None):
        if not pkey:
            pkey = self.getPkey(table)
        q = table.update().where(getattr(table.c, pkey) == pkey).\
            values(values)
        return self.execute(q)
    def delete(self, table, values, pkey=None):
        if not pkey:
            pkey = self.getPkey(table)
        q = table.delete().where(getattr(table.c, pkey) == pkey).\
            values(values)
    
    def getPkey(self, table):
        pkey = self.inspector.from_engine(self.connection).\
            get_primary_keys(table)[0]
        return pkey

    def recordsToListOfDicts(self, records):
        columns = records.keys()
        data = []
        for record in records:
            datum = {}
            for column in columns:
                datum[column] = getattr(record, column)
            data.append(datum)
        return data

   
