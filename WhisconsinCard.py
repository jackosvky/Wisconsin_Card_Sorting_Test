import torch as torch
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from matplotlib.patches import RegularPolygon
from matplotlib.patches import Arrow
import random

'''
Wisconsin Card Sorting task
The WhisconsinCard() takes 2 input:
    - NumTrial: Number of times we want the rule of the game to change 
    - NumExec: Number of trials with the same rule. If NumExec==0, the number of trials will be randomly generated.

The output of the class has to be executed following the shuffleCardwRule() method, resulting in the following items:
    1. FinalDeck: a NumTrial*NumExec long list of 5 rk=2 (3,4,) tensor, in which are stored the cards.
        The first card, is the one we want to associate with one of the other 4 in the deck.
        Each card is coded as follows:
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
'''

class WhisconsinCard():
    def __init__(self, NumTrial, NumExec):
        '''
        NumTrial: number of trials during which the rule does not vary
        NumExec: number of events in the trial
        '''
        self.NumTrial = NumTrial
        self.NumExec = NumExec
        self.CardElemet = (3,4,)
        #pass

    def GenCards(self):
        Card = torch.zeros(self.CardElemet)
        for i in range(self.CardElemet[0]):
            rdnInt = torch.randint(0,4,(1,))
            Card[i, rdnInt] = 1

        return Card

    def ShuffleCards(self):
        Deck = []
        eye_mat = torch.eye(4)
    
        for i in range(5):
            card = self.GenCards()
            Deck.append(card)

        for j in range(4):
            Deck[j+1][0] = torch.roll(Deck[j][0], 1)
            Deck[j+1][1] = torch.roll(Deck[j][1], 1)
            Deck[j+1][2] = torch.roll(Deck[j][2], 1)

        for i in range(3):
            Deck[i+1][i, :] = Deck[0][i, :]

        Deck[-1][0] = torch.roll(Deck[0][0], 1)
        Deck[-1][1] = torch.roll(Deck[1][1], 1)
        Deck[-1][2] = torch.roll(Deck[2][2], 1)

        return Deck

    def shuffleCardwRule(self):
        '''
        Check the Deck dimension when outputting, the rule goes donw to 4 when shuffled. WHy?
        '''
        eye_mat = torch.eye(3)
        rdnInt = torch.randint(0, 3, (self.NumTrial,))
        ShuffledDeckwRule = []

        FinalDeck = []
        FinalResult = []
        FinalRule = []

        if self.NumExec == 0:
            rnd_exec_lenght = torch.randint(1, 10, (self.NumTrial,))
        else:
            rnd_exec_lenght = self.NumExec * torch.ones((self.NumTrial,))
            rnd_exec_lenght = rnd_exec_lenght.int()

        for i in range(self.NumTrial):
            for j in range(rnd_exec_lenght[i]):
                Deck = self.ShuffleCards()
                Res_Vec = [0, 0, 0, 0, 0]
                if rdnInt[i-1,] == 0:
                    rule = [0, 1, 0, 0, 0]
                elif rdnInt[i-1,] == 1:
                    rule = [0, 0, 1, 0, 0]
                elif rdnInt[i-1, ] == 2:
                    rule = [0, 0, 0, 1, 0]
                
                # Shuffle the Deck: the first card is the reference one
                copyDeck = Deck[1:]
                copyrule = rule[1:]
                c = list(zip(copyDeck, copyrule))
                random.shuffle(c)
                copyDeck, copyrule = zip(*c)

                Deck[1:] = copyDeck
                Res_Vec[1:] = copyrule
                
                FinalDeck.append(Deck)
                FinalResult.append(Res_Vec)
                FinalRule.append(eye_mat[rdnInt[i-1, ], :])

        return FinalDeck, FinalResult, FinalRule

if __name__ == "__main__":

    n_sameRule = 2
    n_trial = 2
    test = WhisconsinCard(n_sameRule, n_trial)
    Deck, Res_Vec, Rule = test.shuffleCardwRule()

    fig = plt.subplots(figsize=(15, 10))
    plt.subplots_adjust(hspace=0.1)

    for i in range(n_sameRule*n_trial):
        x_dim = 4
        y_dim = 6
        Dx = x_dim+1
        ax = plt.subplot(n_sameRule, n_trial, i + 1)
        #ax.axis('equal','box')
        ax.set_aspect('equal', 'box')
        ax.set_xlim(0, (5*Dx+1))
        ax.set_ylim(0, y_dim+2)
        for j in range(5):
            # Rectangle Card
            ax.add_patch(Rectangle((1 + j*Dx, 1), x_dim, y_dim,
                                edgecolor='black',
                                facecolor='white',
                                fill=True,
                                lw=2))
            # Get the Color
            if Deck[i][j][1, :].dot(torch.eye(4)[0, :]) == 1:
                color = 'red'
            elif Deck[i][j][1, :].dot(torch.eye(4)[1, :]) == 1:
                color = 'blue'
            elif Deck[i][j][1, :].dot(torch.eye(4)[2, :]) == 1:
                color = 'green'
            elif Deck[i][j][1, :].dot(torch.eye(4)[3, :]) == 1:
                color = 'yellow'

            #Get the number of elemnts
            if Deck[i][j][2, :].dot(torch.eye(4)[0, :]) == 1:
                num_el = 1
            elif Deck[i][j][2, :].dot(torch.eye(4)[1, :]) == 1:
                num_el = 2
            elif Deck[i][j][2, :].dot(torch.eye(4)[2, :]) == 1:
                num_el = 3
            elif Deck[i][j][2, :].dot(torch.eye(4)[3, :]) == 1:
                num_el = 4

            #Draw the patches
            if Deck[i][j][0, :].dot(torch.eye(4)[0, :]) == 1:
                for ii in range(num_el):
                    ax.add_patch(Circle(((x_dim/2) + 1 + j*Dx, (1 + y_dim*(ii+1)/(num_el+1))), 0.5,
                                        facecolor=color,
                                        fill=True))

            if Deck[i][j][0, :].dot(torch.eye(4)[1, :]) == 1:
                for ii in range(num_el):
                    ax.add_patch(RegularPolygon(((x_dim/2) + 1 + j*Dx, (1 + y_dim*(ii+1)/(num_el+1))), 3, 0.5,
                                                facecolor=color,
                                                fill=True))

            if Deck[i][j][0, :].dot(torch.eye(4)[2, :]) == 1:
                for ii in range(num_el):
                    ax.add_patch(RegularPolygon(((x_dim/2)+1 + j*Dx, (1 + y_dim*(ii+1)/(num_el+1))), 5, 0.5,
                                                facecolor=color,
                                                fill=True))

            if Deck[i][j][0, :].dot(torch.eye(4)[3, :]) == 1:
                for ii in range(num_el):
                    ax.add_patch(Arrow((x_dim/2)+1 + j*Dx - 0.5, (1 + y_dim*(ii+1)/(num_el+1))-0.5, 1, 1, 1.2,
                                    facecolor=color,
                                    fill=True))

            
    #display plot
    plt.show()



