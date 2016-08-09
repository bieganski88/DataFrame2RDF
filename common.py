# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 09:16:23 2016

@author: Przemyslaw Bieganski [bieg4n@gmail.com, przemyslaw.bieganski.88@gmail.com]
"""
# wczytywanie modulow - zewnetrzne moduly
import pandas as pd
import fiona
import geopandas
import random

# ladowanie dancyh
def load_excel(path, sheet):
    '''Wczytuje excela do data frame.
    Parametry wejsciowe:
    - path - sciezka do pliku,
    - sheet - numer arkusza w excelu zaczynajac numeracje od 0.
    Laduje dane do pamieci w postaci data frame.'''
    print '\nWczytuje dane z pliku EXCEL z lokalizacji: {}'.format(path)
    xls_file = pd.ExcelFile(path)
    data_frame = xls_file.parse(xls_file.sheet_names[sheet])
    
    print 'Wczytywanie zakonczono!'
    
    return data_frame



def load_shp_to_dataframe(sciezka, kodowanie):
    '''Wczytuje dane z plikow SHP.
    Zachowuje odpowiedni porzadek kolumn.
    '''
    # otwieranie SHP przy pomocy fiony
    layer = fiona.open(sciezka, encoding = kodowanie)
    schemat = layer.schema['properties']
    
    column_order = []
    for name in schemat:
        column_order.append(name)
    column_order.append('geometry') # jako ostatni atrybut
    
    # wczytywanie data frame    
    plik = geopandas.GeoDataFrame.from_features(layer)
    # zmiana kolejnosci wyswietlania kolumn
    plik = plik[column_order]
    
    return plik


def generuj_date(start, koniec):
    '''Generuje pelna date zgodna z ISO dla zadanego przedzialu
    czasowego. Z dokladnoscia do dnia.
    start - rok poczatkowy,
    koniec - rok koncowy.
    '''
    
    rok = random.choice(range(start+1, koniec+1))
    
    miesiac = random.choice(range(1,13))
    if miesiac == 2:
        dzien = random.choice(range(1,29))
    else:
        dzien = random.choice(range(1,32))
    kompletna_data = '{}-{}-{}T00:00:00+01:00'.format(rok, str(miesiac).zfill(2), str(dzien).zfill(2))
    
    return kompletna_data