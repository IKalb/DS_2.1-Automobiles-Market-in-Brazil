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

print("LOSS !\n")

import requests
import camelot
import pandas as pd
import os
import numpy as np
import re


url_database = "http://www.fenabrave.org.br//portal//files//"
path_pdf = "D:\\Docs\\Python\\Projeto Carros\\DS_2.1\\files\\"
path_other_tables = "D:\\Docs\\Python\\Projeto Carros\\DS_2.1\\tables_others\\"
path_master_tables = "D:\\Docs\\Python\\Projeto Carros\\DS_2.1\\tables_masters\\"
path_graphics = "D:\\Docs\\Python\\Projeto Carros\\DS_2.1\\plots\\"


def past_date ():
    """ Verify the last master file saved

        Parameters: none

        Returns: int, int, int
    """
    
    folder_content = os.listdir(path_master_tables)
    folder_content.sort(reverse=True)
    last_file = (folder_content[0])
    last_date = re.findall(r"\d{4}\D\d{2}", last_file)
    last_file_date = last_date[0]
    last_year = int(re.split(r"_", last_date[0])[0])
    last_month = int(re.split(r"_", last_date[0])[1])

    return last_year, last_month,  last_file_date

def next_date(y, m):
    """ Calculate the next file date to download
    
        Parameters: int, last_year
                    int, last_month
                    
        Returns: str
    """

    if m != 12:
        next_file_date = str(y) + "_" + f'{(m+ 1):02d}'
    else:
        next_file_date = str(y + 1) + "_" + "01"
    return next_file_date

def download(nfd):
    """ Download the next pdf file.
    
        Parameters: str
        
        Returns: none
    """
    
    next_file_url = (url_database + nfd + "_2.pdf")
    next_file = (path_pdf + nfd + "_2.pdf")
    response = requests.get(next_file_url, headers={"User-Agent": "Mozilla/5.0"})
    open(next_file, "wb").write(response.content)
    print("Site response = " + str(response.status_code))
    os.startfile(next_file)



def read_pdf(nfd, pg, table):
    """ Read pdf file saving table as Dataframe.

        Parameters: nfd : str, next file date
                    pg : str, file page number where the table is, numeral.
                    table : int, table index to be read on pg.

        Returns : Dataframe.
    """

    table_read = camelot.read_pdf(path_pdf + nfd + "_2.pdf", pages = pg, flavor='stream')
    df_read = table_read[table].df
    return df_read


def clean_df (df, nfd):
    """Clean and format Dataframe.

        Parameters: df : Dataframe, df_read.
                    nfd: str, next file date

        Returns: Dataframe, showing models and quantities.
    """

    df_cleaned = df.iloc[:, 1:3]
    df_cleaned = df_cleaned.replace("", np.nan)
    df_cleaned.dropna(axis=0, inplace=True)
    df_cleaned = df_cleaned.set_axis(["Modelo", str(nfd)], axis=1)
    df_cleaned = df_cleaned[df_cleaned["Modelo"].str.contains("Modelo") == False]    # remove linha com Modelo
    df_cleaned.reset_index(inplace=True, drop=True)
    df_cleaned = df_cleaned.astype("string")
    df_cleaned[str(nfd)] = [re.sub(r"\.", "", i) for i in df_cleaned[str(nfd)]]
    df_cleaned[str(nfd)] = df_cleaned[str(nfd)].astype("int64")
    return df_cleaned


def save_df (df, nfd, xlsx_name):
    """Save Dataframe as xlsx and open it for visual inspection.

        Parameters: df : Dataframe, df_cleaned
                    xlsx_name : str, xlsx file name to be save.
                    nfd: str, next file date
    """

    xls = (path_other_tables + nfd + "_" + xlsx_name + ".xlsx")
    df.to_excel(xls)
    os.startfile(xls)

    if len(df) != 50:
        answer = "N"
        while answer != "Y":
            answer = str.upper(input("Table shoud have 50 rows. \n VERIFY! \n Want to continue? (Y/N)"))


def master (lfd, nfd, master_name, df):
    """ Read prior master file, add new month dataframe, clean and save it.

        Parameters: master_name : Dataframe, to open.
                    df : Dataframe, to merge with.

        Returns: New Master Dataframe
    """

    master = pd.read_excel(path_master_tables + lfd + "_" + master_name + "_1.xlsx")
    master = pd.merge(master, df, how="outer", on="Modelo")
    master = master.fillna(0)
    master.loc[:, "2017_11":str(nfd)] = master.loc[:, "2017_11":str(nfd)].astype("int")
    master.set_index("Modelo", inplace = True)
    master = master.loc[(master!=0).any(axis=1)]       # remove linhas com zero qnt
    master.to_excel(path_master_tables + nfd + "_" + master_name + "_1.xlsx")
    return master


# 10 - Verify files already processed
last_year, last_month, last_file_date = past_date()
print("last file ", last_file_date, " year ", last_year, " month ", last_month)

# 20 - Define next file date
next_file_date = next_date(last_year, last_month)
print("New file date > ", next_file_date)

answer = "N"
while answer != "Y":
    answer = str.upper(input("The last update were on " + str(last_file_date) + 
    ".\nThe next file to download is " + str(next_file_date) + ".\nDo you want to continue? (Y/N)"))

# 30 - Download pdf file
new_file = download(next_file_date)

#  40 - Update master df
df_cars_read = read_pdf(next_file_date, "6", 0)
print(df_cars_read.head())

df_cars_cleaned = clean_df(df_cars_read, next_file_date)
print(df_cars_cleaned.head())

save_df(df_cars_cleaned, next_file_date, "df_cars")

df_master = master(last_file_date, next_file_date, "df_master", df_cars_cleaned)
print(df_master.head())


print("\nES HAT GETAN")

