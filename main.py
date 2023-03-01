import pygame, sys, random, requests
import os.path

# Initialise pygame

pygame.init()

# Set caption and icon

pygame.display.set_caption('PokeWars')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Create the screen

screen = pygame.display.set_mode((1200, 900))

# Define FPS

clock = pygame.time.Clock()
fps = 60

# Retrieve Pokemon info from PokeAPI

pokemon = requests.get('https://pokeapi.co/api/v2/pokemon').json()
#print(pokemon)

# Main game class

class MAIN:
    def __init__(self):
        self.deck = Deck()
        self.player = Player()
        self.pc = PC()
        self.deal()
    
    # Assigns half of the cards in the deck to player and the other half to PC
    def deal(self):
        half = self.deck.lenght//2
        self.player.cards.append(self.deck.full_deck[half:])
        self.pc.cards.append(self.deck.full_deck[:half])


class Player:
    def __init__(self):
        self.cards = []


class PC: 
    def __init__(self):
        self.cards = []


class Deck:
    def __init__(self):
        # A list that will contain a dictionary for each Pokemon card. Each dict will contain id, name, height, weight, image 
        self.lenght = 14
        self.full_deck = []
        self.build_deck()
    

    def build_deck(self):
        for _ in range(self.lenght):
            pokemon = dict()
            # Select a random Pokemon id
            while True:
                id = random.randint(1,898)
                # Check if the id already exists in the deck. If it already exists, select a new id
                if not any(d['id'] == 'id' for d in self.full_deck):
                    # Retrive data from PokeAPI for the Pokemon corresponding to the selected id
                    # Check if there is an image available for the Pokemon with the id selected
                    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}').json()
                    image_path = 'images/' + response["name"] + '.png'
                    if os.path.isfile(image_path):
                        break
                    else:
                        print(image_path)
                        continue
                else:
                    continue
            
            # Create a dictionary that will store Pokemon attributes

            pokemon['id'] = id
            pokemon['name'] = response['name']
            pokemon['height'] = response['height']
            pokemon['weight'] = response['weight']
            pokemon['image'] = f'{pokemon["name"]}.png'

            self.full_deck.append(pokemon)

        print(self.full_deck)
    
    

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
    screen.fill((0, 0, 0))
    clock.tick(fps)

   

    pygame.display.update()