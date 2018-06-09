#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 13:58:35 2018

@author: meyerhof
"""

from PyPDF2 import PdfFileReader, PdfFileWriter

path = './fw9.pdf'





def pdf_splitter(path):

    fname = os.path.splitext(os.path.basename(path))[0]
    # os.path.split: Split the pathname path into a pair, (head, tail) where tail is the last pathname component (i.e. everything after the last slash) and head is everything leading up to that. 
    # os.path.basename: Return the base name of pathname path. This is the second element of the pair returned by passing path to the function os.path.split()
    # os.path.splitext: Split the pathname path into a pair (root, ext) such that root + ext == path, and ext (like 'extension') is empty or begins with a period and contains at most one period. 
 
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page)) 
        
        
        output_filename = 'page_{}.pdf'.format(page+1)

        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)

        print('Created: {}'.format(output_filename))
    
    #Aquí comienzo a crear una página en blanco, de acuerdo al formato del pdf. Para hacerlo, creo un pdf temporal con dos páginas, una que me da el formato para luego permitirme agregar la página en blanco.
    pdf_writer.addBlankPage()
    output_filename = 'page_0.pdf'


    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

    
    #Aquí, con el archivo con la página en blanco creada, tomo la página en blanco y la dejo en un archivo sola.

    
    pdf_blank = PdfFileReader('page_0.pdf')
    pdf_writer = PdfFileWriter()
    pdf_writer.addPage(pdf_blank.getPage(1))
    output_filename = 'page_0.pdf'


    with open(output_filename, 'wb') as out:
        pdf_writer.write(out)

    print('Created: {}'.format(output_filename))
    

pdf_splitter(path)

#with open(path, 'rb') as input:
#
#    pdf=PdfFileReader(input)
#    numPages=pdf.getNumPages()
#
#    if numPages > 1 and (numPages % 2 == 1):
#            outPdf=PdfFileWriter()
#            outPdf.cloneDocumentFromReader(pdf)
#            outPdf.addBlankPage()
#            outStream=file('/tmp/test.pdf','wb')
#            outPdf.write(outStream)
#            outStream.close()