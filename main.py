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
small_card_font_selected = pygame.font.Font('BarlowCondensed-Bold.ttf', 18)

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
        self.game_running = True
        self.player_score = 0
        self.pc_score = 0
        self.round_winner = None





        self.time_round_ended = 0
        self.wait = False
       
    def deal_cards(self):
        self.player.draw(self.deck)
        self.pc.draw(self.deck)

    def draw_elements(self):
        self.draw_background()
        self.player.draw_cards()
        self.pc.draw_cards()
        self.player.draw_selected_card()
        self.pc.draw_selected_card()
        self.draw_score()
        self.player.draw_instructions()
        self.draw_round_result()
        self.draw_game_result()
    
    def draw_background(self):
        bottom_menu = pygame.draw.rect(screen, grey3, [0, 960, WIDTH, 40])
        pc_container = pygame.draw.rect(screen, white, [15, 10, 1175, 295], width = 1)
        pc_text = titles_font.render('PC', True, white)
        pc_text_rect = pc_text.get_rect(center=(WIDTH/2, 28))
        screen.blit(pc_text, pc_text_rect)

        player_container = pygame.draw.rect(screen, white, [15, 655, 1175, 295], width = 1)
        player_text = titles_font.render('Player', True, white)
        player_text_rect = pc_text.get_rect(center=(WIDTH/2, 930))
        screen.blit(player_text, player_text_rect)
        
    def draw_score(self):
        score_text = titles_font.render(f'Player: {self.player_score} | PC: {self.pc_score}', True, white)
        score_rect = score_text.get_rect()
        score_rect.topright = (1180, 965)
        screen.blit(score_text, score_rect)
    
    def game(self):
        
        if any(d['used'] == False for d in self.player.cards):
            self.player.turn = True
            self.player.play_hand()
        
            if self.player.turn == False:
                self.pc.turn = True
                self.pc.play_hand(self.player.selected_attribute[0])
                self.round_winner = self.set_round_winner(self.pc.selected_attribute, self.player.selected_attribute) 
                self.time_round_ended = pygame.time.get_ticks()
                self.wait = True
                  
        else:
            pygame.time.delay(3000)
            self.game_running = False


    def timer(self):
        if self.wait == True:
            current_time = pygame.time.get_ticks()
            if current_time - self.time_round_ended >= 3000:
                self.wait = False
                self.end_round()

    def set_round_winner(self, pc, player):
        if pc[1] > player[1]:
            self.pc_score += 1
            return 'pc'
        elif pc[1] < player[1]:
            self.player_score += 1
            return 'player'
        else:
            return 'tie'
            
    def draw_round_result(self):
        if self.round_winner is not None:
            
            if self.round_winner == 'pc':
                result_text = titles_font.render('PC won this round!', True, white)
            elif self.round_winner == 'player':
                result_text = titles_font.render('You won this round!', True, white)
            else:
                result_text = titles_font.render('Tie!', True, white)
            result_rect = result_text.get_rect()
            result_rect.center = (600, 615)
            screen.blit(result_text, result_rect)

    def end_round(self):
        self.player.turn = False
        self.player.selected_card = None
        self.player.selected_attribute = None
        self.pc.turn = False
        self.pc.selected_card = None
        self.pc.selected_attribute = None
        self.round_winner = None
            
    def draw_game_result(self):
        if self.game_running == False:
            if self.player_score > self.pc_score:
                result_text = titles_font.render('Congratulations! You won!', True, white)
            elif self.player_score < self.pc_score:
                result_text = titles_font.render('Bad luck! PC won.', True, white)
            else:
                result_text = titles_font.render('Tie!', True, white)
            result_rect = result_text.get_rect()
            result_rect.center = (600, 615)
            screen.blit(result_text, result_rect)


