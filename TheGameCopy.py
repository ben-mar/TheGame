import numpy as np
import os
import pygame, sys
#from pygame.locals import *


class Card:

    def __init__(self,
                 number : int,
                 color: str
                 ) -> None: 

        self.number = number
        self.color = color

    def __eq__(self,
               other
               ) -> bool:

        """Overrides the default implementation"""

        if isinstance(other, Card):
            SameNumber = (self.number == other.number)
            SameColor = (self.color == other.color)
            return (SameColor & SameNumber)

        return False

    def __repr__(self):
        return "Card : "+str(self.number)+", color: "+self.color

    def __str__(self):
        return "Card : "+str(self.number)+", color: "+self.color

class Hand:

    def __init__(self,
                 ListOfCards: list
                 ) -> None:

        if isinstance(ListOfCards[0], Card):
            self.color = ListOfCards[0].color
        for card in ListOfCards:
            if not isinstance(card, Card):
                Exception("The list is not only composed of Cards !")
            
            if card.color != self.color:
                Exception("The list is not composed of Cards of the same color !")
        
        self.hand = ListOfCards

    def __repr__(self):
        repre = ''
        for card in self.hand:
            repre = repre +  "Card : "+str(card.number)+", color: "+card.color
        return repre

    def __str__(self):
        list_ = []
        for card in self.hand:
            list_.append(card.number)
        return "hand : "+str(list_)+", color: "+self.color

class Deck:

    def __init__(self,
                 size: int,
                 color: str
                 ) -> None:

        self.color = color
        self.size = size
        self.deck = [Card(i,self.color) for i in range(2,self.size)]

    def ShuffleDeck(self):
        np.random.shuffle(self.deck)

    def __eq__(self,
               other
               ) -> bool:

        """Overrides the default implementation"""

        if isinstance(other, Deck):
            loop = 0
            SameCardNumber = True
            SameCardColor = True
            for card in self.deck:
                #print(loop)
                SameCardNumber = (card.number == other.deck[loop].number) & SameCardNumber
                SameCardColor = (card.color == other.deck[loop].color) & SameCardColor
                loop += 1
            print(SameCardColor,SameCardNumber)
            return (SameCardColor & SameCardNumber)
            
        return False

    def __repr__(self):
        repre = ''
        for card in self.deck:
            repre = repre +  "Card : "+str(card.number)+", color: "+card.color
        return repre

    def __str__(self):
        list_ = []
        for card in self.deck:
            list_.append(card.number)
        return "deck : "+str(list_)+", color: "+self.color

class PlayerCopy:

    def __init__(self,
                 size: int,
                 color: str
                 ) -> None :

        self.color = color
        self.size = size
        self.deckInstance = Deck(size,self.color)
        self.deck = self.deckInstance.deck
        print(self.deck)
        self.deckInstance.ShuffleDeck()
        print(self.deck)        
        self.PileUP = [Card(number = 1, color = self.color)]
        self.PileDOWN = [Card(number = self.size, color = self.color)]
        self.Hand = []
        self.PlayedOnOpponnentPiles = False
        

    
    def EmptyPiles(self):
        self.PileUP = [Card(number = 1, color = self.color)]
        self.PileDOWN = [Card(number = self.size, color = self.color)]

    def Draw(self,
             NumberOfCards: int
             ) -> None:

        """
        Draws a number of cards equal to NumberOfCards from the deck (self.Deck).
        If the deck has not enough cards in it, the function draws the whole resting deck.
        """
        if len(self.deckInstance.deck) >= NumberOfCards :
            self.Hand += self.Deck[-NumberOfCards:]
            self.Deck = self.Deck[:-NumberOfCards]
        else :
            self.Hand += self.Deck
            self.Deck = []

    def setup(self):
        Player.ShuffleDeck(self)
        Player.EmptyPiles(self)
        Player.Draw(self,6)

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

    def Draw(self,
             NumberOfCards: int
             ) -> None:

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
        self.SIZE = 60
        self.Player1 = Player(self.SIZE)
        self.Player2 = Player(self.SIZE)
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


