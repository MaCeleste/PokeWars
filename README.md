# Welcome to PokeWars!

## Description

An exciting game of top trumps with Pokemon cards, developed in Python and [Pygame](https://www.pygame.org/docs/).

This game retrieves data from the [PokeAPI](https://pokeapi.co/). The documentation is available [here](https://pokeapi.co/docs/v2).

The Pokemon images are from [The Complete Pokemon Images Data Set](https://www.kaggle.com/datasets/arenagrenade/the-complete-pokemon-images-data-set) by 
Rohan Asokan.

## Gameplay and screenshots

```python main.py```

After starting the program, the player will be greeted with a welcome message and a menu with two options. 

![Start screen](https://i.imgur.com/vGaSmpK.png)

After pressing 'New Game' a 'Loading' message will appear.

![Loading...](https://i.imgur.com/gD4LJp8.png)

Next, the playing board will be displayed. Each player will be dealt seven cards. First, it's Player's turn to act. They will be asked to select a card.

![Select card](https://i.imgur.com/Fp6icGa.png)

Next, Player will be asked what attribute they would like to choose to play against PC's hand.

![Select attribute](https://i.imgur.com/maejUIe.png)

Now it's time to wait for PC to select a card.

![Waiting for PC to play](https://i.imgur.com/TexnJqb.png)

The value of the attribute selected by Player will be compared to the value of the same attribute on PC's hand. Whoever has the highest value, wins the round and one point will be added to their total score.

![PC plays hand. Round winner announced](https://i.imgur.com/Boe73Fu.png)

The game will continue until all seven cards are played. The player with the highest total score wins. Player will have the possibility to start a new game or quit.

![Game ends. Winner announced. Menu to restart the game or quit](https://i.imgur.com/ZtD0nrC.png)
