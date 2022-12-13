#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   Digital maturity.py
@Time    :   2022/11/24 11:43:19
@Author  :   Xin HUANG 
@Version :   1.0
@Contact :   xin.huang@capgemini.com
'''

# here put the import lib


import streamlit as st
import random
import plotly.express as px
import pandas as pd
import numpy as np
import gspread

list_category = ["Collecte des données", "Analyse de données", "Execution des Processus", "Control des processus", "Data exchange"]

list_category1 = ["Capacité de personnalisation de l'outil", "Gestion du changement", "Ergonomie "]

list_category2 = ["Standardisation des processus", "Gestion de compétences ", "strategie de choix et implementations des nouvelles technologies", "Culture entreprise "]

@st.cache
def get_data():

   gc = gspread.service_account(filename='data/hidden-casing-267814-7c289d93d950.json')

   sh = gc.open_by_key('1sNhzUZRURYJyCCqOrqq7xseGMuss12fVi9lUKXHo024')
   worksheet= sh.get_worksheet(1)
   ques = worksheet.col_values(4)[1:]
   print(worksheet.row_values(2)[4:9])
   num_ques = len(ques)
   ans = list()
   for i in range(num_ques):
      # print(i)
      ans.append(worksheet.row_values(i+2)[4:9])
      #  print(ans[i])
   print("Length of question:",len(ques))
   return ques, ans

qs, ans = get_data()

def radar_chart(df, width, height):  

    fig = px.line_polar(df,r='note', theta='theta',line_close=True,range_r=[0,5],width=width, height=height)
    st.write(fig)

# st.write(qs)
st.header("Maturity digital")
tab1, tab2, tab3, tab4 = st.tabs(["Technologies", "User Experience", "Organisation","Summary"])
if 'num' not in st.session_state:
    st.session_state.num = 0
choices = [ "" for i in range(len(qs))]
note = [ 0 for i in range(len(qs))]
note_mean = [0 for i in range(12)]
print(len(choices))
i=0

with tab1:
   with st.form("my_form1"):
      
      st.header("Collecte des données")
      
      num = st.session_state.num
      for _, _ in zip(qs[0:5], ans[0:5]): 
         choices[i] = st.radio(qs[i], options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[0] = np.mean(note[0:5])
         i+=1

      st.header("Analyse de données")
      for _, _ in zip(qs[5:9], ans[5:9]): 
         choices[i]  = st.radio(qs[i], options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[1] = np.mean(note[5:9])
         i+=1

      st.header("Execution des Processus")
      for _, _ in zip(qs[9:12], ans[9:12]): 
         choices[i]  = st.radio(qs[i], options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[2] = np.mean(note[9:12])
         i+=1

      st.header("Control des processus")
      for _, _ in zip(qs[12:15], ans[12:15]): 
         choices[i]  = st.radio(qs[i], options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[3] = np.mean(note[12:15])
         i+=1

      st.header("Data exchange")
      for _, _ in zip(qs[15:19], ans[15:19]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[4] = np.mean(note[15:19])
         i+=1
      
      submitted1 = st.form_submit_button("Submit")
      if submitted1:
            df = pd.DataFrame({"note":note_mean[0:5],"theta":list_category})
            radar_chart(df,width=None, height=None)
print(choices)
print(note)
   

with tab2:
   with st.form("my_form2"):
      st.header("Capacité de personnalisation de l'outil ")
      for _, _ in zip(qs[19:22], ans[19:22]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[5] = np.mean(note[19:22])
         i+=1

      st.header("Gestion du changement")
      for _, _ in zip(qs[22:26], ans[22:26]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[6] = np.mean(note[22:26])
         i+=1

      st.header("Ergonomie")
      for _, _ in zip(qs[26:30], ans[26:30]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[7] = np.mean(note[26:30])
         i+=1
   
      submitted2 = st.form_submit_button("Submit")
      if submitted2:
            df = pd.DataFrame({"note":note_mean[5:8],"theta":list_category1})
            radar_chart(df,width=None, height=None)

with tab3:
   with st.form("my_form3"):

      st.header("Standardisation des processus")
      for _, _ in zip(qs[30:35], ans[30:35]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[8] = np.mean(note[30:35])
         i+=1

      st.header("Gestion de compétences ")
      for _, _ in zip(qs[35:38], ans[35:38]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[9] = np.mean(note[35:38])
         i+=1

      st.header("strategie de choix et implementations des nouvelles technologies")
      for _, _ in zip(qs[38:41], ans[38:41]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[10] = np.mean(note[38:41])
         i+=1

      st.header("Culture entreprise ")
      for _, _ in zip(qs[41:45], ans[41:45]): 
         choices[i]  = st.radio(qs[i],options=ans[i])
         note[i] = ans[i].index(choices[i])+1
         note_mean[11] = np.mean(note[41:45])
         i+=1
      
      submitted3 = st.form_submit_button("Submit")
      if submitted3:
            df = pd.DataFrame({"note":note_mean[8:12],"theta":list_category2})
            radar_chart(df,width=None, height=None)
    
with tab4:

   col1, col2, col3 = st.columns(3)
   scores =list()
   scores.append(np.mean(note_mean[0:5]))
   scores.append(np.mean(note_mean[5:8]))
   scores.append(np.mean(note_mean[8:12]))
   with col1:
      st.header("Technologies")
      df1=pd.DataFrame({"Technologies":list_category,"Score":note_mean[0:5]})
      st.dataframe(df1) 
      df = pd.DataFrame({"note":note_mean[0:5],"theta":list_category})
      radar_chart(df,width=300, height=300)
      st.text_input("Technologies",value=scores[0])
 

   with col2:
      st.header("User Experience")
      df1=pd.DataFrame({"User Experience":list_category1,"Score":note_mean[5:8]})
      st.dataframe(df1) 
      df = pd.DataFrame({"note":note_mean[5:8],"theta":list_category1})
      radar_chart(df,width=300, height=300)
      st.text_input("User Experience",value=scores[1])

   with col3:
      st.header("Organisation")
      df1=pd.DataFrame({"Organisation":list_category2,"Score":note_mean[8:12]})
      st.dataframe(df1) 
      df = pd.DataFrame({"note":note_mean[8:12],"theta":list_category2})
      radar_chart(df,width=300, height=300)
      st.text_input("Organisation",value=scores[2])

   st.warning("Maturité: "+str(np.mean(scores)))
   df = pd.DataFrame({"note":scores,"theta":["Technologies", "User Experience", "Organisation"]})
   radar_chart(df,width=None, height=None)

   gc = gspread.service_account(filename='C:/Users/xinhuang/Git/appstasc/data/hidden-casing-267814-7c289d93d950.json')
   sh = gc.open_by_key('1sNhzUZRURYJyCCqOrqq7xseGMuss12fVi9lUKXHo024')
   worksheet= sh.get_worksheet(1)
   range_value = 'S2:S46'
   cell_list = worksheet.range(range_value)
   k = 0
   for cell in cell_list:
        cell.value = note[k]
        k+=1
   worksheet.update_cells(cell_list)

if __name__ == '__main__':
   print("Maturity Digital")

# choices = ["Fichiers locaux de travail personnel à entrée manuelle", 
# "Formulaires, fichiers locaux standardisés ",
# "Principalement ERP et une partie provenant d'autres outils essentiels",
# "ERP, Disponibilité des données differée liées aux opérations", 
# "ERP, Données liées aux opérations disponibles en temps réel grâce à un RPA "]

# choices1 = ["Aucune connection / NA", 
# "Pas de connection entre les outils mais l'application principale repose sur des bases de données facilement accessibles et ordonées",
# "Les outils essentiels du flux principal sont interconnectés",
# "Tous les outils de l'entreprises sont interconnectés", 
# "Tous les outils de l'entreprises sont interconnectés + mise en place d'un RPA"]

# col1, col2 = st.columns(2)

# with col1:
#     st.text("Quelle est la source de vos données de travail ?")
#     st.text("\n")
#     st.text("\n")
#     st.text("Comment les BDD des Systèmes d'information sont connectées ?")
# with col2:
#     a = st.selectbox('Answer:', choices)
#     a1 = st.selectbox('Answer:', choices1)
# st.text("Quelle est la source de vos données de travail ?")
# a = st.selectbox('Answer:', choices)
# st.write(f"Note: {choices.index(a)+1}")

# st.text("Comment les BDD des Systèmes d'information sont connectées ?")
# a1 = st.selectbox('Answer:', choices1)
# st.write(f"Note: {choices1.index(a1)+1}")
