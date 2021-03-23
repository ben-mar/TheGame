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
        self.deckInstance = Deck(self.size,self.color) # in order to be able to shuffle the deck
        self.deck = self.deckInstance.deck
        self.PileUP = [Card(number = 1, color = self.color)]
        self.PileDOWN = [Card(number = self.size, color = self.color)]
        HandInstance = Hand([],self.color)
        self.hand = HandInstance.hand
        

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
        self.color = {'P1' : 'Gold', 'P2' : 'Silver'}
        self.Player1 = Player(self.size,self.color['P1'])
        self.Player2 = Player(self.size,self.color['P2'])
        self.ActivePlayer = 1

        self.Player1.setup()
        self.Player2.setup()

        self.Piles = {"P1_UP" : self.Player1.PileUP,
                    "P1_DOWN" : self.Player1.PileDOWN,
                    "P2_UP" : self.Player2.PileUP,
                    "P2_DOWN" : self.Player2.PileDOWN}

        self.Hands = {'P1' : self.Player1.hand, 'P2' : self.Player2.hand}
        self.Decks = {'P1' : self.Player1.deck, 'P2' : self.Player2.deck}
        self.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.PlayedThisTurn = {'P1' : [], 'P2' : []}
        self.GameOver = {'P1': False,'P2': False }

        
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

        self.CopyPlayedThisTurn = copy.deepcopy(self.PlayedThisTurn)
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
        self.Piles = {"P1_UP" : self.Player1.PileUP,
                    "P1_DOWN" : self.Player1.PileDOWN,
                    "P2_UP" : self.Player2.PileUP,
                    "P2_DOWN" : self.Player2.PileDOWN}
        self.Hands = {'P1' : self.Player1.hand, 'P2' : self.Player2.hand}


        # WARNING: However if the values associated with the dictionary keys are iterable objects,
        #  such as lists for example, then if one of the dictionary is modified the other one will be too (it is called a shallow copy)
        # This is why the copy is made key by key
        self.PlayedThisTurn['P1'] = copy.copy(self.CopyPlayedThisTurn['P1'])
        self.PlayedThisTurn['P2'] = copy.copy(self.CopyPlayedThisTurn['P2'])               
        self.PlayedOnOpponnentPiles['P1']  = copy.copy(self.CopyPlayedOnOpponnentPiles['P1'])       
        self.PlayedOnOpponnentPiles['P2']  = copy.copy(self.CopyPlayedOnOpponnentPiles['P2'])  

    def SortHand(self,
                 index : int,
                 CardToSort : Card,
                 PlayerSelected : int
                 ) -> None :
        """
        Sorts the hand
        """

        self.Hands['P'+str(PlayerSelected)].remove(CardToSort)
        self.Hands['P'+str(PlayerSelected)].insert(index,CardToSort)

    def rule(self,
             Pile : str,
             card : Card,
             PlayOnHisOwnPile : bool,
             verbosity = True
             ) -> bool :

        """
        Returns a bool corresponding to the rule applied according to the selected pile
        """
        PileDirection = Pile[3:]
        if PlayOnHisOwnPile & (PileDirection == 'UP'):
            return (self.Piles[Pile][-1].number < card.number ) or\
                   (self.Piles[Pile][-1].number == card.number + 10)  
        elif PlayOnHisOwnPile & (PileDirection == 'DOWN'):  
            return (self.Piles[Pile][-1].number > card.number ) or\
                   (self.Piles[Pile][-1].number == card.number - 10)    
        elif (not PlayOnHisOwnPile) & (not self.PlayedOnOpponnentPiles['P' + str(self.ActivePlayer)]) & (PileDirection == 'UP'):   
            return (self.Piles[Pile][-1].number > card.number)
        elif (not PlayOnHisOwnPile) & (not self.PlayedOnOpponnentPiles['P' + str(self.ActivePlayer)]) & (PileDirection == 'DOWN'):    
            return (self.Piles[Pile][-1].number < card.number)
        elif self.PlayedOnOpponnentPiles['P' + str(self.ActivePlayer)]:         
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
        Returns False if not.
        """

        # check if it's the turn of the  Active player
        if PlayerSelected == self.ActivePlayer:

            # should take into account the color of cards with the active player: on peut paos mettre une carte Silver si on est le joueur 1 puisqu'on est le joueur Gold !!!
            #assert(card.color == )

            if self.ActivePlayer == int(Pile[1]):
                PlayOnHisOwnPile = True
            else :
                PlayOnHisOwnPile = False
            return self.rule(Pile,card,PlayOnHisOwnPile,verbosity=verbosity)
        else :
            print("It's not your turn !")
            return False
    
    def Put(self,
            Pile: str,
            card : Card,
            PlayerSelected : int,
            verbosity : str = True
            ) -> int :

        # TODO change related to color of the card you're trying to put !!
        if self.CheckAction(Pile,card,PlayerSelected,verbosity=True):
            if self.ActivePlayer != int(Pile[1]):
                self.PlayedOnOpponnentPiles['P' + str(self.ActivePlayer)] = True
            self.Piles[Pile].append(card) 
            return 0
        else:
            if verbosity:
                print('Not possible to Put number {} on the Pile {} of the player {}'.format(card.number,Pile[3:],Pile[1]))
            return 1

    def Play(self,
             Pile: str,
             card: Card,
             PlayerSelected : int,
             verbosity :str = True
             ) -> None :
        """
        This function plays the card "card" on the pile "PileName"
        """

        if card in self.Hands['P' + str(self.ActivePlayer)] :
            err = self.Put(Pile,card,PlayerSelected,verbosity)
            if err == 0 :
                self.Hands['P' + str(self.ActivePlayer)].remove(card)
                self.PlayedThisTurn['P' + str(self.ActivePlayer)].append((card,Pile))
                if verbosity:
                    print('Played !')
                return True
            else:
                if verbosity:
                    print('Not Played')
                return False
        else:
            if verbosity:
                print('Not in hand !')
            return False


    def Concede(self
                ) -> None :

        if self.ActivePlayer == 1 :
            self.GameOver['P1'] = True
        else :
            self.GameOver['P2'] = True

    def ChangeActivePlayer(self
                           ) -> None :

        if self.ActivePlayer == 1 :
            self.ActivePlayer = 2
        else :
            self.ActivePlayer = 1

    
    def DrawEndOfTurn(self
                      ) -> None :

        if self.ActivePlayer == 1 :
            if self.PlayedOnOpponnentPiles['P'+str(self.ActivePlayer)]:
                CardsInHandPlayer1 = len(self.Hands['P1'])
                self.Player1.Draw(6-CardsInHandPlayer1)
            else :
                self.Player1.Draw(2)
        elif self.ActivePlayer == 2 :
            if self.PlayedOnOpponnentPiles['P'+str(self.ActivePlayer)]:
                CardsInHandPlayer2 = len(self.Hands['P2'])
                self.Player2.Draw(6-CardsInHandPlayer2)
            else :
                self.Player2.Draw(2)
        else :
            print("Pb : ActivePlayer = ",self.ActivePlayer )

    def HasTheRightToEndTurn(self
                             ) -> int :

        if len(self.PlayedThisTurn['P'+str(self.ActivePlayer)]) < 2:
            return 0 
        else:
            return 1


    def EndOfTurn(self
                  ) -> int :

        if self.HasTheRightToEndTurn() == 1: 
            self.PlayedThisTurn = {'P1' : [], 'P2' : []}
            if (self.Player1.deck == []) and (self.Hands['P1'] == []):
                self.GameOver['P2'] = True # The Player 1 has won the game
            elif (self.Player2.deck == []) and (self.Hands['P2'] == []):
                self.GameOver['P1'] = True # The Player 2 has won the game
            self.DrawEndOfTurn()
            self.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
            self.ChangeActivePlayer()
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

    def Undo(self,
             verbosity : str = True
             ) -> None :

        """
        undo the last action of playing a card
        undo the played on opponenent piles, the card played and etc
        """

        if len(self.PlayedThisTurn['P'+str(self.ActivePlayer)]) > 0:
            LastPlayed = self.PlayedThisTurn['P'+str(self.ActivePlayer)][-1]
            LastPlayedPile = LastPlayed[1]
            LastPlayedCard = LastPlayed[0]
            self.Piles[LastPlayedPile].remove(LastPlayedCard)

            self.PlayedThisTurn['P'+str(self.ActivePlayer)].pop()
            self.Hands['P'+str(self.ActivePlayer)].append(LastPlayedCard)
            if LastPlayedCard.color != self.color[LastPlayedPile[:2]]:
                self.PlayedOnOpponnentPiles['P'+str(self.ActivePlayer)] = False
                if verbosity:
                    print('Undo Played on oppo piles')    
            if verbosity:            
                print('Undone !')

    def CheckIfLoose(self,
                     PlayerSelected : int,
                     verbosity = False) -> bool :
        """
        Tests all the play possibilities at the beginning of the turn
        and change the status of the variable Player.GameOver accordingly (becomes true if the player as indeed lost the game)

        The player looses the game when it cannot play on his piles, or when he cannot play 2 cards on his piles and he cannot play on opponent piles

        It also returns True if the player has lost the game, False otherwise
        """

        PilesList = ['P1_UP','P1_DOWN','P2_UP','P2_DOWN']
        self.DeepcopyForCheckIfLoose() # we create the backup

        # we have played no cards yet
        if len(self.PlayedThisTurn['P' + str(self.ActivePlayer)]) == 0:
            # checks the play possibilities of the ActivePlayer
            for card in self.Hands['P' + str(self.ActivePlayer)]:
                for pile in PilesList:
                    self.LoadDeepCopyForCheckIfLoose() # we load the backup
                    if self.CheckAction(pile,card,PlayerSelected,verbosity=False):
                        self.Play(pile,card,PlayerSelected,verbosity=False)
                        for card2 in self.Hands['P' + str(self.ActivePlayer)]:
                            for pile2 in PilesList:                         
                                if self.CheckAction(pile2,card2,PlayerSelected,verbosity=False):
                                    # the player hasn't lost the game
                                    self.LoadDeepCopyForCheckIfLoose()  
                                    if verbosity:
                                        print("one possible play is : ",card.number," on pile ",pile[3:]," of player ",pile[1])
                                        print("then : ",card2.number," on pile ",pile2[3:]," of player ",pile2[1])
                                    self.GameOver['P' + str(self.ActivePlayer)] = False
                                    return False

            self.GameOver['P' + str(self.ActivePlayer)] = True
            return True

        # we have played 1 card yet, must take into account the played on oppo piles
        elif len(self.PlayedThisTurn['P' + str(self.ActivePlayer)]) == 1:
            # checks the play possibilities of the ActivePlayer
            for card in self.Hands['P' + str(self.ActivePlayer)]:
                for pile in PilesList:
                    self.LoadDeepCopyForCheckIfLoose() # we load the backup
                    if self.CheckAction(pile,card,PlayerSelected,verbosity=False):
                        # the player hasn't lost the game
                        self.LoadDeepCopyForCheckIfLoose()
                        if verbosity:
                            print("one possible play is : ",card.number," on pile ",pile[3:]," of player ",pile[1])
                        self.GameOver['P' + str(self.ActivePlayer)] = False
                        return False
                                    

            self.GameOver['P' + str(self.ActivePlayer)] = True
            return True
        # we already played at least 2 cards
        else :
            return False
   
class GameFrontEnd(Game):

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

        self.PlayerSelected = 0

        self.HandsFrontEnd = {'P1' : copy.copy(self.Hands['P1']),
                              'P2':  copy.copy(self.Hands['P2'])}
        self.Moving = []

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
        #self.HEIGHTCARD = int(self.WINDOWHEIGHT/6)
        self.HEIGHTCARD = int(self.WINDOWHEIGHT/7)
        self.WIDTHCARD = int(self.HEIGHTCARD*250/350)
         
    def DefineColors(self
                     ) -> None :

                            #            R    G    B
        self.ColorsCodes = { "Gray"     : (100, 100, 100),
                            "NAVYBLUE" : ( 60,  60, 100),
                            "White"    : (255, 255, 255),
                            "RED"      : (255,   0,   0),
                            "GREEN"    : (  0, 255,   0),
                            "BLUE"     : (  0,   0, 255),
                            "YELLOW"   : (255, 255,   0),
                            "Orange"   : (255, 128,   0),
                            "PURPLE"   : (255,   0, 255),
                            "CYAN"     : (  0, 255, 255),
                            "Silver"   : (169, 169, 169),
                            "Gold"     : (218, 165,  32)}

        self.HIGHLIGHTCOLOR = self.ColorsCodes["Orange"]

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
        # TODO improve this to have something cleaner as messages, probably another layer

        self.DISPLAYSURF.blit(self.Images["TurnOfImg"], (0,0.4*self.WINDOWHEIGHT))
        if self.ActivePlayer == 1 :   
            self.DISPLAYSURF.blit(self.Images["Player1Img"], (0,0.5*self.WINDOWHEIGHT))
        if self.ActivePlayer == 2 :
            self.DISPLAYSURF.blit(self.Images["Player2Img"], (0,0.5*self.WINDOWHEIGHT))

    def CardToImageStr(self,
                       objectCard
                       ) -> str :
        """
        returns the imageStr (key to the dict image) in function of the objectCard given (can be a card or a str)
        """
        if isinstance(objectCard,Card):
            return str(objectCard.number)+objectCard.color
        elif isinstance(objectCard,str):
            return objectCard
        else :
            print('The objectCard is not a str or a card ! type : {}'.format(type(objectCard)))
            return None

    def DrawCardOnBoard(self,
                        objectCard,
                        LeftTop : list
                        ):
        """
        objectCard can be a card or a str
        """
        # TODO find how to return the correct type (and write it after the ) -> : )
        LeftTopx, LeftTopy = LeftTop
        card = self.DISPLAYSURF.blit(self.Images[self.CardToImageStr(objectCard)], (LeftTopx, LeftTopy))
        return card        

    def MoveACard(self,
                  x : int,
                  y : int,
                  CardIndex : int
                  ) -> None:

        LeftTop = [x-(self.WIDTHCARD//2),y-(self.HEIGHTCARD//2)]
        if self.Moving == []:
            self.Moving.append(self.HandsFrontEnd['P'+str(self.PlayerSelected)][CardIndex])
            self.HandsFrontEnd['P'+str(self.PlayerSelected)].remove(self.HandsFrontEnd['P'+str(self.PlayerSelected)][CardIndex])

        self.DrawCardOnBoard(self.Moving[0],LeftTop)
        pygame.draw.rect(self.DISPLAYSURF, self.HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)

    def DrawSelectedPlayerHand(self
                               ) -> list : 
        """
        Draws the selected player FrontEnd hand
        Running Frequency : every loop  
        """

        # Define a dict instead ? to check at first it won't change anything         
        CardsHand = []
        x0 = (self.WINDOWWIDTH-len(self.HandsFrontEnd['P'+str(self.PlayerSelected)])*self.WIDTHCARD)//2 

        for index, card in enumerate(self.HandsFrontEnd['P'+str(self.PlayerSelected)]):
            LeftTop = (x0+index*self.WIDTHCARD,5*self.HEIGHTCARD)
            CardsHand.append((self.DrawCardOnBoard(card,LeftTop),LeftTop))
        return CardsHand

    def DrawPiles(self
                  ) -> list :

        """
        Draws the Piles of the players
        Running Frequency : every time a card is played (Play) or unplayed (Undo)          
        """

        # Draws The Pile DOWN of Selected Player    
        LeftTop = [(self.WINDOWWIDTH-self.WIDTHCARD)//2,4*self.HEIGHTCARD]
        PileDownAP = self.DrawCardOnBoard(self.Piles['P'+str(self.PlayerSelected)+'_DOWN'][-1],LeftTop)
        pygame.draw.rect(self.DISPLAYSURF, self.ColorsCodes["White"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

        # Draws The Pile Up of Selected Player    
        LeftTop = [(self.WINDOWWIDTH-self.WIDTHCARD)//2,3*self.HEIGHTCARD]
        PileUPAP = self.DrawCardOnBoard(self.Piles['P'+str(self.PlayerSelected)+'_UP'][-1],LeftTop)
        pygame.draw.rect(self.DISPLAYSURF, self.ColorsCodes["White"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

        # Draws The Pile UP of the Player not selected     
        NotSelectedPlayer = 3 - self.PlayerSelected # f(x) = 3 - x verifies f(1)=2 and f(2)=1
        LeftTop = [(self.WINDOWWIDTH-self.WIDTHCARD)//2,2*self.HEIGHTCARD]
        PileUPNAP = self.DrawCardOnBoard(self.Piles['P'+str(NotSelectedPlayer)+'_UP'][-1],LeftTop)
        pygame.draw.rect(self.DISPLAYSURF, self.ColorsCodes["White"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

        # Draws The Pile DOWN of the Player not selected        
        LeftTop = [(self.WINDOWWIDTH-self.WIDTHCARD)//2,self.HEIGHTCARD]
        PileDownNAP = self.DrawCardOnBoard(self.Piles['P'+str(NotSelectedPlayer)+'_DOWN'][-1],LeftTop)
        pygame.draw.rect(self.DISPLAYSURF, self.ColorsCodes["White"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

        return [PileUPAP,PileDownAP,PileUPNAP,PileDownNAP]

    def DrawNotSelectedPlayerHand(self
                                  ) -> None : 
        """
        Draws the not selected player hand
        Running Frequency : every time a card is played (Play) or unplayed (Undo)   
        """

        # Define a dict instead ? to check at first it won't change anything         

        NotSelectedPlayer = 3 - self.PlayerSelected
        LengthHand = len(self.Hands['P'+str(NotSelectedPlayer)])
        x0 = (self.WINDOWWIDTH-LengthHand*self.WIDTHCARD)//2 

        for index in range(LengthHand):
            LeftTop = (x0+index*self.WIDTHCARD,0)
            self.DrawCardOnBoard('THEGAME'+self.color['P'+str(NotSelectedPlayer)],LeftTop)

    def DrawDecks(self
                  ) -> list :
        """
        Draws the deck of the players
        Running Frequency : every change of turn (after the draw)        
        """
        # TODO check that it works if the deck is empty

        #Draws the selected Player Deck
        LeftTop = [int((self.WINDOWWIDTH-5*self.WIDTHCARD)/2),int(3.5*self.HEIGHTCARD)]
        APDeck = self.DrawCardOnBoard('THEGAME'+self.color['P'+str(self.PlayerSelected)],LeftTop)
        pygame.draw.rect(self.DISPLAYSURF, self.ColorsCodes["Gray"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

        #Draws the Not selected Player Deck
        NotSelectedPlayer = 3 - self.PlayerSelected
        LeftTop = [int((self.WINDOWWIDTH + 3*self.WIDTHCARD)/2),int(1.5*self.HEIGHTCARD)]
        NAPDeck = self.DrawCardOnBoard('THEGAME'+self.color['P'+str(NotSelectedPlayer)],LeftTop)
        pygame.draw.rect(self.DISPLAYSURF, self.ColorsCodes["Gray"], (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

        return [APDeck,NAPDeck]

    def DrawSetup(self
                  ) -> None:
        """
        Draws the Pile symbols of the players
        Running Frequency : Once at the setup             
        """

        # Draws The Pile DOWN of ActivePlayer    
        LeftTop = [int((self.WINDOWWIDTH-3*self.WIDTHCARD)/2),4*self.HEIGHTCARD]
        self.DrawCardOnBoard('DOWN'+self.color['P'+str(self.PlayerSelected)],LeftTop)

        # Draws The Pile Up of ActivePlayer   
        LeftTop = [int((self.WINDOWWIDTH-3*self.WIDTHCARD)/2),3*self.HEIGHTCARD]
        self.DrawCardOnBoard('UP'+self.color['P'+str(self.PlayerSelected)],LeftTop)

        # Draws The Pile UP of NonActivePlayer    
        NotSelectedPlayer = 3 - self.PlayerSelected
        LeftTop = [int((self.WINDOWWIDTH+self.WIDTHCARD)/2),2*self.HEIGHTCARD]
        self.DrawCardOnBoard('UP'+self.color['P'+str(NotSelectedPlayer)],LeftTop)

        # Draws The Pile DOWN of NonActivePlayer   
        LeftTop = [int((self.WINDOWWIDTH+self.WIDTHCARD)/2),self.HEIGHTCARD]
        self.DrawCardOnBoard('DOWN'+self.color['P'+str(NotSelectedPlayer)],LeftTop)     

    def DrawBoard(self
                  ) -> list:
        
        FrontEndHand = self.DrawSelectedPlayerHand()
        Piles = self.DrawPiles() 
        Decks = self.DrawDecks()
        self.DrawSetup()
        self.DrawNotSelectedPlayerHand()
        return FrontEndHand, Piles, Decks