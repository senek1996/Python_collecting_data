# -*- coding: utf-8 -*-
"""
Created on Tue Aug  3 22:34:52 2021

@author: Lenovo
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
УЧЕБНЫЙ ПРИМЕР

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title

elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
'''

driver = webdriver.Chrome()
driver.get("https://passport.yandex.ru/auth?from=mail&origin=hostroot_homer_auth_ru&retpath=https%3A%2F%2Fmail.yandex.ru%2F%3Fuid%3D126117399&backpath=https%3A%2F%2Fmail.yandex.ru%3Fnoretpath%3D1")

#ввод ящика
field_email=driver.find_element_by_id('passp-field-login') #поле ввода e-mail
field_email.send_keys("bredihin.igorr@yandex.ru")

#нажатие кнопки
button_entr=driver.find_element_by_id('passp:sign-in') #кнопка "Войти"
button_entr.click()

#ввод пароля
pwd='password'
field_pwd=driver.find_element_by_id('passp-field-passwd')
field_pwd.send_keys(pwd)

button_entr=driver.find_element_by_id('passp:sign-in') #кнопка "Войти"