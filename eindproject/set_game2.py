import pygame
import os
import random
import time

# card visualization 
kaart_breedte = 120
kaart_hoogte = 80
kaarten_per_rij = 4
marge = 20
tijd_per_beurt = 30  # time to find a set
map_kaarten = "kaarten"

kleuren = ['rood', 'groen', 'paars']
vormen = ['ruit', 'golf', 'ovaal']
vullingen = ['open', 'gevuld', 'gestreept']

import os
# checking the card features with the file names
def lees_bestandsnaam(bestandsnaam):
    naam = os.path.basename(bestandsnaam).replace(".gif", "").lower()

#list of all possible card features(same as in the file names)
    kleur_opties = ['red', 'green', 'purple']
    vorm_opties = ['oval', 'squiggle', 'diamond']
    vulling_opties = ['empty', 'shaded', 'filled']
    aantal_opties = ['1', '2', '3']
#giving every feature a value corresponding to the place they have in the list
    for i, kleur in enumerate(kleur_opties):
        if kleur in naam:
            kleur_waarde = i
            break
    for i, vorm in enumerate(vorm_opties):
        if vorm in naam:
            vorm_waarde = i
            break
    for i, vulling in enumerate(vulling_opties):
        if vulling in naam:
            vulling_waarde = i
            break
    for i, aantal in enumerate(aantal_opties):
        if aantal in naam:
            aantal_waarde = i
            break

    return (kleur_waarde, vorm_waarde, vulling_waarde, aantal_waarde)


# Class that visualizes a card in the game by extracting the features from the filename
# and loading the corresponding image inthe game.
class kaart:
    def __init__(self, pad):
        self.pad = pad
        self.eigenschappen = lees_bestandsnaam(pad)
        self.afbeelding = pygame.transform.scale(
            pygame.image.load(pad), (kaart_breedte, kaart_hoogte))


# 3 cards are a set when all features have 3 different characteristics or 3 the same characteristics.
# which means the length of the values of the associated features 
# would then be 3 if they are different
# and 1 if they are all the same, which then makes a set.
# with len 2, 2 cards differ from feature which can never be a set
# and so the algorithm can easliy check whether there is a set or not.
def is_set(k1, k2, k3):
    for i in range(4):
        waarden = {k1.eigenschappen[i], k2.eigenschappen[i], k3.eigenschappen[i]}
        if len(waarden) == 2:
            return False
    return True
    
#checking the definition above for every possible cards combinations 
#and makes a list of all possible sets in that round of 12 cards.
def vind_sets(kaarten):
    gevonden = []
    for i in range(len(kaarten)):
        for j in range(i + 1, len(kaarten)):
            for k in range(j + 1, len(kaarten)):
                if is_set(kaarten[i], kaarten[j], kaarten[k]):
                    gevonden.append((i, j, k))
    return gevonden


# pygame setup(visualization of the game)
pygame.init()
lettertype = pygame.font.SysFont("arial", 20)
rijen = 3
scherm_breedte = kaart_breedte * kaarten_per_rij + marge * (kaarten_per_rij + 1)
scherm_hoogte = kaart_hoogte * rijen + marge * (rijen + 1) + 40  # extra 40 voor timer/score
scherm = pygame.display.set_mode((scherm_breedte, scherm_hoogte))
pygame.display.set_caption("set spel")


# class for the timer: resetting and adding the timer in to the screen.
class Timer:
    def __init__(self, tijd_limiet):
        self.tijd_limiet = tijd_limiet
        self.starttijd = time.time()

    def reset(self):
        self.starttijd = time.time()

    def tijd_over(self):
        resterend = self.tijd_limiet - (time.time() - self.starttijd)
        return max(0, resterend)

    def teken(self, scherm, font):
        resterend = int(self.tijd_over()) + 1
        tekst = font.render(f"Tijd: {resterend}s", True, (255, 255, 255))
        scherm.blit(tekst, (10, 10)) #left top corner


# class for the scorebord: player, computer and adding the scoreboard to the screen.
class Scorebord:
    def __init__(self):
        self.speler = 0
        self.computer = 0

    def speler_scoort(self):
        self.speler += 1

    def computer_scoort(self):
        self.computer += 1

    def teken(self, scherm, font):
        tekst_speler = font.render(f"Speler: {self.speler}", True, (255, 255, 255))
        tekst_computer = font.render(f"Computer: {self.computer}", True, (255, 255, 255))
        scherm.blit(tekst_speler, (120, 10))  # next to the timer
        scherm.blit(tekst_computer, (120 + tekst_speler.get_width() + 20, 10))  # next to the player


