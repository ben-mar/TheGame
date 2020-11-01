import sys
import socket
import select
import random
import pygame
from pygame.locals import *
from pygame import key
import TheGame


class GameClient:

	def __init__(self, addr="192.168.1.6", serverport=9009):
		self.clientport = random.randrange(8000, 8999)
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind to localhost - set to external ip to connect from other computers
		self.addr = addr
		self.conn.bind((self.addr, self.clientport))
		self.serverport = serverport		
		self.read_list = [self.conn]
		self.write_list = []		
		self.setup_pygame()
  
	def setup_pygame(self):
		self.game = TheGame.TheGamePlay()
		pygame.display.set_caption('The Game')

	def Encode(self,
			   objectToEncode,
			   typeToEncode :str  = 'ListOfCards' 
			   ) -> str:
		
		if typeToEncode == 'ListOfCards':
			if not isinstance(objectToEncode, list):
				raise("The ListOfCards for the encoding is not an list type !")
			ListOfCards = objectToEncode	
			# Encodes the messages
			if ListOfCards == []:
				return ''
			else:
				str_encoded = ''
				for card in ListOfCards:
					str_encoded += str(card.number)+'$'+card.color+';'
				str_encoded = str_encoded.rstrip(';')
				return(str_encoded)	

		elif typeToEncode == 'Boolean':
			if not isinstance(objectToEncode, bool):
				raise("The Boolean for the encoding is not an bool type !")
			boolean = objectToEncode
			if boolean:
				return "True"
			else :
				return "False"

		elif typeToEncode == 'CoupleCardPile':
			if not isinstance(objectToEncode, list):
				raise("The CoupleCardPile for the encoding is not an list type !")			
			CoupleCardPile = objectToEncode	
			# Encodes the messages
			if CoupleCardPile == []:
				return ''
			else:
				str_encoded = ''
				for couple in CoupleCardPile:
					card, pile = couple
					str_encoded += str(card.number)+'$'+card.color+'#'+pile+';'
				str_encoded = str_encoded.rstrip(';')
				return(str_encoded)	
		else :
			raise("Not treated yet, the typeToEncode is not correct ! : {}".format(typeToEncode))

	def Decode(self,
			   objectToDecode : str,
			   typeToDecode :str  = 'ListOfCards' 
			   ):

		if typeToDecode == 'ListOfCards':		
			# Decodes the messages
			ListOfCards = [] 
			if objectToDecode =='':
				return ListOfCards
			else:
				spliting = objectToDecode.split(';')
				for encoded_card in spliting:
					number,color = encoded_card.split('$') 
					ListOfCards.append(TheGame.Card(int(number),color))
				return ListOfCards

		elif typeToDecode == 'Boolean':
			if objectToDecode == "True":
				return True
			else :
				return False
		elif typeToDecode == 'CoupleCardPile':
			ListOfCouples = [] 
			if objectToDecode =='':
				return ListOfCouples
			else:
				spliting = objectToDecode.split(';')
				for encoded_couple in spliting:
					encoded_card, pile = encoded_couple.split('#')
					number,color = encoded_card.split('$') 
					ListOfCouples.append((TheGame.Card(int(number),color),pile))
				return ListOfCouples
		else :
			raise("Not treated yet, the typeToEncode is not correct ! : {}".format(typeToDecode))	

	def run(self):

		running = True

		mousex = 0 # used to store x coordinate of mouse event
		mousey = 0 # used to store y coordinate of mouse event

		selected = False
		unselected = False
		Selection = False

		# First screen of Player selection
		while not Selection:
			self.game.DISPLAYSURF.blit(self.game.Images["BGsurface"], (0,0))
			Player1Box = self.game.DISPLAYSURF.blit(self.game.Images["Player1Img"], (int(0.3*self.game.WINDOWWIDTH),int(0.45*self.game.WINDOWHEIGHT)))
			Player2Box = self.game.DISPLAYSURF.blit(self.game.Images["Player2Img"], (int(0.5*self.game.WINDOWWIDTH),int(0.45*self.game.WINDOWHEIGHT)))

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
			NotSU3 = True
			while NotSU1 or NotSU2 or NotSU3:
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
							self.game.Hands = {'P1' : self.game.Player1.hand, 'P2' : self.game.Player2.hand}
							self.game.ActivePlayer = int(ActivePlayer)
							NotSU1 = False
						if cmd == 'SU2': # setup new player piles
							PileUP1,PileDN1 , PileUP2,PileDN2 = msg.split('|')
							self.game.Player1.PileUP = self.Decode(PileUP1)
							self.game.Player1.PileDOWN = self.Decode(PileDN1)
							self.game.Player2.PileUP = self.Decode(PileUP2)
							self.game.Player2.PileDOWN = self.Decode(PileDN2)	
							self.game.Piles = {"P1_UP" : self.game.Player1.PileUP,
											   "P1_DOWN" : self.game.Player1.PileDOWN,
											   "P2_UP" : self.game.Player2.PileUP,
											   "P2_DOWN" : self.game.Player2.PileDOWN}									
							NotSU2 = False
						if cmd == 'SU3': # setup new PlayedThisTurn, PlayedOnOpponnentPiles and GameOver variables
							PlayedThisTurnP1 ,PlayedThisTurnP2 ,\
							PlayedOnOpponnentPilesP1, PlayedOnOpponnentPilesP2,\
							GameOverP1, GameOverP2  = msg.split('|')

							self.game.PlayedThisTurn['P1'] = self.Decode(PlayedThisTurnP1,typeToDecode='CoupleCardPile')
							self.game.PlayedThisTurn['P2'] = self.Decode(PlayedThisTurnP2,typeToDecode='CoupleCardPile')
							self.game.PlayedOnOpponnentPiles['P1'] = self.Decode(PlayedOnOpponnentPilesP1,typeToDecode='Boolean')
							self.game.PlayedOnOpponnentPiles['P2'] = self.Decode(PlayedOnOpponnentPilesP2,typeToDecode='Boolean')
							self.game.GameOver['P1'] = self.Decode(GameOverP1,typeToDecode='Boolean')
							self.game.GameOver['P2'] = self.Decode(GameOverP2,typeToDecode='Boolean')
							NotSU3 = False
							# print(self.game.PlayedThisTurn)
							# print(self.game.PlayedOnOpponnentPiles)
							# print(self.game.GameOver)
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

						if cmd == "PLC":  # Play a Card

							Pile,CardStr,CurrentPlayerSelected = msg.split(";")
							Card = self.Decode(CardStr)[0]
							self.game.Play(Pile,Card,int(CurrentPlayerSelected))

							# message to check piles, hand and deck
							# TODO might be a problem if the len is 0
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

							# returns True if the player has lost the game
							if self.game.ActivePlayer == PlayerSelected:
								if self.game.CheckIfLoose(PlayerSelected):
									self.conn.sendto(("GMO"+str(PlayerSelected)).encode(), (self.addr, self.serverport))

						elif cmd == "EOT": # End Of Turn
							
							self.game.EndOfTurn()

						elif cmd == "CAP": # Change ActivePlayer

							self.game.ChangeActivePlayer()
							if self.game.ActivePlayer == PlayerSelected:

								# returns True if the player has lost the game
								if self.game.CheckIfLoose(PlayerSelected):
									self.conn.sendto(("GMO"+str(PlayerSelected)).encode(), (self.addr, self.serverport))

						elif cmd == "GMO" :
							self.game.GameOver['P'+msg] = True

						elif cmd == "GMP" :
							self.game.GameOver['P'+msg] = False

						elif cmd == "UND":
							self.game.Undo()			

							# returns True if the player has lost the game
							if self.game.ActivePlayer == PlayerSelected:
								if self.game.CheckIfLoose(PlayerSelected):
									self.conn.sendto(("GMO"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
								else :
									self.conn.sendto(("GMP"+str(PlayerSelected)).encode(), (self.addr, self.serverport))

						elif cmd == 'UPD' : 

							Hand1, Hand2, Deck1, Deck2 = msg.split('|')
							self.game.Player1.hand = self.Decode(Hand1)
							self.game.Player1.deck = self.Decode(Deck1)
							self.game.Player2.hand = self.Decode(Hand2)
							self.game.Player2.deck = self.Decode(Deck2)
							self.game.Hands = {'P1' : self.game.Player1.hand, 'P2' : self.game.Player2.hand}


				mouseClicked = False
				unselected = False

				self.game.DISPLAYSURF.blit(self.game.Images["BGsurface"], (0,0))

			
				(PileDownAP,PileUPAP,PileDownNAP,PileUPNAP,APDeck,NAPDeck) = self.game.DrawBoard(PlayerSelected)

				for event in pygame.event.get(): # event handling loop
					mod = key.get_mods()
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
					elif event.type == KEYDOWN and mod and KMOD_CTRL : # event.type == KEYDOWN and event.unicode == 'a':
						if event.type == KEYDOWN and event.key ==  K_w : # we want the azerty for z: event.unicode == 'a' a in
							# send the undo command
							self.conn.sendto(("UND").encode(), (self.addr, self.serverport))
 
					
				
				self.game.DisplayActivePlayer()  
				self.game.OnACard(mousex,mousey,PlayerSelected)
				boxRectEOT = self.game.DISPLAYSURF.blit(self.game.Images["EndOfTurn"], (int(0.8*self.game.WINDOWWIDTH),int(0.45*self.game.WINDOWHEIGHT)))
				boxRectQUIT = self.game.DISPLAYSURF.blit(self.game.Images["Quit"], (int(0.8*self.game.WINDOWWIDTH),0))

				if self.game.GameOver['P1']:
					if PlayerSelected == 1:
						self.game.DISPLAYSURF.blit(self.game.Images["YouLostGold"],(0,0))
					# if PlayerSelected == 2:
					# 	self.game.DISPLAYSURF.blit(self.game.Images["YouWonSilver"],(0,0))
				if self.game.GameOver['P2']:
					# if PlayerSelected == 1:
					# 	self.game.DISPLAYSURF.blit(self.game.Images["YouWonGold"],(0,0))
					if PlayerSelected == 2:
						self.game.DISPLAYSURF.blit(self.game.Images["YouLostSilver"],(0,0))


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
							self.conn.sendto(("PLCP1_DOWN;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(),  (self.addr, self.serverport))
						elif PileUPAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLCP1_UP;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
						elif PileDownNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLCP2_DOWN;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
						elif PileUPNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLCP2_UP;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
					if self.game.ActivePlayer == 2 :# and self.game.ActivePlayer == PlayerSelected:
						CardToPlay = self.game.Player2.hand[CardIndex]
						if PileDownAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLCP2_DOWN;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
						elif PileUPAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLCP2_UP;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
						elif PileDownNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLCP1_DOWN;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(), (self.addr, self.serverport))
						elif PileUPNAP.collidepoint(mousex,mousey):
							self.conn.sendto(("PLCP1_UP;"+self.Encode([CardToPlay])+";"+str(PlayerSelected)).encode(), (self.addr, self.serverport))

				# EOT or concede block
				if mouseClicked :

					# block to improve 
					# Click to see the piles
					if self.game.IsOnAPile(mousex, mousey):

						GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
						GraySurf.fill((150,150,150,150))
						x0 = int(0.2*self.game.WINDOWWIDTH)
						y0 = int((self.game.WINDOWHEIGHT-self.game.HEIGHTCARD)/2)

						PileBoxSize = (int(0.6*self.game.WINDOWWIDTH),int(self.game.HEIGHTCARD))
						PileBox = pygame.draw.rect(self.game.DISPLAYSURF, self.game.Colors["GRAY"],
							( x0, y0 , PileBoxSize[0] , PileBoxSize[1] ), 4)
						self.game.DISPLAYSURF.blit(GraySurf, (0,0))

						# create cursor surface and cursor:

						SurfCursorSize = (int(0.4*self.game.WINDOWWIDTH), int(0.033*self.game.WINDOWHEIGHT))
						SurfCursor = pygame.Surface(SurfCursorSize, pygame.SRCALPHA)   # per-pixel alpha
						SurfCursor.fill((40,40,40,255))
						x0SurfCursor = int(0.3*self.game.WINDOWWIDTH)
						y0SurfCursor = int(y0 + 1.5*self.game.HEIGHTCARD)
						SurfCursorBlit = self.game.DISPLAYSURF.blit(SurfCursor, (x0SurfCursor,y0SurfCursor))

						pygame.draw.rect(self.game.DISPLAYSURF, self.game.Colors["GRAY"],
						( x0SurfCursor, y0SurfCursor , SurfCursorSize[0],SurfCursorSize[1] ), 4)

						# initialise cursor
						
						CursorPos = self.game.WINDOWWIDTH/2  # middle of cursor
						CursorSize = (int(0.04*self.game.WINDOWWIDTH), int(0.033*self.game.WINDOWHEIGHT))

						Cursor = pygame.Surface(CursorSize, pygame.SRCALPHA)   # per-pixel alpha
						Cursor.fill((0,0,0,255))
						CursorBlit = self.game.DISPLAYSURF.blit(Cursor, (int(CursorPos-CursorSize[0]/2),int(y0 + 1.5*self.game.HEIGHTCARD)))

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

								CursorBlit = self.game.DISPLAYSURF.blit(Cursor, (int(CursorPos-CursorSize[0]/2),int(y0 + 1.5*self.game.HEIGHTCARD)))
								
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

								CursorBlit = self.game.DISPLAYSURF.blit(Cursor, (int(CursorPos-CursorSize[0]/2),int(y0 + 1.5*self.game.HEIGHTCARD)))
								
								pygame.display.update()
								self.game.clock.tick(self.game.FPS) 
						elif PileDownNAP.collidepoint(mousex,mousey):
							pass
						elif PileUPNAP.collidepoint(mousex,mousey): 
							pass
					elif boxRectQUIT.collidepoint(mousex,mousey):
						#self.game.Concede()
						#print('concede')
						break 
					elif boxRectEOT.collidepoint(mousex,mousey):
						if self.game.HasTheRightToEndTurn() == 1:
							self.conn.sendto("EOT".encode(), (self.addr, self.serverport))
						elif self.game.ActivePlayer == PlayerSelected and self.game.HasTheRightToEndTurn() ==0 :
							GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
							GraySurf.fill((150,150,150,150))
							NotClickedOutEOTScreen = True
							x0 = int(0.1*self.game.WINDOWWIDTH)
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


			# One player has lost the game 
			if self.game.GameOver['P1']:
				if PlayerSelected == 1:
					# display you lost
					GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
					GraySurf.fill((150,150,150,150))
					NotClickedOutYouLostGoldScreen = True
					x0 = int((self.game.WINDOWWIDTH-0.1*self.game.WINDOWWIDTH)/2)
					y0 = int((self.game.WINDOWHEIGHT-0.06*self.game.WINDOWHEIGHT)/2)

					self.game.DISPLAYSURF.blit(GraySurf, (0,0))
					self.game.DISPLAYSURF.blit(self.game.Images["YouLostGold"], (x0,y0))

					while NotClickedOutYouLostGoldScreen:

						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN and event.button == 1:
								NotClickedOutYouLostGoldScreen = False

						pygame.display.update()
						self.game.clock.tick(self.game.FPS) 
				if PlayerSelected == 2:
					# display you won
					GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
					GraySurf.fill((150,150,150,150))
					NotClickedOutYouWonSilverScreen = True
					x0 = int((self.game.WINDOWWIDTH-0.1*self.game.WINDOWWIDTH)/2)
					y0 = int((self.game.WINDOWHEIGHT-0.06*self.game.WINDOWHEIGHT)/2)

					self.game.DISPLAYSURF.blit(GraySurf, (0,0))
					self.game.DISPLAYSURF.blit(self.game.Images["YouWonSilver"], (x0,y0))

					while NotClickedOutYouWonSilverScreen:

						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN and event.button == 1:
								NotClickedOutYouWonSilverScreen = False

						pygame.display.update()
						self.game.clock.tick(self.game.FPS) 
			elif self.game.GameOver['P2']:
				if PlayerSelected == 1:
					# display you won
					GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
					GraySurf.fill((150,150,150,150))
					NotClickedOutYouWonGoldScreen = True
					x0 = int((self.game.WINDOWWIDTH-0.1*self.game.WINDOWWIDTH)/2)
					y0 = int((self.game.WINDOWHEIGHT-0.06*self.game.WINDOWHEIGHT)/2)

					self.game.DISPLAYSURF.blit(GraySurf, (0,0))
					self.game.DISPLAYSURF.blit(self.game.Images["YouWonGold"], (x0,y0))

					while NotClickedOutYouWonGoldScreen:

						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN and event.button == 1:
								NotClickedOutYouWonGoldScreen = False

						pygame.display.update()
						self.game.clock.tick(self.game.FPS) 
				if PlayerSelected == 2:
					# display you lost
					GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
					GraySurf.fill((150,150,150,150))
					NotClickedOutYouLostSilverScreen = True
					x0 = int((self.game.WINDOWWIDTH-0.1*self.game.WINDOWWIDTH)/2)
					y0 = int((self.game.WINDOWHEIGHT-0.06*self.game.WINDOWHEIGHT)/2)

					self.game.DISPLAYSURF.blit(GraySurf, (0,0))
					self.game.DISPLAYSURF.blit(self.game.Images["YouLostSilver"], (x0,y0))

					while NotClickedOutYouLostSilverScreen:

						for event in pygame.event.get():
							if event.type == MOUSEBUTTONDOWN and event.button == 1:
								NotClickedOutYouLostSilverScreen = False

						pygame.display.update()
						self.game.clock.tick(self.game.FPS) 			

			
		finally:
			print("Quit")
			self.conn.sendto("QUI".encode(), (self.addr, self.serverport))


if __name__ == "__main__":
	g = GameClient()
	g.run()