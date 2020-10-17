import sys
import socket
import select
import random
import pygame
from pygame.locals import *
import TheGame


class GameClient:

	def __init__(self, addr="127.0.0.1", serverport=9009):
		self.clientport = random.randrange(8000, 8999)
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind to localhost - set to external ip to connect from other computers
		self.conn.bind(("127.0.0.1", self.clientport))
		self.addr = addr
		self.serverport = serverport		
		self.read_list = [self.conn]
		self.write_list = []		
		self.setup_pygame()
  
	def setup_pygame(self):
		self.game = TheGame.TheGamePlay()
		pygame.display.set_caption('The Game')

	def Encode(self,
			   ListOfCards: list
			   ) -> str:
		# Encodes the messages
		if ListOfCards == []:
			return ''
		else:
			str_encoded = ''
			for card in ListOfCards:
				str_encoded += str(card.number)+'$'+card.color+';'
			str_encoded = str_encoded.rstrip(';')
			return(str_encoded)

	def Decode (self,
				str_encoded: str
				) -> list:
		# Decodes the messages
		ListOfCards = [] 
		if str_encoded =='':
			return ListOfCards
		else:
			spliting = str_encoded.split(';')
			for encoded_card in spliting:
				number,color = encoded_card.split('$') 
				ListOfCards.append(TheGame.Card(int(number),color))
			return ListOfCards

	def run(self):
		running = (not self.game.P1GameOver) and (not self.game.P2GameOver)

		mousex = 0 # used to store x coordinate of mouse event
		mousey = 0 # used to store y coordinate of mouse event

		selected = False
		unselected = False
		Selection = False

		# First screen of Player selection
		while not Selection:
			self.game.DISPLAYSURF.blit(self.game.Images["BGsurface"], (0,0))
			Player1Box = self.game.DISPLAYSURF.blit(self.game.Images["Player1Img"], (0.3*self.game.WINDOWWIDTH,0.45*self.game.WINDOWHEIGHT))
			Player2Box = self.game.DISPLAYSURF.blit(self.game.Images["Player2Img"], (0.5*self.game.WINDOWWIDTH,0.45*self.game.WINDOWHEIGHT))

			for event in pygame.event.get(): # event handling loop
				if event.type == pygame.VIDEORESIZE: # resize
						self.game.DISPLAYSURF = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
						self.game.DefineSizes()
						self.game.DefineImages()
				if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
					pygame.quit()
					sys.exit()
				elif event.type == MOUSEBUTTONDOWN and event.button == 1 and Player1Box.collidepoint(mousex,mousey):
					PlayerSelected = 1
					Selection = True
				elif event.type == MOUSEBUTTONDOWN and event.button == 1 and Player2Box.collidepoint(mousex,mousey):
					PlayerSelected = 2
					Selection = True
				elif event.type == MOUSEMOTION:
					mousex, mousey = event.pos

			pygame.display.update()
			self.game.clock.tick(self.game.FPS)   
			
		try:
			# Initialize connection to server
			self.conn.sendto(("NEW"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
			
			# setup of the piles
			NotSU1 = True
			NotSU2 = True
			while NotSU1 or NotSU2 :
				readable, _, _ = (
						select.select(self.read_list, self.write_list, [], 0)
					)
				for f in readable:
					if f is self.conn:
						msg, _ = f.recvfrom(65536) # find the best size here
						msg= msg.decode()
						if len(msg) >= 3:
							cmd = msg[0:3]
							msg = msg[3:]
						if cmd == 'SU1': # setup new player hand and deck
							Hand1, Hand2, Deck1, Deck2, ActivePlayer = msg.split('|')
							self.game.Player1.hand = self.Decode(Hand1)
							self.game.Player1.deck = self.Decode(Deck1)
							self.game.Player2.hand = self.Decode(Hand2)
							self.game.Player2.deck = self.Decode(Deck2)
							self.game.ActivePlayer = int(ActivePlayer)
							NotSU1 = False
						if cmd == 'SU2': # setup new player piles
							PileUP1,PileDN1 , PileUP2,PileDN2 = msg.split('|')
							self.game.Player1.PileUP = self.Decode(PileUP1)
							self.game.Player1.PileDOWN = self.Decode(PileDN1)
							self.game.Player2.PileUP = self.Decode(PileUP2)
							self.game.Player2.PileDOWN = self.Decode(PileDN2)											
							NotSU2 = False
			# the game
			while running:

				
				# select on specified file descriptors
				readable, _, _ = (
					select.select(self.read_list, self.write_list, [], 0)
				)
				for f in readable:

					if f is self.conn:

						msg, _ = f.recvfrom(65536)
						msg= msg.decode()

						if len(msg) >= 3:

							cmd = msg[0:3]
							msg = msg[3:]					

						if cmd == "PLC":  # PLay a Card

							PileIndex,CardStr,PileName = msg.split(";")
							Card = self.Decode(CardStr)[0]
							self.game.Play(int(PileIndex),Card,PileName)

							# message to check piles, hand and deck
							LenghtHands = len(self.game.Player1.hand)*len(self.game.Player2.hand)
							LenghtDecks = len(self.game.Player1.deck)*len(self.game.Player2.deck)
							if LenghtDecks*LenghtHands > 0 :

								msg = "CK1"+self.Encode(self.game.Player1.hand)
								msg += "|" +self.Encode(self.game.Player2.hand)
								msg += "|" +self.Encode(self.game.Player1.deck)
								msg += "|" +self.Encode(self.game.Player2.deck)

								msg2 = "CK2"+self.Encode(self.game.Player1.PileUP)
								msg2 += "|"+self.Encode(self.game.Player1.PileDOWN)
								msg2 += "|"+self.Encode(self.game.Player2.PileUP)
								msg2 += "|"+self.Encode(self.game.Player2.PileDOWN)

								self.conn.sendto(msg.encode(), (self.addr, self.serverport))
								self.conn.sendto(msg2.encode(), (self.addr, self.serverport))

						elif cmd == "EOT": # End Of Turn
							
							self.game.EndOfTurn()

						elif cmd == "CAP": # Change ActivePlayer

							self.game.ChangeActivePlayer()

						elif cmd == 'UPD' : 

							Hand1, Hand2, Deck1, Deck2 = msg.split('|')
							self.game.Player1.hand = self.Decode(Hand1)
							self.game.Player1.deck = self.Decode(Deck1)
							self.game.Player2.hand = self.Decode(Hand2)
							self.game.Player2.deck = self.Decode(Deck2)


				mouseClicked = False
				unselected = False

				self.game.DISPLAYSURF.blit(self.game.Images["BGsurface"], (0,0))

			
				(PileDownAP,PileUPAP,PileDownNAP,PileUPNAP,APDeck,NAPDeck) = self.game.DrawBoard(PlayerSelected)

				for event in pygame.event.get(): # event handling loop
					if event.type == pygame.VIDEORESIZE: # resize
						self.game.DISPLAYSURF = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
						self.game.DefineSizes()
						self.game.DefineImages()
					if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
						pygame.quit()
						sys.exit()
					elif event.type == MOUSEBUTTONDOWN and event.button == 1 and self.game.OnACard(mousex,mousey,PlayerSelected):
						mousex, mousey = event.pos
						mouseClicked = True
						selected = True
						CardIndex = self.game.GetCardIndex(mousex,mousey,PlayerSelected)
					elif event.type == MOUSEBUTTONUP and event.button == 1 and selected:
						selected = False
						unselected = True
					elif event.type == MOUSEMOTION:
						mousex, mousey = event.pos
					elif event.type == MOUSEBUTTONDOWN and event.button == 1 :
						mousex, mousey = event.pos
						mouseClicked = True
					
				
				self.game.DisplayActivePlayer()  
				self.game.OnACard(mousex,mousey,PlayerSelected)
				boxRectEOT = self.game.DISPLAYSURF.blit(self.game.Images["EndOfTurn"], (0.8*self.game.WINDOWWIDTH,0.45*self.game.WINDOWHEIGHT))
				boxRectCONCEDE = self.game.DISPLAYSURF.blit(self.game.Images["Quit"], (0.8*self.game.WINDOWWIDTH,0))

				# shows the number of cards of the players
				if APDeck.collidepoint(mousex,mousey) :
					if PlayerSelected == 1 :
						label = self.game.myfont.render(str(len(self.game.Player1.deck)), 1, self.game.Colors["GOLD"])
						self.game.DISPLAYSURF.blit(label, (int((self.game.WINDOWWIDTH-4.4*self.game.WIDTHCARD)/2),int(4.5*self.game.HEIGHTCARD)))
					elif PlayerSelected == 2 :
						label = self.game.myfont.render(str(len(self.game.Player2.deck)), 1, self.game.Colors["SILVER"]) 
						self.game.DISPLAYSURF.blit(label, (int((self.game.WINDOWWIDTH-4.4*self.game.WIDTHCARD)/2),int(4.5*self.game.HEIGHTCARD)))
				if NAPDeck.collidepoint(mousex,mousey) :
					if PlayerSelected == 1 :
						label = self.game.myfont.render(str(len(self.game.Player2.deck)), 1, self.game.Colors["SILVER"])
						self.game.DISPLAYSURF.blit(label, (int((self.game.WINDOWWIDTH+3.4*self.game.WIDTHCARD)/2),int(2.5*self.game.HEIGHTCARD)))
					elif PlayerSelected == 2 :
						label = self.game.myfont.render(str(len(self.game.Player1.deck)), 1, self.game.Colors["GOLD"])
						self.game.DISPLAYSURF.blit(label, (int((self.game.WINDOWWIDTH+3.4*self.game.WIDTHCARD)/2),int(2.5*self.game.HEIGHTCARD)))

				# we move the image selected
				if selected: 
					mousex, mousey = event.pos
					self.game.MoveACard(mousex, mousey,CardIndex,PlayerSelected)

				# we play the card on the pile 	
				if unselected and self.game.IsOnAPile(mousex, mousey): 
					mousex, mousey = event.pos
					if self.game.ActivePlayer == 1 :# and self.game.ActivePlayer == PlayerSelected:
						CardToPlay = self.game.Player1.hand[CardIndex]
						if PileDownAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC1;"+self.Encode([CardToPlay])+";DOWN").encode(),  (self.addr, self.serverport))
						elif PileUPAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC1;"+self.Encode([CardToPlay])+";UP").encode(), (self.addr, self.serverport))
						elif PileDownNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC2;"+self.Encode([CardToPlay])+";DOWN").encode(), (self.addr, self.serverport))
						elif PileUPNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC2;"+self.Encode([CardToPlay])+";UP").encode(), (self.addr, self.serverport))
					if self.game.ActivePlayer == 2 :# and self.game.ActivePlayer == PlayerSelected:
						CardToPlay = self.game.Player2.hand[CardIndex]
						if PileDownAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC2;"+self.Encode([CardToPlay])+";DOWN").encode(), (self.addr, self.serverport))
						elif PileUPAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC2;"+self.Encode([CardToPlay])+";UP").encode(), (self.addr, self.serverport))
						elif PileDownNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC1;"+self.Encode([CardToPlay])+";DOWN").encode(), (self.addr, self.serverport))
						elif PileUPNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLC1;"+self.Encode([CardToPlay])+";UP").encode(), (self.addr, self.serverport))

				# EOT or concede block
				if mouseClicked :

					# block to improve 
					# Click to see the piles
					if self.game.IsOnAPile(mousex, mousey):

						GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
						GraySurf.fill((150,150,150,150))
						x0 = 0.2*self.game.WINDOWWIDTH
						y0 = int((self.game.WINDOWHEIGHT-self.game.HEIGHTCARD)/2)

						PileBoxSize = (0.6*self.game.WINDOWWIDTH,self.game.HEIGHTCARD)
						PileBox = pygame.draw.rect(self.game.DISPLAYSURF, self.game.Colors["GRAY"],
							( x0, y0 , PileBoxSize[0] , PileBoxSize[1] ), 4)
						self.game.DISPLAYSURF.blit(GraySurf, (0,0))

						# create cursor surface and cursor:

						SurfCursorSize = (0.4*self.game.WINDOWWIDTH, 0.033*self.game.WINDOWHEIGHT)
						SurfCursor = pygame.Surface(SurfCursorSize, pygame.SRCALPHA)   # per-pixel alpha
						SurfCursor.fill((40,40,40,255))
						x0SurfCursor = 0.3*self.game.WINDOWWIDTH
						y0SurfCursor = y0 + 1.5*self.game.HEIGHTCARD
						SurfCursorBlit = self.game.DISPLAYSURF.blit(SurfCursor, (x0SurfCursor,y0SurfCursor))

						pygame.draw.rect(self.game.DISPLAYSURF, self.game.Colors["GRAY"],
						( x0SurfCursor, y0SurfCursor , SurfCursorSize[0],SurfCursorSize[1] ), 4)

						# initialise cursor
						
						CursorPos = self.game.WINDOWWIDTH/2  # middle of cursor
						CursorSize = (0.04*self.game.WINDOWWIDTH, 0.033*self.game.WINDOWHEIGHT)

						Cursor = pygame.Surface(CursorSize, pygame.SRCALPHA)   # per-pixel alpha
						Cursor.fill((0,0,0,255))
						CursorBlit = self.game.DISPLAYSURF.blit(Cursor, (CursorPos-CursorSize[0]/2,y0 + 1.5*self.game.HEIGHTCARD))

						CursorSelected = False

						CursorPosMax = x0SurfCursor + SurfCursorSize[0] - CursorSize[0]/2
						CursorPosMin = x0SurfCursor + CursorSize[0]/2

						# pile down
						if PileDownAP.collidepoint(mousex,mousey):
							NotClickedOut = True
							
							# TODO : handle case where the pile is empty (just 1 card in it : division by 0 )
							# TODO : fetch the active player before so that WidthSeenCard depends on the selected player 
							WidthSeenCard = (PileBoxSize[0] - self.game.WIDTHCARD)/(len(self.game.Player1.PileDOWN)+1) # represent the width of a card displayed but not completely shown on a pile

							while NotClickedOut:
								#print("In here !")

								if PlayerSelected == 1:
									lenPileDOWN = len(self.game.Player1.PileDOWN)
									PileDownCurr = self.game.Player1.PileDOWN 
								else:
									lenPileDOWN = len(self.game.Player2.PileDOWN)
									PileDownCurr = self.game.Player2.PileDOWN 									

								i =lenPileDOWN*(CursorPos-CursorPosMin)/(CursorPosMax-CursorPosMin)
								j = 0
								for card in PileDownCurr:
									if j<i : # before the card i
										self.game.DrawCardOnBoard(card.color,card.number,PlayerSelected,LeftTop=[int(x0+j*WidthSeenCard),y0])
									elif j==i:
										self.game.DrawCardOnBoard(card.color,card.number,PlayerSelected,LeftTop=[int(x0+j*WidthSeenCard),y0])
									elif j>i:
										self.game.DrawCardOnBoard(card.color,card.number,PlayerSelected,LeftTop=[int(x0+(j-1)*WidthSeenCard+self.game.WIDTHCARD),y0])
									j+=1

								if PlayerSelected == 2:
									for card in self.game.Player2.PileDOWN :
										pass
															
								for event in pygame.event.get():
									if event.type == MOUSEBUTTONDOWN and event.button == 1 and not (PileBox.collidepoint(mousex,mousey) or SurfCursorBlit.collidepoint(mousex,mousey)):
										NotClickedOut = False
									elif event.type == MOUSEBUTTONDOWN and event.button == 1 and CursorBlit.collidepoint(mousex,mousey):
										CursorSelected = True
									elif event.type == MOUSEBUTTONUP and event.button == 1 and CursorSelected:
										CursorSelected = False
									elif event.type == MOUSEMOTION:
										mousex, mousey = event.pos
								
								if CursorSelected:
									CursorPos = mousex

									# limit the cursor to the surfcursor
									if CursorPos > CursorPosMax:
										CursorPos = CursorPosMax
									elif CursorPos < CursorPosMin:
										CursorPos = CursorPosMin

								# display Cursor and CursorBar
								SurfCursorBlit = self.game.DISPLAYSURF.blit(SurfCursor, (x0SurfCursor,y0SurfCursor))

								pygame.draw.rect(self.game.DISPLAYSURF, self.game.Colors["GRAY"],
								( x0SurfCursor, y0SurfCursor , SurfCursorSize[0],SurfCursorSize[1] ), 4)

								CursorBlit = self.game.DISPLAYSURF.blit(Cursor, (CursorPos-CursorSize[0]/2,y0 + 1.5*self.game.HEIGHTCARD))
								
								pygame.display.update()
								self.game.clock.tick(self.game.FPS) 

						elif PileUPAP.collidepoint(mousex,mousey):
							NotClickedOut = True
							
							# TODO : handle case where the pile is empty (just 1 card in it : division by 0 )
							WidthSeenCard = (PileBoxSize[0] - self.game.WIDTHCARD)/(len(self.game.Player1.PileDOWN)+1) # represent the width of a card displayed but not completely shown on a pile

							while NotClickedOut:
								#print("In here !")

								if PlayerSelected == 1:

									i = len(self.game.Player1.PileDOWN)*(CursorPos-CursorPosMin)/(CursorPosMax-CursorPosMin)
									j = 0
									for card in self.game.Player1.PileDOWN :
										if j<i : # before the card i
											self.game.DrawCardOnBoard(card.color,card.number,PlayerSelected,LeftTop=[int(x0+j*WidthSeenCard),y0])
										elif j==i:
											self.game.DrawCardOnBoard(card.color,card.number,PlayerSelected,LeftTop=[int(x0+j*WidthSeenCard),y0])
										elif j>i:
											self.game.DrawCardOnBoard(card.color,card.number,PlayerSelected,LeftTop=[int(x0+(j-1)*WidthSeenCard+self.game.WIDTHCARD),y0])
										j+=1

								if PlayerSelected == 2:
									for card in self.game.Player2.PileDOWN :
										pass
															
								for event in pygame.event.get():
									if event.type == MOUSEBUTTONDOWN and event.button == 1 and not (PileBox.collidepoint(mousex,mousey) or SurfCursorBlit.collidepoint(mousex,mousey)):
										NotClickedOut = False
									elif event.type == MOUSEBUTTONDOWN and event.button == 1 and CursorBlit.collidepoint(mousex,mousey):
										CursorSelected = True
									elif event.type == MOUSEBUTTONUP and event.button == 1 and CursorSelected:
										CursorSelected = False
									elif event.type == MOUSEMOTION:
										mousex, mousey = event.pos
								
								if CursorSelected:
									CursorPos = mousex

									# limit the cursor to the surfcursor
									if CursorPos > CursorPosMax:
										CursorPos = CursorPosMax
									elif CursorPos < CursorPosMin:
										CursorPos = CursorPosMin

								# display Cursor and CursorBar
								SurfCursorBlit = self.game.DISPLAYSURF.blit(SurfCursor, (x0SurfCursor,y0SurfCursor))

								pygame.draw.rect(self.game.DISPLAYSURF, self.game.Colors["GRAY"],
								( x0SurfCursor, y0SurfCursor , SurfCursorSize[0],SurfCursorSize[1] ), 4)

								CursorBlit = self.game.DISPLAYSURF.blit(Cursor, (CursorPos-CursorSize[0]/2,y0 + 1.5*self.game.HEIGHTCARD))
								
								pygame.display.update()
								self.game.clock.tick(self.game.FPS) 
						elif PileDownNAP.collidepoint(mousex,mousey):
							pass
						elif PileUPNAP.collidepoint(mousex,mousey): 
							pass
					elif boxRectCONCEDE.collidepoint(mousex,mousey):
						self.game.Concede()
						print('concede')
						break 
					elif boxRectEOT.collidepoint(mousex,mousey):
						if self.game.HasTheRightToEndTurn() == 1:
							self.conn.sendto("EOT".encode(), (self.addr, self.serverport))
						elif self.game.ActivePlayer != PlayerSelected:
							None
						else:
							GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
							GraySurf.fill((150,150,150,150))
							NotClickedOutEOTScreen = True
							x0 = 0.1*self.game.WINDOWWIDTH
							y0 = int(self.game.WINDOWHEIGHT/4)

							self.game.DISPLAYSURF.blit(GraySurf, (0,0))
							self.game.DISPLAYSURF.blit(self.game.Images["NoRightEOT"], (x0,y0))

							while NotClickedOutEOTScreen:

								for event in pygame.event.get():
									if event.type == MOUSEBUTTONDOWN and event.button == 1:
										NotClickedOutEOTScreen = False

								pygame.display.update()
								self.game.clock.tick(self.game.FPS) 	

				pygame.display.update()
				self.game.clock.tick(self.game.FPS)  
		finally:
			print("Quit")
			self.conn.sendto("QUI".encode(), (self.addr, self.serverport))


if __name__ == "__main__":
	g = GameClient()
	g.run()