import pygame
import sys
import random
import requests
import os.path

# Initialise pygame

pygame.init()

# Game constants

WIDTH = 1200
HEIGHT = 1000
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY1 = (210,210,210)
GREY2 = (54, 54, 54)
TITLES_FONT = pygame.font.Font('BarlowCondensed-Light.ttf', 25)
CARD_FONT = pygame.font.Font('BarlowCondensed-Light.ttf', 20)
SMALL_CARD_FONT = pygame.font.Font('BarlowCondensed-Light.ttf', 18)

# Set caption and icon

pygame.display.set_caption('PokeWars')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Create the screen

screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define FPS

clock = pygame.time.Clock()
fps = 60

# Retrieve Pokemon info from PokeAPI

pokemon = requests.get('https://pokeapi.co/api/v2/pokemon').json()

# Main game class

class MAIN:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.pc = PC()
        self.deal_cards()
    
    def deal_cards(self):
        self.player.draw(self.deck)
        self.pc.draw(self.deck)
        print(self.player.cards)
        print(self.pc.cards)

    def draw_elements(self):
        self.draw_background()
        self.player.draw_cards()
        self.pc.draw_cards()
    
    def draw_background(self):
        top_menu = pygame.draw.rect(screen, GREY2, [0, 0, WIDTH, 50])
        bottom_menu = pygame.draw.rect(screen, GREY2, [0, 950, WIDTH, 50])

        pc_container = pygame.draw.rect(screen, WHITE, [15, 65, 1175, 320], width = 1)
        pc_text = TITLES_FONT.render('PC', True, WHITE)
        pc_text_rect = pc_text.get_rect(center=(WIDTH/2, 90))
        screen.blit(pc_text, pc_text_rect)

        player_container = pygame.draw.rect(screen, WHITE, [15, 620, 1175, 320], width = 1)
        player_text = TITLES_FONT.render('Player', True, WHITE)
        player_text_rect = pc_text.get_rect(center=(WIDTH/2, 910))
        screen.blit(player_text, player_text_rect)
        
    
    def game(self):
        #while any(d['used'] == False for d in self.player.cards):
        player_selection = self.player_play_hand()
        #pc_selection = self.pc_play_hand()
        
    
    def player_play_hand(self):
        instructions_text = TITLES_FONT.render('Your turn: select a card', True, WHITE)
        screen.blit(instructions_text, (20, 960))
        #return value
    
    def pc_play_hand(self):
        ...
        return value



class PC:
    def __init__(self):
        self.cards = []
        self.card_rects = []
        
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)
    
    def draw_cards(self):
        for i in range(7):
            card = pygame.draw.rect(screen, GREY2, [i * 160 + 50, 125, 140, 240], border_radius = 12)
            self.card_rects.append(card)

class Player: 
    def __init__(self):
        self.cards = []
        self.card_rects = []
    
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)

    def draw_cards(self):
        for i in range(7):
            # Draw a rect that will represent a card in the player's hand

            card = pygame.draw.rect(screen, GREY2, [i * 160 + 50, 640, 140, 240], border_radius = 12)
            self.card_rects.append(card)

            # Render text and images to be displayed on the card
            name_text = CARD_FONT.render(self.cards[i]['name'].capitalize(), True, WHITE)
            id_text = SMALL_CARD_FONT.render(f'ID: {self.cards[i]["id"]}', True, WHITE)
            height_text = SMALL_CARD_FONT.render(f'Height: {self.cards[i]["height"]}', True, WHITE)
            weight_text = SMALL_CARD_FONT.render(f'Weight: {self.cards[i]["weight"]}', True, WHITE)
            image = pygame.image.load(f'images/{self.cards[i]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))

            # Display text and images on card
            screen.blit(name_text, (i * 160 + 55, 645))
            screen.blit(image_resized, (i * 160 + 50, 675))
            screen.blit(id_text, (i * 160 + 55, 815))
            screen.blit(height_text, (i * 160 + 55, 835))
            screen.blit(weight_text, (i * 160 + 55, 855))

class Deck:
    def __init__(self):
        # A list that will contain a dictionary for each Pokemon card. Each dict will contain id, name, height, weight, image 
        self.full_deck = []
        self.build_deck()

    
    def build_deck(self):
        for _ in range(14):

            pokemon = dict()
            # Select a random Pokemon id
            while True:
                id = random.randint(1,898)
                # Check if the id already exists in the deck. If it already exists, select a new id
                if not any(d['id'] == id for d in self.full_deck):
                    # Retrive data from PokeAPI for the Pokemon corresponding to the selected id
                    # Check if there is an image available for the Pokemon with the id selected
                    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}').json()
                    image_path = 'images/' + response["name"] + '.png'
                    if os.path.isfile(image_path):
                        break
                    else:
                        continue
                else:
                    print('id already exists')
                    continue
            
            # Create a dictionary that will store Pokemon attributes

            pokemon['id'] = id
            pokemon['name'] = response['name']
            pokemon['height'] = response['height']
            pokemon['weight'] = response['weight']
            pokemon['image'] = f'{pokemon["name"]}.png'
            pokemon['used'] = False

            self.full_deck.append(pokemon)

    def deal(self):
        return self.full_deck.pop()

# Create instance of a new game

main_game = MAIN()


# Game loop
running = True
while running:
    
    # Event listener

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Screen and fps

    screen.fill(BLACK)
    main_game.draw_elements()
    clock.tick(fps)

    main_game.game()

    pygame.display.update()