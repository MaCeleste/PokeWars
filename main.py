import pygame
import sys
import random
import requests
import os.path
from pygame.locals import *
from pygame import mixer

# Initialise pygame
pygame.init()
mixer.init()

# Screen parameters
WIDTH = 1200
HEIGHT = 1000

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Start screen background
bg_img = pygame.image.load('images/bg.jpg')
bg_img = pygame.transform.scale(bg_img,(WIDTH, HEIGHT))

# Start screen music
mixer.music.load('sounds/music.ogg')
mixer.music.play(-1)

# Load sound effects
win_round = pygame.mixer.Sound('sounds/win_round.wav')
lose_round = pygame.mixer.Sound('sounds/lose_round.wav')
card_selected = pygame.mixer.Sound('sounds/selected.wav')

# Define FPS
clock = pygame.time.Clock()
fps = 60

# Set caption and icon
pygame.display.set_caption('PokeWars')
icon = pygame.image.load('images/icon.png')
pygame.display.set_icon(icon)

# Colours 
black = (0, 0, 0)
white = (255, 255, 255)
grey1 = (210,210,210)
grey2 = (85, 85, 85)
grey3 = (40, 40, 40)

#Fonts
welcome_font = pygame.font.Font('https://raw.githubusercontent.com/MaCeleste/PokeWars/main/fonts/Pokemon%20Solid.ttf', 80)
end_font = pygame.font.Font('https://raw.githubusercontent.com/MaCeleste/PokeWars/main/fonts/Pokemon%20Solid.ttf',45)
instructions_font = pygame.font.Font('https://raw.githubusercontent.com/MaCeleste/PokeWars/main/fonts/BarlowCondensed-LightItalic.ttf', 24)
titles_font = pygame.font.Font('https://raw.githubusercontent.com/MaCeleste/PokeWars/main/fonts/BarlowCondensed-Light.ttf', 25)
card_font = pygame.font.Font('https://raw.githubusercontent.com/MaCeleste/PokeWars/main/fonts/BarlowCondensed-Light.ttf', 20)
small_card_font = pygame.font.Font('https://raw.githubusercontent.com/MaCeleste/PokeWars/main/fonts/BarlowCondensed-Light.ttf', 18)

# Retrieve Pokemon info from PokeAPI
pokemon = requests.get('https://pokeapi.co/api/v2/pokemon').json()

