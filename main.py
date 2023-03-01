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
        print('Hello')

class Deck:
    def __init__(self):
        # A list that will contain id, name, height, weight, image
        self.cards = []
        self.build_deck()

    
    def build_deck(self):
        for _ in range(14):
            pokemon = dict()
            # Select a random Pokemon id
            while True:
                id = random.randint(1,898)
                # Check if the id already exists in the deck. If it already exists, select a new id
                if not any(d['id'] == 'id' for d in self.cards):
                    response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{id}').json()
                    image_path = 'images/' + response["name"] + '.png'
                    if os.path.isfile(image_path):
                        break
                    else:
                        print(image_path)
                        continue
                else:
                    continue
            
            #Retrive data from PokeAPI for the Pokemon corresponding to the selected id
            #response = requests.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon["id"]}').json()

            pokemon['id'] = id
            pokemon['name'] = response['name']
            pokemon['height'] = response['height']
            pokemon['weight'] = response['weight']
            pokemon['image'] = f'{pokemon["name"]}.png'

            self.cards.append(pokemon)

        print(self.cards)


# Create instance of a new game

main_game = MAIN()
deck = Deck()

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