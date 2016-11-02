import random
import string
import urllib

import requests
import tracery
from tracery.modifiers import base_english
import json
from secret import *


weapons = json.load(open("guns_n_rifles.json"))['weapons']
toxins = json.load(open("toxic_chemicals.json"))['chemicals']
objects = json.load(open("objects.json"))['objects']
metals = json.load(open("metals.json"))['metals']
tech = json.load(open("new_technologies.json"))['technologies']
codenames = json.load(open("nsa_projects.json"))['codenames']
body_parts = json.load(open("bodyParts.json"))['bodyParts']
body_fluids = json.load(open("abridged-body-fluids.json"))['abridged body fluids']
interjections = json.load(open("interjections.json"))['interjections']


WORDNIK_API = 'http://api.wordnik.com:80/v4'
headers = {'content-type': 'application/json',
           'api_key': WORDNIK_API_KEY}


def generate_object():
    puns = []

    while not puns:
        # Pick the random object up front
        obj = random.choice(objects)

        searchable_obj = obj.split(' ')[-1]
        # Create terrible puns for the replies
        r = requests.get(WORDNIK_API + '/word.json/{}/relatedWords'.format(urllib.parse.quote(searchable_obj)), headers=headers).json()
        for words in r:
            if words['relationshipType'] == 'rhyme':
                puns = [w for w in words['words'] if not w[0].istitle()]
    return obj, puns

start_rules = {
    'origin': '''"#hello.capitalize#, James. I #want# to #showyou# #our# #next# #toy#".

    #james response#

    #demo rules#

    #james reacts#
    ''',
    'hello': ['hello', 'greetings', 'howdy', 'good day'],
    'want': ['want', 'am happy', 'am delighted', "couldn't be more excited", 'am just delighted', 'am anxious'],
    'showyou': ['show you', 'demonstrate', 'show off', 'present to you', 'let you see'],
    'our': ['our', 'my', "the department's", "Her Majesty's", "the team's", "your"],
    'next': ['next', 'newest', 'latest', 'finest', 'proudest'],
    'toy': ['toy', 'contraption', 'device', 'little trick', 'weapon', 'latest', 'technical wonder'],

    # James responds
    'james response': '"#hello2.capitalize#, Q," James #said#, #interested#. "What #manner# of #device# do you have for me #now#?"',
    'hello2': ['greetings', 'cheerio', 'yes yes', 'indeed', 'as you say', 'hullo'],
    'said': ['said', 'replied', 'intoned', 'answered', 'nodded', 'grunted'],
    'interested': ['interested', 'intrigued', 'curious', 'in anticipation', 'excitedly', 'enthusiastically'],
    'manner': ['manner', 'kind', 'type', 'sort'],
    'device': ['device', 'prop', 'toy', 'contraption', 'thing', 'wonder', 'surprise'],
    'now': ['now', 'today', 'at last', 'again', 'once again', 'this morning'],

    # Q does his demo
    'demo rules': """[device:#object#]Q #held up# #device.a#. "I #know# it looks like #ordinary.a# #device#, but if you #look carefully#, #it turns out that# \
it's #actually# a #weapon type#." """,
    'held up': ['held up', 'walked over to', 'waved his arm towards', 'gestured at', 'nodded towards', 'lifted', 'picked up'],
    'know': ['know', 'realize', 'understand'],
    'ordinary': ['ordinary', 'simple', 'everyday', 'innocent', 'boring'],
    'object': None,
    'look carefully': ['examine it closely', 'unscrew the top', 'turn it over', 'rotate it thus', 'use your voice print',
                      'trigger the remote', 'reverse it', 'whistle', 'blink twice', 'hum'],
    'it turns out that': ['it turns out that', 'in fact', 'in reality'],
    'actually': ['actually', 'really', 'truly', 'revealed to be', 'uncovered to be'],
    'weapon type': ["#gun#", "#trap# that #shoots# #shootables#", "#grenade# that #shoots# #shootables#"],
    'gun': weapons,
    'trap': ["trap", "snare"],
    'shoots': ['shoots', 'dispenses', 'showers the victim with', 'rains', 'sprays', 'aerosolizes'],
    'grenade': ['grenade', 'mine', 'boobytrap', 'dart gun'],
    'shootables': toxins,

    # James reacts
    'james reacts': '"#interjection.capitalize##reaction punct#" James #exclaimed#. #pun#',
    'reaction punct': ['!'],
    'interjection': interjections,
    'exclaimed': ['exclaimed', 'shouted', 'hollard', 'said', 'replied', 'gasped'],

    # The pun generation
    'pun': '"#that certainly will.capitalize# #pun phrase#."',
    'that certainly will': ['that #object# certainly will', 'that #object# definitely will', "that #object# will",
                            "they'll never expect that #object# to "],
    'pun phrase': None
}

tired = {
    'reaction punct': ['.'],
    'exclaimed': ['sighed', 'murmured', 'mumbled', 'whispered'],
    'interjection': ['huh', 'gee', 'fine', 'yes well', 'yes yes', "that's all good"],
    'interested': ['bored', 'staring at his fingernails', 'brushing a speck of dust off his tuxedo', 'staring into space',
              'clearly bored', 'clearly tired', 'obviously uninterested', 'with obvious boredom', 'with indifference'],
}

dead = {
    'james response': ["There was no response, which did not dampen Q's enthusiasm.", "There was no response as he was the only one still alive in the room.",
                       "Only the haunting sound of running machinery answered him.", "The emptiness of the room echoed terribly."],
    'james reacts': ['James said nothing, because he was dead.', "James' corpse had no response.",
                     "James's body continued to lie there."]
}

not_first = {
    'hello': ['next up', 'just one more thing', 'next', 'for another thing', 'even better', 'yet more']
}


def demo():
    print(start_grammar.flatten('#origin#'))

iterations = 10
for i in range(0, iterations):
    if i == 1:
        start_rules.update(not_first)
    elif i > iterations * .60:
        start_rules.update(dead)
    elif i > iterations * .30:
        start_rules.update(tired)
    obj, puns = generate_object()
    start_rules.update({'object': obj, 'pun phrase': puns})
    start_grammar = tracery.Grammar(start_rules)
    start_grammar.add_modifiers(base_english)
    if i == iterations / 30:
        print("\nUnfortunately by this point, James had gone several hours without liquor, and died from withdrawl.\n")
    demo()
