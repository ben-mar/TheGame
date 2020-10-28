import os
import copy
import numpy as np
import pygame

def CreateListOfCards(ListOfNumbers: list,
                      color: str
                      ) -> list:

    return [Card(i,color) for i in ListOfNumbers]

class Card:

    def __init__(self,
                 number : int,
                 color: str
                 ) -> None: 
        if not isinstance(number, int):
            raise("The number for the initialisation is not an int")
        if not isinstance(color, str):
            raise("The color for the initialisation is not a str")
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
                 ListOfNumbers: list,
                 color: str
                 ) -> None:

        if len(ListOfNumbers) != 0:
            for number in ListOfNumbers:
                if not isinstance(number, int):
                    Exception("The list is not only composed of integers !")

        self.color = color        
        self.hand = [Card(i,self.color) for i in ListOfNumbers]

    def __repr__(self
                ) -> str :
        repre = ''
        for card in self.hand:
            repre = repre +  "Card : "+str(card.number)+", color: "+card.color
        return repre

    def __str__(self
                ) -> str :
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
                SameCardNumber = (card.number == other.deck[loop].number) & SameCardNumber
                SameCardColor = (card.color == other.deck[loop].color) & SameCardColor
                loop += 1
            print(SameCardColor,SameCardNumber)
            return (SameCardColor & SameCardNumber)
            
        return False

    def __repr__(self
                 ) -> str :

        repre = ''
        for card in self.deck:
            repre = repre +  "Card : "+str(card.number)+", color: "+card.color
        return repre

    def __str__(self
                ) -> str :

        list_ = []
        for card in self.deck:
            list_.append(card.number)
        return "deck : "+str(list_)+", color: "+self.color

class Player:

    def __init__(self,
                 size: int,
                 color: str
                 ) -> None :

        self.color = color
        self.size = size
        self.deckInstance = Deck(size,self.color)
        self.deck = self.deckInstance.deck
        self.PileUP = [Card(number = 1, color = self.color)]
        self.PileDOWN = [Card(number = self.size, color = self.color)]
        self.HandInstance = Hand([],self.color)
        self.hand = self.HandInstance.hand
        self.PlayedOnOpponnentPiles = False
        self.GameOver = False
        

    def EmptyPiles(self
                   ) -> None :
        self.PileUP = [Card(number = 1, color = self.color)]
        self.PileDOWN = [Card(number = self.size, color = self.color)]

    def Draw(self,
             NumberOfCards: int
             ) -> None:

        """
        Draws a number of cards equal to NumberOfCards from the deck (self.Deck).
        If the deck has not enough cards in it, the function draws the whole resting deck.
        """
        if len(self.deck) >= NumberOfCards :
            self.hand += self.deck[-NumberOfCards:]
            self.deck = self.deck[:-NumberOfCards]
        else :
            self.hand += self.deck
            self.deck = []

    def setup(self
              ) -> None :

        self.deckInstance.ShuffleDeck()
        self.EmptyPiles()
        self.Draw(6)


