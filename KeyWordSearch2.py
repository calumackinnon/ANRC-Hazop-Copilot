# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 11:32:04 2023

@author: nau03220, kenny fong
"""

''' 
by attribution to Chung (Kenny) Fong: 
    https://pureportal.strath.ac.uk/en/persons/chung-man-fong
'''


# Load pdf

import pandas as pd

#In this dictionary each Key is a heading, each value a list
table_dict = {'Keyword':[], 'Page Number':[], 'File Name':[]}

import fitz  # PyMuPDF
def read_pdf(pdf_path):
    # Read the PDF
    doc = fitz.open(pdf_path)
    pdf_text = ""
    page_text_list = []

    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        pdf_text += page_text
        page_text_list.append((page_num + 1, page_text))

    # Close the PDF
    doc.close()

    return pdf_text, page_text_list


pdf_file_path = 'cns-tast-gd-6.1.pdf'  # "cnss-tast-gd-11.1.pdf"


# Read the PDF
pdf_text, page_text_list = read_pdf(pdf_file_path)

# Split the text into sentences
sentences = pdf_text.split('. ')

search_terms = ["No "]
search_terms2 = [""]
#search_terms = ["catastr", "hazard", "must", "should"]
#search_terms2 = ["electri", "battery"]

# Search for sentences containing variations of the search terms
term_sentences = [sentence.strip() for sentence in sentences if any(term.lower() in sentence.lower(
) for term in search_terms) and any(term2.lower() in sentence.lower() for term2 in search_terms2)]

# Print all sentences search term combination
sentence_count = 0
for sentence in term_sentences:
    sentence_count += 1
    for page_num, page_text in page_text_list:
        if sentence in page_text:
            table_dict['Keyword'].append(search_terms)
            table_dict['Page Number'].append(page_num)
            table_dict['File Name'].append(pdf_file_path)
            print(f"Statment {sentence_count}, Page {page_num}: {sentence}")
            break  # Stop after finding the first occurrence on the page
    # Print a separator after each sentence
    print("______________________________________________________________________")
    print()
    print()
print()
print("Number of statements:", sentence_count)

print('\n\n')    
# Displaying the dictionary for illustration.
print("Dictionary before conversion to DataFrame:\n", table_dict)

# Creating a DataFrame from the dictionary. df standards for dataframe
df = pd.DataFrame(table_dict)

print('\nThis is a dataframe, its a type of table defined in the pandas library')
# Displaying the DataFrame.
print("\nDataFrame representation:\n", df)

# EXAMPLES OF SAVING A DATAFRAME AS CSV - USING PANDAS LIBRARY
df.to_csv('dataframe_CSV.csv', index=False, encoding='utf-8')





