# -*- coding: utf-8 -*-
"""
Created on Sat Jul 10 12:48:13 2021

@author: Lenovo
"""

import requests
from pprint import pprint

#требуется предварительная установка командой pip install PyGithub requests
from github import Github 

username='senek1996'
g=Github()
user=g.get_user(username)

for repo in user.get_repos():
    pprint(repo)