class Game:

    def __init__(self
                 ) -> None :

        self.size = 60
        self.color1 = 'Gold'
        self.color2 = 'Silver'
        self.Player1 = Player(self.size,self.color1)
        self.Player2 = Player(self.size,self.color2)
        self.ActivePlayer = 1

        self.Player1.setup()
        self.Player2.setup()

        self.Piles = {"1UP" : self.Player1.PileUP,
                    "1DOWN" : self.Player1.PileDOWN,
                    "2UP" : self.Player2.PileUP,
                    "2DOWN" : self.Player2.PileDOWN}

        self.PlayedOnOpponnentPiles = [False,False]
        self.PlayedOnOpponnentPilesPlayer1 = self.PlayedOnOpponnentPiles[0]
        self.PlayedOnOpponnentPilesPlayer2 = self.PlayedOnOpponnentPiles[1] 

        self.PlayedThisTurnPlayer1 = []
        self.PlayedThisTurnPlayer2 = []

        
    def DeepcopyForCheckIfLoose(self
                                ) -> None :

        """
        Creates deepcopy of the piles and hands for the CheckIfLoose function to check all situations possible without impacting the real game.
        """

        self.CopyPlayer1PileUP = copy.deepcopy(self.Player1.PileUP)
        self.CopyPlayer1PileDOWN = copy.deepcopy(self.Player1.PileDOWN)
        self.CopyPlayer1Hand = copy.deepcopy(self.Player1.hand)
        self.CopyPlayer2PileUP = copy.deepcopy(self.Player2.PileUP)
        self.CopyPlayer2PileDOWN = copy.deepcopy(self.Player2.PileDOWN)
        self.CopyPlayer2Hand = copy.deepcopy(self.Player2.hand)

        self.CopyPlayedThisTurnPlayer1 = copy.deepcopy(self.PlayedThisTurnPlayer1)
        self.CopyPlayedThisTurnPlayer2 = copy.deepcopy(self.PlayedThisTurnPlayer2)
        self.CopyPlayedOnOpponnentPiles = copy.deepcopy(self.PlayedOnOpponnentPiles)     

    def LoadDeepCopyForCheckIfLoose(self
                                    ) -> None :

        """
        Load deepcopy made by the function : DeepCopyForCheckIfLoose 

        The goal here is to load the backup lists and write on them without modifying the backup list.
        This is why the shallow copy is performed, to have the possibility to update the loaded list without modifying the state of the Game 

        """
        self.Player1.PileUP = copy.copy(self.CopyPlayer1PileUP)
        self.Player1.PileDOWN = copy.copy(self.CopyPlayer1PileDOWN)
        self.Player1.hand = copy.copy(self.CopyPlayer1Hand)
        self.Player2.PileUP = copy.copy(self.CopyPlayer2PileUP)
        self.Player2.PileDOWN = copy.copy(self.CopyPlayer2PileDOWN)
        self.Player2.hand = copy.copy(self.CopyPlayer2Hand)
        self.Piles = {"1UP" : self.Player1.PileUP,
                    "1DOWN" : self.Player1.PileDOWN,
                    "2UP" : self.Player2.PileUP,
                    "2DOWN" : self.Player2.PileDOWN}

        self.PlayedThisTurnPlayer1 = copy.copy(self.CopyPlayedThisTurnPlayer1)            
        self.PlayedThisTurnPlayer2 = copy.copy(self.CopyPlayedThisTurnPlayer2)          
        self.PlayedOnOpponnentPiles  = copy.copy(self.CopyPlayedOnOpponnentPiles)       


    def rule(self,
             Pile : str,
             card : Card,
             PlayOnHisOwnPile : bool,
             verbosity = True
             ) -> bool :

        """
        Returns a bool corresponding to the rule applied according to the selected pile
        """
        PileDirection = Pile[1:]
        if PlayOnHisOwnPile & (PileDirection == 'UP'):
            return (self.Piles[Pile][-1:][0].number < card.number ) or\
                   (self.Piles[Pile][-1:][0].number == card.number + 10)  
        elif PlayOnHisOwnPile & (PileDirection == 'DOWN'):    
            return (self.Piles[Pile][-1:][0].number > card.number ) or\
                   (self.Piles[Pile][-1:][0].number == card.number - 10)    
        elif (not PlayOnHisOwnPile) & (not self.PlayedOnOpponnentPiles[self.ActivePlayer-1]) & (PileDirection == 'UP'):   
            return (self.Piles[Pile][-1:][0].number > card.number)
        elif (not PlayOnHisOwnPile) & (not self.PlayedOnOpponnentPiles[self.ActivePlayer-1]) & (PileDirection == 'DOWN'):    
            return (self.Piles[Pile][-1:][0].number < card.number)
        elif self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:         
            if verbosity:
                print("Player {} has already played on opponents piles this turn !".format(self.ActivePlayer))
            return False
        else :
            print("chelou, you're not supposed to be here !")

    def CheckAction(self,
                    Pile: str,
                    card: Card,
                    PlayerSelected : int,
                    verbosity = True
                    ) -> bool :
        """
        Returns True if the rules allow ActivePlayer to put the card N° Number on PileName 'UP'/'DOWN' bellonging to player N° PileIndex
        Returns False if not
        """

        # check if it's the turn of the  Active player
        if PlayerSelected == self.ActivePlayer:

            # should take into account the color of cards with the active player: on peut paos mettre une carte Silver si on est le joueur 1 puisqu'on est le joueur Gold !!!
            #assert(card.color == )

            if self.ActivePlayer == int(Pile[0]):
                PlayOnHisOwnPile = True
            else :
                PlayOnHisOwnPile = False

            return self.rule(Pile,card,PlayOnHisOwnPile,verbosity=verbosity)

        else :
            print("It's not your turn !")
    
    def Put(self,
            Pile: str,
            card : Card,
            PlayerSelected : int
            ) -> int :

        # TODO change related to color of the card you're trying to put !!
        if self.CheckAction(Pile,card,PlayerSelected,verbosity=True):
            if self.ActivePlayer != int(Pile[0]):
                self.PlayedOnOpponnentPiles[self.ActivePlayer-1] = True
            self.Piles[Pile].append(card) 
            return 0
        else:
            print('Not possible to Put number {} on the Pile {} of the player {}'.format(card.number,Pile[1:],Pile[0]))
            return 1

    def Play(self,
             Pile: str,
             card: Card,
             PlayerSelected : int,
             verbosity = True
             ) -> None :
        """
        This function plays the card "card" on the pile "PileName"
        """

        if self.ActivePlayer == 1:
            if card in self.Player1.hand :
                err = self.Put(Pile,card,PlayerSelected)
                if err == 0 :
                    self.Player1.hand.remove(card)
                    self.PlayedThisTurnPlayer1.append((card,Pile))
                    if verbosity:
                        print('Played !')
        elif self.ActivePlayer == 2:
            if card in self.Player2.hand :
                err = self.Put(Pile,card,PlayerSelected)
                if err == 0 :
                    self.Player2.hand.remove(card)      
                    self.PlayedThisTurnPlayer2.append((card,Pile))  
                    if verbosity:   
                        print('Played !')

    def Concede(self
                ) -> None :

        if self.ActivePlayer == 1 :
            self.Player1.GameOver = True
        elif self.ActivePlayer == 2 :
            self.Player2.GameOver = True

    def ChangeActivePlayer(self
                           ) -> None :

        if self.ActivePlayer == 1 :
            self.ActivePlayer = 2
        elif self.ActivePlayer == 2 :
            self.ActivePlayer = 1
    
    def DrawEndOfTurn(self
                      ) -> None :

        if self.ActivePlayer == 1 :
            if self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                CardsInHandPlayer1 = len(self.Player1.hand)
                self.Player1.Draw(6-CardsInHandPlayer1)
            else :
                self.Player1.Draw(2)
        elif self.ActivePlayer == 2 :
            if self.PlayedOnOpponnentPiles[self.ActivePlayer-1]:
                CardsInHandPlayer2 = len(self.Player2.hand)
                self.Player2.Draw(6-CardsInHandPlayer2)
            else :
                self.Player2.Draw(2)

    def HasTheRightToEndTurn(self
                             ) -> int :

        if self.ActivePlayer == 1:
            if len(self.PlayedThisTurnPlayer1) < 2:
                return 0 
            else:
                return 1
        if self.ActivePlayer == 2:
            if len(self.PlayedThisTurnPlayer2) < 2:
                return 0 
            else:
                return 1

    def EndOfTurn(self
                  ) -> int :

        if self.HasTheRightToEndTurn() == 1: 
            self.PlayedThisTurnPlayer1 = []
            self.PlayedThisTurnPlayer2 = []
            if (self.Player1.deck == []) and (self.Player1.hand == []):
                self.Player2.GameOver = True # The Player 1 has won the game
            elif (self.Player2.deck == []) and (self.Player2.hand == []):
                self.Player1.GameOver = True # The Player 2 has won the game
            Game.DrawEndOfTurn(self)
            self.PlayedOnOpponnentPiles = [False,False]
            Game.ChangeActivePlayer(self)
            return 1
        else:
            return 0


    def Display(self
                ) -> None :

        print("Turn of Player {} \n".format(self.ActivePlayer))
        print("Pile UP Player 1 : {}".format(self.Player1.PileUP))
        print("Pile DOWN Player 1 : {} \n".format(self.Player1.PileDOWN))
        print("Pile UP Player 2 : {}".format(self.Player2.PileUP))
        print("Pile DOWN Player 2 : {} \n".format(self.Player2.PileDOWN))
        print("Hand Player 1 {} ".format(self.Player1.hand))
        print("Hand Player 2 {} \n \n \n ".format(self.Player2.hand))
    
    # def INPUT(self):
    #     Number = int(input("What card do you want to play ?"))
    #     if Number ==  0:
    #         Game.Concede(self)
    #         return
    #     if Number == -1:
    #         Game.EndOfTurn(self)
    #         return
    #     PileIndex = int(input("On which Player's Pile do you want to play (Player 1 or 2) ?"))
    #     PileName = str(input("Pile Up or down ?")).upper()
    #     Game.Play(self,PileIndex,Number,PileName)

    def Undo(self
             ) -> None :

        """
        undo the last action of playing a card
        """
        if self.ActivePlayer == 1:
            if len(self.PlayedThisTurnPlayer1) > 0:
                LastPlayed = self.PlayedThisTurnPlayer1[-1]
                LastPlayedPile = LastPlayed[1]
                LastPlayedCard = LastPlayed[0]
                self.Piles[LastPlayedPile].remove(LastPlayedCard)

                self.PlayedThisTurnPlayer1.pop()
                self.Player1.hand.append(LastPlayedCard)                
                print('Undone !')
        else:
            if len(self.PlayedThisTurnPlayer2) > 0:
                LastPlayed = self.PlayedThisTurnPlayer2[-1]
                LastPlayedPile = LastPlayed[1]
                LastPlayedCard = LastPlayed[0]
                self.Piles[LastPlayedPile].remove(LastPlayedCard)
                self.PlayedThisTurnPlayer2.pop()
                self.Player2.hand.append(LastPlayedCard)
                print('Undone !')

    def CheckIfLoose(self,
                     PlayerSelected : int
                     ) -> bool :
        """
        Tests all the play possibilities at the beginning of the turn
        and change the status of the variable Player.GameOver accordingly (becomes true if the player as indeed lost the game)

        The player looses the game when it cannot play on his piles, or when he cannot play 2 cards on his piles and he cannot play on opponent piles

        It also returns True if the player has lost the game, False otherwise
        """
        PilesList = ['1UP','1DOWN','2UP','2DOWN']
        self.DeepcopyForCheckIfLoose() # we create the backup

        if self.ActivePlayer == 1: # checks the play possibilities of the player 1
            for card in self.Player1.hand:
                for pile in PilesList:
                    self.LoadDeepCopyForCheckIfLoose() # we load the backup
                    if self.CheckAction(pile,card,PlayerSelected,verbosity=False):
                        self.Play(pile,card,PlayerSelected,verbosity=False)
                        for card2 in self.Player1.hand:
                            for pile2 in PilesList:                         
                                if self.CheckAction(pile2,card2,PlayerSelected,verbosity=False):
                                    # the player hasn't lost the game
                                    self.LoadDeepCopyForCheckIfLoose()  
                                    print("one possible play is : ",card.number," on pile ",pile[1:]," of player ",pile[0])
                                    print("then : ",card2.number," on pile ",pile2[1:]," of player ",pile2[0])
                                    return False

            self.Player1.GameOver = True
            return True

        else: # checks the play possibilities of the player 2
            for card in self.Player2.hand:
                for pile in PilesList:
                    self.LoadDeepCopyForCheckIfLoose() # we load the backup
                    if self.CheckAction(pile,card,PlayerSelected,verbosity=False):
                        self.Play(pile,card,PlayerSelected,verbosity=False)
                        for card2 in self.Player2.hand:
                            for pile2 in PilesList:                         
                                if self.CheckAction(pile2,card2,PlayerSelected,verbosity=False):
                                    # the player hasn't lost the game
                                    self.LoadDeepCopyForCheckIfLoose()  
                                    print("One possible play is : ",card.number," on pile ",pile[1:]," of player ",pile[0])
                                    print("followed by : ",card2.number," on pile ",pile2[1:]," of player ",pile2[0])
                                    return False
            
            self.Player2.GameOver = True
            return True

   

