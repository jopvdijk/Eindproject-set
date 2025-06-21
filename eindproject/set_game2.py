import pygame
import os
import random
import time

# grootte kaarten 
kaart_breedte = 120
kaart_hoogte = 80
kaarten_per_rij = 4
marge = 20
tijd_per_beurt = 30  # seconden om een set te vinden
map_kaarten = "kaarten"

kleuren = ['rood', 'groen', 'paars']
vormen = ['ruit', 'golf', 'ovaal']
vullingen = ['open', 'gevuld', 'gestreept']


import os
#verschillende eigenschappen halen uit bestandsnaam
def lees_bestandsnaam(bestandsnaam):
    naam = os.path.basename(bestandsnaam).replace(".gif", "").lower()

    kleur_opties = ['red', 'green', 'purple']
    vorm_opties = ['oval', 'squiggle', 'diamond']
    vulling_opties = ['empty', 'shaded', 'filled']
    aantal_opties = ['1', '2', '3']

    for i in range(len(kleur_opties)):
        if kleur_opties[i] in naam:
            kleur_waarde = i
            break

    for i in range(len(vorm_opties)):
        if vorm_opties[i] in naam:
            vorm_waarde = i
            break

    for i in range(len(vulling_opties)):
        if vulling_opties[i] in naam:
            vulling_waarde = i
            break

    for i in range(len(aantal_opties)):
        if aantal_opties[i] in naam:
            aantal_waarde = i
            break

    # Teruggeven van de gevonden waarden (kan je zelf aanpassen)
    return (kleur_waarde, vorm_waarde, vulling_waarde, aantal_waarde)

# class van de kaarten die de functie hierboven gebruikt om de eigenschappen in te vullen
class kaart:
    def __init__(self, pad):
        self.pad = pad
        self.eigenschappen = lees_bestandsnaam(pad)
        self.afbeelding = pygame.transform.scale(
            pygame.image.load(pad), (kaart_breedte, kaart_hoogte)
        )


# 3 kaarten zijn een set wanneer elk kenmerk of alles verschillend
    #heeft of alles hetzelfde, waarmee dus de lengte van de waarden
    #van de bijbehorende kenmerekn dan 3 zou zijn als ze verschillend zijn
    #en 1 wanneer ze allemaal hetzeflde zijn, wat dan een set maakt 
    #bij len 2 verschillen 2 kaarten van kenmerk wat nooit een set kan zijn
    #waarmee dus wordt gecheckt of er een set is of niet zo.
def is_set(k1, k2, k3):
    for i in range(4):
        waarden = {k1.eigenschappen[i], k2.eigenschappen[i], k3.eigenschappen[i]}
        if len(waarden) == 2:
            return False
    return True

# elke mogelijkheid die er is langsgaan en checken of die aan bovenstaande definitie voldoet, maakt lijst aan
# met alle mogelijke sets die erin zetten. 
def vind_sets(kaarten):
    gevonden = []
    for i in range(len(kaarten)):
        for j in range(i + 1, len(kaarten)):
            for k in range(j + 1, len(kaarten)):
                if is_set(kaarten[i], kaarten[j], kaarten[k]):
                    gevonden.append((i, j, k))
    return gevonden


# --- pygame setup ---
pygame.init()
lettertype = pygame.font.SysFont("arial", 20)
rijen = 3
scherm_breedte = kaart_breedte * kaarten_per_rij + marge * (kaarten_per_rij + 1)
scherm_hoogte = kaart_hoogte * rijen + marge * (rijen + 1) + 40
scherm = pygame.display.set_mode((scherm_breedte, scherm_hoogte))
pygame.display.set_caption("set spel")


def teken_kaarten(kaarten, geselecteerd, highlight_set=None):
    scherm.fill((0, 0, 0))
    for i in range(len(kaarten)):
        k = kaarten[i]
        rij = i // kaarten_per_rij
        kolom = i % kaarten_per_rij
        x = marge + kolom * (kaart_breedte + marge)
        y = marge + rij * (kaart_hoogte + marge)
        scherm.blit(k.afbeelding, (x, y))
        
        # de tekst
        label = lettertype.render(str(i + 1), True, (255, 255, 255))
        scherm.blit(label, (x + 5, y + 5))

        # Rode rand bij geselecteerde kaarten
        if i in geselecteerd:
            pygame.draw.rect(scherm, (255, 0, 0), (x, y, kaart_breedte, kaart_hoogte), 4)

        # Groene rand als een set is gevonden
        if highlight_set and i in highlight_set:
            pygame.draw.rect(scherm, (0, 255, 0), (x - 2, y - 2, kaart_breedte + 4, kaart_hoogte + 4), 4)

    pygame.display.flip()

# --- spelopzet ---
alle_paden = [os.path.join(map_kaarten, f) for f in os.listdir(map_kaarten) if f.endswith(".gif")]
random.shuffle(alle_paden)
stapel = [kaart(p) for p in alle_paden]
tafel = stapel[:12]
stapel = stapel[12:]

score_speler = 0
score_computer = 0
geselecteerd = []
starttijd = time.time()
loopt = True

# --- hoofdlus ---
while loopt:
    teken_kaarten(tafel, geselecteerd)
    for gebeurtenis in pygame.event.get():
        if gebeurtenis.type == pygame.QUIT:
            loopt = False
        elif gebeurtenis.type == pygame.MOUSEBUTTONDOWN:
            x, y = gebeurtenis.pos
            kolom = (x - marge) // (kaart_breedte + marge)
            rij = (y - marge) // (kaart_hoogte + marge)
            index = rij * kaarten_per_rij + kolom
            if 0 <= index < len(tafel):
                if index in geselecteerd:
                    geselecteerd.remove(index)
                else:
                    geselecteerd.append(index)
            if len(geselecteerd) == 3:
                k1, k2, k3 = geselecteerd
                if is_set(tafel[k1], tafel[k2], tafel[k3]):
                    # Toon groene randjes
                    teken_kaarten(tafel, geselecteerd, highlight_set=geselecteerd)
                    pygame.display.flip()
                    pygame.time.delay(500)  # 0.5 seconde pauze
                    score_speler += 1
                    print(f"speler scoorde! totaal: {score_speler}")
                    for i in sorted(geselecteerd, reverse=True):
                        del tafel[i]
                    while len(tafel) < 12 and stapel:
                        tafel.append(stapel.pop(0))
                    starttijd = time.time()
                else:
                print("geen set.")
                geselecteerd = []

    if time.time() - starttijd > tijd_per_beurt:
        sets = vind_sets(tafel)
        if sets:
            k1, k2, k3 = sets[0]
            for i in sorted((k1, k2, k3), reverse=True):
                del tafel[i]
            while len(tafel) < 12 and stapel:
                tafel.append(stapel.pop(0))
            score_computer += 1
            print(f"computer scoorde! totaal: {score_computer}")
        else:
            print("geen sets gevonden. verwijder bovenste 3 kaarten.")
            for _ in range(3):
                if tafel:
                    tafel.pop(0)
            while len(tafel) < 12 and stapel:
                tafel.append(stapel.pop(0))
        geselecteerd = []
        starttijd = time.time()

pygame.quit()
