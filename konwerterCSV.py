# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 08:00:41 2016

@author: Przemyslaw Bieganski [bieg4n@gmail.com, przemyslaw.bieganski.88@gmail.com]

Skrypt ma na celu konwersje danych do formatu RDF.
W celu prawidlowej transformacji do kazdego pliku musi byc dolaczony
plik konfiguracyjny ze schematem.

Dane ladowane sa wpierw do pandas DataFrame.
Z tej postaci dopiero do RDF.

Plik konfiguracyjny wzorowany jest na sposobie ladowania CSV
w CYPHER'ze.

"""
import pandas as pd
import json
import codecs
import common as cm
import bebechy as bb
import konfiguracjaCSV as cfg

for data2load in cfg.data:

    # load CSV
    try:
        loadPath = 'src/csv/{}'.format(data2load[0])
        informacje = pd.read_csv(loadPath, delimiter = ';', encoding = "utf8")
        print '\n\n###########  {}  ############\n'.format(loadPath)
        print 'Ladowanie CSV >> OK!'
    except:
        print 'Nie udalo sie zaladowac pliku CSV: {}'.format(loadPath)
        break
    
    # load JSON -schema
    try:
        loadPath = 'src/csv/{}'.format(data2load[1])
        jason = json.loads(open(loadPath, 'r').read())
        informacje_schemat = jason['CONFIG']
        print 'Ladowanie JSON >> OK!\n'
    except:
        print 'Nie udalo sie zaladowac pliku JSON: {}'.format(loadPath)
        break
    
    # walidacja poprawnosci pliku konfiguracyjnego wzgledem DATA FRAME
    try:
        assert bb.check_schema(informacje, informacje_schemat) == True
    except:
        print "Sprawdzanie konfiguracji zakonczone niepowodzeniem."
    
    # konwersja DATA FRAME do RDF
    
    rdf = bb.konwertujDataFrame(informacje, informacje_schemat)
    
    
    # zapis do pliku
    outputName = 'dest/{}.rdf'.format(data2load[0].replace('.csv', ''))
    print '\nZapis RDF/XML w lokalizacji:{}'.format(outputName)
    try:
        text_file = codecs.open(outputName, "w", "utf-8")
        text_file.write(rdf)
        text_file.close()
        del text_file
    except:
        print 'Nie udalo sie zapisac pliku {}\n'.format(outputName)
        break
    print 'Zapis do lokalizacji {} zakonczony powodzeniem.'.format(outputName)