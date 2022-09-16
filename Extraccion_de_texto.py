# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:15:47 2022

@author: Joan camilo tamayo

pip install spacy
pip install spacypdfreader
python -m spacy download es_core_news_sm
"""
import os
import spacy
from spacypdfreader import pdf_reader
import pandas as pd
# import openpyxl
# import xlsxwriter

from datetime import datetime
import time

start = datetime.now()
time.sleep(1)

nlp = spacy.load('es_core_news_sm')
pdf_path = r"D:\Users\WS-012\Desktop\P_Colmedica\estructura\pdf\\" 
df = pd.DataFrame()
for pdf in os.listdir(pdf_path):
    doc = pdf_reader(pdf_path+pdf, nlp) #pru
    nombre_pdf = pdf
    paciente = os.path.splitext(nombre_pdf)[0]
    
    id_paciente = paciente.split("_")[1] # ----------------------- id
    ruta_pdf = doc._.pdf_file_name       # ----------------------- ruta_pdf
    tot_paginas = doc[-1]._.page_number  # ----------------------- numero tot paginas
    
    for pagina in range(doc[-1]._.page_number):
        pagina = pagina +1               # ----------------------- pagina
        print("_______________ inicio _________________")
        print("pagina: " + str(pagina))
        text = str(doc._.page(pagina))
        texto_pag  = [text]              # ----------------------- texto
        print(texto_pag)
        
        d = {'id_paciente':int(id_paciente),'ruta_pdf': ruta_pdf, 'tot_paginas': int(tot_paginas),'pagina':int(pagina),'texto_pag':texto_pag}
        df = df.append(d,ignore_index=True)
        df.to_excel(excel_writer = r"D:\Users\WS-012\Desktop\P_Colmedica\estructura\output.xlsx" ,index = False, engine='xlsxwriter') 
        
        print("_______________ fin _________________")
        print("                                        ")


end = datetime.now()
print(f"El tiempo de ejecucion [hh:mm:ss.ms] is {end - start}")



# #----------------------------------------------------

# # Get the page number of any token.
# print(doc[0]._.page_number)  # 1
# print(doc[-1]._.page_number) # 4

# # Get page meta data about the PDF document.
# print(doc._.pdf_file_name)   # 'D:\Users\WS-012\Desktop\P_Colmedica\estructura\pdf\CC_51907563.pdf'
# print(doc._.page_range)      # (1, 4)
# print(doc._.first_page)      # 1
# print(doc._.last_page)       # 4

# # Get all of the text from a specific PDF page.
# pag = doc._.page(0)     # 'able to display the destination page (unless...'
# pag = doc._.page(11)  
# pag
