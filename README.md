# Welcome to PokeWars!

## Description

An exciting game of top trumps with Pokemon cards, developed in Python and Pygame.

## Description

This game retrieves data from the [PokeAPI](https://pokeapi.co/). The documentation is available [here](https://pokeapi.co/docs/v2).

The Pokemon images are from [The Complete Pokemon Images Data Set](https://www.kaggle.com/datasets/arenagrenade/the-complete-pokemon-images-data-set) by 
Rohan Asokan.

## Libraries

- PyGame: [https://www.pygame.org/docs/](https://www.pygame.org/docs/)
- random: [https://docs.python.org/3/library/random.html](https://docs.python.org/3/library/random.html)
- sys: [https://docs.python.org/3/library/sys.html](https://docs.python.org/3/library/sys.html)
- requests: [https://pypi.org/project/requests/](https://pypi.org/project/requests/)
- os.path: [https://docs.python.org/3/library/os.path.html](https://docs.python.org/3/library/os.path.html)

## Usage

```python main.py```

Player and PC will be dealt 7 cards each.

When the game starts, Player will be asked to select a card.

![Select card](https://i.imgur.com/RBWEPSQ.png)

Next, Player will be asked what attribute they would like to choose to play against PC's hand.

![Select attribute](https://i.imgur.com/oMZcUzH.png)

Now it's PC's turn to select a card. The value of the attribute selected by Player will be compared to the value of the same attribute on PC's hand. Whoever has the highest value, wins the round and 1 point will be added to their total score.

![PC plays hand. Round winner announced](https://i.imgur.com/nZIudpK.png)

The game will continue until all 7 cards are played. The player with the highest total score wins.

![Game ends. Winner announced](https://i.imgur.com/Jj3MQPi.png)
