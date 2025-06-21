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
# verschillende eigenschappen halen uit bestandsnaam
def lees_bestandsnaam(bestandsnaam):
    naam = os.path.basename(bestandsnaam).replace(".gif", "").lower()

#lijsten van alle verschillende mogelijke kenmerken, zijn in het Engels omdat ze zo in de bestandsnaam staan
    kleur_opties = ['red', 'green', 'purple']
    vorm_opties = ['oval', 'squiggle', 'diamond']
    vulling_opties = ['empty', 'shaded', 'filled']
    aantal_opties = ['1', '2', '3']

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

# class van de kaarten die de functie hierboven gebruikt om de eigenschappen in te vullen
class kaart:
    def __init__(self, pad):
        self.pad = pad
        self.eigenschappen = lees_bestandsnaam(pad)
        self.afbeelding = pygame.transform.scale(
            pygame.image.load(pad), (kaart_breedte, kaart_hoogte)
        )


# 3 kaarten zijn een set wanneer elk kenmerk of alles verschillend
# heeft of alles hetzelfde, waarmee dus de lengte van de waarden
# van de bijbehorende kenmerken dan 3 zou zijn als ze verschillend zijn
# en 1 wanneer ze allemaal hetzelfde zijn, wat dan een set maakt 
# bij len 2 verschillen 2 kaarten van kenmerk wat nooit een set kan zijn
# waarmee dus wordt gecheckt of er een set is of niet zo.
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
scherm_hoogte = kaart_hoogte * rijen + marge * (rijen + 1) + 40  # extra 40 voor timer/score
scherm = pygame.display.set_mode((scherm_breedte, scherm_hoogte))
pygame.display.set_caption("set spel")


# class voor timer met tekenen en resetten
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
        tekst = font.render(f"Tijd: {resterend}s", True, (255, 255, 255))  # wit
        scherm.blit(tekst, (10, 10))  # linksboven


# class voor scorebord, speler en computer bijhouden en tekenen
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
        scherm.blit(tekst_speler, (120, 10))  # rechts naast timer
        scherm.blit(tekst_computer, (120 + tekst_speler.get_width() + 20, 10))  # naast speler


# deze functie tekent ALLES: kaarten, timer en scorebord in 1 frame
def teken_scherm(kaarten, geselecteerd, scorebord, timer, highlight_set=None, computer_set=None):
    scherm.fill((0, 0, 0))  # zwart scherm

    timer.teken(scherm, lettertype)  # timer linksboven
    scorebord.teken(scherm, lettertype)  # score rechts van timer

    nummer_font = pygame.font.SysFont("arial", 16)  # kleiner lettertype voor nummers

    for i in range(len(kaarten)):
        k = kaarten[i]
        rij = i // kaarten_per_rij
        kolom = i % kaarten_per_rij
        x = marge + kolom * (kaart_breedte + marge)
        y = marge + rij * (kaart_hoogte + marge) + 40  # ruimte bovenin voor timer/score

        scherm.blit(k.afbeelding, (x, y))

        # Kaartnummer linksboven op de kaart, zwart, iets naar binnen
        nummer = str(i + 1)
        tekst = nummer_font.render(nummer, True, (0, 0, 0))
        scherm.blit(tekst, (x + 5, y + 4))

        # Rode rand bij geselecteerde kaarten
        if i in geselecteerd:
            pygame.draw.rect(scherm, (255, 0, 0), (x, y, kaart_breedte, kaart_hoogte), 4)

        # Groene rand als een set door speler is gevonden
        if highlight_set and i in highlight_set:
            pygame.draw.rect(scherm, (0, 255, 0), (x - 2, y - 2, kaart_breedte + 4, kaart_hoogte + 4), 4)

        # Rode rand als set door computer gekozen wordt getoond
        if computer_set and i in computer_set:
            pygame.draw.rect(scherm, (255, 0, 0), (x - 2, y - 2, kaart_breedte + 4, kaart_hoogte + 4), 4)

    pygame.display.flip()




