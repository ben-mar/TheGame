import pygame, sys, TheGame
from pygame.locals import *


FPS = 60 # frames per second setting

WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
heightCard = int(WINDOWHEIGHT/6)
width = int(heightCard*250/350)
widthCard = width 

               
# BGCOLOR = NAVYBLUE
# LIGHTBGCOLOR = GRAY
# BOXCOLOR = WHITE





class Total:

    def main():
        global FPSCLOCK
        pygame.init()

        # initialize font; must be called after 'pygame.init()' to avoid 'Font not Initialized' error
        myfont = pygame.font.SysFont("monospace", 30)
        
        FPSCLOCK = pygame.time.Clock()
        DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

        mousex = 0 # used to store x coordinate of mouse event
        mousey = 0 # used to store y coordinate of mouse event
        pygame.display.set_caption('The Game')

        selected = False
        unselected = False

        background = pygame.image.load('./Pictures/BG1280x720.jpg').convert()
        DISPLAYSURF.blit(background, (0,0))
        
        MainGame = TheGame.Game()

        while (not MainGame.P1GameOver) and (not MainGame.P2GameOver):

            mouseClicked = False
            unselected = False

            DISPLAYSURF.blit(background, (0,0))
            (PileDownAP,PileUPAP,PileDownNAP,PileUPNAP,APDeck,NAPDeck) = Total.DrawBoard(MainGame,DISPLAYSURF,MainGame.ActivePlayer)

            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 and OnACard(mousex,mousey,MainGame,DISPLAYSURF,MainGame.ActivePlayer):
                    mousex, mousey = event.pos
                    mouseClicked = True
                    selected = True
                    CardIndex = GetCardIndex(mousex,mousey,MainGame,MainGame.ActivePlayer)
                elif event.type == MOUSEBUTTONUP and event.button == 1 and selected:
                    selected = False
                    unselected = True
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONDOWN and event.button == 1 :
                    mousex, mousey = event.pos
                    mouseClicked = True

            DisplayActivePlayer(MainGame,DISPLAYSURF)   
            OnACard(mousex,mousey,MainGame,DISPLAYSURF,MainGame.ActivePlayer)
            boxRectEOT = pygame.draw.rect(DISPLAYSURF, BLUE, (WINDOWWIDTH-100 , 360 , 100 , 100), 4)
            boxRectCONCEDE = pygame.draw.rect(DISPLAYSURF, RED, (WINDOWWIDTH-100 ,0 , 100,100), 4)

            if APDeck.collidepoint(mousex,mousey) :
                if MainGame.ActivePlayer == 1 :
                    label = myfont.render(str(len(MainGame.Player1.Deck)), 1, (255,255,0))
                    DISPLAYSURF.blit(label, (int((WINDOWWIDTH-4.4*self.WIDTHCARD)/2),int(4.5*self.HEIGHTCARD)))
                elif MainGame.ActivePlayer == 2 :
                    label = myfont.render(str(len(MainGame.Player2.Deck)), 1, (169,169,169))
                    DISPLAYSURF.blit(label, (int((WINDOWWIDTH-4.4*self.WIDTHCARD)/2),int(4.5*self.HEIGHTCARD)))

            if NAPDeck.collidepoint(mousex,mousey) :
                if MainGame.ActivePlayer == 1 :
                    label = myfont.render(str(len(MainGame.Player2.Deck)), 1, (169,169,169))
                    DISPLAYSURF.blit(label, (int((WINDOWWIDTH+3.4*self.WIDTHCARD)/2),int(2.5*self.HEIGHTCARD)))
                elif MainGame.ActivePlayer == 2 :
                    label = myfont.render(str(len(MainGame.Player1.Deck)), 1, (255,255,0))
                    DISPLAYSURF.blit(label, (int((WINDOWWIDTH+3.4*self.WIDTHCARD)/2),int(2.5*self.HEIGHTCARD)))



            if selected: # we move the image selected
                mousex, mousey = event.pos
                MoveACard(mousex, mousey,CardIndex, MainGame,DISPLAYSURF,MainGame.ActivePlayer)

            if unselected and IsOnAPile(mousex, mousey): # we play the card on the pile 
                mousex, mousey = event.pos
                if MainGame.ActivePlayer == 1:
                    CardToPlay = MainGame.Player1.Hand[CardIndex]
                    if PileDownAP.collidepoint(mousex,mousey):
                        MainGame.Play(1,CardToPlay,'DOWN')
                    elif PileUPAP.collidepoint(mousex,mousey):
                        MainGame.Play(1,CardToPlay,'UP')
                    elif PileDownNAP.collidepoint(mousex,mousey):
                        MainGame.Play(2,CardToPlay,'DOWN')
                    elif PileUPNAP.collidepoint(mousex,mousey):
                        MainGame.Play(2,CardToPlay,'UP')
                if MainGame.ActivePlayer == 2:
                    CardToPlay = MainGame.Player2.Hand[CardIndex]
                    if PileDownAP.collidepoint(mousex,mousey):
                        MainGame.Play(2,CardToPlay,'DOWN')
                    elif PileUPAP.collidepoint(mousex,mousey):
                        MainGame.Play(2,CardToPlay,'UP')
                    elif PileDownNAP.collidepoint(mousex,mousey):
                        MainGame.Play(1,CardToPlay,'DOWN')
                    elif PileUPNAP.collidepoint(mousex,mousey):
                        MainGame.Play(1,CardToPlay,'UP')

            if mouseClicked :
                if boxRectCONCEDE.collidepoint(mousex,mousey):
                    MainGame.Concede()
                elif boxRectEOT.collidepoint(mousex,mousey):
                    MainGame.EndOfTurn()
                
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            FPSCLOCK.tick(FPS)

    def DisplayActivePlayer(self,MainGame,DISPLAYSURF):
        if MainGame.ActivePlayer == 1 :
            DISPLAYSURF.blit(TurnOfImg, (0,0))
            DISPLAYSURF.blit(Player1Img, (0,72))
        if MainGame.ActivePlayer == 2 :
            DISPLAYSURF.blit(TurnOfImg, (0,0))
            DISPLAYSURF.blit(Player2Img, (0,72))

    def IsOnAPile(self,x,y):
        if x > (WINDOWWIDTH - self.WIDTHCARD)/2 and x < (WINDOWWIDTH + self.WIDTHCARD)/2 :
            if y > self.HEIGHTCARD and y < 5*self.HEIGHTCARD :
                return True
            else :
                return False
        else:
            return 0 


    def DrawCardOnBoard(self,ColorStr,CardReference,DISPLAYSURF,PlayerSelected,LeftTop=None, index=-1 ,Game = None, ActivePlayer = True):
        cardImg = pygame.image.load('./Pictures/Cards/'+ColorStr+'Cards/Card_'+str(CardReference)+'.png')
        cardImg = pygame.transform.scale(cardImg, (self.WIDTHCARD, self.HEIGHTCARD))
        if index>=0:
            Card = DISPLAYSURF.blit(cardImg, leftTopCoordsOfCard(Game,index,PlayerSelected,ActivePlayer=ActivePlayer))
            return Card
        elif index<0:
            Card = DISPLAYSURF.blit(cardImg, (LeftTop[0], LeftTop[1]))
            return Card

    def MoveACard(self,x,y,CardIndex,Game,DISPLAYSURF,PlayerSelected):
        LeftTop = [x-(self.WIDTHCARD//2),y-(self.HEIGHTCARD//2)]
        if PlayerSelected == 1:
            Total.DrawCardOnBoard('Gold',Game.Player1.Hand[CardIndex],DISPLAYSURF,PlayerSelected,LeftTop=LeftTop, index=-1 ,Game = None, ActivePlayer = True)
            pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)
            
        elif PlayerSelected == 2:
            Total.DrawCardOnBoard('Silver',Game.Player2.Hand[CardIndex],DISPLAYSURF,PlayerSelected,LeftTop=LeftTop, index=-1 ,Game = None, ActivePlayer = True)
            pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)
            


    def OnACard(self,x,y,Game,DISPLAYSURF,PlayerSelected):
        CardIndex = Total.GetCardIndex(x,y,Game,PlayerSelected)
        if CardIndex >= 0:
            if PlayerSelected == 1:
                LeftTop = Total.leftTopCoordsOfCard(Game,CardIndex,PlayerSelected)
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , self.WIDTHCARD, self.HEIGHTCARD ), 4)
                return True

            elif PlayerSelected == 2:
                LeftTop = leftTopCoordsOfCard(Game,CardIndex,PlayerSelected)
                pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0] - 5, LeftTop[1] - 5, self.WIDTHCARD + 10, self.HEIGHTCARD + 10), 4)
                return True
        else :
            return False

    def GetCardIndex(self,x,y,Game,PlayerSelected):
        if y > WINDOWHEIGHT - self.HEIGHTCARD:
            if PlayerSelected == 1:
                L = len(Game.Player1.Hand)
                x0 = (WINDOWWIDTH-L*self.WIDTHCARD)//2
                if x > x0 and x < x0 + L*self.WIDTHCARD:
                    CardIndex = (x-x0)//self.WIDTHCARD
                    return CardIndex
                else :
                    return -1
                    
            elif PlayerSelected == 2:
                L = len(Game.Player2.Hand)
                x0 = (WINDOWWIDTH-L*self.WIDTHCARD)//2
                if x > x0 and x < x0 + L*self.WIDTHCARD:
                    CardIndex = (x-x0)//self.WIDTHCARD
                    return CardIndex
                else :
                    return -1 
        else :
            return -1

    def leftTopCoordsOfCard(self,Game,i,PlayerSelected,ActivePlayer = True):
        # Convert board coordinates to pixel coordinates
        if PlayerSelected == 1:
            if ActivePlayer :
                x0 = (WINDOWWIDTH-len(Game.Player1.Hand)*self.WIDTHCARD)//2 
                return (x0+i*self.WIDTHCARD,5*self.HEIGHTCARD-10)
            elif not ActivePlayer :
                x0 = (WINDOWWIDTH-len(Game.Player2.Hand)*self.WIDTHCARD)//2
                return (x0+i*self.WIDTHCARD,0)
        elif PlayerSelected == 2:
            if ActivePlayer :   
                x0 = (WINDOWWIDTH-len(Game.Player2.Hand)*self.WIDTHCARD)//2 
                return (x0+i*self.WIDTHCARD,5*self.HEIGHTCARD-10)
            elif not ActivePlayer :
                x0 = (WINDOWWIDTH-len(Game.Player1.Hand)*self.WIDTHCARD)//2
                return (x0+i*self.WIDTHCARD,0)

    def DrawBoard(Game,DISPLAYSURF,PlayerSelected):
        i = 0
        if PlayerSelected == 1:
            ColorStr = 'Gold'
            for number in Game.Player1.Hand:
                DrawCardOnBoard(ColorStr,number,DISPLAYSURF,PlayerSelected,index = i,Game=Game)
                i+=1

            NumberOfCardsOppo = len(Game.Player2.Hand)
            for k in range(NumberOfCardsOppo):
                DrawCardOnBoard('Silver','THEGAME',DISPLAYSURF,PlayerSelected,index = k,Game=Game,ActivePlayer=False)


            ####### DRAWS THE PILES SYMBOLES #######

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),4*self.HEIGHTCARD-10]
            PileDownAP = DrawCardOnBoard(ColorStr,Game.Player1.PileDOWN[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile Up of ActivePlayer   
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),3*self.HEIGHTCARD-10]
            PileUPAP = DrawCardOnBoard(ColorStr,Game.Player1.PileUP[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),2*self.HEIGHTCARD-10]
            PileUPNAP = DrawCardOnBoard('Silver',Game.Player2.PileUP[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),self.HEIGHTCARD-10]
            PileDownNAP = DrawCardOnBoard('Silver',Game.Player2.PileDOWN[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)



            ####### DRAWS THE PILES SYMBOLES #######

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((WINDOWWIDTH-3*self.WIDTHCARD)/2),4*self.HEIGHTCARD-10]
            DrawCardOnBoard(ColorStr,'DOWN',DISPLAYSURF,PlayerSelected,LeftTop)

            # Draws The Pile Up of ActivePlayer   
            LeftTop = [int((WINDOWWIDTH-3*self.WIDTHCARD)/2),3*self.HEIGHTCARD-10]
            DrawCardOnBoard(ColorStr,'UP',DISPLAYSURF,PlayerSelected,LeftTop)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((WINDOWWIDTH+self.WIDTHCARD)/2),2*self.HEIGHTCARD-10]
            DrawCardOnBoard('Silver','UP',DISPLAYSURF,PlayerSelected,LeftTop)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((WINDOWWIDTH+self.WIDTHCARD)/2),self.HEIGHTCARD-10]
            DrawCardOnBoard('Silver','DOWN',DISPLAYSURF,PlayerSelected,LeftTop)

            ####### DRAWS THE DECKS #######

            ## DRAWS THE DECK OF ACTIVEPLAYER
            LeftTop = [int((WINDOWWIDTH-5*self.WIDTHCARD)/2),int(3.5*self.HEIGHTCARD-10)]
            APDeck = DrawCardOnBoard(ColorStr,'THEGAME',DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            ## DRAWS THE DECK OF NONACTIVEPLAYER
            LeftTop = [int((WINDOWWIDTH + 3*self.WIDTHCARD)/2),int(1.5*self.HEIGHTCARD-10)]
            NAPDeck = DrawCardOnBoard('Silver','THEGAME',DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)



        elif PlayerSelected == 2:
            ColorStr = 'Silver'
            for number in Game.Player2.Hand:
                DrawCardOnBoard('Silver',number,DISPLAYSURF,PlayerSelected,index = i,Game=Game)
                i+=1

            NumberOfCardsOppo = len(Game.Player1.Hand)
            for k in range(NumberOfCardsOppo):
                DrawCardOnBoard('Gold','THEGAME',DISPLAYSURF,PlayerSelected,index = k,Game=Game,ActivePlayer=False)

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),4*self.HEIGHTCARD-10]
            PileDownAP = DrawCardOnBoard(ColorStr,Game.Player2.PileDOWN[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of ActivePlayer   
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),3*self.HEIGHTCARD-10]
            PileUPAP = DrawCardOnBoard(ColorStr,Game.Player2.PileUP[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),2*self.HEIGHTCARD-10]
            PileUPNAP = DrawCardOnBoard('Gold',Game.Player1.PileUP[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((WINDOWWIDTH-self.WIDTHCARD)/2),self.HEIGHTCARD-10]
            PileDownNAP = DrawCardOnBoard('Gold',Game.Player1.PileDOWN[-1:][0],DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)


            ####### DRAWS THE PILES SYMBOLES #######

            # Draws The Pile DOWN of ActivePlayer    
            LeftTop = [int((WINDOWWIDTH-3*self.WIDTHCARD)/2),4*self.HEIGHTCARD-10]
            DrawCardOnBoard(ColorStr,'DOWN',DISPLAYSURF,PlayerSelected,LeftTop)


            # Draws The Pile Up of ActivePlayer   
            LeftTop = [int((WINDOWWIDTH-3*self.WIDTHCARD)/2),3*self.HEIGHTCARD-10]
            DrawCardOnBoard(ColorStr,'UP',DISPLAYSURF,PlayerSelected,LeftTop)

            # Draws The Pile UP of NonActivePlayer    
            LeftTop = [int((WINDOWWIDTH+self.WIDTHCARD)/2),2*self.HEIGHTCARD-10]
            DrawCardOnBoard('Gold','UP',DISPLAYSURF,PlayerSelected,LeftTop)

            # Draws The Pile DOWN of NonActivePlayer   
            LeftTop = [int((WINDOWWIDTH+self.WIDTHCARD)/2),self.HEIGHTCARD-10]
            DrawCardOnBoard('Gold','DOWN',DISPLAYSURF,PlayerSelected,LeftTop)

            ####### DRAWS THE DECKS #######

            ## DRAWS THE DECK OF ACTIVEPLAYER
            LeftTop = [int((WINDOWWIDTH-5*self.WIDTHCARD)/2),int(3.5*self.HEIGHTCARD-10)]
            APDeck = DrawCardOnBoard(ColorStr,'THEGAME',DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)

            ## DRAWS THE DECK OF NONACTIVEPLAYER
            LeftTop = [int((WINDOWWIDTH + 3*self.WIDTHCARD)/2),int(1.5*self.HEIGHTCARD-10)]
            NAPDeck = DrawCardOnBoard('Gold','THEGAME',DISPLAYSURF,PlayerSelected,LeftTop)
            pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , self.WIDTHCARD , self.HEIGHTCARD ), 4)
        
        return PileDownAP,PileUPAP,PileDownNAP,PileUPNAP,APDeck,NAPDeck

if __name__ == '__main__':
    Total.main()