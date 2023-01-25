#-------------------------------------------------------------------------------
# Name:        DS 2.1 - Projeto Carros
# Purpose:
#
# Author:      Ivo
#
# Created:      23dez2022
# Copyright:   (c) Ivo 2022
# Licence:     <your licence>
#-------------------------------------------------------------------------------

print("LOSS !")

import pandas as pd
from collections import defaultdict
import os
import re
import plotly.express as px

path_other_tables = "D:\\Docs\\Python\\Projeto Carros\\DS_2.1\\tables_others\\"
path_master_tables = "D:\\Docs\\Python\\Projeto Carros\\DS_2.1\\tables_masters\\"
path_graphics = "D:\\Docs\\Python\\Projeto Carros\\DS_2.1\\plots\\"

def find_last ():
    """ Verify the last master file saved

        Parameters: none

        Returns: str
    """
    folder_content = os.listdir(path_master_tables)
    folder_content.sort(reverse=True)
    #print("folder content :", folder_content)
    last_file = (folder_content[0])
    last_date = re.findall(r"\d{4}\D\d{2}", last_file)
    last_date = last_date[0]
    return last_date


def read_master (master_date):
    """ Read newest master file.

        Parameters: master_name : str

        Returns : Dataframe
    """

    master = pd.read_excel(path_master_tables + master_date + "_df_master_1.xlsx")
    master.set_index("Modelo", inplace = True)
    return master

def cars_dicio (df):
    """ Creates a dict with brands as keys and respectives models as values.
        
        Parameter: Dataframe
        
        Retuns: dict
    """
    df_brands_and_models = sorted(df.index)
    #print(df_brands_and_models)
    splitted_models=[]
    for item in df_brands_and_models:
        splitted_item = item.split(sep="/")
        splitted_models.append(splitted_item)

    dicio_brands_models = defaultdict(list)
    for k, v in splitted_models:
        dicio_brands_models[k].append(v)
    #print(dicio_brands_models)
    return dicio_brands_models

def choose_brand(dicio):
    """  """
    brands = dicio.keys()
    print(brands)
    brand_chosen = "none"
    while brand_chosen not in brands:
        brand_chosen = (input("Choose one of the brands: ")).upper()
    print(brand_chosen)
    return brand_chosen

def choose_model(dicio):
    """   """
    models = dicio[brand]

    print(models)
    model_chosen = None
    while model_chosen not in models:
        model_chosen = (input("Choose one of the model: ")).upper()
    print(model_chosen)
    return model_chosen

def transpor (df, car):
    """Transpose master df preparing it to generate grphics.
        
        Parameters: Dataframe, str

        Returns: Dataframe
        """
    df_t = df.transpose()
    df_t['TOTAL'] = df_t.sum(axis=1)
    df_t["M_A_TOTAL"] = df_t['TOTAL'].rolling(window=6, min_periods=1).mean().astype(int)
    df_t["M_A_car"] = df_t[car].rolling(window=6, min_periods=1).mean().astype(int)
    df_t["pc_car/TOTAL"] = df_t[car] * 100 / df_t["TOTAL"]
    df_t["M_A_pc"]= df_t["pc_car/TOTAL"].rolling(window=6, min_periods=1).mean()
    df_t = df_t.loc[initial_date : final_date , :]
    df_t = df_t.loc[:, df_t.any()]       # remove linhas com zero qnt
    return df_t

def graphs (df_col, gr_title, name, label):
    """ Generate graphics.
        
        Parameters: Dataframe sliced
                    str, str, dict
        
        Output: plot image
        """

    graph = px.line(df_col, title=gr_title,
    color_discrete_sequence=["red", "green", "blue"],
    labels=label, markers=True)
    graph.update_layout(autosize=False, width=1200, height=600,
    margin=dict(l=30, r=20, t=40, b=20),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
    font_family="IBM Plex Mono Medium")
    graph.write_image(path_graphics + last_file_date + "_" + name + ".png")



last_file_date = find_last()
print("last date :", last_file_date)

df_master = read_master(last_file_date)
print(df_master.head())

all_models = cars_dicio(df_master)
 
brand = choose_brand(all_models)
model = choose_model(all_models)

brand_model_chosen = (brand + "/" + model)
print(brand_model_chosen)

i_date = str.upper(input("choose start date , yyyy_mm :\n Or type 'N'"))
if i_date == "N":
    initial_date = "2003-01"
else:
    initial_date = i_date
print("starts on > " + initial_date)

f_date = str.upper(input("choose final date , yyyy_mm :\n Or type 'N'"))
if f_date == "N":
    final_date = last_file_date
else:
    final_date = f_date
print("End on > " + final_date)

df_master_t = transpor(df_master, brand_model_chosen)
#print(df_master_t)

labels_qnt = {"value": "Unidades x 1.000",  "index": "Ano_mês"}
labels_per_cent = {"value": "%",  "index": "Ano_mês"}

gr01 = graphs(df_master_t[[brand_model_chosen, "M_A_TOTAL", "TOTAL"]],
"Carros Novos Emplacados", "gr01 - Totais", labels_qnt)

gr03 = graphs(df_master_t[[brand_model_chosen, "M_A_car"]],
brand_model_chosen + " Novos Emplacados", ("gr03 - " + brand + model), labels_qnt)

gr05 = graphs(df_master_t[["pc_car/TOTAL", "M_A_pc"]],
brand_model_chosen + " % do Total de Novos Emplacados", ("gr05 - % " + brand + model), labels_per_cent)


#    # FIM

print("ES HAT GETAN")

