#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 29 16:54:24 2022

@author: mathilde
"""

import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
import numpy as np

## FUNZIONI

def input_csv():
    e=str(input('Estensione? '))
    nome=str(input('Nome file: '))
    if ('xml' in e):
        df=pd.read_xml(nome)
        df=df.set_index('id.1')
        df=df.drop(columns=['person_id'])
       # print(df)
    elif ('json' in e):
        df=pd.read_json(nome)
       # print(df)
        df=df.drop(columns=['iperson_id'])
        df=df.set_index('id.1')
    elif ('csv' in e):
        df=pd.read_csv(nome)
       # print(df)
        df=df.set_index('id.1')
        df= df.drop(columns=['person_id'])
    elif (('db' or 'database') in e):
        conA=sqlite3.connect(nome)
        cur=conA.cursor()
        cur.execute('SELECT*FROM people')
        df=pd.DataFrame(cur.fetchall())
        df.columns=['id','first_name','last_name','email','gender','ip_address','country']
    else:
        print('Formato non supportato!')
        #salva su database
    try:
        conA=sqlite3.connect('people_data.db')
        cur=conA.cursor()
        cur.execute("CREATE TABLE people (id,first_name, last_name, email, gender,ip_address, country)")
        cur.executemany("INSERT INTO people VALUES(?,?,?,?,?,?,?)",df.values)
        conA.close()
    except:
        print('Database già aggiornato')
    return(df)

def output_su_db(x):
#create a relational database
    conA=sqlite3.connect('people_data_new.db')
    cur=conA.cursor()
# intestazione colonne
    try:
        cur.execute("CREATE TABLE people (id,first_name, last_name, email, gender,ip_address, country)")
    except:
       pass
    cur.executemany("INSERT INTO people VALUES(?,?,?,?,?,?,?)",x.values)
    conA.commit()
    conA.close()
    print('Salvato sul database. Prossima operazione.')
 
def output_su_db1(x):
    conA=sqlite3.connect('people_data_new.db')
    cur=conA.cursor()
    cur.execute("CREATE TABLE country_table(id,first_name, last_name, email, gender,ip_address, country)")
    cur.executemany("INSERT INTO country_table VALUES(?,?,?,?,?,?,?)",x.values)
    conA.commit()
    conA.close()
    print('Salvato sul database. Prossima operazione.')

def output_su_db2(x,y,z):
    conA=sqlite3.connect('people_data_new.db')
    cur=conA.cursor()
    cur.execute("CREATE TABLE people_nazione(indice,quantità)")
    cur.execute("CREATE TABLE people_genere(indice,quantità)")
    cur.execute("CREATE TABLE people_IP(indice,quantità)")
    cur.executemany('INSERT INTO people_nazione VALUES(?,?)',x.values)
    cur.executemany('INSERT INTO people_genere VALUES(?,?)',y.values)
    cur.executemany('INSERT INTO people_IP VALUES(?,?)',z.values)
    conA.commit()
    conA.close()
    print('Salvato sul database. Prossima operazione')

def output_su_db3(x,y):
    conA=sqlite3.connect('people_data_new.db')
    cur=conA.cursor()
    cur.execute("CREATE TABLE dominio_gender(domino,gender,quantità)")
    cur.execute("CREATE TABLE domino_pease(idominio,paese,quantità)")
    cur.executemany('INSERT INTO dominio_gender VALUES(?,?,?)',x.values)
    cur.executemany('INSERT INTO domino_pease VALUES(?,?,?)',y.values)
    conA.commit()
    conA.close() 
    print('Salvato sul database. Prossima operazione.')
  
   
  
def IP_class(x):
    array=x.split('.')
    if int(array[0])<128:
        return('class A')
    elif (int(array[0])>=128) and (int(array[0])<192):
        return('class B')
    elif (int(array[0])>=192) and (int(array[0])<224):
        return('class C')
    elif (int(array[0])>=224) and (int(array[0])<241):
        return('class D')
    else:
        return('class E')

def dominio(x):
    array=x.split('@')
    array2=array[1].split('.')
    return(array2[0])

  
#MAIN
df=input_csv()
while(1!=0):
    a=int(input('Operazione desiderata. Scegliere tra aggiungere una persona, tasto 1; Lista degli utenti di data nazione, tasto 2; ottenere statistiche sui dati,tasto 3; statistiche avanzate, tasto 4; Uscire dal programma, tasto 5: '))
    if a==1:
        print('"Scrivere in ordine:')
        id_,nome,cognome,email,genere,IP,nazione = str(input('Id,nome,cognome,email,genere,indirizzoIP,nazione: ')).split(',')
        pers=pd.DataFrame([[id_],[nome],[cognome],[email],[genere],[IP],[nazione]])
        pers=pers.transpose()
        pers.columns=['id','first_name','last_name','email','gender','ip_address','country']
        df=pd.concat([df,pers],join='inner')
        # export db
        output_su_db(df)
    elif a==2: 
        df['count']=np.ones((len(df),1))
        nazioni=df[['count','country']].groupby('country').sum()
        country=str(input('Scegli la nazione tra:' +str(nazioni.index.values)+' : '))
        lista_p_nazioni=df[df['country']==country]
        lista_p_nazioni=lista_p_nazioni.drop(columns='count')
        print('Lista di persone per la nazione ' + str(country)+': ')
        print(lista_p_nazioni)
    
    ## export db
        output_su_db1(lista_p_nazioni)
    elif a==3:
    # trasferisce i dati su dataframe pandas
        df['count']=np.ones((len(df),1))
        print('Numero di persone per nazione:')
        print(df[['count','country']].groupby('country').sum())
        somma_nazione=df[['count','country']].groupby('country').sum()
        print(somma_nazione)
        somma_nazione.plot(kind='bar', width=0.8,edgecolor='black',figsize=(60,20))
        plt.xticks(rotation=90)
        plt.ylabel('nr.people',fontsize=20)
        plt.yticks(np.arange(0, 600+1,20))
        plt.xlabel('country',fontsize=20)
        plt.grid(axis='y')
        plt.savefig('risultati/somma_nazione.png',dpi=300,bbox_inches='tight')
    
        somma_nazione['nazioni']=somma_nazione.index
        print(somma_nazione.describe())
        print('Numero di persone per genere:')
        genere=df[['count','gender']].groupby('gender').sum()
        genere['genere']=genere.index
        print(genere)
        print(genere.describe())
        genere.plot(kind='bar',edgecolor='black')
        plt.xticks(rotation=90)
        plt.grid(axis='y')
        plt.savefig('risultati/genere.png',dpi=300,bbox_inches='tight')

        print('IP per classi:')
        df['classe']=df['ip_address'].apply(IP_class)
        IP=df[['count','classe']].groupby('classe').sum()
        IP['classe_indirizziIP']=IP.index
        print(IP)
        print(IP.describe())
        IP.plot(kind='bar',width=0.7,edgecolor='black')
        plt.xticks(rotation=90)
        plt.grid(axis='y')
        plt.savefig('risultati/classiIP.png',dpi=300,bbox_inches='tight')

        #export db 

        output_su_db2(somma_nazione,genere,IP)


    elif a==4:
        
        ##DOMINIO
        df['dominio']=df['email'].apply(dominio)
        classi_dominio=df[['dominio','gender','country']]
        print(classi_dominio.describe())
        classi_dominio['count']=np.ones((len(classi_dominio),1))
        sudd=classi_dominio[['gender','dominio','count']].groupby(['dominio','gender']).sum()
        print(sudd.describe())
        sudd.plot(kind='bar',width=0.9,figsize=(150,50))
        plt.xticks(rotation=90)
        plt.savefig('risultati/dominio_gender.png',dpi=300,bbox_inches='tight')
        #export db 
        sudd2=classi_dominio[['country','dominio','count']].groupby(['dominio','country']).sum()
        print(sudd2.describe())
        sudd2.plot(kind='bar',width=0.9,figsize=(150,50))
        plt.xticks(rotation=90)
        plt.savefig('risultati/dominio_country.png',dpi=300,bbox_inches='tight')
        print('Il dominio più ricorrente è Google. Le scale dominio-gender e dominio-country non sono paragonabili')


        gf=classi_dominio[['country','dominio','gender','count']].groupby(['dominio','country','gender']).sum()
        gf.plot(kind='bar',width=0.9,figsize=(150,50))
        plt.savefig('risultati/dominio.png',dpi=300,bbox_inches='tight')
        print('Nessuna correlazione significativa tra dominio-gender e domninio-country a parte qualche eccezione: il dominio sembra essere distribuito in modo abbastanza uniforme (Vedi grafico dominio.png).')
        output_su_db3(sudd,sudd2)
        
        ##FORMA E_MAILS
        
        
    elif a==5:
        print('Termine del programma.')
        break
    else:
        print('Errore!! Prova ancora.')    
#def convert_xml_to_csv():
    #...
#def convert_json_to_csv():
    #..