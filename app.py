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


def generate_object(from_objects):
    puns = []

    while not puns:
        # Pick the random object up front
        obj = random.choice(from_objects)

        searchable_obj = obj.split(' ')[-1]
        # Create terrible puns for the replies
        r = requests.get(WORDNIK_API + '/word.json/{}/relatedWords'.format(urllib.parse.quote(searchable_obj)), headers=headers)
        if r.status_code != 200:
            sleep(5)
            continue
        for words in r.json():
            if words['relationshipType'] == 'rhyme':
                puns = [w for w in words['words'] if not w[0].istitle()]
    return obj, puns

start_rules = {
    'origin': '''
"#hello.capitalize#, James. I #want# to #showyou# #our# #next# #toy#."

#james response#

#demo rules#

#james reacts#

#demo continues#

#james reacts again#

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
    'now': ['now', 'today', 'at last', 'again', 'once again', 'this morning'],

    # Q does his demo
    'demo rules': """[device:#object#]Q #held up# #device.a#. "I #know# it looks like #ordinary.a# #device#, but if you #look carefully#, #it turns out that# \
it's #actually# a #weapon type#. Pure #metal# #shielding#, developed during project #codenames#." """,
    'held up': ['held up', 'walked over to', 'waved his arm towards', 'gestured at', 'nodded towards', 'lifted', 'picked up'],
    'know': ['know', 'realize', 'understand'],
    'ordinary': ['ordinary', 'simple', 'everyday', 'innocent', 'boring'],
    'object': None,
    'metal': metals,
    'shielding': ['shielding', 'casing', 'armour', 'coating', 'covering'],
    'codenames': codenames,
    'look carefully': ['examine it closely', 'unscrew the top', 'turn it over', 'rotate it thus', 'speak the launch code',
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
    'exclaimed': ['exclaimed', 'shouted', 'said', 'replied', 'gasped'],

    # The pun generation
    'pun': '"#that certainly will.capitalize# #pun phrase#."',
    'that certainly will': ['that #object# certainly will', 'that #object# definitely will', "that #object# will",
                            "they'll never expect that #object# to "],
    'pun phrase': None,

    # Demo continues
    'demo continues': '"#chides#, James. #caution.capitalize#, #of course#. #whatever you do.capitalize#—#dont touch it#."',
    'chides': ['Do pay attention', 'This is dangerous stuff you know', "I won't be responsible if you hurt yourself",
        "Please give me your attention", "Do listen to me"],
    'caution': ["It hasn't been perfected yet", "This is still in the experimental stage", "This needs a bit more research"],
    'of course': ["of course", "naturally", "you understand", "one understands", "you realize"],
    'whatever you do': ["and for God's sake", "whatever you do", "above all else", "use caution"],
    'dont touch it': ["don't actually touch it", "don't look at it", "don't breathe on it", "don't shake it",
    "don't leave it in the sun", "don't use it after midnight", "avoid jostling it", "avoid looking at it"],

    # James replies again
    'james reacts again': 'James #said#, "#well.capitalize#, that will #come in handy# #in the field#."',
    'well': ['well', 'huh', 'hmm', 'yes', 'mmm'],
    'come in handy': ['come in handy', 'be useful', 'do in a pinch', 'help out'],
    'in the field': ['in the field', 'on a mission', 'on the job', 'on the go', ''],

    # Demo close
    'demo close': """"#finally.capitalize#," Q #said#, "There is #one more thing#: if you #do this#, it #precisely targets#
    your enemy's #body_part#, #spraying# #body fluids# everywhere." """,
    'finally': ['Finally', 'At last', 'And'],
    'spraying': ['spraying', 'shooting', 'leaking', 'atomizing'],
    'one more thing': ['one more thing', 'one last thing', 'one final feature', 'an additional note'],
    'do this': ['wave it counterclockwise', 'point it at the sun', 'point it at yourself', 'point it at the floor', 'put it down your pants',
                'wear it like a brooch', 'put it behind your ear'],
    'precisely targets': ['precisely targets', 'is programmed to aim at', 'aims at', 'targets', 'seeks out'],

    # James final reaction
    'james final': '"#that certainly will2.capitalize# #pun phrase2#."',
    'that certainly will2': ['Ouch! I dare say that #body_part# will', 'Yow! Surely the #body_part# will', "Yikes! That #body_part# will",
                            "Ouch! Who will expect the #body_part# to "],
    'body_part': None,
    'pun phrase2': None,
    'body fluids': body_fluids
}

tired = {
    'reaction punct': ['.'],
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
    'james reacts again': [''],
    'james response': ['There are no reply, as the room was otherwise empty.', "There was no sound in the room but Q's own voice.",
                       "There was no response, but Q continued as if there were."],

}

not_first = {
    'hello': ['next up', 'just one more thing', 'next', 'if you have another minute', 'also', 'before you go', 'even better']
}


def demo():
    print(start_grammar.flatten('#origin#'))

print("""# Trapped in the Q

A NaNoGenMo "novel".

""")
iterations = 10
tired_message = False
dead_message = False
for i in range(0, iterations):
    if i == 1:
        start_rules.update(not_first)
    elif i > iterations * .60:
        if not dead_message:
            print("\n_Unfortunately by this point, James had gone several hours without liquor, and died from withdrawl._\n")
            dead_message = True
        start_rules.update(dead)
    elif i > iterations * .30:
        if not tired_message:
            print('\n"_I say, Q, is this going on much longer? Terribly thirsty._"\n')
            tired_message = True
        start_rules.update(tired)
    obj, puns = generate_object(objects)
    body_part, body_puns = generate_object(body_parts)
    start_rules.update({'object': obj, 'pun phrase': puns, 'body_part': body_part, 'pun phrase2': body_puns})
    start_grammar = tracery.Grammar(start_rules)
    start_grammar.add_modifiers(base_english)
    demo()
