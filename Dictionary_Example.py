# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:18:02 2024

@author: callu
"""
import csv 


#EXAMPLES OF ARRAYS/LISTS
# Here's how arrays (lists in Python terminology) can be defined.
USA = ['USA', 'Washington', "$"]
UK = ['UK', 'London', "£"]
France = ['France', 'Paris', "Euro"]

# We can form arrays of arrays to act as tables.
countryList = [USA, UK, France]



# #EXAMPLES OF SAVING LISTS AS CSV - Using Library
# # Opening a file to write to, then using csv.writer to write rows.
# with open('library_list.csv', 'w') as f:
#     writer = csv.writer(f)
#     # write arrays as rows to CSV file
#     for row in countryList:
#         writer.writerow(row)

# #--------------------------------------------------------


# # EXAMPLES OF DICTIONARY
# # Creating a dictionary where countries are keys and their details are values.

# lis_dic = {};
# for c in countryList:
#     lis_dic[c[0]] = c;
#     print(str(c))

# print(f'This is a dictionary where the keys are strings and the values are arrays or lists \n {lis_dic}')
# print(f"We can identify specific lists within the dictionary by refering to their key: lis_dic['USA'] {lis_dic['USA']}")
# print(f"We can identify specific  elements within the list if we know it's index: lis_dic['USA'][1]  {lis_dic['USA'][1]}")


    

# # EXAMPLES OF SAVING LISTS AS CSV - MANUALLY
# # Writing to a file manually without using the csv module.
# with open('manual_list.csv','w') as f:
#     for lis in lis_dic.values():
#         f.write(str(lis).replace('[', '').replace(']',''))
#         f.write('\n')

# #------------------------------------------------------------------------------------
# #Here's how classes are defined in python
# class Country:
#   def __init__(self, _name, c, cur):
#     self.name = _name
#     self.capital = c
#     self.currency = cur
   
#   def sayHi(self):
#     print('Hello, my name is ' + self.name)
    
# # Creating a dictionary of Country objects.
# class_dic = {};
# for c in countryList:
#     class_dic[c[0]] = Country(c[0], c[1], c[2]);

# print('\n\n')
# print(f'This is a dictionary where the keys are strings and the values are objects or instances of a class \n {class_dic}')
# print("We can pick one object from this class by referng to it's key: class_dic['USA']")
# print(class_dic['USA'])
# print("We can then find attributes associated with that class: class_dic['USA'].capital")
# print(class_dic['USA'].capital)
# print("We can also call methods associated with that class: class_dic['USA'].sayHi()")
# class_dic['USA'].sayHi()

# # EXAMPLES OF SAVING Class AS CSV - MANUALLY
# # Writing class object attributes to a CSV file.
# with open('manual_classes.csv','w') as f:
#     for obj in class_dic.values():
#         f.write(f"{obj.name}, {obj.capital}, {obj.currency} \n")
        
    
# import json       
# # EXAMPLES OF SAVING Class AS JSON - USING LIBRARY
# # Serializing class object attributes to JSON format and writing to a file.
# with open('Library_classes.json','w') as f:
#     for obj in class_dic.values():
#         #We can turn an object to a dictionary 
#         obj_dict = obj.__dict__
#         jsonStr = json.dumps(obj_dict)
#         f.write(jsonStr)
        
        
#-------------------------------------------------------------------------------------
# EXAMPLES OF USING DATAFRAMES
#You could also store this all as a dataframe, which is a useful kind of table in python. Often used in data science
        
import pandas as pd

#In this dictionary each Key is a heading, each value a list
table_dict = {'Name':[], 'Capital':[], 'Currency':[]}

for c in countryList:
    table_dict['Name'].append(c[0])
    table_dict['Capital'].append(c[1])
    table_dict['Currency'].append(c[2])
    
print('\n\n')    
# Displaying the dictionary for illustration.
print("Dictionary before conversion to DataFrame:\n", table_dict)

# Creating a DataFrame from the dictionary.
df = pd.DataFrame(table_dict)

print('\nThis is a dataframe, its a type of table defined in the pandas library')
# Displaying the DataFrame.
print("\nDataFrame representation:\n", df)

# Showing more DataFrame functionalities.
print("\nDisplay the first 2 rows of the DataFrame:\n", df.head(2))
print("\nInformation about the DataFrame:")
df.info()

print(f"\nWe can refer to specific collumns in the dataframe df.filter(['Capital']) {df.filter(['Capital'])}")

print(f"\nWe can refer to specific rows in the dataframe df.loc[df['Name'] == 'USA'] {df.loc[df['Name'] == 'USA']}")

print(f"\nWe can refer to specific elements in the dataframe df.loc[df['Name'] == 'USA'].filter(['Capital']) {df.loc[df['Name'] == 'USA'].filter(['Capital'])}")

# EXAMPLES OF SAVING A DATAFRAME AS CSV - USING PANDAS LIBRARY
df.to_csv('dataframe_CSV.csv', index=False, encoding='utf-8')



















