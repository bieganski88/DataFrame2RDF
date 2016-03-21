# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 08:00:41 2016

@author: Przemyslaw Bieganski, WIZIPISI

Skrypt ma na celu konwersje danych do formatu RDF.
W celu prawidlowej transformacji do kazdego pliku musi byc dolaczony
plik konfiguracyjny ze schematem.

Dane ladowane sa wpierw do pandas DataFrame.
Z tej postaci dopiero do RDF.

Plik konfiguracyjny wzorowany jest na sposobie ladowania CSV
w CYPHER'ze.

"""
import codecs
import common as cm
import bebechy as bb
import konfiguracja as cfg

data2load = ['src/xlsx/osoby_fizyczne.xlsx' , 'src/xlsx/osoby_fizyczne.py']

# wczytywanie danych z plikow zrodlowych do DATA FRAME
# docelowo obsluga CSV, SHP oraz XLSX.
#informacje = cm.load_excel(data2load[0], 3)
informacje = cm.load_shp_to_dataframe('D:/Wizipisi_DataScience/004.AllegroGraph/005.python_projects/01.DataFrame2RDF/src/shp/przylacza_wodne_24.shp', 'Windows-1250')
informacje_schemat = cfg.CONFIG

# walidacja poprawnosci pliku konfiguracyjnego wzgledem DATA FRAME
try:
    assert bb.check_schema(informacje, informacje_schemat) == True
except:
    print "Sprawdzanie konfiguracji zakonczone niepowodzeniem."

# konwersja DATA FRAME do RDF

rdf = bb.konwertujDataFrame(informacje, informacje_schemat)

print type(rdf)

# zapis do pliku
text_file = codecs.open("dest/Output.xml", "w", "utf-8")
text_file.write(rdf)
text_file.close()
del text_file