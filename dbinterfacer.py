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

def create_connection(database):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(database)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()


def createTablesInThe(database):
    
    sqlToCreateTableTasks = """ CREATE TABLE IF NOT EXISTS tasks (
                                    id INTEGER PRIMARY KEY,
                                    description TEXT NOT NULL,
                                    follows INTEGER
                                    );"""
    
    sqlToCreateTableHazards = """ CREATE TABLE IF NOT EXISTS hazards (
                                    id INTEGER PRIMARY KEY,
                                    description TEXT NOT NULL
                                    );"""
    
    sqlToCreateTableHierarchyOfControls = """ CREATE TABLE hierarchy_of_controls (
                                            id INTEGER PRIMARY KEY,
                                            type TEXT UNIQUE
                                            );"""
    
    sqlToCreateTableCountermeasures = """ CREATE TABLE IF NOT EXISTS countermeasures (
                                            id INTEGER PRIMARY KEY,
                                            description TEXT NOT NULL,
                                            class INTEGER, 
                                            control_type INTEGER FOREIGN KEY
                                            );"""
    
    sqlToCreateTableLikelihood = """ CREATE TABLE IF NOT EXISTS likelihood (
                                        id INTEGER PRIMARY KEY,
                                        task INTEGER FOREIGN KEY,
                                        hazard INTEGER FOREIGN KEY,
                                        probability REAL CHECK (probability < 1)
                                        );"""

    sqlToCreateTableMitigations = """ CREATE TABLE IF NOT EXISTS mitigations (
                                        id INTEGER PRIMARY KEY,
                                        hazard INTEGER FOREIGN KEY,
                                        countermeasure INTEGER FOREIGN KEY
                                        );"""

    
def main():
    
    pass


if __name__ == '__main__':
    #create_connection(r"C:\sqlite\db\pythonsqlite.db")
    #create_connection(r"pythonsqlite.db")
    main()
    
    
    
