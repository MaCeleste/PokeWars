import pygame
import sys
import random
import requests
import os.path

# Initialise pygame

pygame.init()

# Game parameters

WIDTH = 1200
HEIGHT = 1000
black = (0, 0, 0)
white = (255, 255, 255)
grey1 = (210,210,210)
grey2 = (85, 85, 85)
grey3 = (40, 40, 40)
titles_font = pygame.font.Font('BarlowCondensed-Light.ttf', 25)
card_font = pygame.font.Font('BarlowCondensed-Light.ttf', 20)
small_card_font = pygame.font.Font('BarlowCondensed-Light.ttf', 18)

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
        #self.game()
        self.game_running = True
       
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
        top_menu = pygame.draw.rect(screen, grey3, [0, 0, WIDTH, 50])
        bottom_menu = pygame.draw.rect(screen, grey3, [0, 950, WIDTH, 50])

        pc_container = pygame.draw.rect(screen, white, [15, 65, 1175, 320], width = 1)
        pc_text = titles_font.render('PC', True, white)
        pc_text_rect = pc_text.get_rect(center=(WIDTH/2, 90))
        screen.blit(pc_text, pc_text_rect)

        player_container = pygame.draw.rect(screen, white, [15, 620, 1175, 320], width = 1)
        player_text = titles_font.render('Player', True, white)
        player_text_rect = pc_text.get_rect(center=(WIDTH/2, 910))
        screen.blit(player_text, player_text_rect)
        
    def game(self):
        if any(d['used'] == False for d in self.player.cards):
            player_selection = self.player.play_hand()
            if player_selection != None:
                self.pc.turn = True
                pc_selection = self.pc.choose_card(player_selection[0])
                if pc_selection != None:
                    print(player_selection)
                    print(pc_selection)
        else:
            self.game_running = False
        
class PC:
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.turn = False

    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)
    
    def draw_cards(self):
        for i in range(7):
            card = pygame.draw.rect(screen, grey3, [i * 160 + 50, 125, 140, 240], border_radius = 12)
            self.card_rects.append(card)
    
    def choose_card(self, attribute_name):
        selected_card = random.choice([x for x in self.cards if x['used'] != True])
        selected_card_index = self.cards.index(selected_card)
        self.cards[selected_card_index]['used'] = True
        return attribute_name, selected_card[attribute_name]


class Player: 
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.card_clicked = False
        self.turn_to_choose_card = True
        self.turn_to_choose_attribute = False
        self.selected_card = None
        self.selected_attribute = None
        
    
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)

    def draw_cards(self):
        for i in range(7):
            # Draw a rect that will represent a card in the player's hand

            card = pygame.Rect((i * 160 + 50, 640), (140, 240))

            mouse_pos = pygame.mouse.get_pos()
            if card.collidepoint(mouse_pos) and self.turn_to_choose_card == True or self.selected_card == i:
                pygame.draw.rect(screen, grey2, card, border_radius = 12)
            elif self.cards[i]['used'] == True:
                pygame.draw.rect(screen, grey2, card, border_radius = 12)
            else:
                pygame.draw.rect(screen, grey3, card, border_radius = 12)

            self.card_rects.append(card)

            # Render text and images to be displayed on the card
            name_text = card_font.render(self.cards[i]['name'].capitalize(), True, white)
            id_text = small_card_font.render(f'ID: {self.cards[i]["id"]}', True, white)
            height_text = small_card_font.render(f'Height: {self.cards[i]["height"]}', True, white)
            weight_text = small_card_font.render(f'Weight: {self.cards[i]["weight"]}', True, white)
            image = pygame.image.load(f'images/{self.cards[i]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))

            # Display text and images on card
            screen.blit(name_text, (i * 160 + 55, 645))
            screen.blit(image_resized, (i * 160 + 50, 675))
            screen.blit(id_text, (i * 160 + 55, 815))
            screen.blit(height_text, (i * 160 + 55, 835))
            screen.blit(weight_text, (i * 160 + 55, 855))

    def play_hand(self):
        if self.turn_to_choose_card == True:
            instructions_text = titles_font.render('Your turn: select a card.', True, white)
            screen.blit(instructions_text, (20, 960))
        
            self.select_card()
            if self.selected_card != None:
                self.turn_to_choose_card = False
                self.turn_to_choose_attribute = True
        
        if self.turn_to_choose_attribute == True:        
            instructions_text = titles_font.render('Which attribute would your like to use? Press i for id, w for weight or h for height.', True, white)
            screen.blit(instructions_text, (20, 960))

            self.selected_attribute = self.select_attribute(self.selected_card)

            if self.selected_attribute != None:
                self.turn_to_choose_attribute = False
                #self.player.selected_card = None
                #self.player.selected_attribute = None
                return self.selected_attribute

    def select_card(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.turn_to_choose_card == True:
            for card in self.card_rects:
                if card.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0] and self.cards[self.card_rects.index(card)]['used'] == False:
                        self.card_clicked = True
                    else:
                        if self.card_clicked == True:
                            self.card_clicked = False
                            self.selected_card = self.card_rects.index(card)
                                                
    def select_attribute(self, index):
        if self.turn_to_choose_attribute == True:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_i]:
                self.cards[index]['used'] = True
                return ('id', self.cards[index]['id'])
            elif pressed[pygame.K_h]:
                self.cards[index]['used'] = True
                return ('height', self.cards[index]['height'])
            elif pressed[pygame.K_w]:
                self.cards[index]['used'] = True
                return ('weight', self.cards[index]['weight'])     

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

    screen.fill(black)
    main_game.draw_elements()
    clock.tick(fps)

    if main_game.game_running == True:
        main_game.game()

    pygame.display.update()