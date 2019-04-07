import numpy as np
import unittest
import TheGame

class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.SIZE = 60
        self.DECKLIST = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
                    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45,
                    46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
        self.PILEUP = [1]
        self.PILEDOWN = [60]
        
    
    def test_Init(self):
        PlayerTestInstance = TheGame.Player(self.SIZE)
        self.Deck = PlayerTestInstance.Deck

        self.assertListEqual(self.Deck,self.DECKLIST)

    def test_Shuffle(self):
        PlayerTestInstance = TheGame.Player(self.SIZE)
        self.Deck = PlayerTestInstance.Deck
        PlayerTestInstance.ShuffleDeck()
        self.assertTrue(self.Deck != self.DECKLIST)
        self.assertSetEqual(set(self.Deck),set(self.DECKLIST))
    
    def test_EmptyPiles(self):
        PlayerTestInstance = TheGame.Player(self.SIZE)
        self.PileUP = PlayerTestInstance.PileUP
        self.PileDOWN = PlayerTestInstance.PileDOWN
        PlayerTestInstance.EmptyPiles()
        self.assertListEqual(self.PileUP,self.PILEUP)    
        self.assertListEqual(self.PileDOWN,self.PILEDOWN)
    
    def test_DrawBeginningHand(self):
        PlayerTestInstance = TheGame.Player(self.SIZE)
        PlayerTestInstance.DrawBeginningHand()
        self.HAND = [54, 55, 56, 57, 58, 59]
        self.Hand = PlayerTestInstance.Hand
        self.assertListEqual(self.HAND,self.Hand)

    def test_DrawHand(self):
        PlayerTestInstance = TheGame.Player(self.SIZE)
        PlayerTestInstance.Hand = [2,3,4]
        self.HANDFINAL = [2,3,4,57,58,59]
        PlayerTestInstance.Draw(3)
        self.assertListEqual(self.HANDFINAL,PlayerTestInstance.Hand)

        PlayerTestInstance = TheGame.Player(5)
        PlayerTestInstance.Hand = [20,30,40]
        self.HANDFINAL = [20,30,40,2,3,4]
        PlayerTestInstance.Draw(3)
        self.assertListEqual(self.HANDFINAL,PlayerTestInstance.Hand)
        self.assertListEqual(PlayerTestInstance.Deck,[])
        PlayerTestInstance.Draw(2)
        self.assertListEqual(self.HANDFINAL,PlayerTestInstance.Hand)
        self.assertListEqual(PlayerTestInstance.Deck,[])

        PlayerTestInstance = TheGame.Player(5)
        PlayerTestInstance.Hand = [20,30,40]
        self.HAND = [20,30,40,3,4]
        self.HANDFINAL = [20,30,40,3,4,2]
        PlayerTestInstance.Draw(2)
        self.assertListEqual(self.HAND,PlayerTestInstance.Hand)
        self.assertListEqual(PlayerTestInstance.Deck,[2])
        PlayerTestInstance.Draw(2)
        self.assertListEqual(self.HANDFINAL,PlayerTestInstance.Hand)
        self.assertListEqual(PlayerTestInstance.Deck,[])

    def test_setup(self):
        """
        This test doesn't test again the DrawBeginningHand function
        """
        PlayerTestInstance = TheGame.Player(self.SIZE)
        self.Deck = PlayerTestInstance.Deck
        self.PileUP = PlayerTestInstance.PileUP
        self.PileDOWN = PlayerTestInstance.PileDOWN

        PlayerTestInstance.setup()
        self.assertTrue(self.Deck != self.DECKLIST)
        self.assertSetEqual(set(self.Deck),set(self.DECKLIST))
        self.assertListEqual(self.PileUP,self.PILEUP)    
        self.assertListEqual(self.PileDOWN,self.PILEDOWN)



