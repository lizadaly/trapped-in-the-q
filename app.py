import random
import string
import time
import urllib

import requests
import tracery
from tracery.modifiers import base_english
import json
from secret import *

print("""
# Trapped in the Q

## A "spy" "novel."
### By Liza Daly for NaNoGenMo 2016

James B. was making one of his usual visits to see the master weaponsmaker at headquarters.
These tours were important, but sometimes they could be a bit tedious!

""")

weapons = json.load(open("guns_n_rifles.json"))['weapons']
toxins = json.load(open("toxic_chemicals.json"))['chemicals']
objects = json.load(open("objects.json"))['objects']
metals = json.load(open("metals.json"))['metals']
tech = json.load(open("new_technologies.json"))['technologies']
codenames = json.load(open("nsa_projects.json"))['codenames']
body_parts = json.load(open("bodyParts.json"))['bodyParts']
body_fluids = json.load(open("abridged-body-fluids.json"))['abridged body fluids']
interjections = json.load(open("interjections.json"))['interjections']
colors = [c['color'].lower() for c in json.load(open("crayola.json"))['colors']]

WORDNIK_API = 'http://api.wordnik.com:80/v4'
headers = {'content-type': 'application/json',
           'api_key': WORDNIK_API_KEY}


def generate_object(from_objects, relationship_type="rhyme", part_of_speech="noun"):
    puns = []

    while not puns:
        # Pick the random object up front
        obj = random.choice(from_objects)
        searchable_obj = obj # obj.split(' ')[-1]
        # Create terrible puns for the replies
        r = requests.get(WORDNIK_API + '/word.json/' + urllib.parse.quote(searchable_obj) + '/relatedWords',
                                                       params={'relationshipTypes': relationship_type,
                                                              'limitPerRelationshipType': 50},
                                                       headers=headers)
        if r.status_code != 200:
            time.sleep(5)
            continue
        for words in r.json():
            clean_words = [w.strip() for w in words['words'] if not w[0].istitle()]
            for word in clean_words:
                r2 = requests.get(WORDNIK_API + '/word.json/' + word + '/definitions',
                                  params={'partOfSpeech': part_of_speech}, headers=headers)
                if len(r2.content) > 0:
                    puns.append(word)

    return obj, puns

start_rules = {
    'origin': '''
"#hello.capitalize#, James. I #want# to #showyou# #our# #next# #toy#."

#james response#

#demo rules#

#james reacts#

#demo continues#

#demo close#

#james final#

    ''',
    'hello': ['hello', 'greetings', 'howdy', 'good day'],
    'want': ['want', 'am happy', 'am delighted', "couldn't be more excited", 'am just delighted', 'am anxious'],
    'showyou': ['show you', 'demonstrate', 'show off', 'present to you', 'let you see'],
    'our': ['our', 'my', "the department's", "Her Majesty's", "the team's"],
    'next': ['next', 'newest', 'latest', 'finest', 'proudest'],
    'toy': ['toy', 'contraption', 'device', 'little trick', 'weapon', 'latest', 'technical wonder'],

    # James responds
    'james response': '"#hello2.capitalize#, Q," James #said#, #interested#. "What #manner# of #device# do you have for me #now#?"',
    'hello2': ['greetings', 'cheerio', 'yes yes', 'indeed', 'as you say', 'hullo'],
    'said': ['said', 'replied', 'intoned', 'answered', 'nodded', 'grunted'],
    'interested': ['interested', 'intrigued', 'curious', 'in anticipation', 'excitedly', 'enthusiastically'],
    'manner': ['manner', 'kind', 'type', 'sort'],
    'device': ['device', 'prop', 'toy', 'contraption', 'thing', 'wonder', 'surprise'],
    'now': ['now', 'today', 'again', 'once again', 'this morning'],

    # Q does his demo
    'demo rules': """[device:#object#]Q #held up# #color.a# #device#. "I #know# it looks like #ordinary.a# #device#, but if you #look carefully#, #it turns out that# \
it's #actually# a #weapon type#. Pure #metal# #shielding#, developed during project #codenames#." """,
    'held up': ['held up', 'walked over to', 'waved his arm towards', 'gestured at', 'nodded towards', 'lifted', 'picked up'],
    'color': colors,
    'know': ['know', 'realize', 'understand'],
    'ordinary': ['ordinary', 'simple', 'everyday', 'innocent', 'boring'],
    'object': None,
    'metal': metals,
    'shielding': ['shielding', 'casing', 'armour', 'coating', 'covering'],
    'codenames': codenames,
    'look carefully': ['examine it closely', 'unscrew the top', 'turn it over', 'rotate it thus', 'speak the launch code',
                      'trigger the remote', 'reverse it', 'whistle', 'blink twice', 'hum', 'look inside'],
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
    'exclaimed': ['exclaimed', 'shouted', 'said', 'replied', 'gasped'],

    # The pun generation
    'pun': '"#i do love a.capitalize# #pun phrase#."',
    'i do love a': ['i do love a good', 'one always appreciates a fine',
                    "never leave home without your", "don't come between a man and his"],
    'pun phrase': None,

    # Demo continues
    'demo continues': '"#chides#, James. #chides again.capitalize#.',
    'chides': ['Do pay attention', 'This is dangerous stuff you know', "I won't be responsible if you hurt yourself",
        "Please give me your attention", "Do listen to me"],
    'chides again': ['please take this seriously', 'do act your age', 'at least pretend to be interested'],

    # Demo close
    'demo close': """"#finally.capitalize#," Q #said#, "There is #one more thing#: if you #do this#, it #precisely targets#
    your enemy's #body_part#, #spraying# #body fluids# everywhere." """,
    'finally': ['Finally', 'Also', 'Anyway'],
    'spraying': ['spraying', 'shooting', 'leaking', 'atomizing'],
    'one more thing': ['one more thing', 'one last thing', 'one final feature', 'an additional note'],
    'do this': ['wave it counterclockwise', 'point it at the sun', 'point it at yourself', 'point it at the floor', 'put it down your pants',
                'wear it like a brooch', 'put it behind your ear'],
    'precisely targets': ['precisely targets', 'is programmed to aim at', 'aims at', 'targets', 'seeks out'],

    # James final reaction
    'james final': '"#that certainly will2.capitalize# #pun phrase2#."',
    'that certainly will2': ['Well, I dare say that #body_part# will', 'Surely the #body_part# will', "That #body_part# surely will",
                            "That #body_part# certainly will "],
    'body_part': None,
    'pun phrase2': None,
    'body fluids': body_fluids
}

