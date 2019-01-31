#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 03:41:53 2018

@author: meyerhof
"""
import os
import shutil
from PyPDF2 import PdfFileReader, PdfFileWriter
from shutil import copyfile



def mk_directory():
    global PATH
    PATH = os.getcwd()
    
    global PATH_input
    PATH_input = PATH + '/PDF_Input'
    
    global PATH_output
    PATH_output = PATH + '/PDF_Output'
    
    global PATH_temp
    PATH_temp = PATH + '/PDF_Temp'
    
    if os.path.exists(PATH_input) == False:
        os.mkdir(PATH_input)
    if os.path.exists(PATH_output) == False:
        os.mkdir(PATH_output)
    if os.path.exists(PATH_temp) == True:
        shutil.rmtree(PATH_temp)
    os.mkdir(PATH_temp)
    
    print("Please put your pdf inside the 'PDF_input' folder")
    input("Press Enter to continue...")
    #print (os.listdir(PATH_input))
    assert os.listdir(PATH_input) != [], "There is no files inside the input folder"
    
    
    

def clean_directory():
    shutil.rmtree(PATH_temp)

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
    


def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter() 

    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))

    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)


def rearrange(num):

    global pages
    pages = []
    cycle = num//4
    rest = num%4
    assert rest < 4    

    a = 4
    b = 1
    c = 2
    d = 3


    for i in range(1,cycle+1):
        pages.append(a)
        pages.append(b)
        pages.append(c)
        pages.append(d)
        a = a + 4
        b = b + 4
        c = c + 4
        d = d + 4

    if (rest != 0) and (num > 4):
        begin = pages[-4] +1
        end = pages[-4] + rest
        #print(begin, end)
        pages.append(0)
    
        for i in range (begin, end+1):
            pages.append(i)
    
    elif 0 < num < 4:
        pages.append(0)
        for i in range(1,num+1):
            pages.append(i)
    
    elif num == 0:
        pages = []
    
    

#BEGIN OF THE PROGRAM. 
    
print("This program will create files and folders in the local folder in where this script.py is executed")
a = input("Do you want to continue? Press 'y' for yes / Pres 'n' for no:  ")
if a == 'n':
    raise SystemExit

mk_directory()

for files in (os.listdir(PATH_input)):
        #print(files)
        
        temp_path = PATH_temp + '/' + os.path.splitext(files)[0]
        dest_fname = temp_path + '/' + files
        orig_fname = PATH_input + '/' + files
        out_path = PATH_output + '/FOR_BOOKING_PRINTING_' + files
        #print(temp_path)
        print(orig_fname)
        os.mkdir(temp_path) 
        
        try:
            os.chdir(temp_path)
            copyfile(orig_fname, dest_fname)
            pdf_splitter(dest_fname)
            #input('...')
            os.remove(dest_fname)
            
        finally:
            os.chdir(PATH_temp)
        
        pdf_file = PdfFileReader(orig_fname)
        pdf_num = pdf_file.getNumPages()
        
        
        try: 
            os.chdir(temp_path)
            rearrange(pdf_num)
            paths = []            
            for i in pages:
                i = str(i)
                temp = 'page_' + i + '.pdf'
                paths.append(temp)
            #input('...')
            merger(out_path, paths)
            
        
        finally:
            os.chdir(PATH_temp)

print("The processed file will be in the 'Output Folder'")


        
            





#input("...")


print("=====================================================================================================")
print()
print()
print("PAGE REARRANGING APP")
print("Instructions: ")
print()
print()
print("The Problem:") 
print("If you want to print a pdf in order to make a book*, the natural order of the pages in the pdf file make")
print("imposible to achieve the correct order in the printed book.")
print()
print("*This mean: two page for sheet, in a doble-siding printing. Each printed page is folded by half and stack with every")
print("other folded page printed. In this way, you can create a manageable book with a confort size and less paper waste.")
print()
print()
print("The Solution:")
print("This utility rearrange the pages of the pdf file in a way that achieve the correct order in the printed book.")
print("After this, you take the output_pdf and configure the printer in 'two page for sheet, doble-siding printing'.")
print("And if your printer shift the page automatically, you have to set 'Short edge flip' or something similar.")
print()
print("Also, you can use this utility with any number of PDFs at once.")
print()
print("I hope that this may will be usefull for you. And that someone ever use it apart from me jajaja.")
print()
print()
print("Greetings!  Nicolás Schiappacasse Vega")
print()
print()
input("When you're ready, press Enter to exit... ")


clean_directory()





#assert rearrange(5) == [4,1,2,3,0,5]
#assert rearrange(6) == [4,1,2,3,0,5,6]
#assert rearrange(7) == [4,1,2,3,0,5,6,7]
#assert rearrange(8) == [4,1,2,3,8,5,6,7]
#assert rearrange(0) == []
#assert rearrange(1) == [0,1]
#assert rearrange(2) == [0,1,2]
#assert rearrange(3) == [0,1,2,3]