class GameTest(unittest.TestCase):

    def test_checkAction(self):

        self.Game = TheGame.Game()

        PileIndex = ["False",1,2]

        self.Game.Player1.PileUP = [1]
        self.Game.Player1.PileDOWN = [60]
        self.Game.Player2.PileUP = [1,5]
        self.Game.Player2.PileDOWN = [60,53]
        self.assertTrue(self.Game.CheckAction(PileIndex[1],3,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[1],59,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[1],56,'DOWN'))
        self.assertTrue(self.Game.CheckAction(PileIndex[1],1,'DOWN'))
        self.assertTrue(self.Game.CheckAction(PileIndex[2],3,'UP'))
        self.assertFalse(self.Game.CheckAction(PileIndex[2],6,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[2],56,'DOWN'))
        self.assertFalse(self.Game.CheckAction(PileIndex[2],52,'DOWN'))


        self.Game.ActivePlayer = 2
        self.Game.Player1.PileUP = [1,13]
        self.Game.Player1.PileDOWN = [60,51]
        self.Game.Player2.PileUP = [1,5,6]
        self.Game.Player2.PileDOWN = [60,53,49]
        self.assertTrue(self.Game.CheckAction(PileIndex[1],3,'UP'))
        self.assertFalse(self.Game.CheckAction(PileIndex[1],59,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[1],56,'DOWN'))
        self.assertFalse(self.Game.CheckAction(PileIndex[1],1,'DOWN'))
        self.assertFalse(self.Game.CheckAction(PileIndex[2],3,'UP'))
        self.assertFalse(self.Game.CheckAction(PileIndex[2],6,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[2],59,'DOWN'))
        self.assertFalse(self.Game.CheckAction(PileIndex[2],52,'DOWN'))
    
    def test_put(self):
        PileIndex = ["False",1,2]
        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2

        self.Game.Player1.PileUP = [1,13]
        self.Game.Player1.PileDOWN = [60,51]
        self.Game.Player2.PileUP = [1,5,6]
        self.Game.Player2.PileDOWN = [60,53,49]
        
        self.Game.Put(PileIndex[1],3,'UP')
        self.assertListEqual(self.Game.Player1.PileUP,[1,13,3])

        self.Game.Put(PileIndex[1],59,'UP')
        self.assertListEqual(self.Game.Player1.PileUP,[1,13,3])

        self.Game.Put(PileIndex[1],56,'DOWN')
        self.assertListEqual(self.Game.Player1.PileDOWN,[60,51])

        self.Game.ActivePlayer = 1
        self.Game.Put(PileIndex[1],46,'DOWN')
        self.assertListEqual(self.Game.Player1.PileDOWN,[60,51,46])

        self.Game.Put(PileIndex[1],56,'DOWN')
        self.assertListEqual(self.Game.Player1.PileDOWN,[60,51,46,56])


        self.Game.ActivePlayer = 2
        self.Game.Put(PileIndex[2],3,'UP')
        self.assertListEqual(self.Game.Player2.PileUP, [1,5,6])
        
        self.Game.Put(PileIndex[2],14,'UP')
        self.Game.Put(PileIndex[2],21,'UP')
        self.Game.Put(PileIndex[2],11,'UP')
        self.assertListEqual(self.Game.Player2.PileUP, [1,5,6,14,21,11])

    def test_play(self):
        PileIndex = ["False",1,2]
        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2

        self.Game.Player1.Hand = [2,14,16,18,47,57]
        self.Game.Player2.Hand = [20,34,36,38,49,57]
        self.Game.Player1.PileUP = [1,13]
        self.Game.Player1.PileDOWN = [60,51]
        self.Game.Player2.PileUP = [1,5,6]
        self.Game.Player2.PileDOWN = [60,53,49]        


        self.Game.Play(PileIndex[2],20,'UP')
        self.assertListEqual(self.Game.Player2.Hand,[34,36,38,49,57])
        self.assertListEqual(self.Game.Player2.PileUP,[1,5,6,20])

        self.Game.ActivePlayer = 1
        self.Game.Play(PileIndex[1],57,'DOWN') # won't work
        self.Game.Play(PileIndex[1],47,'DOWN')
        self.Game.Play(PileIndex[1],57,'DOWN')
        self.assertListEqual(self.Game.Player1.Hand,[2,14,16,18])
        self.assertListEqual(self.Game.Player1.PileDOWN,[60,51,47,57])

    def test_Concede(self):
        self.Game = TheGame.Game()
        self.assertFalse(self.Game.P1GameOver)
        self.assertFalse(self.Game.P2GameOver)

        self.Game.Concede()
        self.assertTrue(self.Game.P1GameOver)
        self.assertFalse(self.Game.P2GameOver)

        self.Game.ActivePlayer = 2
        self.Game.Concede()
        self.assertTrue(self.Game.P1GameOver)
        self.assertTrue(self.Game.P2GameOver)

    def test_ChangeActivePlayer(self):
        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 1
        self.Game.ChangeActivePlayer()
        self.assertEqual(self.Game.ActivePlayer,2)
        self.Game.ChangeActivePlayer()
        self.assertEqual(self.Game.ActivePlayer,1)
    
    def test_DrawEndOfTurn(self):
        self.Game = TheGame.Game()
        self.Game.Player1.Deck = [5,23,15,58,46]
        self.Game.Player2.Deck = [5,32,9,51,53,48]
        self.Game.Player1.Hand = [2,3]
        self.Game.Player2.Hand = [7,52,45]
        self.Game.PlayedOnOpponnentPiles = [False,True]

        self.PLAYER1HAND = [2,3,58,46]
        self.PLAYER2HAND = [7,52,45,51,53,48]

        self.Game.DrawEndOfTurn()

        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.Hand)
        self.assertListEqual(self.Game.Player1.Deck,[5,23,15])

        self.Game.ActivePlayer = 2
        self.Game.DrawEndOfTurn()

        self.assertListEqual(self.PLAYER2HAND,self.Game.Player2.Hand)
        self.assertListEqual(self.Game.Player2.Deck,[5,32,9])

    def test_EndOfTurn(self):
        self.Game = TheGame.Game()

        self.Game.Player1.Deck = [5,23,15,58,46]
        self.Game.Player2.Deck = [5,32,9,51,53,48]
        self.Game.Player1.Hand = [2,3]
        self.Game.Player2.Hand = [7,52,45]
        self.Game.PlayedOnOpponnentPiles = [False,True]       


        self.PLAYER1HAND = [2,3,58,46]
        self.PLAYER1DECK = [5,23,15]

        self.PLAYER2HAND = [7,52,45,51,53,48]
        self.PLAYER2DECK = [5,32,9]

        self.Game.EndOfTurn()

        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.Hand)
        self.assertListEqual(self.Game.Player1.Deck,self.PLAYER1DECK)
        self.assertListEqual(self.Game.PlayedOnOpponnentPiles,[False,False])
        self.assertEqual(self.Game.ActivePlayer,2)

        self.Game.PlayedOnOpponnentPiles = [False,True] 

        self.Game.EndOfTurn()
        self.assertListEqual(self.PLAYER2HAND,self.Game.Player2.Hand)
        self.assertListEqual(self.Game.Player2.Deck,self.PLAYER2DECK)      
        self.assertListEqual(self.Game.PlayedOnOpponnentPiles,[False,False])
        self.assertEqual(self.Game.ActivePlayer,1)

        self.Game.Player1.Hand = [2,3,58]

        self.PLAYER1HAND = [2,3,58,5,23,15]
        self.PLAYER1DECK = []

        self.Game.PlayedOnOpponnentPiles = [True,False]

        self.Game.EndOfTurn()
        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.Hand)
        self.assertListEqual(self.Game.Player1.Deck,self.PLAYER1DECK)   
        self.Game.ActivePlayer = 1

        self.Game.Player1.Hand = []
        self.Game.EndOfTurn()
        self.assertTrue(self.Game.P2GameOver)