# dit zorgt ervoor dat van alle kaarten een willekeurige volgorde wordt genomen en de kaarten worden geladen 
alle_paden = [os.path.join(map_kaarten, f) for f in os.listdir(map_kaarten) if f.endswith(".gif")]
random.shuffle(alle_paden)
stapel = [kaart(p) for p in alle_paden]
tafel = stapel[:12]
stapel = stapel[12:]

scorebord = Scorebord()  # maak scorebord aan
timer = Timer(tijd_per_beurt)  # maak timer aan
geselecteerd = []
loopt = True
clock = pygame.time.Clock()  # maakt een clock aan 


while loopt:
    #alles laten tekenen via de functie teken_scherm
    teken_scherm(tafel, geselecteerd, scorebord, timer)  
    sets_op_tafel = vind_sets(tafel)
    computer_keuze = random.choice(sets_op_tafel) if sets_op_tafel else None #is nodig voor later om een computerkeuze vast te stellen uit de mogelijk sets op tafel 
    for gebeurtenis in pygame.event.get():
        if gebeurtenis.type == pygame.QUIT:
            loopt = False
#dit is wanneer er met een muisklik geklikt wordt, zorgt ervoor dat de kaart waarop is geklikt wordt opgeslagen en teogevoegd aan geselecteerd 
        elif gebeurtenis.type == pygame.MOUSEBUTTONDOWN:
            x, y = gebeurtenis.pos 
            kolom = (x - marge) // (kaart_breedte + marge)
            rij = (y - marge - 40) // (kaart_hoogte + marge) 

            if 0 <= kolom < kaarten_per_rij and 0 <= rij < rijen:
                index = rij * kaarten_per_rij + kolom
                if index < len(tafel):
                    if index in geselecteerd:
                        geselecteerd.remove(index)
                    else:
                        geselecteerd.append(index)
# alleen zinvol om te checken wanneer 3 kaarten geselecteerd zijn 
                    if len(geselecteerd) == 3:
                        i1, i2, i3 = geselecteerd
# checken via de functie of de geselecteerde kaarten een set vormen, 
# daarna in de functie teken_scherm zorgen dat de geselcteerde sets gehighlight worden wanneer ze een set zijn
 
                        if is_set(tafel[i1], tafel[i2], tafel[i3]):
                            teken_scherm(tafel, geselecteerd, scorebord, timer, highlight_set=geselecteerd)
                            pygame.time.delay(500)  # halve seconde pauze zodat ff te zien is wel dat het gehighlight is 
                            scorebord.speler_scoort() 
                            # verwijder de kaarten die een set vormen en vervang ze door nieuwe kaarten van de stapel als die er zijn
                            for i in sorted(geselecteerd, reverse=True):
                                if stapel:
                                    tafel[i] = stapel.pop(0)
                                else:
                                    del tafel[i]
                            timer.reset()
                        else:
                            # geen set betekent gewoon deselecteren 
                            pass
                        geselecteerd = []

    # dit gedeelte gaat over de dingen die gebeuren wanneer de tijd verlopen en dus de computer een punt heeft. 
    if timer.tijd_over() <= 0:
        #dit verwijst naar de class van het scorebord zodat er een punt bij de computer komt 
        scorebord.computer_scoort()
        
        #dit verwijst naar de functie teken_scherm om de highlights toe te passen op het setje dat de computer kiest, zodat duidelijk is voor de speler
        #welke set ze gemist hebben en welke de computer heeft gekozen
        teken_scherm(tafel, geselecteerd, scorebord, timer,highlight_set=computer_keuze)
        pygame.time.delay(500)  # 0.5 seconde pauze    scorebord.computer_scoort()
        
        #tijd wordt gereset nadat de computer een set heeft gekozen
        timer.reset()
        
        #van de gekozen zet moeten de kaarten die gekozen zijn gepopt worden
        for i in sorted(computer_keuze, reverse=TRUE):
            if stapel: 
                tafel[i] = stapel.pop(0)
            else: 
                del tafel[i]
                
    clock.tick(30)

pygame.quit()
