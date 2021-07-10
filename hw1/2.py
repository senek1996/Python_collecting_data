# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 13:32:18 2021

@author: Lenovo
"""

import requests, json
from pprint import pprint

numb='a001aa22' #буквы латинские, без пробелов
ser=f'http://avto-nomer.ru/mobile/api_photo_test.php?nomer={numb}'

res=requests.get(ser)
d=json.loads(res.text)
try:
    last_car=d['cars'][len(d['cars'])-1]
    print('Номер {} закреплен за автомобилем {} {} (дата: {})'.format(numb.upper(),\
                        last_car['make'],last_car['model'],last_car['date'][:10]))
except:
    print('Номер {} отсутствует в базе'.format(numb.upper()))