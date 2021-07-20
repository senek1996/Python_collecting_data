# -*- coding: utf-8 -*-
"""
Вариант 1

Необходимо собрать информацию о вакансиях на вводимую должность 
с сайтов Superjob и HH. Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать 
в себе минимум:

Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
"""

from bs4 import BeautifulSoup as bs
from fake_headers import Headers
from requests import get
from numpy import nan
from numpy.testing import assert_equal
import pandas as pd
from pymongo import MongoClient

def nan_equal(a,b):
     try:
         assert_equal(a,b)
     except AssertionError:
         return False
     return True

vac=input('Введите вакансию: ')

#работа с hh.ru
que1='https://hh.ru/search/vacancy?\
items_on_page={}\
&order_by={}\
&text={}'.format(500,'salary-desc',vac.replace(' ','-'))

header = Headers(
    browser="yandex",
    os="win",
    headers=True
)

h=header.generate()
res1=get(que1,headers=h).content
soup=bs(res1)
table = soup.find_all('div', 'vacancy-serp-item') #все вакансии

hh_Vacs={
    'name':    [],
    'link':    [],
    'comp':    [],
    'sal_min': [],
    'sal_max': [],
    'sal_exc': []
}

for vac1 in table:
    table1=vac1.find_all('a', 'bloko-link')
    vac_name=table1[0].contents[0] #название вакансии
    vac_link=table1[0]['href'] #ссылка на вакансию
    vac_comp=table1[1].contents #обработка работодателя
    vac_company=''
    for s in vac_comp:
        vac_company=vac_company+str(s.replace('\xa0',''))
    
    del vac_comp
    
    #обработка зарплаты
    table1=vac1.find_all('div',attrs={'class': 'vacancy-serp-item__sidebar'})    
    try:
        vac_sal=table1[0].contents[0].contents[0]
        vac_sal=vac_sal.replace('\u202f','').replace(' – ','-')
        vac_sal=vac_sal.split(' ')
        vac_sal_exch=vac_sal[1] #валюта
        vac_sal=vac_sal[0]
        vac_sal=vac_sal.split('-')
        if len(vac_sal)==2: #есть мин/макс зарплата
            vac_sal_min=int(vac_sal[0]) #минимальная зарплата
            vac_sal_max=int(vac_sal[1]) #максимальная зарплата
        elif len(vac_sal)==1: #фикс. зарплата
            vac_sal_min=int(vac_sal[0]) #минимальная зарплата
            vac_sal_max=vac_sal_min #максимальная зарплата
        else: #зарплата не указана
            vac_sal_min=nan #минимальная зарплата
            vac_sal_max=nan #максимальная зарплата
    except:
        vac_sal_exch=nan #валюта
        vac_sal_min=nan #минимальная зарплата
        vac_sal_max=nan #максимальная зарплата
        
    
    hh_Vacs['name'].append(str(vac_name))
    hh_Vacs['link'].append(str(vac_link))
    hh_Vacs['comp'].append(vac_company)
    hh_Vacs['sal_min'].append(vac_sal_min)
    hh_Vacs['sal_max'].append(vac_sal_max)
    hh_Vacs['sal_exc'].append(str(vac_sal_exch).replace('.','') if not vac_sal_exch is nan else vac_sal_exch)

hh_Vacs=pd.DataFrame(hh_Vacs)


#работа с Superjob
que2='https://russia.superjob.ru/vakansii/{}.html?\
click_from=facet&order_by%5Bpayment_sort%5D=\
desc'.format(vac.replace(' ','-'))
res2=get(que2,headers=h).content
soup=bs(res2)

table = soup.find_all('div', attrs={'class': 'f-test-search-result-item'}) #все вакансии

sj_Vacs={
    'name':    [],
    'link':    [],
    'comp':    [],
    'sal_min': [],
    'sal_max': [],
    'sal_exc': []
}

for vac1 in table:
    #извлечение названия
    vac_name=vac1.find('div',attrs={'class','_1h3Zg _2rfUm _2hCDz _21a7u'})
    if vac_name is None:
        continue
    
    x=vac_name.find('a')
    vac_data=x.contents
    vac_link='https://superjob.ru/'+x['href']      #ссылка на вакансию
    if len(vac_data)==1:
        vac_name=vac_data[0]  #название вакансии
    else:
        vac_name=''
        for s in vac_data:
            try:
                vac_name=vac_name+str(s.contents[0])
            except:
                vac_name=vac_name+str(s)
    
    #извлечение зарплаты
    vac_sal=vac1.find('span',attrs={'class': '_1h3Zg _2Wp8I _2rfUm _2hCDz _2ZsgW'})
    if vac_sal is None:
        vac_sal_exch=nan #валюта
        vac_sal_min=nan #минимальная зарплата
        vac_sal_max=nan #максимальная зарплата
    else:
        vac_sal=vac_sal.contents
        vac_sal2=[]
        
        for x in vac_sal:
            xx=str(x)
            if xx.find('<span>')>-1:
                continue
            xx=xx.replace('\xa0','').replace(' ','')
            if len(xx)>0:
                vac_sal2.append(xx.replace('\xa0','').replace(' ',''))
        
        
        if len(vac_sal2)==2:
            vac_sal_exch=vac_sal2[1] #валюта
            vac_sal_min=int(vac_sal2[0]) #минимальная зарплата
            vac_sal_max=int(vac_sal2[0]) #максимальная зарплата
        elif len(vac_sal2)==3:
            vac_sal_exch=vac_sal2[2] #валюта
            vac_sal_min=int(vac_sal2[0]) #минимальная зарплата
            vac_sal_max=int(vac_sal2[1]) #максимальная зарплата
        elif len(vac_sal2)==1: #По договоренности
            vac_sal_exch=nan #валюта
            vac_sal_min=nan #минимальная зарплата
            vac_sal_max=nan #максимальная зарплата
    
    #извлечение названия компании
    vac_comp=vac1.find('span',attrs={'class': '_1h3Zg _3Fsn4 f-test-text\
-vacancy-item-company-name e5P5i _2hCDz _2ZsgW _2SvHc'})
    x=vac_comp.find('a')
    vac_comp=str(x.contents[0]) #название компании
    
    sj_Vacs['name'].append(str(vac_name))
    sj_Vacs['link'].append(str(vac_link))
    sj_Vacs['comp'].append(vac_comp)
    sj_Vacs['sal_min'].append(vac_sal_min)
    sj_Vacs['sal_max'].append(vac_sal_max)
    sj_Vacs['sal_exc'].append(str(vac_sal_exch).replace('.','') if not vac_sal_exch is nan else vac_sal_exch)

sj_Vacs=pd.DataFrame(sj_Vacs)
Vacs=pd.concat([hh_Vacs,sj_Vacs])
print(Vacs)

#подключение к БД Mongo
client = MongoClient('localhost', 27017)
db = client['work']
vacs_db = db.vacs

for i in range(len(Vacs)):
    rec={
        'name':    [],
        'link':    [],
        'comp':    [],
        'sal_min': [],
        'sal_max': [],
        'sal_exc': []
    }
    xxx=Vacs.iloc[[i]].to_dict()
    for x in xxx:
        for y in xxx[x]:
            if not nan_equal(xxx[x][y],nan):
                rec[x]=xxx[x][y]
    
    #удаление пустых полей
    for x in ['sal_min','sal_max','sal_exc']:
        if rec[x]==[]:
            rec.pop(x)
    
    vacs_db.insert_one(rec)