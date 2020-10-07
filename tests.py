import numpy as np
import unittest
import TheGame


class CardTest(unittest.TestCase):

    def setUp(self
              ) -> None:
        self.TestNumberList = [1,50,32,41,10]
        self.color = 'Silver'
        
    def test_Card(self
                 ) -> None:

        for numberTest in self.TestNumberList:
            cardtest = TheGame.Card(numberTest,self.color)
            self.assertTrue(cardtest.color == 'Silver')
            self.assertTrue(cardtest.number == numberTest)

    def test_equality(self) -> None:
        self.number1 = 15
        self.color1 = 'Silver'
        self.card1 = TheGame.Card(self.number1,self.color1)

        self.number2 = 53
        self.color2 = 'Silver'
        self.card2 = TheGame.Card(self.number2,self.color2)        

        self.number3 = 15
        self.color3 = 'Gold'
        self.card3 = TheGame.Card(self.number3,self.color3)   

        self.number4 = 15
        self.color4 = 'Silver'
        self.card4 = TheGame.Card(self.number4,self.color4)

        # self.number5 = '15'
        # self.color5 = 'Silver'
        # self.card5 = TheGame.Card(self.number5,self.color5)       

        self.assertNotEqual(self.card1,self.card2)
        self.assertNotEqual(self.card1,self.card3)
        self.assertNotEqual(self.card2,self.card3)
        self.assertEqual(self.card1,self.card4)



class DeckTest(unittest.TestCase):

    def setUp(self
                ) -> None:
        self.color = 'Silver'
        self.size = 60
        self.deck = TheGame.Deck(size = self.size, color = self.color)

    def test_Equal(self):
        DeckTestInstance = TheGame.Deck(size = self.size, color = self.color)
        self.assertEqual(self.deck, DeckTestInstance)

    def test_Shuffle(self):
        DeckTestInstance = TheGame.Deck(size = self.size, color = self.color)
        DeckTestInstance.ShuffleDeck()
        self.assertNotEqual(self.deck, DeckTestInstance)

class HandTest(unittest.TestCase):

    def setUp(self):
        self.listOfNumbers = [1,50,32,41,10]
        self.color = 'Silver'     
        self.ListOfCards = []  
        for number in self.listOfNumbers:
            self.ListOfCards.append(TheGame.Card(number,self.color))
         
    
    def test_listofcards(self):
        TestHand = TheGame.Hand(self.listOfNumbers,self.color)
        print(TestHand)
        for card in TestHand.hand:
            print(card)


class PlayerTest(unittest.TestCase):

    def setUp(self):
        self.color = 'Silver'
        self.size = 60
        self.PlayerInstance = TheGame.Player(self.size,self.color)
        self.decklist = [TheGame.Card(i,self.color) for i in range(2,self.size)]
        self.PILEUP = [TheGame.Card(number = 1, color = self.color)]
        self.PILEDOWN = [TheGame.Card(number = self.size, color = self.color)]
      
    
    def test_Init(self):
        PlayerTestInstance = TheGame.Player(self.size,self.color)
        self.deck = PlayerTestInstance.deck
        self.assertEqual(self.deck,self.decklist)

    def test_EmptyPiles(self):
        self.PileUP = self.PlayerInstance.PileUP
        self.PileDOWN = self.PlayerInstance.PileDOWN
        self.PlayerInstance.EmptyPiles()
        self.assertEqual(self.PileUP,self.PILEUP)    
        self.assertEqual(self.PileDOWN,self.PILEDOWN)

    def test_DrawHand(self):
        PlayerTestInstance = TheGame.Player(self.size,self.color)
        PlayerTestInstance.hand = TheGame.CreateListOfCards([2,3,4],self.color)
        self.HANDFINAL = TheGame.CreateListOfCards([2,3,4,57,58,59],self.color) 
        PlayerTestInstance.Draw(3)
        self.assertEqual(self.HANDFINAL,PlayerTestInstance.hand)

        PlayerTestInstance = TheGame.Player(5,self.color)
        PlayerTestInstance.hand = TheGame.CreateListOfCards([20,30,40],self.color)
        self.HANDFINAL = TheGame.CreateListOfCards([20,30,40,2,3,4],self.color)
        PlayerTestInstance.Draw(3)
        self.assertEqual(self.HANDFINAL,PlayerTestInstance.hand)
        self.assertEqual(PlayerTestInstance.deck,[])
        PlayerTestInstance.Draw(2)
        self.assertEqual(self.HANDFINAL,PlayerTestInstance.hand)
        self.assertEqual(PlayerTestInstance.deck,[])

        PlayerTestInstance = TheGame.Player(5,self.color)
        PlayerTestInstance.hand = TheGame.CreateListOfCards([20,30,40],self.color)
        self.HAND = TheGame.CreateListOfCards([20,30,40,3,4],self.color) 
        self.HANDFINAL = TheGame.CreateListOfCards([20,30,40,3,4,2],self.color) 
        PlayerTestInstance.Draw(2)
        self.assertListEqual(self.HAND,PlayerTestInstance.hand)
        self.assertListEqual(PlayerTestInstance.deck,[TheGame.Card(2,self.color)])
        PlayerTestInstance.Draw(2)
        self.assertListEqual(self.HANDFINAL,PlayerTestInstance.hand)
        self.assertListEqual(PlayerTestInstance.deck,[])

    def test_setup(self):
        """
        This test doesn't test again the DrawBeginningHand function
        """
        PlayerTestInstance = TheGame.Player(self.size,self.color)
        self.deck = PlayerTestInstance.deck
        self.PileUP = PlayerTestInstance.PileUP
        self.PileDOWN = PlayerTestInstance.PileDOWN

        PlayerTestInstance.setup()
        self.assertTrue(self.deck != self.decklist)
        self.assertListEqual(self.PileUP,self.PILEUP)    
        self.assertListEqual(self.PileDOWN,self.PILEDOWN)