class TheGamePlay(Game):

    def __init__(self,
                 width :int = 1280,
                 height :int = 720
                 )-> None:

        Game.__init__(self)

        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(self.dir_path)
        self.SetupPygame(width,height)

        self.DefineSizes()
        self.DefineColors()
        self.DefineImages()

    def SetupPygame(self, 
                    width: int,
                    height: int
                    ) -> None:

        pygame.init()

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        self.myfont = pygame.font.SysFont("monospace", 35,bold=True)

        self.FPS = 120 # frames per second setting
        self.clock = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    def DefineSizes(self
                    ) -> None :

        self.WINDOWWIDTH = self.DISPLAYSURF.get_width()
        self.WINDOWHEIGHT = self.DISPLAYSURF.get_height()
        self.HEIGHTCARD = int(self.WINDOWHEIGHT/6)
        self.WIDTHCARD = int(self.HEIGHTCARD*250/350)

               
    def DefineColors(self
                     ) -> None :

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
                        "CYAN"     : (  0, 255, 255),
                        "SILVER"   : (169, 169, 169),
                        "GOLD"     : (218, 165,  32)}

        self.HIGHLIGHTCOLOR = self.Colors["ORANGE"]

    def DefineImages(self
                     ) -> None :

        self.Images = { "Player1Img" : pygame.transform.scale(pygame.image.load('./Pictures/Player1.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "Player2Img" : pygame.transform.scale(pygame.image.load('./Pictures/Player2.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "TurnOfImg" : pygame.transform.scale(pygame.image.load('./Pictures/TurnOf.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "BGsurface" : pygame.transform.scale(pygame.image.load('./Pictures/BG1280x720.jpg').convert(),(self.WINDOWWIDTH, self.WINDOWHEIGHT)),
                        "EndOfTurn" : pygame.transform.scale(pygame.image.load('./Pictures/EndOfTurn.png'),(int(0.2*self.WINDOWWIDTH), int(0.1*self.WINDOWHEIGHT))),
                        "Quit" : pygame.transform.scale(pygame.image.load('./Pictures/Quit.png'),(int(0.2*self.WINDOWWIDTH), int(0.2*self.WINDOWWIDTH))),
                        "NoRightEOT" : pygame.transform.scale(pygame.image.load('./Pictures/NoRightEOT.png'),(int(0.8*self.WINDOWWIDTH), int(0.5*self.WINDOWHEIGHT))),
                        "YouWonGold" : pygame.transform.scale(pygame.image.load('./Pictures/YouWonGold.png'),(int(0.1*self.WINDOWWIDTH), int(0.06*self.WINDOWHEIGHT))),
                        "YouLostGold" : pygame.transform.scale(pygame.image.load('./Pictures/YouLostGold.png'),(int(0.1*self.WINDOWWIDTH), int(0.06*self.WINDOWHEIGHT))),
                        "YouWonSilver" : pygame.transform.scale(pygame.image.load('./Pictures/YouWonSilver.png'),(int(0.1*self.WINDOWWIDTH), int(0.06*self.WINDOWHEIGHT))),
                        "YouLostSilver" : pygame.transform.scale(pygame.image.load('./Pictures/YouLostSilver.png'),(int(0.1*self.WINDOWWIDTH), int(0.06*self.WINDOWHEIGHT)))}
                        # with or without convert ?? TODO

        #self.Images["BGsurface"].set_alpha(0)
        CardReferenceList = [i for i in range(1,self.size + 1)] + ['THEGAME','DOWN','UP']
        for ColorStr in ['Gold','Silver']:
            for CardReference in CardReferenceList:
                cardImg = pygame.image.load('./Pictures/Cards/'+ColorStr+'Cards/Card_'+str(CardReference)+'.png')
                cardImg = pygame.transform.scale(cardImg, (self.WIDTHCARD, self.HEIGHTCARD))
                self.Images[str(CardReference)+ColorStr] = cardImg

    def DisplayActivePlayer(self
                            ) -> None :

        self.DISPLAYSURF.blit(self.Images["TurnOfImg"], (0,0.4*self.WINDOWHEIGHT))
        if self.ActivePlayer == 1 :   
            self.DISPLAYSURF.blit(self.Images["Player1Img"], (0,0.5*self.WINDOWHEIGHT))
        if self.ActivePlayer == 2 :
            self.DISPLAYSURF.blit(self.Images["Player2Img"], (0,0.5*self.WINDOWHEIGHT))

    def IsOnAPile(self,
                  x:int,
                  y:int
                  ) -> bool :

        # TODO change the function with : pile.colidepoint
        if x > (self.WINDOWWIDTH - self.WIDTHCARD)/2 and x < (self.WINDOWWIDTH + self.WIDTHCARD)/2 :
            if y > self.HEIGHTCARD and y < 5*self.HEIGHTCARD :
                return True
            else :
                return False
        else:
            return False

    def leftTopCoordsOfCard(self,
                            i: int,
                            PlayerSelected: int,
                            ActivePlayer = True
                            ) -> tuple :

        # Convert board coordinates to pixel coordinates
        if PlayerSelected == 1:
            if ActivePlayer :
                x0 = (self.WINDOWWIDTH-len(self.Player1.hand)*self.WIDTHCARD)//2 
                return (x0+i*self.WIDTHCARD,5*self.HEIGHTCARD)
            elif not ActivePlayer :
                x0 = (self.WINDOWWIDTH-len(self.Player2.hand)*self.WIDTHCARD)//2
                return (x0+i*self.WIDTHCARD,0)
        elif PlayerSelected == 2:
            if ActivePlayer :   
                x0 = (self.WINDOWWIDTH-len(self.Player2.hand)*self.WIDTHCARD)//2 
                return (x0+i*self.WIDTHCARD,5*self.HEIGHTCARD)
            elif not ActivePlayer :
                x0 = (self.WINDOWWIDTH-len(self.Player1.hand)*self.WIDTHCARD)//2
                return (x0+i*self.WIDTHCARD,0)

    def DrawCardOnBoard(self,
                        ColorStr : str,
                        CardReference : int,
                        PlayerSelected : int,
                        LeftTop=None,
                        index=-1 ,
                        ActivePlayer = True
                        ):
        
        if index>=0:
            card = self.DISPLAYSURF.blit(self.Images[str(CardReference)+ColorStr], self.leftTopCoordsOfCard(index,PlayerSelected,ActivePlayer=ActivePlayer))
            return card
        elif index<0:
            card = self.DISPLAYSURF.blit(self.Images[str(CardReference)+ColorStr], (LeftTop[0], LeftTop[1]))
            return card
            
    def MoveACard(self,
                  x : int,
                  y : int,
                  CardIndex : int,
                  PlayerSelected : int
                  ) -> None:

        LeftTop = [x-(self.WIDTHCARD//2),y-(self.HEIGHTCARD//2)]
        if PlayerSelected == 1:
            self.DrawCardOnBoard('Gold',self.Player1.hand[CardIndex].number,PlayerSelected,LeftTop=LeftTop, index=-1 ,ActivePlayer = True)
            pygame.draw.rect(self.DISPLAYSURF, self.HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)
            
        elif PlayerSelected == 2:
            self.DrawCardOnBoard('Silver',self.Player2.hand[CardIndex].number,PlayerSelected,LeftTop=LeftTop, index=-1 , ActivePlayer = True)
            pygame.draw.rect(self.DISPLAYSURF, self.HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)

    def GetCardIndex(self,
                     x : int,
                     y : int,
                     PlayerSelected : int
                     ) -> int :

        if y > self.WINDOWHEIGHT - self.HEIGHTCARD:

            if PlayerSelected == 1:
                L = len(self.Player1.hand)
            else :
                L = len(self.Player2.hand)
            
            x0 = (self.WINDOWWIDTH-L*self.WIDTHCARD)//2
            if x > x0 and x < x0 + L*self.WIDTHCARD:
                CardIndex = (x-x0)//self.WIDTHCARD
                return CardIndex
            else :
                return -1
        else :
            return -1            

    def OnACard(self,
                x : int,
                y : int,
                PlayerSelected : int
                ) -> bool :

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

    def DrawBoard(self,
                  PlayerSelected: int
                  ) -> tuple:
        i = 0
        if PlayerSelected == 1:
            ColorStr = 'Gold'
            for card in self.Player1.hand:
                self.DrawCardOnBoard(card.color,card.number,PlayerSelected,index = i)
                i+=1

            NumberOfCardsOppo = len(self.Player2.hand)
            for k in range(NumberOfCardsOppo):
                self.DrawCardOnBoard('Silver','THEGAME',PlayerSelected,index = k,ActivePlayer=False)

            ####### DRAWS THE PILES #######

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),4*self.HEIGHTCARD]
            PileDownAP = self.DrawCardOnBoard(self.Player1.PileDOWN[-1:][0].color,self.Player1.PileDOWN[-1:][0].number,PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile Up of ActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),3*self.HEIGHTCARD]
            PileUPAP = self.DrawCardOnBoard(self.Player1.PileUP[-1:][0].color,self.Player1.PileUP[-1:][0].number,PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),2*self.HEIGHTCARD]
            PileUPNAP = self.DrawCardOnBoard(self.Player2.PileUP[-1:][0].color,self.Player2.PileUP[-1:][0].number,PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),self.HEIGHTCARD]
            PileDownNAP = self.DrawCardOnBoard(self.Player2.PileDOWN[-1:][0].color,self.Player2.PileDOWN[-1:][0].number,PlayerSelected,LeftTop)
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
            for card in self.Player2.hand:
                self.DrawCardOnBoard(card.color,card.number,PlayerSelected,index = i)
                i+=1

            NumberOfCardsOppo = len(self.Player1.hand)
            for k in range(NumberOfCardsOppo):
                self.DrawCardOnBoard('Gold','THEGAME',PlayerSelected,index = k,ActivePlayer=False)

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),4*self.HEIGHTCARD]
            PileDownAP = self.DrawCardOnBoard(self.Player2.PileDOWN[-1:][0].color,self.Player2.PileDOWN[-1:][0].number,PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of ActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),3*self.HEIGHTCARD]
            PileUPAP = self.DrawCardOnBoard(self.Player2.PileUP[-1:][0].color,self.Player2.PileUP[-1:][0].number,PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),2*self.HEIGHTCARD]
            PileUPNAP = self.DrawCardOnBoard(self.Player1.PileUP[-1:][0].color,self.Player1.PileUP[-1:][0].number,PlayerSelected,LeftTop)
            pygame.draw.rect(self.DISPLAYSURF, self.Colors["WHITE"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((self.WINDOWWIDTH-self.WIDTHCARD)/2),self.HEIGHTCARD]
            PileDownNAP = self.DrawCardOnBoard(self.Player1.PileDOWN[-1:][0].color,self.Player1.PileDOWN[-1:][0].number,PlayerSelected,LeftTop)
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
        
        return (PileDownAP,PileUPAP,PileDownNAP,PileUPNAP,APDeck,NAPDeck)