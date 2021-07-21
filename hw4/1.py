# -*- coding: utf-8 -*-
"""
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru,
yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:

название источника;
наименование новости;
ссылку на новость;
дата публикации.
"""

from pprint import pprint
from lxml import html
from copy import deepcopy
import requests, re, pandas as pd
from datetime import datetime
#from fake_headers import Headers

#header
header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

#работа с сайтом mail.ru
site1='https://news.mail.ru/'
res=requests.get(site1,headers=header)
root=html.fromstring(res.text)

result = root.xpath("//ul[contains(@class,'list list_type_square list_half js-module')]")

news={
      'resource':   [],
      'hea':        [],
      'link':       [],
      'date':       []
}

for elem in result:
    link=elem.xpath(".//li[@class='list__item']/a/@href")
    hea=elem.xpath(".//li[@class='list__item']/a/text()")
    for l in link:
        news['resource'].append('Mail.ru')
        news['link'].append(str(l))
        
        #извлечение даты с переходом на след. страницу
        date=requests.get(str(l),headers=header)
        date=html.fromstring(date.text)
        date=date.xpath("//span[contains(@class,'note__text breadcrumbs__text js-ago')]/@datetime")
        date=date[0]
        date=datetime.fromisoformat(date)
        news['date'].append(date)        
        
      
    for h in hea:
        news['hea'].append(str(h).replace('\xa0',' '))

#работа с сайтом lenta.ru
site2='https://lenta.ru/parts/news/'
res=requests.get(site2,headers=header)
root=html.fromstring(res.text)

news_Lenta={
      'resource':   [],
      'hea':        [],
      'link':       [],
      'date':       []
}

struct="//section[@class[substring(.,string-length(.) - string-length('b-parts-layout__longrid') + 1) = 'b-parts-layout__longrid']]/div"
result = root.xpath(struct)
result=result[0].xpath(".//div[contains(@class,'item') and contains(@class,'news')]")

tme=datetime.today() #сегодняшняя дата

for x in result: #проход по новостным блокам
    x=x.xpath(".//div")
    
    dte=str(x[0].xpath('.//text()')[-1]) 
    dte=dte.split(':')
    tm=deepcopy(tme)
    tm=tm.replace(hour=int(dte[0]),minute=int(dte[1]))#время    
    
    hea=str(x[1].xpath(".//h3//a//text()")[0]).replace('\xa0',' ') #заголовок    
    
    link=str(x[1].xpath(".//h3//a//@href")[0])
    if link[0]=='/':
        link='https://lenta.ru'+link #ссылка
        resource='lenta.ru' #источник
    else:
        resource='Сторонний ресурс' #источник
        pass
    
    news_Lenta['resource'].append(resource)
    news_Lenta['hea'].append(hea)
    news_Lenta['link'].append(link)
    news_Lenta['date'].append(tm)


#работа с сайтом Яндекс.Новости
site3='https://yandex.ru/news/'
res=requests.get(site3,headers=header)
root=html.fromstring(res.text)

news_Yandex={
      'resource':   [],
      'hea':        [],
      'link':       [],
      'date':       []
}

result = root.xpath("//div[contains(@class,'mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top')]/div[contains(@class,'mg-grid__col mg-grid__col_xs_8')]")

for elem in result:
    elm=elem.xpath(".//div[contains(@class,'mg-card__inner')]")
    link=str(elm[0].xpath(".//a/@href")[0]) #ссылка
    hea=str(elm[0].xpath(".//a/h2/text()")[0]) #заголовок
    
    #извлечение времени и источника
    el=elm[0].xpath(".//div[contains(@class,'mg-card-source mg-card__source mg-card__source_dot')]")[0]
    resource=el.xpath(".//span[contains(@class,'mg-card-source__source')]")
    resource=str(resource[0].xpath(".//a/text()")[0])
    
    time=str(el.xpath(".//span[contains(@class,'mg-card-source__time')]/text()")[0])
    time=time.split(":")
    tm=deepcopy(tme)
    tm=tm.replace(hour=int(time[0]),minute=int(time[1]))#время
    
    news_Yandex['resource'].append(resource)
    news_Yandex['hea'].append(hea)
    news_Yandex['link'].append(link)
    news_Yandex['date'].append(tm)

result = root.xpath("//div[contains(@class,'mg-grid__row mg-grid__row_gap_8 news-top-flexible-stories news-app__top')]/div[contains(@class,'mg-grid__col mg-grid__col_xs_4')]")

for elem in result:
    elm=elem.xpath(".//div[contains(@class,'mg-card__text')]")
    link=str(elm[0].xpath(".//a/@href")[0]) #ссылка
    hea=str(elm[0].xpath(".//a/h2/text()")[0]) #заголовок
    
    #извлечение времени и источника
    el=elem.xpath(".//div[contains(@class,'mg-card-source mg-card__source mg-card__source_dot')]")
    resource=el[0].xpath(".//span[contains(@class,'mg-card-source__source')]")
    resource=str(resource[0].xpath(".//a/text()")[0])
    
    time=str(el[0].xpath(".//span[contains(@class,'mg-card-source__time')]/text()")[0])
    time=time.split(":")
    tm=deepcopy(tme)
    tm=tm.replace(hour=int(time[0]),minute=int(time[1]))#время
    
    news_Yandex['resource'].append(resource)
    news_Yandex['hea'].append(hea)
    news_Yandex['link'].append(link)
    news_Yandex['date'].append(tm)

news_Mail=pd.DataFrame(news)
news_Lenta=pd.DataFrame(news_Lenta)
news_Yandex=pd.DataFrame(news_Yandex)
news_all=pd.concat([news_Mail,news_Lenta,news_Yandex])
print(news_all)