# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 11:32:04 2023

@author: nau03220, kenny fong
"""

''' 
by attribution to Chung (Kenny) Fong: 
    https://pureportal.strath.ac.uk/en/persons/chung-man-fong
'''

import fitz  # PyMuPDF


# Load pdf
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


pdf_file_path = 'THSIS.Ch0.pdf' #"cnss-tast-gd-11.1.pdf"


# Read the PDF
pdf_text, page_text_list = read_pdf(pdf_file_path)

# Split the text into sentences
sentences = pdf_text.split('. ')

search_terms = ["capacitor"]
search_terms2 = ["unit"]
#search_terms = ["catastr", "hazard", "must", "should"] 
#search_terms2 = ["electri", "battery"] 

# Search for sentences containing variations of the search terms
term_sentences = [sentence.strip() for sentence in sentences if any(term.lower() in sentence.lower() for term in search_terms) and any(term2.lower() in sentence.lower() for term2 in search_terms2)]

# Print all sentences search term combination
sentence_count = 0
for sentence in term_sentences:
    sentence_count += 1
    for page_num, page_text in page_text_list:
        if sentence in page_text:
            print(f"Statment {sentence_count}, Page {page_num}: {sentence}")
            break  # Stop after finding the first occurrence on the page
    print("______________________________________________________________________")  # Print a separator after each sentence
    print()
    print()
print()
print("Number of statements:", sentence_count)
