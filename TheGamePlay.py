import pygame, sys, TheGame
from pygame.locals import *


FPS = 60 # frames per second setting

WINDOWWIDTH = 1280
WINDOWHEIGHT = 720
heightCard = int(WINDOWHEIGHT/6)
width = int(heightCard*250/350)
widthCard = width 


#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = ORANGE


def main():
    global DISPLAYSURF
    pygame.init()
    
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('The Game')

    selected = False
    unselected = False


    DISPLAYSURF.fill(BGCOLOR)
    MainGame = TheGame.Game()

    while (not MainGame.P1GameOver) and (not MainGame.P2GameOver):

        mouseClicked = False
        unselected = False

        DISPLAYSURF.fill(BGCOLOR) # drawing the window
        (PileDownAP,PileUPAP,PileDownNAP,PileUPNAP) = DrawBoard(MainGame,heightCard,widthCard,width)

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 and OnACard(mousex,mousey,MainGame):
                mousex, mousey = event.pos
                mouseClicked = True
                selected = True
                CardIndex = GetCardIndex(mousex,mousey,MainGame)
            elif event.type == MOUSEBUTTONUP and event.button == 1 and selected:
                selected = False
                unselected = True
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN and event.button == 1 :
                mousex, mousey = event.pos
                mouseClicked = True
           
        OnACard(mousex,mousey,MainGame)
        boxRectEOT = pygame.draw.rect(DISPLAYSURF, BLUE, (WINDOWWIDTH-100 , 360 , 100 , 100), 4)
        boxRectCONCEDE = pygame.draw.rect(DISPLAYSURF, RED, (WINDOWWIDTH-100 ,0 , 100,100), 4)

        if selected: # we move the image selected
            mousex, mousey = event.pos
            MoveACard(mousex, mousey,CardIndex, MainGame)

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

def IsOnAPile(x,y):
    if x > (WINDOWWIDTH - widthCard)/2 and x < (WINDOWWIDTH + widthCard)/2 :
        if y > heightCard and y < 5*heightCard :
            return True
        else :
            return False
    else:
        return 0 


def DrawCardOnBoard(ColorStr,CardReference,LeftTop=None, index=-1 ,Game = None, ActivePlayer = True):
    cardImg = pygame.image.load('Cards/'+ColorStr+'Cards/Card_'+str(CardReference)+'.png')
    cardImg = pygame.transform.scale(cardImg, (widthCard, heightCard))
    if index>=0:
        Card = DISPLAYSURF.blit(cardImg, leftTopCoordsOfCard(Game,index,ActivePlayer=ActivePlayer))
        return Card
    elif index<0:
        Card = DISPLAYSURF.blit(cardImg, (LeftTop[0], LeftTop[1]))
        return Card

def MoveACard(x,y,CardIndex,Game):
    LeftTop = [x-(widthCard//2),y-(heightCard//2)]
    if Game.ActivePlayer == 1:
        DrawCardOnBoard('Gold',Game.Player1.Hand[CardIndex],LeftTop=LeftTop, index=-1 ,Game = None, ActivePlayer = True)
        pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , width, heightCard ), 4)
        
    elif Game.ActivePlayer == 2:
        DrawCardOnBoard('Silver',Game.Player2.Hand[CardIndex],LeftTop=LeftTop, index=-1 ,Game = None, ActivePlayer = True)
        pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , width, heightCard ), 4)
          

def OnACard(x,y,Game):
    CardIndex = GetCardIndex(x,y,Game)
    if CardIndex >= 0:
        if Game.ActivePlayer == 1:
            LeftTop = leftTopCoordsOfCard(Game,CardIndex)
            pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0], LeftTop[1] , width, heightCard ), 4)
            return True

        elif Game.ActivePlayer == 2:
            LeftTop = leftTopCoordsOfCard(Game,CardIndex)
            pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (LeftTop[0] - 5, LeftTop[1] - 5, width + 10, heightCard + 10), 4)
            return True
    else :
        return False

def GetCardIndex(x,y,Game):
    if y > WINDOWHEIGHT - heightCard:
        if Game.ActivePlayer == 1:
            L = len(Game.Player1.Hand)
            x0 = (WINDOWWIDTH-L*width)//2
            if x > x0 and x < x0 + L*width:
                CardIndex = (x-x0)//width
                return CardIndex
            else :
                return -1
                
        elif Game.ActivePlayer == 2:
            L = len(Game.Player2.Hand)
            x0 = (WINDOWWIDTH-L*width)//2
            if x > x0 and x < x0 + L*width:
                CardIndex = (x-x0)//width
                return CardIndex
            else :
                return -1 
    else :
        return -1

def leftTopCoordsOfCard(Game,i,ActivePlayer = True):
    # Convert board coordinates to pixel coordinates
    if Game.ActivePlayer == 1:
        if ActivePlayer :   
            x0 = (WINDOWWIDTH-len(Game.Player1.Hand)*width)//2 
            return (x0+i*width,5*heightCard-10)
        elif not ActivePlayer :
            x0 = (WINDOWWIDTH-len(Game.Player2.Hand)*width)//2
            return (x0+i*width,0)
    elif Game.ActivePlayer == 2:
            if ActivePlayer :   
                x0 = (WINDOWWIDTH-len(Game.Player2.Hand)*width)//2 
                return (x0+i*width,5*heightCard-10)
            elif not ActivePlayer :
                x0 = (WINDOWWIDTH-len(Game.Player1.Hand)*width)//2
                return (x0+i*width,0)

