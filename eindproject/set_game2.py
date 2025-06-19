import pygame 
import os
import random
import time

#weergave van de kaarten in de game panel
Kaart_breed = 120
Kaart_hoogte = 80
Kaarten_per_rij= 4
Kaarten_per_kolom=3
rijopvulling= 20
tijd_limiet = 30  
Kaarten = "kaarten"
rijen = 3
#kaartkenmerken
kleuren = ["red", "green", "purple"]
vormen = ["oval", "squigle", "diamond"]
vullingen = ["empty", "shaded", "filled"]
aantallen = ["1", "2", "3"]

pygame.init()
font = pygame.font.SysFont("Arial", 20)
breedte_venster = Kaart_breed * Kaarten_per_rij + rijopvulling * (Kaarten_per_rij + 1)
hoogte_venster = Kaart_hoogte * rijen + rijopvulling * (rijen + 1) + 40
scherm = pygame.display.set_mode((breedte_venster, hoogte_venster))
pygame.display.set_caption("SET Spel")

def teken_kaarten(kaarten, geselecteerd):
    scherm.fill((255, 255, 255))
    for i, kaart in enumerate(kaarten):
        rij = i // Kaarten_per_rij
        kolom = i % Kaarten_per_rij
        x = rijopvulling + kolom * (Kaart_breed + rijopvulling)
        y = rijopvulling + rij * (Kaart_hoogte + rijopvulling)
        scherm.blit(kaart.image, (x, y))
        label = font.render(str(i + 1), True, (0, 0, 0))
        scherm.blit(label, (x + 5, y + 5))
        if i in geselecteerd:
            pygame.draw.rect(scherm, (255, 0, 0), (x, y, Kaart_breed, Kaart_hoogte), 4)
    pygame.display.flip()

# set up 
all_paths = [os.path.join(Kaarten, f) for f in os.listdir(Kaarten) if f.endswith('.gif')]
random.shuffle(all_paths)
deck = [Kaart(p) for p in all_paths]
table = deck[:12]
deck = deck[12:]
selected = [] 

score_speler = 0
score_computer = 0
start_tijd = time.time
running = True


def lees_bestandsnaam(bestandsnaam):
    #pakt van elke kaart bestandsnaam elk kenmerk apart
    naam = os.path.basename(bestandsnaam).replace(".gif", "").lower()
    #van elk kenmerk een lijst maken met alle soorten om vervolgens
    #een nummer eeraan te kunnen geven 
    kleuren = ["red", "green", "purple"]
    vormen = ["oval", "squigle", "diamond"]
    vullingen = ["empty", "shaded", "filled"]
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
#geeft nu dan per kaart een lijst met waarden die elk voor een kenmerk staan
    return [aantal_waarde, vorm_waarde, kleur_waarde, vulling_waarde]

class Kaart:
    def __init__(self, pad):
        self.pad = pad
        self.kenmerken = lees_bestandsnaam(pad)
        self.afbeelding = pygame.transform.scale(pygame.image.load(pad), (Kaart_breed, Kaart_hoogte))


def setje(kaart1,kaart2,kaart3):
    #3 kaarten zijn een set wanneer elk kenmerk of alles verschillend
    #heeft of alles hetzelfde, waarmee dus de lengte van de waarden
    #van de bijbehorende kenmerekn dan 3 zou zijn als ze verschillend zijn
    #en 1 wanneer ze allemaal hetzeflde zijn, wat dan een set maakt 
    #bij len 2 verschillen 2 kaarten van kenmerk wat nooit een set kan zijn
    #waarmee dus wordt gecheckt of er een set is of niet zo.
    for i in range(4):
        waarden = {kaart1.kenmerken[i],kaart2.kenmerken[i],kaart3.kenmerken[i]}
        if len(waarden) == 2:
            return False
        return True 

# checkt voor alle mogelijke combinaties i,j,k kaarten of het voldoet
# aan de eisen van def setje en voegt het toe aan lijst alle_sets 
def vind_alle_sets(kaarten):
    alle_sets = []
    for i in range(len(kaarten)):
        for j in range(i + 1, len(kaarten)):
            for k in range(j + 1, len(kaarten)):
                if setje(kaarten[i], kaarten[j], kaarten[k]):
                    alle_sets.append((i, j, k))
    return alle_sets 

while running:
    teken_kaarten(table, selected)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - rijopvulling) // (Kaart_breed + rijopvulling)
            row = (y - rijopvulling) // (Kaart_hoogte + rijopvulling)
            idx = row * Kaarten_per_rij + col
            if 0 <= idx < len(table):
                if idx in selected:
                    selected.remove(idx)
                else:
                    selected.append(idx)
            if len(selected) == 3:
                c1, c2, c3 = selected
                if setje(table[c1], table[c2], table[c3]):
                    player_score += 1
                    print(f"Player scored! Total: {player_score}")
                    for i in sorted(selected, reverse=True):
                        del table[i]
                    while len(table) < 12 and deck:
                        table.append(deck.pop(0))
                else:
                    print("Not a set.")
                selected = []
                start_time = time.time()

    # Check timer for computer move
    if time.time() - start_time > tijd_limiet:
        sets_found = vind_alle_sets(table)
        if sets_found:
        # Computer speelt eerste gevonden set
            c1, c2, c3 = sets_found[0]
            for i in sorted((c1, c2, c3), reverse=True):
                del table[i]
            while len(table) < 12 and deck:
                table.append(deck.pop(0))
            computer_score += 1
            print(f"Computer scored! Total: {computer_score}")
        else:
        # Geen enkele set op tafel: verwijder bovenste 3 kaarten
            print("No sets found. Removing top 3 cards from the table.")
            for _ in range(3):
                if table:
                    table.pop(0)
            while len(table) < 12 and deck:
                table.append(deck.pop(0))
        selected = []
        start_time = time.time()




    


    





    