class PC:
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.turn = False
        self.selected_card = None
        self.selected_attribute = None

    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)
    
    def draw_cards(self):

        # Render text and images to be displayed on the selected card
        
        for i in range(7):
            card = pygame.Rect((i * 160 + 50, 50), (140, 240))
            self.card_rects.append(card)
            if self.cards[i]['used'] == True:
                pygame.draw.rect(screen, black, card)
            else:
                pygame.draw.rect(screen, grey3, card, border_radius = 12)
        
            # Display text and images on card

    def play_hand(self, attribute_name):
        
        played_card = random.choice([x for x in self.cards if x['used'] != True])
        self.selected_card = self.cards.index(played_card)
        self.cards[self.selected_card]['used'] = True
        self.selected_attribute = (attribute_name, played_card[attribute_name])
        return self.selected_attribute
    
    def draw_selected_card(self):
        if self.turn == True:
            selected_card = pygame.Rect((625, 340), (140, 240))
            #selected_card.center = (400, 500)
            pygame.draw.rect(screen, grey2, selected_card, border_radius = 12)

            name_text = card_font.render(self.cards[self.selected_card]['name'].capitalize(), True, white)
            id_text = small_card_font.render(f'ID: {self.cards[self.selected_card]["id"]}', True, white)
            height_text = small_card_font.render(f'Height: {self.cards[self.selected_card]["height"]}', True, white)
            weight_text = small_card_font.render(f'Weight: {self.cards[self.selected_card]["weight"]}', True, white)
            image = pygame.image.load(f'images/{self.cards[self.selected_card]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))

            screen.blit(name_text, (630, 345))
            screen.blit(image_resized, (625, 375))
            screen.blit(id_text, (630, 515))
            screen.blit(height_text, (630, 535))
            screen.blit(weight_text, (630, 555))

            played_text = titles_font.render(f'PC played: {self.cards[self.selected_card]["name"].capitalize()}!', True, white)
            played_text_rect = played_text.get_rect()
            played_text_rect.topleft = (795, 410)
            screen.blit(played_text, played_text_rect)

            attribute_text = titles_font.render(f'{self.selected_attribute[0].capitalize()}: {self.selected_attribute[1]}', True, white)
            attribute_text_rect = attribute_text.get_rect()
            attribute_text_rect.topleft = (795, 440)
            screen.blit(attribute_text, attribute_text_rect)
            

class Player: 
    def __init__(self):
        self.cards = []
        self.card_rects = []
        self.card_clicked = False
        self.turn = False
        self.selected_card = None
        self.selected_attribute = None
        
    
    def draw(self, deck):
        for _ in range(7):
            card = deck.deal()
            self.cards.append(card)

    def draw_cards(self):
        for i in range(7):
            # Draw a rect that will represent a card in the player's hand

            card = pygame.Rect((i * 160 + 50, 670), (140, 240))

            mouse_pos = pygame.mouse.get_pos()
            if card.collidepoint(mouse_pos) and self.turn == True and self.cards[i]['used'] == False and self.selected_card == None or self.turn == True and self.selected_card == i and self.cards[i]['used'] == False:
                pygame.draw.rect(screen, grey2, card, border_radius = 12)
            elif self.cards[i]['used'] == True:
                pygame.draw.rect(screen, black, card)
            else:
                pygame.draw.rect(screen, grey3, card, border_radius = 12)

            self.card_rects.append(card)

            # Render text and images to be displayed on the card
            name_text = card_font.render(self.cards[i]['name'].capitalize(), True, white)
            image = pygame.image.load(f'images/{self.cards[i]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))
            id_text = small_card_font.render(f'ID: {self.cards[i]["id"]}', True, white)
            height_text = small_card_font.render(f'Height: {self.cards[i]["height"]}', True, white)
            weight_text = small_card_font.render(f'Weight: {self.cards[i]["weight"]}', True, white)
            
            if self.cards[i]['used'] == False:
            # Display text and images on card
                screen.blit(name_text, (i * 160 + 55, 675))
                screen.blit(image_resized, (i * 160 + 50, 705))
                screen.blit(id_text, (i * 160 + 55, 845))
                screen.blit(height_text, (i * 160 + 55, 865))
                screen.blit(weight_text, (i * 160 + 55, 885))

    def play_hand(self):
        if self.turn == True and self.selected_card is None:
            self.selected_card = self.select_card()
        
        if self.turn == True and self.selected_card is not None and self.selected_attribute is None:       
            self.selected_attribute = self.select_attribute(self.selected_card)
            if self.selected_attribute is not None:
                self.cards[self.selected_card]['used'] = True
                self.turn = False
            #return self.selected_attribute

    def select_card(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.turn == True and self.selected_card is None:
            for card in self.card_rects:
                if card.collidepoint(mouse_pos):
                    if pygame.mouse.get_pressed()[0] and self.cards[self.card_rects.index(card)]['used'] == False:
                        self.card_clicked = True
                    else:
                        if self.card_clicked == True:
                            self.card_clicked = False
                            return self.card_rects.index(card)
                                                
    def select_attribute(self, index):
        if self.turn == True and self.selected_attribute is None:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_i]:
                return ('id', self.cards[index]['id'])
            elif pressed[pygame.K_h]:
                return ('height', self.cards[index]['height'])
            elif pressed[pygame.K_w]:
                return ('weight', self.cards[index]['weight'])     

    def draw_instructions(self):
        if self.turn == True and self.selected_card is None:
            instructions_text = titles_font.render('Your turn: select a card.', True, white)
            screen.blit(instructions_text, (20, 965))
        elif self.turn == True and self.selected_attribute is None:        
            instructions_text = titles_font.render('Which attribute would your like to use? Press i for id, w for weight or h for height.', True, white)
            screen.blit(instructions_text, (20, 965))

    def draw_selected_card(self):
        if self.selected_attribute is not None:
            selected_card = pygame.Rect((435, 340), (140, 240))
            #selected_card.center = (400, 500)
            pygame.draw.rect(screen, grey2, selected_card, border_radius = 12)

            name_text = card_font.render(self.cards[self.selected_card]['name'].capitalize(), True, white)
            id_text = small_card_font.render(f'ID: {self.cards[self.selected_card]["id"]}', True, white)
            height_text = small_card_font.render(f'Height: {self.cards[self.selected_card]["height"]}', True, white)
            weight_text = small_card_font.render(f'Weight: {self.cards[self.selected_card]["weight"]}', True, white)
            image = pygame.image.load(f'images/{self.cards[self.selected_card]["image"]}').convert_alpha()
            image_resized = pygame.transform.scale(image, (140,140))

            screen.blit(name_text, (440, 345))
            screen.blit(image_resized, (435, 375))
            screen.blit(id_text, (440, 515))
            screen.blit(height_text, (440, 535))
            screen.blit(weight_text, (440, 555))

            played_text = titles_font.render(f'You played: {self.cards[self.selected_card]["name"].capitalize()}!', True, white)
            played_text_rect = played_text.get_rect()
            played_text_rect.topright = (420, 410)
            screen.blit(played_text, played_text_rect)

            attribute_text = titles_font.render(f'{self.selected_attribute[0].capitalize()}: {self.selected_attribute[1]}', True, white)
            attribute_text_rect = attribute_text.get_rect()
            attribute_text_rect.topright = (420, 440)
            screen.blit(attribute_text, attribute_text_rect)


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
    main_game.timer()
    clock.tick(fps)
    
    if main_game.game_running == True:
        main_game.game()

    pygame.display.update()