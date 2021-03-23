import sys
import copy
import socket
import select
import random
import pygame
from pygame.locals import *
from pygame import key
import TheGame
#from button import Button

class GameClient:

	def __init__(self, addr="127.0.0.1", serverport=9009):
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
		self.game = TheGame.GameFrontEnd()
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

	def SelectionScreen(self,
					    Selection : bool
					    ) -> None:

		"""
		The functions that displays the SelectionScreen as long as the selection is not done
		"""

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
				elif event.type == MOUSEBUTTONDOWN and event.button == 1 and Player1Box.collidepoint(self.mousex,self.mousey):
					self.game.PlayerSelected = 1
					Selection = True
				elif event.type == MOUSEBUTTONDOWN and event.button == 1 and Player2Box.collidepoint(self.mousex,self.mousey):
					self.game.PlayerSelected = 2
					Selection = True
				elif event.type == MOUSEMOTION:
					self.mousex, self.mousey = event.pos

			pygame.display.update()
			self.game.clock.tick(self.game.FPS)  

	def SetupClientServer(self,
						  NotSU1 : bool,
						  NotSU2 : bool,
						  NotSU3 : bool
						  ) -> None:

		"""
		Functions that sets up the piles, hand and decks by connecting to the server
		"""
		
		while NotSU1 or NotSU2 or NotSU3:
			readable, _, _ = (
					select.select(self.read_list, self.write_list, [], 0)
				)
			for f in readable:
				if f is self.conn:
					message, _ = f.recvfrom(65536) # find the best size here
					message = message.decode()
					if len(message) >= 3:
						command = message[0:3]
						message = message[3:]
					if command == 'SU1': # setup new player hand and deck
						Hand1, Hand2, Deck1, Deck2, ActivePlayer = message.split('|')
						self.game.Player1.hand = self.Decode(Hand1)
						self.game.Player1.deck = self.Decode(Deck1)
						self.game.Player2.hand = self.Decode(Hand2)
						self.game.Player2.deck = self.Decode(Deck2)
						self.game.Hands = {'P1' : self.game.Player1.hand, 'P2' : self.game.Player2.hand}
						self.game.HandsFrontEnd = {'P1' : copy.copy(self.game.Hands['P1']),
												'P2':  copy.copy(self.game.Hands['P2'])}
						self.game.Decks = {'P1' : self.game.Player1.deck, 'P2' : self.game.Player2.deck}
						self.game.ActivePlayer = int(ActivePlayer)
						# TODO add setup for Zones in hand with [(card, zone),(card,zone),...]
						NotSU1 = False
					if command == 'SU2': # setup new player piles
						PileUP1,PileDN1 , PileUP2,PileDN2 = message.split('|')
						self.game.Player1.PileUP = self.Decode(PileUP1)
						self.game.Player1.PileDOWN = self.Decode(PileDN1)
						self.game.Player2.PileUP = self.Decode(PileUP2)
						self.game.Player2.PileDOWN = self.Decode(PileDN2)	
						self.game.Piles = {"P1_UP" : self.game.Player1.PileUP,
										"P1_DOWN" : self.game.Player1.PileDOWN,
										"P2_UP" : self.game.Player2.PileUP,
										"P2_DOWN" : self.game.Player2.PileDOWN}									
						NotSU2 = False
					if command == 'SU3': # setup new PlayedThisTurn, PlayedOnOpponnentPiles and GameOver variables
						PlayedThisTurnP1 ,PlayedThisTurnP2 ,\
						PlayedOnOpponnentPilesP1, PlayedOnOpponnentPilesP2,\
						GameOverP1, GameOverP2  = message.split('|')

						self.game.PlayedThisTurn['P1'] = self.Decode(PlayedThisTurnP1,typeToDecode='CoupleCardPile')
						self.game.PlayedThisTurn['P2'] = self.Decode(PlayedThisTurnP2,typeToDecode='CoupleCardPile')
						self.game.PlayedOnOpponnentPiles['P1'] = self.Decode(PlayedOnOpponnentPilesP1,typeToDecode='Boolean')
						self.game.PlayedOnOpponnentPiles['P2'] = self.Decode(PlayedOnOpponnentPilesP2,typeToDecode='Boolean')
						self.game.GameOver['P1'] = self.Decode(GameOverP1,typeToDecode='Boolean')
						self.game.GameOver['P2'] = self.Decode(GameOverP2,typeToDecode='Boolean')
						NotSU3 = False

	def RunCommand(self,
				   command : str,
				   message : str,
				   CardIndex : int
				   ) -> None :

		"""
		Runs the command "command" sent by the server
		"""

		# the verbosity is True if the selected player is the actual player 
		verbosity = (self.game.ActivePlayer == self.game.PlayerSelected)

		if command == "PLC":  # Play a Card
			Pile,CardStr,CurrentPlayerSelected = message.split(";")
			Card = self.Decode(CardStr)[0]
			# TODO check if the card to play is in the moving zone and play it only if it's the case

			played = self.game.Play(Pile, Card, int(CurrentPlayerSelected), verbosity)
			if (not played) & (int(CurrentPlayerSelected) == self.game.PlayerSelected) :
				self.game.HandsFrontEnd['P'+str(self.game.PlayerSelected)].insert(CardIndex,self.game.Moving[0])
			self.game.Moving = []
				
			# message to check piles, hand and deck
			# TODO might be a problem if the len is 0
			LenghtHands = len(self.game.Player1.hand)*len(self.game.Player2.hand)
			LenghtDecks = len(self.game.Player1.deck)*len(self.game.Player2.deck)
			if LenghtDecks*LenghtHands > 0 :

				message = "CK1"+self.Encode(self.game.Player1.hand)
				message += "|" +self.Encode(self.game.Player2.hand)
				message += "|" +self.Encode(self.game.Player1.deck)
				message += "|" +self.Encode(self.game.Player2.deck)

				message2 = "CK2"+self.Encode(self.game.Player1.PileUP)
				message2 += "|"+self.Encode(self.game.Player1.PileDOWN)
				message2 += "|"+self.Encode(self.game.Player2.PileUP)
				message2 += "|"+self.Encode(self.game.Player2.PileDOWN)

				self.conn.sendto(message.encode(), (self.addr, self.serverport))
				self.conn.sendto(message2.encode(), (self.addr, self.serverport))

			# returns True if the player has lost the game
			if self.game.ActivePlayer == self.game.PlayerSelected:
				if self.game.CheckIfLoose(self.game.PlayerSelected):
					self.conn.sendto(("GMO"+str(self.game.PlayerSelected)).encode(), (self.addr, self.serverport))

		elif command == "EOT": # End Of Turn		
			self.game.EndOfTurn()
			self.game.HandsFrontEnd = {'P1' : copy.copy(self.game.Hands['P1']),
									   'P2':  copy.copy(self.game.Hands['P2'])}					

		elif command == "CAP": # Change ActivePlayer
			self.game.ChangeActivePlayer()
			if self.game.ActivePlayer == self.game.PlayerSelected:
				# returns True if the player has lost the game
				if self.game.CheckIfLoose(self.game.PlayerSelected):
					self.conn.sendto(("GMO"+str(self.game.PlayerSelected)).encode(), (self.addr, self.serverport))

		elif command == "GMO" :
			self.game.GameOver['P' + message] = True

		elif command == "GMP" :
			self.game.GameOver['P' + message] = False

		elif command == "UND":
			self.game.Undo(verbosity)			
			# TODO if we effectively put back a card in the hand, we must associate the zone hand to it
			self.game.HandsFrontEnd = {'P1' : copy.copy(self.game.Hands['P1']),
									   'P2':  copy.copy(self.game.Hands['P2'])}

			# returns True if the player has lost the game
			if self.game.ActivePlayer == self.game.PlayerSelected:
				if self.game.CheckIfLoose(self.game.PlayerSelected):
					self.conn.sendto(("GMO"+str(self.game.PlayerSelected)).encode(), (self.addr, self.serverport))
				else :
					self.conn.sendto(("GMP"+str(self.game.PlayerSelected)).encode(), (self.addr, self.serverport))
		
		elif command == "SRT":
			Cardstr,index,CurrentPlayerSelected = message.split(";")
			Card = self.Decode(Cardstr)[0]
			self.game.SortHand(int(index),Card,CurrentPlayerSelected)
			self.game.Moving = []
			self.game.HandsFrontEnd = {'P1' : copy.copy(self.game.Hands['P1']),
									   'P2':  copy.copy(self.game.Hands['P2'])}

		elif command == 'UPD' : 
			Hand1, Hand2, Deck1, Deck2 = message.split('|')
			self.game.Player1.hand = self.Decode(Hand1)
			self.game.Player1.deck = self.Decode(Deck1)
			self.game.Player2.hand = self.Decode(Hand2)
			self.game.Player2.deck = self.Decode(Deck2)
			self.game.Hands = {'P1' : self.game.Player1.hand, 'P2' : self.game.Player2.hand}


	def ShowPilesScreen(self,
						index : int
						) -> None:
		"""
		Displays the piles Screen
		"""

		GraySurf = pygame.Surface((self.game.WINDOWWIDTH, self.game.WINDOWHEIGHT), pygame.SRCALPHA)   # per-pixel alpha
		GraySurf.fill((150,150,150,150))
		x0 = int(0.2*self.game.WINDOWWIDTH)
		y0 = int((self.game.WINDOWHEIGHT-self.game.HEIGHTCARD)/2)

		PileBoxSize = (int(0.6*self.game.WINDOWWIDTH),int(self.game.HEIGHTCARD))
		PileBox = pygame.draw.rect(self.game.DISPLAYSURF, self.game.ColorsCodes["Gray"],
			( x0, y0 , PileBoxSize[0] , PileBoxSize[1] ), 4)
		self.game.DISPLAYSURF.blit(GraySurf, (0,0))

		# create cursor surface and cursor:

		SurfCursorSize = (int(0.4*self.game.WINDOWWIDTH), int(0.033*self.game.WINDOWHEIGHT))
		SurfCursor = pygame.Surface(SurfCursorSize, pygame.SRCALPHA)   # per-pixel alpha
		SurfCursor.fill((40,40,40,255))
		x0SurfCursor = int(0.3*self.game.WINDOWWIDTH)
		y0SurfCursor = int(y0 + 1.5*self.game.HEIGHTCARD)
		SurfCursorBlit = self.game.DISPLAYSURF.blit(SurfCursor, (x0SurfCursor,y0SurfCursor))

		pygame.draw.rect(self.game.DISPLAYSURF, self.game.ColorsCodes["Gray"],
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

		NotClickedOut = True		
		DisplayedPile = self.game.Piles[self.mapping_play_card[(index,self.game.PlayerSelected)]]


		# TODO : handle case where the pile is empty (just 1 card in it : division by 0 )
		# TODO : fetch the active player before so that WidthSeenCard depends on the selected player 
		WidthSeenCard = (PileBoxSize[0] - self.game.WIDTHCARD)/(len(DisplayedPile)+1) # represent the width of a card displayed but not completely shown on a pile

		while NotClickedOut:
							

			i =len(DisplayedPile)*(CursorPos-CursorPosMin)/(CursorPosMax-CursorPosMin)
			j = 0
			for card in DisplayedPile:
				if j<i : # before the card i
					self.game.DrawCardOnBoard(card,LeftTop=[int(x0+j*WidthSeenCard),y0])
				elif j==i:
					self.game.DrawCardOnBoard(card,LeftTop=[int(x0+j*WidthSeenCard),y0])
				elif j>i:
					self.game.DrawCardOnBoard(card,LeftTop=[int(x0+(j-1)*WidthSeenCard+self.game.WIDTHCARD),y0])
				j+=1

										
			for event in pygame.event.get():
				if event.type == MOUSEBUTTONDOWN and event.button == 1 and not (PileBox.collidepoint(self.mousex,self.mousey) or SurfCursorBlit.collidepoint(self.mousex,self.mousey)):
					NotClickedOut = False
				elif event.type == MOUSEBUTTONDOWN and event.button == 1 and CursorBlit.collidepoint(self.mousex,self.mousey):
					CursorSelected = True
				elif event.type == MOUSEBUTTONUP and event.button == 1 and CursorSelected:
					CursorSelected = False
				elif event.type == MOUSEMOTION:
					self.mousex, self.mousey = event.pos
			
			if CursorSelected:
				CursorPos = self.mousex

				# limit the cursor to the surfcursor
				if CursorPos > CursorPosMax:
					CursorPos = CursorPosMax
				elif CursorPos < CursorPosMin:
					CursorPos = CursorPosMin

			# display Cursor and CursorBar
			SurfCursorBlit = self.game.DISPLAYSURF.blit(SurfCursor, (x0SurfCursor,y0SurfCursor))

			pygame.draw.rect(self.game.DISPLAYSURF, self.game.ColorsCodes["Gray"],
			( x0SurfCursor, y0SurfCursor , SurfCursorSize[0],SurfCursorSize[1] ), 4)

			CursorBlit = self.game.DISPLAYSURF.blit(Cursor, (int(CursorPos-CursorSize[0]/2),int(y0 + 1.5*self.game.HEIGHTCARD)))
			
			pygame.display.update()
			self.game.clock.tick(self.game.FPS) 


	def run(self
			) -> None:

		"""
		Principal function, that makes the game run		
		"""

		running = True

		self.mousex = 0 # used to store x coordinate of mouse event
		self.mousey = 0 # used to store y coordinate of mouse event

		selected = False
		unselected = False
		Selection = False


		self.SelectionScreen(Selection = Selection) 
 
			
		try:
			# Initialize connection to server
			self.conn.sendto(("NEW"+str(self.game.PlayerSelected)).encode(), (self.addr, self.serverport))
			
			# The first value represent the index of the pile in the list [PileUPAP,PileDownAP,PileUPNAP,PileDownNAP]
			# The second value represent the selected player.
			# (1,2) means that I selected the PileDownAP pile, and that I'm player 2
			
			self.mapping_play_card = {(0,1): 'P1_UP',(1,1): 'P1_DOWN',
									  (2,1): 'P2_UP',(3,1): 'P2_DOWN',
									  (0,2): 'P2_UP',(1,2): 'P2_DOWN',
									  (2,2): 'P1_UP',(3,2): 'P1_DOWN'}

			# setup of the piles
			NotSU1 = True
			NotSU2 = True
			NotSU3 = True

			self.SetupClientServer(NotSU1, NotSU2, NotSU3)


			# the game
			# Initialisation
			CardIndex = 0

			while running:

				# select on specified file descriptors
				readable, _, _ = (select.select(self.read_list, self.write_list, [], 0)	)
				for f in readable:
					if f is self.conn:
						message, _ = f.recvfrom(65536)
						message= message.decode()

						if len(message) >= 3:

							command = message[0:3]
							message = message[3:]					

						self.RunCommand(command, message, CardIndex)

				# re-initialisation of dynamic variables
				mouseClicked = False
				unselected = False

				self.game.DISPLAYSURF.blit(self.game.Images["BGsurface"], (0,0))
				self.game.DisplayActivePlayer()  
				FrontEndHand, Piles, Decks = self.game.DrawBoard()

				for event in pygame.event.get(): # event handling loop
					mod = key.get_mods()
					if event.type == pygame.VIDEORESIZE: # resize
						self.game.DISPLAYSURF = pygame.display.set_mode((event.w, event.h),pygame.RESIZABLE)
						self.game.DefineSizes()
						self.game.DefineImages()
					if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
						pygame.quit()
						sys.exit()
					elif event.type == MOUSEMOTION:
						self.mousex, self.mousey = event.pos
					for index,cardFrontHand in enumerate(FrontEndHand):
						cardZone = cardFrontHand[0]
						if event.type == MOUSEBUTTONDOWN and event.button == 1 and cardZone.collidepoint(self.mousex, self.mousey):
							self.mousex, self.mousey = event.pos
							mouseClicked = True
							selected = True
							CardIndex = index					
					if event.type == MOUSEBUTTONUP and event.button == 1 and selected:
						selected = False
						unselected = True
						self.mousex, self.mousey = event.pos
					elif event.type == MOUSEBUTTONDOWN and event.button == 1 :
						self.mousex, self.mousey = event.pos
						mouseClicked = True
					elif event.type == KEYDOWN and mod and KMOD_CTRL : # event.type == KEYDOWN and event.unicode == 'a':
						if event.type == KEYDOWN and event.key ==  K_z : # we want the azerty for z: event.unicode == 'a' a in
							if self.game.PlayedThisTurn['P'+str(self.game.PlayerSelected)] != []:
								self.conn.sendto(("UND").encode(), (self.addr, self.serverport))
 
				# Highlight the card we're on
				for cardFrontHand in FrontEndHand:
					cardZone = cardFrontHand[0]
					if cardZone.collidepoint(self.mousex, self.mousey):
						LeftTopx, LeftTopy = cardFrontHand[1]
						pygame.draw.rect(self.game.DISPLAYSURF, self.game.HIGHLIGHTCOLOR,
							(LeftTopx, LeftTopy, self.game.WIDTHCARD, self.game.HEIGHTCARD), 4)

				# TODO put buttons here ?
				boxRectEOT = self.game.DISPLAYSURF.blit(self.game.Images["EndOfTurn"], (int(0.8*self.game.WINDOWWIDTH),int(0.45*self.game.WINDOWHEIGHT)))
				boxRectQUIT = self.game.DISPLAYSURF.blit(self.game.Images["Quit"], (int(0.8*self.game.WINDOWWIDTH),0))

				# Shows the "Won or lost" indicator in the upper left corner of the screen
				if self.game.GameOver['P'+str(self.game.PlayerSelected)]:
						self.game.DISPLAYSURF.blit(self.game.Images["YouLost"+self.game.color['P'+str(self.game.PlayerSelected)]],(0,0))

				# shows the number of cards of the players
				for index, deck in enumerate(Decks):
					# index == 0 : SelectedPlayer deck, index == 1 : Non SelectedPlayer deck
					if deck.collidepoint(self.mousex,self.mousey) :
						LeftTopx = int((self.game.WINDOWWIDTH + (7.8*index-4.4)*self.game.WIDTHCARD)/2)
						LeftTopy = int((-2*index+4.5)*self.game.HEIGHTCARD)
						label = self.game.myfont.render(str(len(self.game.Decks['P'+str(index+1)])), 1,
														self.game.ColorsCodes[self.game.color['P'+str(index+1)]])
						self.game.DISPLAYSURF.blit(label, (LeftTopx,LeftTopy))

				# we move the image selected
				if selected: 
					self.game.MoveACard(self.mousex, self.mousey, CardIndex)

				# we play the card on the pile or we sort the hand	
				if unselected:
					play_tmp = False
					if self.game.PlayerSelected == self.game.ActivePlayer:
						for index, pile in enumerate(Piles):
							if pile.collidepoint(self.mousex, self.mousey):
								CardToPlay = self.game.Moving[0]
								message_to_encode = 'PLC' + self.mapping_play_card[(index,self.game.PlayerSelected)] + ';'
								message_to_encode += self.Encode([CardToPlay]) + ';' + str(self.game.PlayerSelected)
								self.conn.sendto(message_to_encode.encode(),  (self.addr, self.serverport))
								play_tmp = True
					for index, cardFrontHand in enumerate(FrontEndHand):
						cardZone = cardFrontHand[0]
						if cardZone.collidepoint(self.mousex, self.mousey) and not play_tmp:
							message_to_encode = 'SRT' + self.Encode(self.game.Moving) + ';' + str(index) + ';' + str(self.game.PlayerSelected)
							self.conn.sendto(message_to_encode.encode(),  (self.addr, self.serverport))
					if self.game.Moving != [] and not play_tmp:
						self.game.HandsFrontEnd['P' + str(self.game.PlayerSelected)].insert(CardIndex,self.game.Moving[0])	
						self.game.Moving = []
										
		

				# Pile, EOT or concede block
				if mouseClicked :
					for index, pile in enumerate(Piles):
						if pile.collidepoint(self.mousex, self.mousey):
							self.ShowPilesScreen(index)

					if boxRectQUIT.collidepoint(self.mousex,self.mousey):
						#self.game.Concede()
						#print('concede')
						break 
					elif boxRectEOT.collidepoint(self.mousex,self.mousey):
						if self.game.HasTheRightToEndTurn() == 1:
							self.conn.sendto("EOT".encode(), (self.addr, self.serverport))
						elif self.game.ActivePlayer == self.game.PlayerSelected and self.game.HasTheRightToEndTurn() ==0 :
							# TODO if you don't have the right to end the turn the popup must be cleaner and not distorded
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
				# TODO improve the handle of the win in the backend and therfore in the front end
				if self.game.PlayerSelected == 1:
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
				if self.game.PlayerSelected == 2:
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
				if self.game.PlayerSelected == 1:
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
				if self.game.PlayerSelected == 2:
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