tired = {
    'reaction punct': [','],
    'exclaimed': ['sighed', 'murmured', 'mumbled', 'whispered'],
    'interjection': ['huh', 'gee', 'fine', 'yes well', 'yes yes', "that's all good"],
    'interested': ['bored', 'staring at his fingernails', 'brushing a speck of dust off his tuxedo', 'staring into space',
              'clearly bored', 'clearly tired', 'obviously uninterested', 'with obvious boredom', 'with indifference'],
}

dead = {
    'james final': ["There was no response, which did not dampen Q's enthusiasm.", "There was no response as he was the only one still alive in the room.",
                       "Only the haunting sound of running machinery answered him.", "The emptiness of the room echoed terribly."],
    'james reacts': ['James said nothing, because he was dead.', "James' corpse had no response.",
                     "James's body continued to lie there."],
    'james reacts again': ['...'],
    'james response': ['There was no reply, as the room was otherwise empty.', "There was no sound in the room but Q's own voice.",
                       "There was no response, but Q continued as if there were."],

}

not_first = {
    'hello': ['next up', 'just one more thing', 'next', 'if you have another minute', 'also', 'before you go', 'even better'],
    'hello2': ['okay', 'yes, hello', 'all right', 'another?', 'really'],
    'next': ['next', 'yet another', 'one more', 'even finer', 'even more exciting'],
}





iterations = 6 # 350
tired_message = False
dead_message = False
skip_puns = False


def demo():
    print(start_grammar.flatten('#origin#'))


for i in range(0, iterations):
    if i == 1:
        start_rules.update(not_first)
    elif i > iterations * .60:
        if not dead_message:
            print("\n_Unfortunately by this point, James had gone several hours without liquor, and died from withdrawal._\n")
            dead_message = True
        start_rules.update(dead)
        skip_puns = True
    elif i > iterations * .30:
        if not tired_message:
            print('\nJames cleared his throat. "I say, Q, is this going on much longer? Terribly thirsty, you know."\n')
            tired_message = True
        start_rules.update(tired)
    if not skip_puns:
        obj, puns = generate_object(objects, relationship_type="hypernym")
        body_part, body_puns = generate_object(body_parts, part_of_speech="verb")
        start_rules.update({'object': obj, 'pun phrase': puns, 'body_part': body_part, 'pun phrase2': body_puns})

    start_grammar = tracery.Grammar(start_rules)
    start_grammar.add_modifiers(base_english)
    demo()
