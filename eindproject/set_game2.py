import pygame 
import os
import random
import time

Kaart_breed = 120
Kaa = 80
teCARDS_PER_ROW = 4
PADDING = 20
DISPLAY_TIME = 30  
IMG_FOLDER = "kaarten"

kleuren = ["rood", "groen", "paars"]
vormen = ["ovaal", "krul", "ruit"]
vullingen = ["open", "gestreept", "vol"]
aantallen = ["1", "2", "3"]

def lees_bestandsnaam(bestandsnaam):
    #pakt van elke kaart bestandsnaam elk kenmerk apart
    naam = os.path.basename(bestandsnaam).replace(".gif", "").lower()
    #van elk kenmerk een lijst maken met alle soorten om vervolgens
    #een nummer eeraan te kunnen geven 
    kleuren = ["rood", "groen", "paars"]
    vormen = ["ovaal", "krul", "ruit"]
    vullingen = ["open", "gestreept", "vol"]
    aantallen = ["1", "2", "3"]
#erkent een bepaalde waarde aan elk kenmerk 
    for i, kleur in enumerate(kleuren):
        if kleur in naam:
            kleur_waarde = i
            break
    for i, vorm in enumerate(vormen):
        if vorm in naam:
            vorm_waarde = i
            break
    for i, vulling in enumerate(vullingen):
        if vulling in naam:
            vulling_waarde = i
            break
    for i, aantal in enumerate(aantallen):
        if aantal in naam:
            aantal_waarde = i
            break
#
    return [aantal_waarde, vorm_waarde, kleur_waarde, vulling_waarde]


def check_set(bestand):
    naam = os.path.basename(bestandsnaam).replace(".gif", "").lower()
    kleuren = ["red", "green", "purple"]
    vormen = ["oval", "squiggle", "diamond"]
    vullingen = ["empty", "shaded", "filled"]
    aantallen = ["1", "2", "3"]

    


    #maakt lijst van elk kenmerk

    #erken getal aan elk soort kenmerk 
    #elk element van een kaart wordt vergelijken met ander element
    #als de lengte van elk getal precies 2 is is het een set
    #lengte twee wil zeggen dat per categorie, dus kleuren vomrn,
    #aantallen enzo dat twee van de 3 kaarten zelfde in 1 categorie 
    #zitten waarmee het nooit een set kan zijn 
    #het is een set wanneer voor elke categorie dan dus elke kaart
    #in vergelijking met elkaar of hetzeflde is of alles verschilt
    #en dat transleert dan naar lijst van lengte 1 of 3 dus 
    #een fucntie def is_set zal dan checkcen of t 1 of 3 is en alleen 
    #dan true geven 





    