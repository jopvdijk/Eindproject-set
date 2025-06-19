import pygame
import os
import random
import time

# --- Configuration ---
CARD_WIDTH = 120
CARD_HEIGHT = 80
CARDS_PER_ROW = 4
PADDING = 20
DISPLAY_TIME = 30  # seconds to find a set
IMG_FOLDER = "kaarten"

colors = ['red', 'green', 'purple']
symbols = ['diamond', 'squiggle', 'oval']
shadings = ['open', 'solid', 'striped']

# --- Game Logic ---
def parse_filename(filename):
    name = os.path.basename(filename).replace(".gif", "").lower()
    
    # Mappings
    colors = ["red", "green", "purple"]
    shapes = ["oval", "squiggle", "diamond"]
    shadings = ["empty", "shaded", "filled"]
    numbers = ["1", "2", "3"]

    # Zoek welke eigenschap in de naam zit
    for i, color in enumerate(colors):
        if color in name:
            color_val = i
            break
    for i, shape in enumerate(shapes):
        if shape in name:
            shape_val = i
            break
    for i, shading in enumerate(shadings):
        if shading in name:
            shading_val = i
            break
    for i, number in enumerate(numbers):
        if number in name:
            number_val = i
            break

    return [number_val, shape_val, color_val, shading_val]


class Card:
    def __init__(self, filepath):
        self.filepath = filepath
        self.attrs = parse_filename(filepath)
        self.image = pygame.transform.scale(pygame.image.load(filepath), (CARD_WIDTH, CARD_HEIGHT))

def is_set(c1, c2, c3):
    for i in range(4):
        values = {c1.attrs[i], c2.attrs[i], c3.attrs[i]}
        if len(values) == 2:
            return False
    return True

def find_sets(cards):
    found = []
    for i in range(len(cards)):
        for j in range(i + 1, len(cards)):
            for k in range(j + 1, len(cards)):
                if is_set(cards[i], cards[j], cards[k]):
                    found.append((i, j, k))
    return found

# --- Pygame Setup ---
pygame.init()
font = pygame.font.SysFont("Arial", 20)
ROWS = 3
WINDOW_WIDTH = CARD_WIDTH * CARDS_PER_ROW + PADDING * (CARDS_PER_ROW + 1)
WINDOW_HEIGHT = CARD_HEIGHT * ROWS + PADDING * (ROWS + 1) + 40
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SET Game")

def draw_cards(cards, selected):
    screen.fill((255, 255, 255))
    for i, card in enumerate(cards):
        row = i // CARDS_PER_ROW
        col = i % CARDS_PER_ROW
        x = PADDING + col * (CARD_WIDTH + PADDING)
        y = PADDING + row * (CARD_HEIGHT + PADDING)
        screen.blit(card.image, (x, y))
        label = font.render(str(i + 1), True, (0, 0, 0))
        screen.blit(label, (x + 5, y + 5))
        if i in selected:
            pygame.draw.rect(screen, (255, 0, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 4)
    pygame.display.flip()

# --- Game Setup ---
all_paths = [os.path.join(IMG_FOLDER, f) for f in os.listdir(IMG_FOLDER) if f.endswith('.gif')]
random.shuffle(all_paths)
deck = [Card(p) for p in all_paths]
table = deck[:12]
deck = deck[12:]

player_score = 0
computer_score = 0

# --- Game Loop ---
running = True
selected = []
start_time = time.time()

while running:
    draw_cards(table, selected)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - PADDING) // (CARD_WIDTH + PADDING)
            row = (y - PADDING) // (CARD_HEIGHT + PADDING)
            idx = row * CARDS_PER_ROW + col
            if 0 <= idx < len(table):
                if idx in selected:
                    selected.remove(idx)
                else:
                    selected.append(idx)
            if len(selected) == 3:
                c1, c2, c3 = selected
                if is_set(table[c1], table[c2], table[c3]):
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
    if time.time() - start_time > DISPLAY_TIME:
        sets_found = find_sets(table)
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


pygame.quit()