class MAIN:
    def __init__(self):
        self.game_running = False
        self.menu_buttons = []
        self.player_score = 0
        self.pc_score = 0
        self.round_winner = None
        self.pc_wait = False
        self.end_round_wait = False
        self.game_over = None
        self.loading = False
        self.bg = 0
    
    # Reset game parameters and start new game
    def start_game(self):
        self.game_running = True
        self.player_score = 0
        self.pc_score = 0
        self.round_winner = None
        self.pc_wait = False
        self.end_round_wait = False
        self.game_over = False
        self.deck = Deck()
        self.player = Player()
        self.pc = PC()
        self.deal_cards()
        self.loading = False
        pygame.mixer.music.fadeout(1000)

    # Deal cards to each player
    def deal_cards(self):
        self.player.draw(self.deck)
        self.pc.draw(self.deck)

    # Screen elements
    def draw_elements(self):
        if self.game_running == True:
            self.draw_board()
            self.player.draw_cards()
            self.pc.draw_cards()
            self.player.draw_selected_card()
            self.pc.draw_selected_card()
            self.draw_score()
            self.draw_instructions()
            self.draw_round_result()
        else:
            self.draw_game_result()
            self.draw_start_screen()
            self.draw_loading()

    def draw_backgroud(self):
        if self.game_running == True:
            screen.fill(black)
        else:
            screen.fill(black)
            screen.blit(bg_img,(self.bg,0))
            screen.blit(bg_img,(WIDTH+self.bg,0))
            if (self.bg==-WIDTH):
                screen.blit(bg_img,(WIDTH+self.bg,0))
                self.bg=0
            self.bg-=1

    def draw_board(self):
        bottom_menu = pygame.draw.rect(screen, grey3, [0, 0, WIDTH, 40])

        pc_container = pygame.draw.rect(screen, white, [15, 50, 1175, 295], width = 1)
        pc_text = titles_font.render('PC', True, white)
        pc_text_rect = pc_text.get_rect(center=(WIDTH/2, 68))
        screen.blit(pc_text, pc_text_rect)

        player_container = pygame.draw.rect(screen, white, [15, 695, 1175, 295], width = 1)
        player_text = titles_font.render('Player', True, white)
        player_text_rect = player_text.get_rect(center=(WIDTH/2, 970))
        screen.blit(player_text, player_text_rect)
    
    def draw_start_screen(self):
        # Draw welcome message when the program starts
        if self.game_over == None:
            welcome_text = welcome_font.render('Welcome to PokeWars!', True, white)
            welcome_text_rect = welcome_text.get_rect(center=(600, 200))
            screen.blit(welcome_text, welcome_text_rect)

        # New game and quit buttons
        mouse_pos = pygame.mouse.get_pos()
        start = pygame.Rect([450, 650, 140, 50])
        start_text = titles_font.render('New Game', True, white)
        start_text_rect = start_text.get_rect(center=(520, 675))
        if start.collidepoint(mouse_pos):
            pygame.draw.rect(screen, grey2, start, border_radius = 6)
            if pygame.mouse.get_pressed()[0]:
                self.loading = True
        else:
            pygame.draw.rect(screen, white, start, width = 1, border_radius = 6)
        screen.blit(start_text, start_text_rect)

        quit = pygame.Rect([610, 650, 140, 50])
        quit_text = titles_font.render('Quit', True, white)
        quit_text_rect = quit_text.get_rect(center=(680, 675))
        if quit.collidepoint(mouse_pos):
            pygame.draw.rect(screen, grey2, quit, border_radius = 6)
        else:
            pygame.draw.rect(screen, white, quit, width = 1, border_radius = 6)
        screen.blit(quit_text, quit_text_rect)

        self.menu_buttons.append(start)
        self.menu_buttons.append(quit)
    
    # Loading message after player pressed "New Game" button
    def draw_loading(self):
        if self.loading == True:
            loading_text = titles_font.render('Loading...', True, white)
            loading_text_rect = loading_text.get_rect(center=(600, 800))
            screen.blit(loading_text, loading_text_rect)

    # Draw player and PC total score on the bottom right corner of the screen
    def draw_score(self):
        score_text = titles_font.render(f'Player: {self.player_score} | PC: {self.pc_score}', True, white)
        score_rect = score_text.get_rect()
        score_rect.topright = (1180, 5)
        screen.blit(score_text, score_rect)

    # Draw instructions on the bottom menu
    def draw_instructions(self):
        if self.player.turn == True:
            if self.player.selected_card is None and self.player.selected_attribute is None:
                instructions_text = instructions_font.render('Your turn: select a card.', True, white)
                screen.blit(instructions_text, (20, 6))
            elif self.player.selected_card is not None and self.player.selected_attribute is None:        
                instructions_text = instructions_font.render('Which attribute would your like to use? Press i for id, w for weight or h for height.', True, white)
                screen.blit(instructions_text, (20, 6))
        elif self.player.turn == False:
            if self.pc.selected_attribute is None:
                instructions_text = instructions_font.render('Waiting for PC to choose a card...', True, white)
                screen.blit(instructions_text, (20, 6))
    
    # Update main game logic
    def update(self):
        self.player.check_played()
        self.check_pc_turn()
        self.check_end_round()
        self.pc_timer()
        self.round_timer()

    # Check if player's turn is finished and if PC needs to select a card. If true, a timer is activated.
    def check_pc_turn(self):
        if self.player.turn == False and self.pc.selected_attribute is None:
            self.pc_wait = True

    # Wait 3000ms and then PC selects a card. Then set round winner.
    def pc_timer(self):
        if self.pc_wait == True:
            current_time = pygame.time.get_ticks()
            if current_time - self.player.time_played >= 2000:
                self.pc_wait = False
                self.pc.play_hand(self.player.selected_attribute[0])
                self.round_winner = self.set_round_winner(self.pc.selected_attribute, self.player.selected_attribute)
    
    # Set round winner and add one point to their score
    def set_round_winner(self, pc, player):
        if pc[1] > player[1]:
            self.pc_score += 1
            pygame.mixer.Sound.play(lose_round)
            return 'pc'
        elif pc[1] < player[1]:
            self.player_score += 1
            pygame.mixer.Sound.play(win_round)
            return 'player'
        else:
            pygame.mixer.Sound.play(lose_round)
            return 'tie'

    # Check if pc's turn is finished. If true, a timer is activated.
    def check_end_round(self):
        if self.pc.selected_attribute is not None:
            self.end_round_wait = True

    # Wait 3000ms before resetting round.
    def round_timer(self):
        if self.end_round_wait == True:
            current_time = pygame.time.get_ticks()
            if current_time - self.pc.time_played >= 3000:
                self.end_round_wait = False
                self.reset_round()

    # Reset round parameters and check if game should finish
    def reset_round(self):
        self.player.turn = True
        self.player.selected_card = None
        self.player.selected_attribute = None
        self.pc.turn = False
        self.pc.selected_card = None
        self.pc.selected_attribute = None
        self.round_winner = None
        self.check_end_game()

    # Check if all cards have been used
    def check_end_game(self):
        if not any(d['used'] == False for d in self.pc.cards):
            self.game_over = True
            self.game_running = False
            pygame.mixer.music.play(-1)

    # Display round result
    def draw_round_result(self):
        if self.round_winner is not None:
            if self.round_winner == 'pc':
                result_text = titles_font.render('PC won this round!', True, white)
            elif self.round_winner == 'player':
                result_text = titles_font.render('You won this round!', True, white)
            else:
                result_text = titles_font.render('Tie!', True, white)
            result_rect = result_text.get_rect()
            result_rect.center = (600, 655)
            screen.blit(result_text, result_rect)
            
    # Display game result
    def draw_game_result(self):
        if self.game_running == False and self.game_over == True:
            if self.player_score > self.pc_score:
                result_text = end_font.render('Congratulations! You won!', True, white)
            elif self.player_score < self.pc_score:
                result_text = end_font.render('Bad luck! PC won.', True, white)
            else:
                result_text = end_font.render('Tie!', True, white)
            result_rect = result_text.get_rect()
            result_rect.center = (600, 400)
            screen.blit(result_text, result_rect)

