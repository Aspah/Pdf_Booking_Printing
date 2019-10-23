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
    PATH = os.getcwd()                  #retorna un string referente al actual directorio. Soporta Unix y Windows.
    
    global PATH_input
    PATH_input = PATH + '/PDF_Input'
    
    global PATH_output
    PATH_output = PATH + '/PDF_Output'
    
    global PATH_temp
    PATH_temp = PATH + '/PDF_Temp'
    
    if os.path.exists(PATH_input) == False:         #Revisa si existen las carpetas PDF_input y PDF_Output.
        os.mkdir(PATH_input)                        #Si no existen, las crea. 
    if os.path.exists(PATH_output) == False:
        os.mkdir(PATH_output)
    if os.path.exists(PATH_temp) == True:           #Revisa si existe la carpeta PDF_temp. Si existe, borra la carpeta 
        shutil.rmtree(PATH_temp)                    #y todo su contenido (para evitar mezclar archivos intermedios)
    os.mkdir(PATH_temp)                             #Finalmente crea una carpeta mkPDF_temp nueva y vacía. 
    
    print("Please put your pdf inside the 'PDF_input' folder")
    input("Press Enter to continue...")
    #print (os.listdir(PATH_input))
    assert os.listdir(PATH_input) != [], "There is no files inside the input folder"    
    
    
    

def clean_directory():
    shutil.rmtree(PATH_temp)        #Elimina el directorio PATH_temp y todo lo que esté dentro de él. 

def pdf_splitter(path_to_pdf):

    pdf = PdfFileReader(path_to_pdf)                    #Creo el objeto PDF
    for page in range(pdf.getNumPages()):               #Por cada página de este
        pdf_writer = PdfFileWriter()                    #Creo una instancia del 'wirter' de pdf
        pdf_writer.addPage(pdf.getPage(page))           #Le agrego la página correspondiente
        
        
        output_filename = 'page_{}.pdf'.format(page+1)  #Le asigno el nombre correspondiente

        with open(output_filename, 'wb') as out:        #Y lo imprimo como archivo independiente
            pdf_writer.write(out)                           #Aquí el detalle es que creo un archivo 'vacío' con el open() y -luego- el writer le escribe todo lo necesario para convertir este archivo vacío en un pdf que contiene la página correspondiente. 

        print('Created: {}'.format(output_filename))    #Aquí anuncio la creación del archibo
    
    
    #Creación de una página en blanco de acuerdo al formato del PDF. 
                                         
    pdf_writer.addBlankPage()               #Aquí me aprovecho de que el writer tiene ya incorporada la última página del formato. 
                                            #De esta manera el .addBlankPage() aprovecha el formato de esta última página para crear la página en blanco.                    
    output_filename = 'page_0.pdf'          #Aquí le asigno un nombre. 


    with open(output_filename, 'wb') as out: #Aquí lo creo como archivo. 
        pdf_writer.write(out)                #Hasta ahora este archivo tiene 2 páginas. La última página del PDF
                                             #Y la página en blanco de interés. 

        
    pdf_blank = PdfFileReader('page_0.pdf')     #Luego recupero este archivo recién creado 
    pdf_writer = PdfFileWriter()                #Reinicio el Writer
    pdf_writer.addPage(pdf_blank.getPage(1))    #Le agrego sólo la página en blanco 
    output_filename = 'page_0.pdf'              #Le asigno un nombre (el mismo que el anterior para sobreescribir)


    with open(output_filename, 'wb') as out:    #Y lo creo como archivo, sobrescribiendo el anterior. 
        pdf_writer.write(out)

    print('Created: {}'.format(output_filename))#E informo su creación. 
    


def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()                            #Creo un writer limpio 

    for path in input_paths:                                #Luego para cada path en la lista de input_paths
        pdf_reader = PdfFileReader(path)                    #Recupero el archivo (que debería contener una página única)
        for page in range(pdf_reader.getNumPages()):        #Luego por cada página de este archivo 
            pdf_writer.addPage(pdf_reader.getPage(page))    #Se la agrego al writer (este for está demás porque cada PDF sólo tiene una página)
                                                            #pero así el merge queda más genérico en caso de ser necesario. 
    
    with open(output_path, 'wb') as merged_pdf:             #Se crea el PDF
        pdf_writer.write(merged_pdf)


