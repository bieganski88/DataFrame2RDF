# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 10:18:15 2016

@author: wizipisi-007
"""

def check_schema(df, config):
    '''
    Sprawdzenie czy schemat jest poprawny wzgledem data frame.
    Wejscie to df - data frame, config - dict z konfiguracja.
    Zwraca TRUE lub FALSE.
    '''
    print "Sprawdzanie schematu z faktycznymi danymi."
    flag = True # stan poczatkowy
    
    # lista kolumn w df
    print "Kolumny w DATA FRAME"
    kolumny = list(df.columns.values)
    print kolumny
    
    # wczytuje poszczegolne elementy z konfigu
    try:
        namespaces = config['NAMESPACES']
        about = config['ABOUT']
        literal = config['LITERAL']
        reference = config['REFERENCE']
        geom = config['GEOM']
        print "Kluczowe elementy >> OK!"
    except:
        print "Brak kluczowych elementow w pliku CFG."
        return False
    
    # licznosc elementow
    try:
        assert len(namespaces) > 0
        assert len(about) > 0
        print "Licznosc elementow >> OK!"
    except:
        print 'Brak zadeklarowanych przestrzeni nazw albo subjectu.'
        return False
    
    # zgodnosc atrybutow df vs config
    do_sprawdzenia = [about, literal, reference, geom]
    
    for item in do_sprawdzenia:
        if len(item.keys()) > 0:
            for klucz in item.keys():
                try:
                    assert klucz in kolumny
                except:
                    print 'Niepoprawne klucz dla: {}'.format(klucz)
                    return False
                    
                try:
                    assert item[klucz][0] in namespaces.keys()
                except:
                    print 'Niepoprawny namespace dla: {}'.format(klucz)
                    return False
                
                try:
                    if item in [about, literal]:
                        assert len(item[klucz]) == 2
                except:
                    print 'Dla {} brak/zbyt wiele namespace lub klas.'
                    return False
                    
    print "Nazwy atrybutow df vs config >> OK!"
    
    return flag



def konwertujDataFrame(df, config):
    '''
    '''
    # spis elemntow do zaladowania
    namespaces = config['NAMESPACES']
    about = config['ABOUT']
    literal = config['LITERAL']
    reference = config['REFERENCE']
    geom = config['GEOM']
    
    # zmienna, do ktorej beda zapisywane wszystkie wersy
    xml = ['<?xml version="1.0"?>\n']
    
    # DELKARACJA PLIKU I NAMESPACE
    xml.append('<RDF ')
    for namespace in namespaces.keys():
        xml.append('{} = "{}"\n'.format(namespace, namespaces[namespace]))
    xml.append('>\n')
    
    # iteruje po obiektach w data frame
    for index, row in df.iterrows():
        # rozpoczecie ABOUT
        about_keys = about.keys()
        namespace = namespaces[about[about_keys[0]][0]] # namespace
        wartosc = row[about_keys[0]]
        typ = about[about_keys[0]][1]
        xml.append(u'<Description rdf:about="{}{}">\n'.format(
                    namespace, wartosc)) # wartosc z df
        xml.append(u'<rdf:type rdf:resource="{}{}"/>\n'.format(
                    namespace, typ))
        
        # LITERAL jesli wystepuje
        literal_keys = literal.keys()
        if len(literal_keys) > 0:
            for obj in literal_keys:
                klucz = obj
                ns = literal[obj][0]
                typ = literal[obj][1]
                xml.append(u'<{}:{}>{}</{}:{}>\n'.format(
                        ns, typ, row[klucz], ns, typ))
        
        # REFERENCE jesli wystepuje
        ref_keys = reference.keys()
        if len(ref_keys) > 0:
            for obj in ref_keys:
                ns = reference[obj][0]
                nsObj = namespaces[reference[obj][2]]
                predykat = reference[obj][1]
                
                xml.append(u'<{}:{} rdf:resource="{}{}"/>\n'.format(
                ns, predykat, nsObj, row[obj]))
        
        # GEOM jesli wystepuje
                
        
        # konczenie ABOUT
        xml.append(u'</Description>\n\n')
    
    # znacznik zamykajacy
    xml.append('</RDF>')
    
    # łączenie listy w jedna calosc
    xml = ''.join(xml)
    
    return xml