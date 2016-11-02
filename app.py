import requests
import tracery
from tracery.modifiers import base_english

from secret import *

rules = {
    'origin': '#hello.capitalize#, #location#!',
    'hello': ['hello', 'greetings', 'howdy', 'hey'],
    'location': ['world', 'solar system', 'galaxy', 'universe']
}

grammar = tracery.Grammar(rules)
grammar.add_modifiers(base_english)
print(grammar.flatten("#origin#")) # prints, e.g., "Hello, world!"

WORDNIK_API = 'http://api.wordnik.com:80/v4'
headers = {'content-type': 'application/json',
           'api_key': WORDNIK_API_KEY}
r = requests.get(WORDNIK_API + '/word.json/gun/relatedWords', headers=headers)
print(r.json())