class TheGamePlay(Game):

    def __init__(self, width = 1280, height = 720):

        Game.__init__(self)

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.dir_path)
        self.SetupPygame(width,height)

        self.DefineSizes()
        self.DefineColors()
        self.DefineImages()

    def SetupPygame(self, width, height):

        pygame.init()

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.myfont = pygame.font.SysFont("monospace", 30)

        self.FPS = 120 # frames per second setting
        self.clock = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def DefineSizes(self):

        self.WINDOWWIDTH = self.DISPLAYSURF.get_width()
        self.WINDOWHEIGHT = self.DISPLAYSURF.get_height()
        self.HEIGHTCARD = int(self.WINDOWHEIGHT/6)
        self.WIDTHCARD = int(self.HEIGHTCARD*250/350)

               
    def DefineColors(self):
                            #            R    G    B
        self.Colors = { "GRAY"     : (100, 100, 100),
                        "NAVYBLUE" : ( 60,  60, 100),
                        "WHITE"    : (255, 255, 255),
                        "RED"      : (255,   0,   0),
                        "GREEN"    : (  0, 255,   0),
                        "BLUE"     : (  0,   0, 255),
                        "YELLOW"   : (255, 255,   0),
                        "ORANGE"   : (255, 128,   0),
                        "PURPLE"   : (255,   0, 255),
                        "CYAN"     : (  0, 255, 255)}

        self.HIGHLIGHTCOLOR = self.Colors["ORANGE"]

    def DefineImages(self):

        self.Images = { "Player1Img" : pygame.transform.scale(pygame.image.load('./Pictures/Player1.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "Player2Img" : pygame.transform.scale(pygame.image.load('./Pictures/Player2.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "TurnOfImg" : pygame.transform.scale(pygame.image.load('./Pictures/TurnOf.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "BGsurface" : pygame.transform.scale(pygame.image.load('./Pictures/BG1280x720.jpg').convert(),(self.WINDOWWIDTH, self.WINDOWHEIGHT)),
                        "EndOfTurn" : pygame.transform.scale(pygame.image.load('./Pictures/EndOfTurn.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "Quit" : pygame.transform.scale(pygame.image.load('./Pictures/Quit.png'),(int(0.2*self.WINDOWWIDTH), int(0.2*self.WINDOWWIDTH)))}
                        # with or without convert ?? TODO

        #self.Images["BGsurface"].set_alpha(0)


        CardReferenceList = [i for i in range(1,self.SIZE + 1)] + ['THEGAME','DOWN','UP']
        for ColorStr in ['Gold','Silver']:
            for CardReference in CardReferenceList:
                cardImg = pygame.image.load('./Pictures/Cards/'+ColorStr+'Cards/Card_'+str(CardReference)+'.png')
                cardImg = pygame.transform.scale(cardImg, (self.WIDTHCARD, self.HEIGHTCARD))
                self.Images[str(CardReference)+ColorStr] = cardImg

        
                    

    def DisplayActivePlayer(self):

        self.DISPLAYSURF.blit(self.Images["TurnOfImg"], (0,0.4*self.WINDOWHEIGHT))
        if self.ActivePlayer == 1 :   
            self.DISPLAYSURF.blit(self.Images["Player1Img"], (0,0.5*self.WINDOWHEIGHT))
        if self.ActivePlayer == 2 :
            self.DISPLAYSURF.blit(self.Images["Player2Img"], (0,0.5*self.WINDOWHEIGHT))

    def IsOnAPile(self,x,y):
        # TODO change the function with : pile.colidepoint
        if x > (self.WINDOWWIDTH - self.WIDTHCARD)/2 and x < (self.WINDOWWIDTH + self.WIDTHCARD)/2 :
            if y > self.HEIGHTCARD and y < 5*self.HEIGHTCARD :
                return True
            else :
                return False
        else:
            return False

    def leftTopCoordsOfCard(self,i,PlayerSelected,ActivePlayer = True):
        # Convert board coordinates to pixel coordinates
        if PlayerSelected == 1:
            if ActivePlayer :
                x0 = (self.WINDOWWIDTH-len(self.Player1.Hand)*self.WIDTHCARD)//2 
                return (x0+i*self.WIDTHCARD,5*self.HEIGHTCARD)
            elif not ActivePlayer :
                x0 = (self.WINDOWWIDTH-len(self.Player2.Hand)*self.WIDTHCARD)//2
                return (x0+i*self.WIDTHCARD,0)
        elif PlayerSelected == 2:
            if ActivePlayer :   
                x0 = (self.WINDOWWIDTH-len(self.Player2.Hand)*self.WIDTHCARD)//2 
                return (x0+i*self.WIDTHCARD,5*self.HEIGHTCARD)
            elif not ActivePlayer :
                x0 = (self.WINDOWWIDTH-len(self.Player1.Hand)*self.WIDTHCARD)//2
                return (x0+i*self.WIDTHCARD,0)

    def DrawCardOnBoard(self,ColorStr,CardReference,PlayerSelected,LeftTop=None, index=-1 ,Game = None, ActivePlayer = True):
        
        if index>=0:
            Card = self.DISPLAYSURF.blit(self.Images[str(CardReference)+ColorStr], self.leftTopCoordsOfCard(index,PlayerSelected,ActivePlayer=ActivePlayer))
            return Card
        elif index<0:
            Card = self.DISPLAYSURF.blit(self.Images[str(CardReference)+ColorStr], (LeftTop[0], LeftTop[1]))
            return Card

    def MoveACard(self,x,y,CardIndex,PlayerSelected):
        LeftTop = [x-(self.WIDTHCARD//2),y-(self.HEIGHTCARD//2)]
        if PlayerSelected == 1:
            self.DrawCardOnBoard('Gold',self.Player1.Hand[CardIndex],PlayerSelected,LeftTop=LeftTop, index=-1 ,Game = None, ActivePlayer = True)
            pygame.draw.rect(self.DISPLAYSURF, self.HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)
            
        elif PlayerSelected == 2:
            self.DrawCardOnBoard('Silver',self.Player2.Hand[CardIndex],PlayerSelected,LeftTop=LeftTop, index=-1 ,Game = None, ActivePlayer = True)
            pygame.draw.rect(self.DISPLAYSURF, self.HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)

    def GetCardIndex(self,x,y,PlayerSelected):
        if y > self.WINDOWHEIGHT - self.HEIGHTCARD:

            if PlayerSelected == 1:
                L = len(self.Player1.Hand)
            else :
                L = len(self.Player2.Hand)
            
            x0 = (self.WINDOWWIDTH-L*self.WIDTHCARD)//2
            if x > x0 and x < x0 + L*self.WIDTHCARD:
                CardIndex = (x-x0)//self.WIDTHCARD
                return CardIndex
            else :
                return -1
        else :
            return -1            

    def OnACard(self,x,y,PlayerSelected):
        CardIndex = self.GetCardIndex(x,y,PlayerSelected)
        if CardIndex >= 0:
            if PlayerSelected == 1:
                LeftTop = self.leftTopCoordsOfCard(CardIndex,PlayerSelected)
            elif PlayerSelected == 2:
                LeftTop = self.leftTopCoordsOfCard(CardIndex,PlayerSelected)
            pygame.draw.rect(self.DISPLAYSURF, self.HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)
            return True
        else :
            return False

    def DrawBoard(self,PlayerSelected):
        i = 0
        if PlayerSelected == 1:
            ColorStr = 'Gold'
            for number in self.Player1.Hand:
                self.DrawCardOnBoard(ColorStr,number,PlayerSelected,index = i,Game=Game)
                i+=1

            NumberOfCardsOppo = len(self.Player2.Hand)
            for k in range(NumberOfCardsOppo):
                self.DrawCardOnBoard('Silver','THEGAME',PlayerSelected,index = k,Game=Game,ActivePlayer=False)


            ####### DRAWS THE PILES #######

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),4*self.HEIGHTCARD]
            PileDownAP = self.DrawCardOnBoard(ColorStr,self.Player1.PileDOWN[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile Up of ActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),3*self.HEIGHTCARD]
            PileUPAP = self.DrawCardOnBoard(ColorStr,self.Player1.PileUP[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),2*self.HEIGHTCARD]
            PileUPNAP = self.DrawCardOnBoard('Silver',self.Player2.PileUP[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),self.HEIGHTCARD]
            PileDownNAP = self.DrawCardOnBoard('Silver',self.Player2.PileDOWN[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)



            ####### DRAWS THE PILES SYMBOLES #######

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-3*self.WIDTHCARD)/2),4*self.HEIGHTCARD]
            self.DrawCardOnBoard(ColorStr,'DOWN',PlayerSelected,LeftTop)

            # Draws The Pile Up of ActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-3*self.WIDTHCARD)/2),3*self.HEIGHTCARD]
            self.DrawCardOnBoard(ColorStr,'UP',PlayerSelected,LeftTop)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH+self.WIDTHCARD)/2),2*self.HEIGHTCARD]
            self.DrawCardOnBoard('Silver','UP',PlayerSelected,LeftTop)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH+self.WIDTHCARD)/2),self.HEIGHTCARD]
            self.DrawCardOnBoard('Silver','DOWN',PlayerSelected,LeftTop)

            ####### DRAWS THE DECKS #######

            ## DRAWS THE DECK OF ACTIVEPLAYER
            LeftTop = [int((self.WINDOWWIDTH-5*self.WIDTHCARD)/2),int(3.5*self.HEIGHTCARD)]
            APDeck = self.DrawCardOnBoard(ColorStr,'THEGAME',PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["GRAY"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            ## DRAWS THE DECK OF NONACTIVEPLAYER
            LeftTop = [int((self.WINDOWWIDTH + 3*self.WIDTHCARD)/2),int(1.5*self.HEIGHTCARD)]
            NAPDeck = self.DrawCardOnBoard('Silver','THEGAME',PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["GRAY"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

        elif PlayerSelected == 2:
            ColorStr = 'Silver'
            for number in self.Player2.Hand:
                self.DrawCardOnBoard('Silver',number,PlayerSelected,index = i,Game=Game)
                i+=1

            NumberOfCardsOppo = len(self.Player1.Hand)
            for k in range(NumberOfCardsOppo):
                self.DrawCardOnBoard('Gold','THEGAME',PlayerSelected,index = k,Game=Game,ActivePlayer=False)

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),4*self.HEIGHTCARD]
            PileDownAP = self.DrawCardOnBoard(ColorStr,self.Player2.PileDOWN[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of ActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),3*self.HEIGHTCARD]
            PileUPAP = self.DrawCardOnBoard(ColorStr,self.Player2.PileUP[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),2*self.HEIGHTCARD]
            PileUPNAP = self.DrawCardOnBoard('Gold',self.Player1.PileUP[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),self.HEIGHTCARD]
            PileDownNAP = self.DrawCardOnBoard('Gold',self.Player1.PileDOWN[-1:][0],PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)


            ####### DRAWS THE PILES SYMBOLES #######

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-3*self.WIDTHCARD)/2),4*self.HEIGHTCARD]
            self.DrawCardOnBoard(ColorStr,'DOWN',PlayerSelected,LeftTop)


            # Draws The Pile Up of ActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-3*self.WIDTHCARD)/2),3*self.HEIGHTCARD]
            self.DrawCardOnBoard(ColorStr,'UP',PlayerSelected,LeftTop)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH+self.WIDTHCARD)/2),2*self.HEIGHTCARD]
            self.DrawCardOnBoard('Gold','UP',PlayerSelected,LeftTop)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH+self.WIDTHCARD)/2),self.HEIGHTCARD]
            self.DrawCardOnBoard('Gold','DOWN',PlayerSelected,LeftTop)

            ####### DRAWS THE DECKS #######

            ## DRAWS THE DECK OF ACTIVEPLAYER
            LeftTop = [int((self.WINDOWWIDTH-5*self.WIDTHCARD)/2),int(3.5*self.HEIGHTCARD)]
            APDeck = self.DrawCardOnBoard(ColorStr,'THEGAME',PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["GRAY"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            ## DRAWS THE DECK OF NONACTIVEPLAYER
            LeftTop = [int((self.WINDOWWIDTH + 3*self.WIDTHCARD)/2),int(1.5*self.HEIGHTCARD)]
            NAPDeck = self.DrawCardOnBoard('Gold','THEGAME',PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["GRAY"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)
        
        return PileDownAP,PileUPAP,PileDownNAP,PileUPNAP,APDeck,NAPDeck





