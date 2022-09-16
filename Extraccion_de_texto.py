# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 11:15:47 2022

@author: Joan camilo tamayo

pip install spacy
pip install spacypdfreader
python -m spacy download es_core_news_sm

Cambios:
        - cambniar append por concat 
        - revisar problemas con nombres para otros proveedores
"""
import os
import spacy
from spacypdfreader import pdf_reader
import pandas as pd
from datetime import datetime
import time
import re
nlp = spacy.load('es_core_news_sm')

start = datetime.now() # inicio del cod ----
time.sleep(1)


nlp = spacy.load('es_core_news_sm')
data_path = r"D:\Users\WS-012\Desktop\P_Colmedica\estructura\data_path\\" 
fail_message = []
df = pd.DataFrame()

for infolder_pacientes in os.listdir(data_path):
    tipo = os.path.splitext(infolder_pacientes)[1]
    
    # si el archivo dentro del paciente no es un pdf 
    if os.path.splitext(infolder_pacientes)[1] != ".pdf":
        folder_paciente = infolder_pacientes
        
        # leo los archivos dentro del folder del paciente
        for fold_prestador in os.listdir(data_path+folder_paciente+"/"):
            folder_prestador = fold_prestador
            
            # leo los archivos dentro del folder del prestador
            for file_prestador in os.listdir(data_path+folder_paciente+"/"+folder_prestador+"/"):
                
                # si el archivo es un pdf
                if os.path.splitext(file_prestador)[1] == ".pdf" or os.path.splitext(file_prestador)[1] == ".PDF" :                        
                    pdf = file_prestador #   funciona
                    
                    doc = pdf_reader(data_path+folder_paciente+"/"+folder_prestador+"/"+pdf, nlp) #pru
                    nombre_pdf = pdf
                    
                    if folder_prestador =="Bienestar":
                        paciente = os.path.splitext(nombre_pdf)[0]
                        id_paciente = paciente.split("_")[1] # ----------------------- id
                        
                    if folder_prestador !="Bienestar":
                        paciente = os.path.splitext(nombre_pdf)[0]
                        id_paciente = paciente.split("_")[0] # ----------------------- id
                        id_paciente = str([int(s) for s in re.findall(r'-?\d+\.?\d*', str(id_paciente))][0])
                    
                    
                    ruta_pdf = doc._.pdf_file_name       # ----------------------- ruta_pdf
                    tot_paginas = doc[-1]._.page_number  # ----------------------- numero tot paginas
                    pagina = 0
                    
                    for pagina in range(doc[-1]._.page_number):
                        pagina = pagina +1               # ----------------------- pagina
                        text = str(doc._.page(pagina))
                        texto_pag  = [text]              # ----------------------- texto
                        
                        d = {'id_paciente':int(id_paciente),
                             'Prestador': folder_prestador,
                             'ruta_pdf': ruta_pdf, 
                             'tot_paginas': int(tot_paginas),
                             'pagina':int(pagina),
                             'texto_pag':texto_pag}
                        
                        df = df.append(d,ignore_index=True)
                        df.to_excel(excel_writer = r"D:\Users\WS-012\Desktop\P_Colmedica\estructura\out\output.xlsx" ,index = False, engine='xlsxwriter') 
                        
  
                print("----------------------------")
                print("Paciente: "+folder_paciente)
                print("Prestador: "+folder_prestador)
                print("Documento: "+pdf)
                        
end = datetime.now() # fin del cod -------
print(f"El tiempo de ejecucion [hh:mm:ss.ms] is {end - start}")



# #--------------------- para carpeta con pdfs-------------------------------

# --------------
# carpeta con pdfs
# pdf_path = r"D:\Users\WS-012\Desktop\P_Colmedica\estructura\pdf\\" 
# df = pd.DataFrame()
# for pdf in os.listdir(pdf_path):
#     doc = pdf_reader(pdf_path+pdf, nlp) #pru
#     nombre_pdf = pdf
#     paciente = os.path.splitext(nombre_pdf)[0]
    
#     id_paciente = paciente.split("_")[1] # ----------------------- id
#     ruta_pdf = doc._.pdf_file_name       # ----------------------- ruta_pdf
#     tot_paginas = doc[-1]._.page_number  # ----------------------- numero tot paginas
    
#     for pagina in range(doc[-1]._.page_number):
#         pagina = pagina +1               # ----------------------- pagina
#         print("_______________ inicio _________________")
#         print("pagina: " + str(pagina))
#         text = str(doc._.page(pagina))
#         texto_pag  = [text]              # ----------------------- texto
#         print(texto_pag)
        
#         d = {'id_paciente':int(id_paciente),'ruta_pdf': ruta_pdf, 'tot_paginas': int(tot_paginas),'pagina':int(pagina),'texto_pag':texto_pag}
#         df = df.append(d,ignore_index=True)
#         df.to_excel(excel_writer = r"D:\Users\WS-012\Desktop\P_Colmedica\estructura\output.xlsx" ,index = False, engine='xlsxwriter') 
        
#         print("_______________ fin _________________")
#         print("                                        ")

# --------------

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