def DrawBoard(Game,heightCard,widthCard,width):
    i = 0
    if Game.ActivePlayer == 1:
        ColorStr = 'Gold'
        for number in Game.Player1.Hand:
            DrawCardOnBoard(ColorStr,number,index = i,Game=Game)
            i+=1

        NumberOfCardsOppo = len(Game.Player2.Hand)
        for k in range(NumberOfCardsOppo):
            DrawCardOnBoard('Silver','THEGAME',index = k,Game=Game,ActivePlayer=False)


        # Draws The Pile DOWN of ActivePlayer    
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),4*heightCard-10]
        PileDownAP = DrawCardOnBoard(ColorStr,Game.Player1.PileDOWN[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # Draws The Pile Up of ActivePlayer   
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),3*heightCard-10]
        PileUPAP = DrawCardOnBoard(ColorStr,Game.Player1.PileUP[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # Draws The Pile UP of NonActivePlayer    
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),2*heightCard-10]
        PileUPNAP = DrawCardOnBoard('Silver',Game.Player2.PileUP[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # Draws The Pile DOWN of NonActivePlayer   
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),heightCard-10]
        PileDownNAP = DrawCardOnBoard('Silver',Game.Player2.PileDOWN[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # DRAWS THE PILES SYMBOLES !

        # Draws The Pile DOWN of ActivePlayer    
        LeftTop = [int((WINDOWWIDTH-3*widthCard)/2),4*heightCard-10]
        DrawCardOnBoard(ColorStr,'DOWN',LeftTop)

        # Draws The Pile Up of ActivePlayer   
        LeftTop = [int((WINDOWWIDTH-3*widthCard)/2),3*heightCard-10]
        DrawCardOnBoard(ColorStr,'UP',LeftTop)

        # Draws The Pile UP of NonActivePlayer    
        LeftTop = [int((WINDOWWIDTH+widthCard)/2),2*heightCard-10]
        DrawCardOnBoard('Silver','UP',LeftTop)

        # Draws The Pile DOWN of NonActivePlayer   
        LeftTop = [int((WINDOWWIDTH+widthCard)/2),heightCard-10]
        DrawCardOnBoard('Silver','DOWN',LeftTop)

        ## DRAWS THE DECK OF ACTIVEPLAYER

        LeftTop = [int((WINDOWWIDTH-5*widthCard)/2),int(3.5*heightCard-10)]
        DrawCardOnBoard(ColorStr,'THEGAME',LeftTop)
        pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        LeftTop = [int((WINDOWWIDTH + 3*widthCard)/2),int(1.5*heightCard-10)]
        DrawCardOnBoard('Silver','THEGAME',LeftTop)
        pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

    elif Game.ActivePlayer == 2:
        ColorStr = 'Silver'
        for number in Game.Player2.Hand:
            DrawCardOnBoard('Silver',number,index = i,Game=Game)
            i+=1

        NumberOfCardsOppo = len(Game.Player1.Hand)
        for k in range(NumberOfCardsOppo):
            DrawCardOnBoard('Gold','THEGAME',index = k,Game=Game,ActivePlayer=False)

        # Draws The Pile DOWN of ActivePlayer    
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),4*heightCard-10]
        PileDownAP = DrawCardOnBoard(ColorStr,Game.Player2.PileDOWN[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # Draws The Pile UP of ActivePlayer   
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),3*heightCard-10]
        PileUPAP = DrawCardOnBoard(ColorStr,Game.Player2.PileUP[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # Draws The Pile UP of NonActivePlayer    
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),2*heightCard-10]
        PileUPNAP = DrawCardOnBoard('Gold',Game.Player1.PileUP[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # Draws The Pile DOWN of NonActivePlayer   
        LeftTop = [int((WINDOWWIDTH-widthCard)/2),heightCard-10]
        PileDownNAP = DrawCardOnBoard('Gold',Game.Player1.PileDOWN[-1:][0],LeftTop)
        pygame.draw.rect(DISPLAYSURF, WHITE, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        # DRAWS THE PILES SYMBOLES !

        # Draws The Pile DOWN of ActivePlayer    
        LeftTop = [int((WINDOWWIDTH-3*widthCard)/2),4*heightCard-10]
        DrawCardOnBoard(ColorStr,'DOWN',LeftTop)


        # Draws The Pile Up of ActivePlayer   
        LeftTop = [int((WINDOWWIDTH-3*widthCard)/2),3*heightCard-10]
        DrawCardOnBoard(ColorStr,'UP',LeftTop)

        # Draws The Pile UP of NonActivePlayer    
        LeftTop = [int((WINDOWWIDTH+widthCard)/2),2*heightCard-10]
        DrawCardOnBoard('Gold','UP',LeftTop)

        # Draws The Pile DOWN of NonActivePlayer   
        LeftTop = [int((WINDOWWIDTH+widthCard)/2),heightCard-10]
        DrawCardOnBoard('Gold','DOWN',LeftTop)

        LeftTop = [int((WINDOWWIDTH-5*widthCard)/2),int(3.5*heightCard-10)]
        DrawCardOnBoard(ColorStr,'THEGAME',LeftTop)
        pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)

        LeftTop = [int((WINDOWWIDTH + 3*widthCard)/2),int(1.5*heightCard-10)]
        DrawCardOnBoard('Gold','THEGAME',LeftTop)
        pygame.draw.rect(DISPLAYSURF, GRAY, (LeftTop[0] , LeftTop[1] , width , heightCard ), 4)
    
    return PileDownAP,PileUPAP,PileDownNAP,PileUPNAP
if __name__ == '__main__':
    main()