class PC:
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.create_card_rects()
        self.turn = False
        self.selected_card = None
        self.selected_attribute = None
        self.time_played = 0

    # Assign cards to PC
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)
    
    # PC selects random card
    def play_hand(self, attribute_name):
        played_card = random.choice([x for x in self.cards if x['used'] != True])
        self.selected_card = self.cards.index(played_card)
        self.cards[self.selected_card]['used'] = True
        self.time_played = pygame.time.get_ticks()
        self.selected_attribute = (attribute_name, played_card[attribute_name])

    def create_card_rects(self):
        for i in range(7):
            card = pygame.Rect((i * 160 + 50, 90), (140, 240))
            self.card_rects.append(card)

    def draw_cards(self):
        for card in self.card_rects:   
            i = self.card_rects.index(card)
            if self.cards[i]['used'] == True:
                pygame.draw.rect(screen, black, card)
            else:
                pygame.draw.rect(screen, grey3, card, border_radius = 12)

    def draw_selected_card(self):
        # Once PC card and attribute are selected, draw selected card and render images and text
        if self.selected_attribute is not None:
            selected_card = pygame.Rect((625, 380), (140, 240))
            pygame.draw.rect(screen, grey2, selected_card, border_radius = 12)

            name_text = card_font.render(self.cards[self.selected_card]['name'].capitalize(), True, white)
            id_text = small_card_font.render(f'ID: {self.cards[self.selected_card]["id"]}', True, white)
            height_text = small_card_font.render(f'Height: {self.cards[self.selected_card]["height"]}', True, white)
            weight_text = small_card_font.render(f'Weight: {self.cards[self.selected_card]["weight"]}', True, white)
            image = pygame.image.load(f'images/pokemon/{self.cards[self.selected_card]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))

            screen.blit(name_text, (630, 385))
            screen.blit(image_resized, (625, 415))
            screen.blit(id_text, (630, 555))
            screen.blit(height_text, (630, 575))
            screen.blit(weight_text, (630, 595))

            played_text = titles_font.render(f'PC played: {self.cards[self.selected_card]["name"].capitalize()}!', True, white)
            played_text_rect = played_text.get_rect()
            played_text_rect.topleft = (795, 440)
            screen.blit(played_text, played_text_rect)

            attribute_text = titles_font.render(f'{self.selected_attribute[0].capitalize()}: {self.selected_attribute[1]}', True, white)
            attribute_text_rect = attribute_text.get_rect()
            attribute_text_rect.topleft = (795, 480)
            screen.blit(attribute_text, attribute_text_rect)
            
class Player: 
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.create_card_rects()
        self.card_clicked = False
        self.turn = True
        self.selected_card = None
        self.selected_attribute = None
        self.time_played = 0
        self.sound_played = False

    # Assign cards to PC
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)

    def create_card_rects(self):
        for i in range(7):
            card = pygame.Rect((i * 160 + 50, 710), (140, 240))
            self.card_rects.append(card)

    def draw_cards(self):
        for card in self.card_rects:
            # Draw a rect that will represent a card in the player's hand
            #card = pygame.Rect((i * 160 + 50, 670), (140, 240))
            i = self.card_rects.index(card)
            mouse_pos = pygame.mouse.get_pos()
            if card.collidepoint(mouse_pos) and self.turn == True and self.cards[i]['used'] == False and self.selected_card == None or self.turn == True and self.selected_card == i:
                pygame.draw.rect(screen, grey2, card, border_radius = 12)
            elif self.cards[i]['used'] == True:
                pygame.draw.rect(screen, black, card)
            else:
                pygame.draw.rect(screen, grey3, card, border_radius = 12)
            #self.card_rects.append(card)

            # Render text and images to be displayed on the card
            name_text = card_font.render(self.cards[i]['name'].capitalize(), True, white)
            image = pygame.image.load(f'images/pokemon/{self.cards[i]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))
            id_text = small_card_font.render(f'ID: {self.cards[i]["id"]}', True, white)
            height_text = small_card_font.render(f'Height: {self.cards[i]["height"]}', True, white)
            weight_text = small_card_font.render(f'Weight: {self.cards[i]["weight"]}', True, white)
            
            if self.cards[i]['used'] == False or self.cards[i]['used'] == True and self.selected_card == i and self.selected_attribute is None:
            # Display text and images on  unused cards or selected card
                screen.blit(name_text, (i * 160 + 55, 715))
                screen.blit(image_resized, (i * 160 + 50, 745))
                screen.blit(id_text, (i * 160 + 55, 885))
                screen.blit(height_text, (i * 160 + 55, 905))
                screen.blit(weight_text, (i * 160 + 55, 925))

    def draw_selected_card(self):
        # Once Player card and attribute are selected, draw selected card and render images and text
        if self.selected_attribute is not None:
            selected_card = pygame.Rect((435, 380), (140, 240))
            pygame.draw.rect(screen, grey2, selected_card, border_radius = 12)

            name_text = card_font.render(self.cards[self.selected_card]['name'].capitalize(), True, white)
            id_text = small_card_font.render(f'ID: {self.cards[self.selected_card]["id"]}', True, white)
            height_text = small_card_font.render(f'Height: {self.cards[self.selected_card]["height"]}', True, white)
            weight_text = small_card_font.render(f'Weight: {self.cards[self.selected_card]["weight"]}', True, white)
            image = pygame.image.load(f'images/pokemon/{self.cards[self.selected_card]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))

            screen.blit(name_text, (440, 385))
            screen.blit(image_resized, (435, 415))
            screen.blit(id_text, (440, 555))
            screen.blit(height_text, (440, 575))
            screen.blit(weight_text, (440, 595))

            played_text = titles_font.render(f'You played: {self.cards[self.selected_card]["name"].capitalize()}!', True, white)
            played_text_rect = played_text.get_rect()
            played_text_rect.topright = (420, 450)
            screen.blit(played_text, played_text_rect)

            attribute_text = titles_font.render(f'{self.selected_attribute[0].capitalize()}: {self.selected_attribute[1]}', True, white)
            attribute_text_rect = attribute_text.get_rect()
            attribute_text_rect.topright = (420, 480)
            screen.blit(attribute_text, attribute_text_rect)

    # Check if Player has selected card and attribute and end Player turn
    def check_played(self):
        if self.turn == True and self.selected_attribute is not None:
            self.time_played = pygame.time.get_ticks()
            pygame.mixer.Sound.play(card_selected)
            self.turn = False

class Deck:
    def __init__(self):
        # A list that will contain a dictionary for each Pokemon card. Each dict will contain id, name, height, weight, image. 
        self.deck = []
        self.build_deck()

    def build_deck(self):
        # Add 14 cards to deck
        for _ in range(14):
            pokemon = dict()
            # Select a random Pokemon id
            while True:
                id = random.randint(1,898)
                # Check if the id already exists in the deck. If it already exists, select a new id
                if not any(d['id'] == id for d in self.deck):
                    # Retrive data from PokeAPI for the Pokemon corresponding to the selected id
                    # Check if there is an image available for the Pokemon with the id selected
                    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}').json()
                    image_path = 'images/pokemon/' + response["name"] + '.png'
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
            self.deck.append(pokemon)

    # Method called by PC and Player when cards are dealt
    def deal(self):
        return self.deck.pop()

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
        if event.type == pygame.MOUSEBUTTONUP:
            # Start menu buttons
            if main_game.game_running == False:
                if main_game.menu_buttons[1].collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if main_game.menu_buttons[0].collidepoint(event.pos):
                    main_game.start_game()
            # Player select card
            if main_game.game_running == True:
                if main_game.player.selected_card is None and main_game.player.selected_attribute is None:
                    for card in main_game.player.card_rects:
                        if card.collidepoint(event.pos) and main_game.player.cards[main_game.player.card_rects.index(card)]['used'] == False:
                            main_game.player.selected_card = main_game.player.card_rects.index(card)
                            main_game.player.cards[main_game.player.selected_card]['used'] = True
        # Player select attribute
        if event.type == pygame.KEYDOWN:
            if main_game.game_running == True:
                if main_game.player.selected_card is not None and main_game.player.selected_attribute is None:
                    if event.key == pygame.K_i:
                        main_game.player.selected_attribute = ('id', main_game.player.cards[main_game.player.selected_card]['id'])
                    if event.key == pygame.K_h:
                        main_game.player.selected_attribute = ('height', main_game.player.cards[main_game.player.selected_card]['height'])
                    if event.key == pygame.K_w:
                        main_game.player.selected_attribute = ('weight', main_game.player.cards[main_game.player.selected_card]['weight'])

    # Screen and fps
    
    main_game.draw_backgroud()
    main_game.draw_elements()
    clock.tick(fps)
    
    # Update game logic once game has started
    if main_game.game_running == True:
        main_game.update()

    pygame.display.update()