class GameTest(unittest.TestCase):

    def setUp(self):

        self.color1 = 'Gold'
        self.color2 = 'Silver'

    def test_checkAction(self):

        self.Game = TheGame.Game()
        PileIndex = ["False",1,2]

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5],self.color1) 
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53],self.color1)

        self.assertTrue(self.Game.CheckAction(PileIndex[1],3,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[1],59,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[1],56,'DOWN'))
        self.assertTrue(self.Game.CheckAction(PileIndex[1],1,'DOWN'))
        self.assertTrue(self.Game.CheckAction(PileIndex[2],3,'UP'))
        self.assertFalse(self.Game.CheckAction(PileIndex[2],6,'UP'))
        self.assertTrue(self.Game.CheckAction(PileIndex[2],56,'DOWN'))
        self.assertFalse(self.Game.CheckAction(PileIndex[2],52,'DOWN'))


        self.Game.ActivePlayer = 2
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color1)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color1)

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

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color2)
        
        # the player 2 puts on player 1's pile Up the number 5 < 13 : Works !
        self.Game.Put(PileIndex[1],TheGame.Card(5,self.color1),'UP')
        self.assertListEqual(self.Game.Player1.PileUP,TheGame.CreateListOfCards([1,13,5],self.color1))

        # the player 2 already played on opponent piles : Doesn't work ! Moreover the card is too high to be put on this pile (59 >5)
        self.Game.Put(PileIndex[1],TheGame.Card(59,self.color1),'UP')
        self.assertListEqual(self.Game.Player1.PileUP,TheGame.CreateListOfCards([1,13,5],self.color1))

        # the player 2 already played on opponent piles : Doesn't work !
        self.Game.Put(PileIndex[1],TheGame.Card(56,self.color1),'DOWN')
        self.assertListEqual(self.Game.Player1.PileDOWN,TheGame.CreateListOfCards([60,51],self.color1))

        # let's reset the played on opponent piles for player 2
        self.Game.PlayedOnOpponnentPiles[1] = False

        self.Game.Put(PileIndex[1],TheGame.Card(2,self.color2),'UP')
        self.assertListEqual(self.Game.Player1.PileUP,TheGame.CreateListOfCards([1,13,5],self.color1)+[TheGame.Card(2,self.color2)])

        self.Game.ActivePlayer = 1
        self.Game.Put(PileIndex[1],TheGame.Card(46,self.color1),'DOWN')
        self.assertListEqual(self.Game.Player1.PileDOWN,TheGame.CreateListOfCards([60,51,46],self.color1))

        self.Game.Put(PileIndex[1],TheGame.Card(56,self.color1),'DOWN')
        self.assertListEqual(self.Game.Player1.PileDOWN,TheGame.CreateListOfCards([60,51,46,56],self.color1))


        self.Game.ActivePlayer = 2
        self.Game.Put(PileIndex[2],TheGame.Card(3,self.color2),'UP')
        self.assertListEqual(self.Game.Player2.PileUP, TheGame.CreateListOfCards([1,5,6],self.color2))
        
        self.Game.Put(PileIndex[2],TheGame.Card(14,self.color2),'UP')
        self.Game.Put(PileIndex[2],TheGame.Card(21,self.color2),'UP')
        self.Game.Put(PileIndex[2],TheGame.Card(11,self.color2),'UP')
        self.assertEqual(self.Game.Player2.PileUP, TheGame.CreateListOfCards([1,5,6,14,21,11],self.color2))

    def test_play(self):

        PileIndex = ["False",1,2]
        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.color1)
        self.Game.Player2.hand = TheGame.CreateListOfCards([20,34,36,38,49,57],self.color2)
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color2)      


        self.Game.Play(PileIndex[2],TheGame.Card(20,self.color2),'UP')
        self.assertListEqual(self.Game.Player2.hand,TheGame.CreateListOfCards([34,36,38,49,57],self.color2))
        self.assertListEqual(self.Game.Player2.PileUP,TheGame.CreateListOfCards([1,5,6,20],self.color2))

        self.Game.ActivePlayer = 1
        self.Game.Play(PileIndex[1],TheGame.Card(57,self.color1),'DOWN') # won't work
        self.Game.Play(PileIndex[1],TheGame.Card(47,self.color1),'DOWN')
        self.Game.Play(PileIndex[1],TheGame.Card(57,self.color1),'DOWN')
        self.assertListEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([2,14,16,18],self.color1))
        self.assertListEqual(self.Game.Player1.PileDOWN,TheGame.CreateListOfCards([60,51,47,57],self.color1))

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
        self.Game.Player1.deck = TheGame.CreateListOfCards([5,23,15,58,46],self.color1)
        self.Game.Player2.deck = TheGame.CreateListOfCards([5,32,9,51,53,48],self.color2)
        self.Game.Player1.hand = TheGame.CreateListOfCards([2,3],self.color1)
        self.Game.Player2.hand = TheGame.CreateListOfCards([7,52,45],self.color2)
        self.Game.PlayedOnOpponnentPiles = [False,True]

        self.PLAYER1HAND = TheGame.CreateListOfCards([2,3,58,46],self.color1)
        self.PLAYER2HAND = TheGame.CreateListOfCards([7,52,45,51,53,48],self.color2)

        self.Game.DrawEndOfTurn()

        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.hand)
        self.assertListEqual(self.Game.Player1.deck,TheGame.CreateListOfCards([5,23,15],self.color1))

        self.Game.ActivePlayer = 2
        self.Game.DrawEndOfTurn()

        self.assertListEqual(self.PLAYER2HAND,self.Game.Player2.hand)
        self.assertListEqual(self.Game.Player2.deck,TheGame.CreateListOfCards([5,32,9],self.color2))

    def test_EndOfTurn(self):
        self.Game = TheGame.Game()

        self.Game.Player1.deck = TheGame.CreateListOfCards([5,23,15,58,46],self.color1)
        self.Game.Player2.deck = TheGame.CreateListOfCards([5,32,9,51,53,48],self.color2)
        self.Game.Player1.hand = TheGame.CreateListOfCards([2,3],self.color1)
        self.Game.Player2.hand = TheGame.CreateListOfCards([7,52,45],self.color2)
        self.Game.PlayedOnOpponnentPiles = [False,True]       


        self.PLAYER1HAND = TheGame.CreateListOfCards([2,3,58,46],self.color1)
        self.PLAYER1DECK = TheGame.CreateListOfCards([5,23,15],self.color1)

        self.PLAYER2HAND = TheGame.CreateListOfCards([7,52,45,51,53,48],self.color2)
        self.PLAYER2DECK = TheGame.CreateListOfCards([5,32,9],self.color2)

        self.Game.EndOfTurn()

        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.hand)
        self.assertListEqual(self.Game.Player1.deck,self.PLAYER1DECK)
        self.assertListEqual(self.Game.PlayedOnOpponnentPiles,[False,False])
        self.assertEqual(self.Game.ActivePlayer,2)

        self.Game.PlayedOnOpponnentPiles = [False,True] 

        self.Game.EndOfTurn()
        self.assertListEqual(self.PLAYER2HAND,self.Game.Player2.hand)
        self.assertListEqual(self.Game.Player2.deck,self.PLAYER2DECK)      
        self.assertListEqual(self.Game.PlayedOnOpponnentPiles,[False,False])
        self.assertEqual(self.Game.ActivePlayer,1)

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,3,58],self.color1)

        self.PLAYER1HAND = TheGame.CreateListOfCards([2,3,58,5,23,15],self.color1)
        self.PLAYER1DECK = []

        self.Game.PlayedOnOpponnentPiles = [True,False]

        self.Game.EndOfTurn()
        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.hand)
        self.assertListEqual(self.Game.Player1.deck,self.PLAYER1DECK)   
        self.Game.ActivePlayer = 1

        self.Game.Player1.hand = []
        self.Game.EndOfTurn()
        self.assertTrue(self.Game.P2GameOver)