# Adding every aspect to one frame on the screen
def teken_scherm(kaarten, geselecteerd, scorebord, timer, highlight_set=None, computer_set=None):
    scherm.fill((0, 0, 0))  
    
# Timer and scoreboard 
    timer.teken(scherm, lettertype)  
    scorebord.teken(scherm, lettertype)  
# Numbers on the cards
    nummer_font = pygame.font.SysFont("arial", 16)  

    for i in range(len(kaarten)):
        k = kaarten[i]
        rij = i // kaarten_per_rij
        kolom = i % kaarten_per_rij
        x = marge + kolom * (kaart_breedte + marge)
        y = marge + rij * (kaart_hoogte + marge) + 40  # ruimte bovenin voor timer/score

        scherm.blit(k.afbeelding, (x, y))

        # Adding numbers to the cards
        nummer = str(i + 1)
        tekst = nummer_font.render(nummer, True, (0, 0, 0))
        scherm.blit(tekst, (x + 5, y + 4))

        # Red outline while sellecting the cards.
        if i in geselecteerd:
            pygame.draw.rect(scherm, (255, 0, 0), (x, y, kaart_breedte, kaart_hoogte), 4)

        # Green outline when the set is found
        if highlight_set and i in highlight_set:
            pygame.draw.rect(scherm, (0, 255, 0), (x - 2, y - 2, kaart_breedte + 4, kaart_hoogte + 4), 4)

        # Red outline on the set that is found by the computer.
        if computer_set and i in computer_set:
            pygame.draw.rect(scherm, (255, 0, 0), (x - 2, y - 2, kaart_breedte + 4, kaart_hoogte + 4), 4)

    pygame.display.flip()




# --- spelopzet ---
alle_paden = [os.path.join(map_kaarten, f) for f in os.listdir(map_kaarten) if f.endswith(".gif")]
random.shuffle(alle_paden)
stapel = [kaart(p) for p in alle_paden]
tafel = stapel[:12]
stapel = stapel[12:]

scorebord = Scorebord()  # maak scorebord aan
timer = Timer(tijd_per_beurt)  # maak timer aan

geselecteerd = []
loopt = True

clock = pygame.time.Clock()  # maak klok aan voor FPS limiter

# --- hoofdlus ---
while loopt:
    teken_scherm(tafel, geselecteerd, scorebord, timer)  # teken alles in 1 functie
    sets_op_tafel = vind_sets(tafel)
    computer_keuze = random.choice(sets_op_tafel) if sets_op_tafel else None
    for gebeurtenis in pygame.event.get():
        if gebeurtenis.type == pygame.QUIT:
            loopt = False
        elif gebeurtenis.type == pygame.MOUSEBUTTONDOWN:
            x, y = gebeurtenis.pos
            kolom = (x - marge) // (kaart_breedte + marge)
            rij = (y - marge - 40) // (kaart_hoogte + marge)  # 40 px offset voor timer/score

            if 0 <= kolom < kaarten_per_rij and 0 <= rij < rijen:
                index = rij * kaarten_per_rij + kolom
                if index < len(tafel):
                    if index in geselecteerd:
                        geselecteerd.remove(index)
                    else:
                        geselecteerd.append(index)

                    if len(geselecteerd) == 3:
                        i1, i2, i3 = geselecteerd
                        if is_set(tafel[i1], tafel[i2], tafel[i3]):
                            teken_scherm(tafel, geselecteerd, scorebord, timer, highlight_set=geselecteerd)
                            pygame.time.delay(500)  # 0.5 seconde pauze
                            scorebord.speler_scoort()
                            # verwijder de kaarten die een set vormen en vervang ze door nieuwe kaarten van de stapel als die er zijn
                            for i in sorted(geselecteerd, reverse=True):
                                if stapel:
                                    tafel[i] = stapel.pop(0)
                                else:
                                    del tafel[i]
                            timer.reset()
                        else:
                            # foutieve set, gewoon deselecteren
                            pass
                        geselecteerd = []

    # timer check
    if timer.tijd_over() <= 0:
        # tijd om = computer krijgt een punt
        scorebord.computer_scoort()
        teken_scherm(tafel, geselecteerd, scorebord, timer,highlight_set=computer_keuze)
        pygame.time.delay(500)  # 0.5 seconde pauze    scorebord.computer_scoort()
        timer.reset()



    clock.tick(30)

pygame.quit()
