# Wisconsin Card Sorting Test
Python Implementation of the Wisconsin Card Sorting Test.

The WhisconsinCard() takes 2 input:
- NumTrial: Number of times we want the rule of the game to change 
- NumExec: Number of trials with the same rule. If NumExec==0, the number of trials will be randomly generated.
The output of the class has to be executed following the shuffleCardwRule() method, resulting in the following items:
1. FinalDeck: a NumTrial*NumExec long list of 5 rk=2 (3,4,) tensor, in which are stored the cards. The first card, is the one we want to associate with one of the other 4 in the deck. Each card is coded as follows:
  Card[0,:] describes the shape -> Circle, Triangle, Pentago and Arrow.
  Card[1,:] descrives the color -> red, blue, green, yellow.
  Card[2,:] describes the number of items on a card -> 1,2,3,4.
2. FinalResult: a list composed of NumTrial*NumExec lists of 5 elements, 4 zero and a 1. The position of the 1 represents the correct association, given the rule. 
3. FinalRule: a list of NumTrial*NumExec rk=1 (3,) tensor, which represent the association rule (randomly generated) as follow:
  [1,0,0] -> Shape assocaition.
  [0,1,0] -> Color assocaition.
  [0,0,1] -> Number of items assocaition.
-----
Giacomo Vedovati
g.vedovati@wustl.edu

Braindynamics and Control Group, Dr. Ching.
Washington University in St. Louis
Department of Electrical & System Enginerring
ese.wustl.edu
