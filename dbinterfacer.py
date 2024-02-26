# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 16:11:18 2024

@author: qrb15201 (Calum Mackinnon)
"""


# The below is from 
# https://www.sqlitetutorial.net/sqlite-python/creating-database/ and 
# https://www.sqlitetutorial.net/sqlite-python/creating-tables/

import sqlite3
from sqlite3 import Error

class DatabaseInterfacer:
    
    _databaseConnection = None
    filename = r"pythonsqlite.db"

    def __init__(self):
        
        self._databaseConnection = self.createConnection(self.filename)
    
    def __str__(self):
        
        return f"A DatabaseInterfacer to {self.filename}"
    
    def createConnection(self, filename):
        
        """ create a database connection to a SQLite database """
        
        conn = None
        
        try:
            conn = sqlite3.connect(filename)
            print(sqlite3.version)
            
            return conn
            
        except Error as e:
            print(e)
            
        return conn
    

    def createTables(self):
        
        sqlToCreateTableTasks = """ CREATE TABLE IF NOT EXISTS tasks (
                                        id INTEGER PRIMARY KEY,
                                        description TEXT NOT NULL,
                                        follows INTEGER
                                        );"""
        
        sqlToCreateTableHazards = """ CREATE TABLE IF NOT EXISTS hazards (
                                        id INTEGER PRIMARY KEY,
                                        description TEXT NOT NULL
                                        );"""
        
        
        sqlToCreateTableHierarchyOfControls = """ CREATE TABLE IF NOT EXISTS hierarchy_of_controls (
                                                id INTEGER PRIMARY KEY,
                                                type TEXT UNIQUE
                                                );"""
        
        
        sqlToCreateTableCountermeasures = """ CREATE TABLE IF NOT EXISTS countermeasures (
                                                id INTEGER PRIMARY KEY,
                                                description TEXT NOT NULL,
                                                class INTEGER, 
                                                control_type INTEGER,
                                                FOREIGN KEY (control_type) REFERENCES hierarchy_of_controls(id)
                                                );"""
        
        sqlToCreateTableLikelihood = """ CREATE TABLE IF NOT EXISTS likelihood (
                                            id INTEGER PRIMARY KEY,
                                            task INTEGER,
                                            hazard INTEGER,
                                            probability REAL CHECK (probability < 1),
                                            FOREIGN KEY (task) REFERENCES tasks(id),
                                            FOREIGN KEY (hazard) REFERENCES hazards(id)
                                            );"""
    
        sqlToCreateTableMitigations = """ CREATE TABLE IF NOT EXISTS mitigations (
                                            id INTEGER PRIMARY KEY,
                                            danger INTEGER,
                                            countermeasure INTEGER,
                                            FOREIGN KEY (danger) REFERENCES hazards(id),
                                            FOREIGN KEY (countermeasure) REFERENCES countermeasures(id)
                                            );"""
        
        if self._databaseConnection is None: 
            print('Could not create the database connection.')
            return
        else:        
            try:
                
                dbCursor = self._databaseConnection.cursor()
                
                dbCursor.execute(sqlToCreateTableTasks)
                
                dbCursor.execute(sqlToCreateTableHazards)
                
                print('built 2 tables ')
                
                dbCursor.execute(sqlToCreateTableHierarchyOfControls)
    
                dbCursor.execute(sqlToCreateTableCountermeasures)            
                
                print('built 4 tables')
                
                dbCursor.execute(sqlToCreateTableLikelihood)
                
                print('built 5 tables')
                
                dbCursor.execute(sqlToCreateTableMitigations)
                
            except Error as e:
                
                print(e)
            
    def closeConnections(self):
        
        if self._databaseConnection is not None:
            self._databaseConnection.close()

    
def main():
    
    dbi = DatabaseInterfacer()
    dbi.createTables()
    
    dbi.closeConnections()

    print('To test, navigate to ' + str(dbi.filename) + ' and run sqlite3 ' + dbi.filename + ', then use the command .tables')

if __name__ == '__main__':
    #create_connection(r"C:\sqlite\db\pythonsqlite.db")
    #create_connection(r"pythonsqlite.db")
    main()
    
    
    
