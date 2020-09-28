import socket
import select
import sys
import TheGame


# Messages:
#  Client->Server
#   Three characters minimum . Three first characters are the command:
#     c: connect
#     u: update position
#     d: disconnect
#   Second character only applies to position and specifies direction (udlr)
#
#  Server->Client
#   '|' delimited pairs of positions to draw the players (there is no
#     distinction between the players - not even the client knows where its
#     player is.

class GameServer(object):
	def __init__(self, port=9009, max_num_players=5):
		self.listener = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Bind to localhost - set to external ip to connect from other computers
		self.listener.bind(("127.0.0.1", port))
		self.read_list = [self.listener]
		self.write_list = []   
		self.game = TheGame.Game()
		self.players = {}

	def setupNewPlayer(self,addr):

		# SetUp1 : send the hand, deck , and activeplayer
		msg = "SU1"+";".join(map(str,self.game.Player1.Hand))
		msg += "|" + ";".join(map(str,self.game.Player2.Hand))
		msg += "|" + ";".join(map(str,self.game.Player1.Deck))
		msg += "|" + ";".join(map(str,self.game.Player2.Deck))
		msg += "|" + str(self.game.ActivePlayer)

		# SetUp2 : send the piles
		msg2 = "SU2"+";".join(map(str,self.game.Player1.PileUP))
		msg2 += "|"+";".join(map(str,self.game.Player1.PileDOWN))
		msg2 += "|"+";".join(map(str,self.game.Player2.PileUP))
		msg2 += "|"+";".join(map(str,self.game.Player2.PileDOWN))

		self.listener.sendto(msg.encode(), addr)
		self.listener.sendto(msg2.encode(), addr)
    
	def run(self):
		Running = True
		print("Waiting...")
	#try:
		while Running:
			
			readable, _, _ = (
			select.select(self.read_list, self.write_list, [])
			)
			for f in readable:
				if f is self.listener:
					msg, addr = f.recvfrom(1024)
					msg = msg.decode()
					if len(msg) >= 3:
						cmd = msg[0:3]
						msg = msg[3:]
					if cmd == "NEW":  # New Connection
						PlayerSelected = int(msg)
						self.players[addr] = (addr,PlayerSelected)
						self.setupNewPlayer(addr)
						print("New Player")
					elif cmd == "PLC":  # PLay a Card
						if self.players[addr][1] == self.game.ActivePlayer: # it it's the turn of the active player
							print('do action')
							PileIndex,Number,PileName = msg.split(";")
							self.game.Play(int(PileIndex),int(Number),PileName)
							for addr in self.players:
								self.listener.sendto((cmd + msg).encode(), addr)
						else :
							print(" it's not the turn of the player {}".format(self.players[addr][1]))
					elif cmd == "EOT": # End Of Turn
						if self.players[addr][1] == self.game.ActivePlayer: # it it's the turn of the active player
							self.game.EndOfTurn()
							self.listener.sendto(cmd.encode(), addr)
							for addrLoop, PlayerSelected in self.players.values():
								if addr[1] != addrLoop[1]:
									self.listener.sendto("CAP".encode(), addrLoop) # Change ActivePlayer
									msg = "UPD"+";".join(map(str,self.game.Player1.Hand))
									msg += "|" + ";".join(map(str,self.game.Player2.Hand))
									msg += "|" + ";".join(map(str,self.game.Player1.Deck))
									msg += "|" + ";".join(map(str,self.game.Player2.Deck))
									self.listener.sendto(msg.encode(), addrLoop) # Update Hands and deck
						else :
							print(" it's not the turn of the player {}".format(self.players[addr][1]))
					elif cmd[:2] == "CK":
						if cmd == "CK1" :
							Hand1, Hand2, Deck1, Deck2 = msg.split('|')
							checkPlayer1Hand = ( list(map(int,Hand1.split(';'))) == self.game.Player1.Hand)
							checkPlayer1Deck = ( list(map(int,Deck1.split(';'))) == self.game.Player1.Deck)
							checkPlayer2Hand = ( list(map(int,Hand2.split(';'))) == self.game.Player2.Hand)
							checkPlayer2Deck = ( list(map(int,Deck2.split(';'))) == self.game.Player2.Deck)
							if not checkPlayer1Hand:
								print('checkPlayer1Hand is False !')
							if not checkPlayer1Deck:
								print('checkPlayer1Deck is False !')
							if not checkPlayer2Hand:
								print('checkPlayer2Hand is False !')
							if not checkPlayer2Deck:
								print('checkPlayer2Deck is False !')
							
						if cmd == 'CK2': # 
							PileUP1,PileDN1 , PileUP2,PileDN2 = msg.split('|')
							checkPlayer1PileUP   = ( list(map(int,PileUP1.split(';'))) == self.game.Player1.PileUP)
							checkPlayer1PileDOWN = ( list(map(int,PileDN1.split(';'))) == self.game.Player1.PileDOWN)
							checkPlayer2PileUP   = ( list(map(int,PileUP2.split(';'))) == self.game.Player2.PileUP)
							checkPlayer2PileDOWN = ( list(map(int,PileDN2.split(';')))	== self.game.Player2.PileDOWN)
							if not checkPlayer1PileUP:
								print('checkPlayer1PileUP is False !')
							if not checkPlayer1PileDOWN:
								print('checkPlayer1PileDOWN is False !')
							if not checkPlayer2PileUP:
								print('checkPlayer2PileUP is False !')
							if not checkPlayer2PileDOWN:
								print('checkPlayer2PileDOWN is False !')
					
					elif cmd == "QUI":  # Player Quitting
						if addr in self.players:
							print('Player quitting')
							del self.players[addr]
							# if self.players == {}:
							# 	print ('Server Shutdown')
							# 	Running = False
					else:
						print("Unexpected: {0}".format(msg))
	#except :
		#print ('Server Shutdown')
      
if __name__ == "__main__":
	g = GameServer()
	g.run()