def rearrange(num):

    pages = []                          #Creo una lista vacía que contendrá el 'orden' de las páginas. 
    cycle = num//4                      #Cuantos 
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
        
    paths = []            
    for i in pages:
        i = str(i)
        temp = 'page_' + i + '.pdf'
        paths.append(temp)
    
    return list(paths)
    

#BEGIN OF THE PROGRAM. 
    
print("This program will create files and folders in the local folder in where this script.py is executed")
a = input("Do you want to continue? Press 'y' for yes / Pres 'n' for no:  ")
if a == 'n':
    raise SystemExit            #Uso de 'raise SystemExit' para que el programa se cierre. 
elif a == 'y':
    mk_directory()

    for file in (os.listdir(PATH_input)):
                        
            #Directory Path definition
            temp_path = PATH_temp + '/' + os.path.splitext(file)[0]     #splitext: sería algo como split-ext = 'split the extension'.  
            os.mkdir(temp_path)                                         #Aquí le quito el .pdf al archivo y creo una carpeta con el nombre que queda. 
            
            #File Paths definitions
            dest_fname = temp_path + '/' + file
            orig_fname = PATH_input + '/' + file
            out_path = PATH_output + '/FOR_BOOKING_PRINTING_' + file
            
            print(orig_fname)
            
            #División en páginas únicas
            try:                                    #Intento lo siguiente: 
                os.chdir(temp_path)                 #Entro a la carpeta temporal creada en PDF_temp
                copyfile(orig_fname, dest_fname)    #Copio el archivo original a la carpeta temporal
                pdf_splitter(dest_fname)            #Divido la copia en sus páginas
                #input('...')
                os.remove(dest_fname)               #Elimino la copia original (así no la agrego después en el merger)
                
            finally:                                #Independiente si lo anterior falló o no
                os.chdir(PATH_temp)                 #Vuelvo a la carpeta PATH_temp (así puedo seguir intentando con los siguientes archivos.)
            
            
            #Unión de páginas reordenadas en nuevo PDF
            pdf_file = PdfFileReader(orig_fname)    #Aquí sólo obtengo el número de páginas del pdf actal 
            pdf_num = pdf_file.getNumPages()
            
            
            try:                                    #Intento lo siguiente: 
                os.chdir(temp_path)                 #Vuelvo a ingresar a la carpeta temporal creada en PDF_temp
                pages_paths = rearrange(pdf_num)    #Reordeno las páginas y devuelvo una lista con todas las rutas a las páginas con el nuevo orden
                merger(out_path, pages_paths)       #Finalmente creo el nuevo PDF con este nuevo orden
            
            finally:                                #Independiente si lo anterior falló o no
                os.chdir(PATH_temp)                 #Vuelvo a la carpeta PATH_temp (así puedo seguir intentando con los siguientes archivos.)
    
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



#USO DE os.split y similares: 
    
    # os.path.split: Split the pathname path into a pair, (head, tail) where tail is the last pathname component (i.e. everything after the last slash) and head is everything leading up to that. 
    # os.path.basename: Return the base name of pathname path. This is the second element of the pair returned by passing path to the function os.path.split()
    # os.path.splitext: Split the pathname path into a pair (root, ext) such that root + ext == path, and ext (like 'extension') is empty or begins with a period and contains at most one period. 
    
    #Ej:
    #fname = os.path.splitext(os.path.basename(path_to_pdf))[0]  
        #Basename retorna el namepdf.pdf y el splitext[0] retorna el namepdf

#assert rearrange(5) == [4,1,2,3,0,5]
#assert rearrange(6) == [4,1,2,3,0,5,6]
#assert rearrange(7) == [4,1,2,3,0,5,6,7]
#assert rearrange(8) == [4,1,2,3,8,5,6,7]
#assert rearrange(0) == []
#assert rearrange(1) == [0,1]
#assert rearrange(2) == [0,1,2]
#assert rearrange(3) == [0,1,2,3]


