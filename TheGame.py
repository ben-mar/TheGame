import numpy as np

class Player:

    def __init__(self,SIZE):
        self.SIZE = SIZE
        self.Deck = [i for i in range(2,self.SIZE)]
        self.PileUP = [1]
        self.PileDOWN = [self.SIZE]
        self.Hand = []
        self.PlayedOnOpponnentPiles = False
        
    def ShuffleDeck(self):
        np.random.shuffle(self.Deck)
    
    def EmptyPiles(self):
        self.PileUP = [1]
        self.PileDOWN = [self.SIZE]

    def Draw(self,NumberOfCards):
        """
        Draws a number of cards equal to NumberOfCards from the deck (self.Deck).
        If the deck has not enough cards in it, the function draws the whole resting deck.
        """
        if len(self.Deck) >= NumberOfCards :
            self.Hand += self.Deck[-NumberOfCards:]
            self.Deck = self.Deck[:-NumberOfCards]
        else :
            self.Hand += self.Deck
            self.Deck = []

    def setup(self):
        Player.ShuffleDeck(self)
        Player.EmptyPiles(self)
        Player.Draw(self,6)


class Game:

    def __init__(self):
        SIZE = 60
        self.Player1 = Player(SIZE)
        self.Player2 = Player(SIZE)
        self.ActivePlayer = 1

        self.Player1.setup()
        self.Player2.setup()
        self.PlayedOnOpponnentPiles = [False,False]
        self.PlayedOnOpponnentPilesPlayer1 = self.PlayedOnOpponnentPiles[0]
        self.PlayedOnOpponnentPilesPlayer2 = self.PlayedOnOpponnentPiles[1] 

        self.P1GameOver = False 
        self.P2GameOver = False

    def CheckAction(self,PileIndex,Number,PileName):
        """
        Returns True if the rules allow ActivePlayer to put the card N° Number on PileName 'UP'/'DOWN' bellonging to player N° PileIndex
        Returns False if not
        """
        if PileName=='UP':

            if PileIndex == 1:
                if self.ActivePlayer == PileIndex :
                    return (self.Player1.PileUP[-1:][0] < Number ) or\
                        (self.Player1.PileUP[-1:][0] == Number + 10)
                elif not self.PlayedOnOpponnentPiles[self.ActivePlayer-1] :
                    return (self.Player1.PileUP[-1:][0] > Number )
                elif self.PlayedOnOpponnentPiles[self.ActivePlayer-1] :
                    print("Player {} has already played on opponents piles this turn !".format(self.ActivePlayer))
                    return False

            elif PileIndex == 2:
                if self.ActivePlayer == PileIndex :
                    return (self.Player2.PileUP[-1:][0] < Number ) or\
                        (self.Player2.PileUP[-1:][0] == Number + 10)
                elif not self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                    return (self.Player2.PileUP[-1:][0] > Number )
                elif not self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                    print("Player {} has already played on opponents piles this turn !".format(self.ActivePlayer))
                    return False
            else:
                print("PileIndex {} unkown".format(PileIndex))

        elif PileName=='DOWN':
            if PileIndex == 1:
                if self.ActivePlayer == PileIndex :
                    return (self.Player1.PileDOWN[-1:][0] > Number ) or\
                        (self.Player1.PileDOWN[-1:][0] == Number - 10)
                elif not self.PlayedOnOpponnentPiles[self.ActivePlayer-1] :
                    return (self.Player1.PileDOWN[-1:][0] < Number )
                elif self.PlayedOnOpponnentPiles[self.ActivePlayer-1] :
                    print("Player {} has already played on opponents piles this turn !".format(self.ActivePlayer))
                    return False

            elif PileIndex == 2:
                if self.ActivePlayer == PileIndex :
                    return (self.Player2.PileDOWN[-1:][0] > Number ) or\
                        (self.Player2.PileDOWN[-1:][0] == Number - 10)
                elif not self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                    return (self.Player2.PileDOWN[-1:][0] < Number )
                elif not self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                    print("Player {} has already played on opponents piles this turn !".format(self.ActivePlayer))
                    return False
            else:
                print("PileIndex {} unkown".format(PileIndex))      
        
        else:
            print("PileName {} unknown".format(PileName))
        
    
    def Put(self,PileIndex,Number,PileName):
        if Game.CheckAction(self,PileIndex,Number,PileName):
            if self.ActivePlayer != PileIndex:
                self.PlayedOnOpponnentPiles[self.ActivePlayer-1] = True
            if PileIndex==1:
                if PileName=='UP':
                    self.Player1.PileUP.append(Number)
                if PileName=='DOWN':
                    self.Player1.PileDOWN.append(Number)
            elif PileIndex==2:
                if PileName=='UP':
                    self.Player2.PileUP.append(Number)
                if PileName=='DOWN':
                    self.Player2.PileDOWN.append(Number)
            return 0
        else:
            print('Not possible to Put number {} on the Pile {} of the player {}'.format(Number,PileName,PileIndex))
            return 1
    
    def Play(self,PileIndex,Number,PileName):
        if self.ActivePlayer == 1:
            if Number in self.Player1.Hand :
                err = Game.Put(self,PileIndex,Number,PileName)
                if err == 0 :
                    self.Player1.Hand.remove(Number)
        elif self.ActivePlayer == 2:
            if Number in self.Player2.Hand :
                err = Game.Put(self,PileIndex,Number,PileName)
                if err == 0 :
                    self.Player2.Hand.remove(Number)           
                
    def Concede(self):
        if self.ActivePlayer == 1 :
            self.P1GameOver = True
        elif self.ActivePlayer == 2 :
            self.P2GameOver = True

    def ChangeActivePlayer(self):
        if self.ActivePlayer == 1 :
            self.ActivePlayer = 2
        elif self.ActivePlayer == 2 :
            self.ActivePlayer = 1
    
    def DrawEndOfTurn(self):
        if self.ActivePlayer == 1 :
            if self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                CardsInHandPlayer1 = len(self.Player1.Hand)
                self.Player1.Draw(6-CardsInHandPlayer1)
            else :
                self.Player1.Draw(2)
        elif self.ActivePlayer == 2 :
            if self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                CardsInHandPlayer2 = len(self.Player2.Hand)
                self.Player2.Draw(6-CardsInHandPlayer2)
            else :
                self.Player2.Draw(2)

    def EndOfTurn(self):
        if (self.Player1.Deck == []) and (self.Player1.Hand == []):
            self.P2GameOver = True # The Player 1 has won the game
        elif (self.Player2.Deck == []) and (self.Player2.Hand == []):
            self.P1GameOver = True # The Player 2 has won the game
        Game.DrawEndOfTurn(self)
        self.PlayedOnOpponnentPiles = [False,False]
        Game.ChangeActivePlayer(self)

    def Display(self):
        print("Turn of Player {} \n".format(self.ActivePlayer))
        print("Pile UP Player 1 : {}".format(self.Player1.PileUP))
        print("Pile DOWN Player 1 : {} \n".format(self.Player1.PileDOWN))
        print("Pile UP Player 2 : {}".format(self.Player2.PileUP))
        print("Pile DOWN Player 2 : {} \n".format(self.Player2.PileDOWN))
        print("Hand Player 1 {} ".format(self.Player1.Hand))
        print("Hand Player 2 {} \n \n \n ".format(self.Player2.Hand))
    
    def INPUT(self):
        Number = int(input("What card do you want to play ?"))
        if Number ==  0:
            Game.Concede(self)
            return
        if Number == -1:
            Game.EndOfTurn(self)
            return
        PileIndex = int(input("On which Player's Pile do you want to play (Player 1 or 2) ?"))
        PileName = str(input("Pile Up or down ?")).upper()
        Game.Play(self,PileIndex,Number,PileName)


        

def main():
    
    MainGame = Game()
    while((not MainGame.P1GameOver) and (not MainGame.P2GameOver)):
        MainGame.Display()
        MainGame.INPUT()

# redraw function at end of turn : detects when player says end of turn    
   
#main()    




