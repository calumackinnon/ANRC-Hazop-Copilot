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
    #filename = r"pythonsqlite.db"
    filename = r"pythonsqlite-guidewords.db"

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
        
        self.sendQueryToDatabase(sqlToCreateTableTasks)
        self.sendQueryToDatabase(sqlToCreateTableHazards)
        self.sendQueryToDatabase(sqlToCreateTableHierarchyOfControls)
        self.sendQueryToDatabase(sqlToCreateTableCountermeasures)
        self.sendQueryToDatabase(sqlToCreateTableLikelihood)
        self.sendQueryToDatabase(sqlToCreateTableMitigations)
        
    def sendQueryToDatabase(self, query, access='r'):
        
        stripQ = query.strip()
        assert stripQ[len(stripQ)-1] == ';' # Verify it ends with an ';'.
        
        if self._databaseConnection is None: 
            print('Could not create the database connection.')
            return
        else:
            
            
            try:
                
                dbCursor = self._databaseConnection.cursor()
                
                if access == 'w':
                    dbCursor.execute(query)
                else:    
                    rows = []
                    rows = dbCursor.execute(query).fetchall()
                    return rows
                
                
                # dbCursor.execute(sqlToCreateTableTasks)
                
                # dbCursor.execute(sqlToCreateTableHazards)
                
                # #print('built 2 tables ')
                
                # dbCursor.execute(sqlToCreateTableHierarchyOfControls)
    
                # dbCursor.execute(sqlToCreateTableCountermeasures)            
                
                # #print('built 4 tables')
                
                # dbCursor.execute(sqlToCreateTableLikelihood)
                
                # #print('built 5 tables')
                
                # dbCursor.execute(sqlToCreateTableMitigations)
                
            except Error as e:
                
                print(e)
                
            
    def insertData(self, data, table):
        """
                            ('take powder A', 0),
;"""
        
        sqlCommand = """ INSERT INTO tasks (description, follows)
                        VALUES 
                            ('place in blender', 1),
                            ('take 3 kg of colourant powder B', 2),
                            ('place in blender', 3),
                            ('start blender', 4),
                            ('mix for 15 min and stop blender', 5),
                            ('remove blended mixture into 3 by 5 kg bags', 6),
                            ('wash out blender', 7),
                            ('add 50 l of resin to mixing vessel', 8),
                            ('add 0.5 kg of hardener into mixing vessel', 9),
                            ('add 5 kg of mixed powder A and B', 10),
                            ('stir for 1 min', 11),
                            ('pour mixture into molds within 5 min', 12);
                    """
        pass # TODO Run this query to add the data
        #place in blender, take 3 kg of colourant powder),
        #(0, 1, 2);
        self.sendQueryToDatabase(sqlCommand)
    
    def searchForData(self, searchterm, table):
        print('About to search for data.')
        
        sqlQuery = """SELECT * FROM tasks;""" #""" SELECT id FROM tasks WHERE description LIKE '%blend%';"""
    
        returndata = self.sendQueryToDatabase(sqlQuery, 'r')
        print(returndata)
    
    def closeConnections(self):
        
        if self._databaseConnection is not None:
            self._databaseConnection.close()
            print('connection successfully closed')
            
        
    
    def checkTables(self):
        
        sqlToCheckTables = '.tables'
        
        try:
            
            dbCursor = self._databaseConnection.cursor()
            
            dbCursor.execute(sqlToCheckTables)
            
            outcome = dbCursor.fetchall()
            
            print(outcome)
            
        except Error as e:
            
            print(e)
            
    
def main():
    
    dbi = DatabaseInterfacer()
    dbi.createTables()
    
    # TODO Here we would populate with data.
    if 'y' == input('Check database? (y/n)'):
        # dbi.checkTables()
        dbi.insertData(None, None)
        print('data inserted, about to search')
        dbi.searchForData(None, None)
    
    dbi.closeConnections()

    print('To test, navigate to ' + str(dbi.filename) + ' and run sqlite3 ' + dbi.filename + ', then use the command .tables')

if __name__ == '__main__':
    #create_connection(r"C:\sqlite\db\pythonsqlite.db")
    #create_connection(r"pythonsqlite.db")
    main()
    
    
    
