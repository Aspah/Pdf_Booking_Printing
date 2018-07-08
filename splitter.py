#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 23:00:40 2018

@author: meyerhof
"""

# pdf_splitter.py

 

import os

#import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
#from PyPDF2 import PageObject



def pdf_splitter(path):

    fname = os.path.splitext(os.path.basename(path))[0]
 
    pdf = PdfFileReader(path)
    máx = pdf.getNumPages()
    
    for page in range(máx +1):
        pdf_writer = PdfFileWriter()
        
        if page == máx:
            blank = PageObject.createBlankPage
            output_filename = 'page_0.pdf'
        
        else:
            pdf_writer.addPage(pdf.getPage(page)) 
            output_filename = 'page_{}.pdf'.format(page+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))

   
if __name__ == '__main__':
    path = 'fw9.pdf'
    pdf_splitter(path)