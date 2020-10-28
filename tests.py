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

    def test_DeepcopyForCheckIfLoose(self):

        self.Game = TheGame.Game()
        self.Game.DeepcopyForCheckIfLoose()

        # we competely change the value of the 1UP pile and we insure the copy hasn't changed
        self.Game.Player1.PileUP = []

        self.assertEqual(self.Game.CopyPlayer1PileUP, TheGame.CreateListOfCards([1],self.color1))

    def test_LoadDeepCopyForCheckIfLoose(self):

        """
        Here the test must ensure that the loaded copy can de changed without imacting the backup created by DeepcopyForCheckIfLoose
        """

        self.Game = TheGame.Game()

        # let's modify the game state just a bit
        self.Game.Player1.PileUP.append(TheGame.Card(number = 10, color = self.color1))
        self.Game.DeepcopyForCheckIfLoose()

        self.Game.LoadDeepCopyForCheckIfLoose()
        self.assertEqual(self.Game.Piles['1UP'],TheGame.CreateListOfCards([1,10],self.color1))

        self.Game.Player1.PileUP.append(TheGame.Card(number = 14, color = self.color1))

        # we ensure the Pile has changed but not the backup
        self.assertEqual(self.Game.Piles['1UP'],TheGame.CreateListOfCards([1,10,14],self.color1))
        self.assertEqual(self.Game.CopyPlayer1PileUP,TheGame.CreateListOfCards([1,10],self.color1))

    def test_rule(self):

        self.Game = TheGame.Game()

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,30],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5],self.color2) 
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53],self.color2)

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                            "1DOWN" : self.Game.Player1.PileDOWN,
                            "2UP" : self.Game.Player2.PileUP,
                            "2DOWN" : self.Game.Player2.PileDOWN}

        self.assertTrue(self.Game.rule('1UP',TheGame.Card(3,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('1UP',TheGame.Card(59,'gold'),PlayOnHisOwnPile = True))
        self.assertFalse(self.Game.rule('1DOWN',TheGame.Card(56,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('1DOWN',TheGame.Card(20,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('1DOWN',TheGame.Card(40,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('2UP',TheGame.Card(3,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('2UP',TheGame.Card(6,'gold'),PlayOnHisOwnPile = False))
        self.assertTrue(self.Game.rule('2DOWN',TheGame.Card(56,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('2DOWN',TheGame.Card(52,'gold'),PlayOnHisOwnPile = False))


        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color2)
        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                    "1DOWN" : self.Game.Player1.PileDOWN,
                    "2UP" : self.Game.Player2.PileUP,
                    "2DOWN" : self.Game.Player2.PileDOWN}

        self.assertTrue(self.Game.rule('1UP',TheGame.Card(3,'silver'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('1UP',TheGame.Card(59,'gold'),PlayOnHisOwnPile = False))
        self.assertTrue(self.Game.rule('1DOWN',TheGame.Card(56,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('1DOWN',TheGame.Card(1,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('2UP',TheGame.Card(3,'gold'),PlayOnHisOwnPile = True))
        self.assertFalse(self.Game.rule('2UP',TheGame.Card(6,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('2DOWN',TheGame.Card(59,'gold'),PlayOnHisOwnPile = True))
        self.assertFalse(self.Game.rule('2DOWN',TheGame.Card(52,'gold'),PlayOnHisOwnPile = True))


    def test_checkAction(self):

        self.Game = TheGame.Game()

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5],self.color2) 
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53],self.color2)

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                            "1DOWN" : self.Game.Player1.PileDOWN,
                            "2UP" : self.Game.Player2.PileUP,
                            "2DOWN" : self.Game.Player2.PileDOWN}

        PlayerSelected = 1

        self.assertTrue(self.Game.CheckAction('1UP',TheGame.Card(3,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('1UP',TheGame.Card(59,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('1DOWN',TheGame.Card(56,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('1DOWN',TheGame.Card(1,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('2UP',TheGame.Card(3,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('2UP',TheGame.Card(6,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('2DOWN',TheGame.Card(56,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('2DOWN',TheGame.Card(52,'gold'),PlayerSelected))


        self.Game.ActivePlayer = 2
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color2)
        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                    "1DOWN" : self.Game.Player1.PileDOWN,
                    "2UP" : self.Game.Player2.PileUP,
                    "2DOWN" : self.Game.Player2.PileDOWN}

        PlayerSelected = 2

        self.assertTrue(self.Game.CheckAction('1UP',TheGame.Card(3,'silver'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('1UP',TheGame.Card(59,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('1DOWN',TheGame.Card(56,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('1DOWN',TheGame.Card(1,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('2UP',TheGame.Card(3,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('2UP',TheGame.Card(6,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('2DOWN',TheGame.Card(59,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('2DOWN',TheGame.Card(52,'gold'),PlayerSelected))


    def test_put(self):

        self.Game = TheGame.Game()
        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color2)

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                    "1DOWN" : self.Game.Player1.PileDOWN,
                    "2UP" : self.Game.Player2.PileUP,
                    "2DOWN" : self.Game.Player2.PileDOWN}

        # the player 2 puts on player 1's pile Up the number 5 < 13 : Works !
        self.Game.Put('1UP',TheGame.Card(5,self.color1),PlayerSelected)
        self.assertListEqual(self.Game.Piles['1UP'],TheGame.CreateListOfCards([1,13,5],self.color1))

        # the player 2 already played on opponent piles : Doesn't work ! Moreover the card is too high to be put on this pile (59 >5)
        self.Game.Put('1UP',TheGame.Card(59,self.color1),PlayerSelected)
        self.assertListEqual(self.Game.Piles['1UP'],TheGame.CreateListOfCards([1,13,5],self.color1))

        # the player 2 already played on opponent piles : Doesn't work !
        self.Game.Put('1DOWN',TheGame.Card(56,self.color1),PlayerSelected)
        self.assertListEqual(self.Game.Piles['1DOWN'],TheGame.CreateListOfCards([60,51],self.color1))

        # let's reset the played on opponent piles for player 2
        self.Game.PlayedOnOpponnentPiles[1] = False

        self.Game.Put('1UP',TheGame.Card(2,self.color2),PlayerSelected)
        self.assertListEqual(self.Game.Piles['1UP'],TheGame.CreateListOfCards([1,13,5],self.color1)+[TheGame.Card(2,self.color2)])

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        self.Game.Put('1DOWN',TheGame.Card(46,self.color1),PlayerSelected)
        self.assertListEqual(self.Game.Piles['1DOWN'],TheGame.CreateListOfCards([60,51,46],self.color1))

        self.Game.Put('1DOWN',TheGame.Card(56,self.color1),PlayerSelected)
        self.assertListEqual(self.Game.Piles['1DOWN'],TheGame.CreateListOfCards([60,51,46,56],self.color1))


        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Put('2UP',TheGame.Card(3,self.color2),PlayerSelected)
        self.assertListEqual(self.Game.Piles['2UP'], TheGame.CreateListOfCards([1,5,6],self.color2))
        
        self.Game.Put('2UP',TheGame.Card(14,self.color2),PlayerSelected)
        self.Game.Put('2UP',TheGame.Card(21,self.color2),PlayerSelected)
        self.Game.Put('2UP',TheGame.Card(11,self.color2),PlayerSelected)
        self.assertEqual(self.Game.Piles['2UP'], TheGame.CreateListOfCards([1,5,6,14,21,11],self.color2))


    def test_play(self):


        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.color1)
        self.Game.Player2.hand = TheGame.CreateListOfCards([20,34,36,38,49,57],self.color2)
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color2)      

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                        "1DOWN" : self.Game.Player1.PileDOWN,
                        "2UP" : self.Game.Player2.PileUP,
                        "2DOWN" : self.Game.Player2.PileDOWN}


        self.Game.Play('2UP',TheGame.Card(20,self.color2),PlayerSelected)
        self.assertListEqual(self.Game.Player2.hand,TheGame.CreateListOfCards([34,36,38,49,57],self.color2))
        self.assertListEqual(self.Game.Piles['2UP'],TheGame.CreateListOfCards([1,5,6,20],self.color2))

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        self.Game.Play('1DOWN',TheGame.Card(57,self.color1),PlayerSelected) # won't work
        self.Game.Play('1DOWN',TheGame.Card(47,self.color1),PlayerSelected)
        self.Game.Play('1DOWN',TheGame.Card(57,self.color1),PlayerSelected)
        self.assertListEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([2,14,16,18],self.color1))
        self.assertListEqual(self.Game.Piles['1DOWN'],TheGame.CreateListOfCards([60,51,47,57],self.color1))


    def test_Concede(self):

        self.Game = TheGame.Game()
        self.assertFalse(self.Game.Player1.GameOver)
        self.assertFalse(self.Game.Player2.GameOver)


        self.Game.Concede()
        self.assertTrue(self.Game.Player1.GameOver)
        self.assertFalse(self.Game.Player2.GameOver)


        self.Game.ActivePlayer = 2
        self.Game.Concede()
        self.assertTrue(self.Game.Player1.GameOver)
        self.assertTrue(self.Game.Player2.GameOver)

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

    def test_HasTheRightToEndTurn(self):

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.color1)
        self.Game.Player2.hand = TheGame.CreateListOfCards([20,34,36,38,49,57],self.color2)
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.color2)      


        self.Game.Play('2UP',TheGame.Card(20,self.color2),PlayerSelected)
        self.assertEqual(self.Game.HasTheRightToEndTurn(),0)

        self.Game.Play('2UP',TheGame.Card(34,self.color2),PlayerSelected)
        self.assertEqual(self.Game.HasTheRightToEndTurn(),1)        

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

        self.assertEqual(self.Game.EndOfTurn(),0)

        self.Game.PlayedThisTurnPlayer1 = ['Whatever1','Whatever2']
        self.assertEqual(self.Game.EndOfTurn(),1)

        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.hand)
        self.assertListEqual(self.Game.Player1.deck,self.PLAYER1DECK)
        self.assertListEqual(self.Game.PlayedOnOpponnentPiles,[False,False])
        self.assertEqual(self.Game.ActivePlayer,2)

        self.Game.PlayedOnOpponnentPiles = [False,True] 
        self.Game.PlayedThisTurnPlayer2 = ['Whatever1','Whatever2']

        self.assertEqual(self.Game.EndOfTurn(),1)
        self.assertListEqual(self.PLAYER2HAND,self.Game.Player2.hand)
        self.assertListEqual(self.Game.Player2.deck,self.PLAYER2DECK)      
        self.assertListEqual(self.Game.PlayedOnOpponnentPiles,[False,False])
        self.assertEqual(self.Game.ActivePlayer,1)

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,3,58],self.color1)

        self.PLAYER1HAND = TheGame.CreateListOfCards([2,3,58,5,23,15],self.color1)
        self.PLAYER1DECK = []

        self.Game.PlayedOnOpponnentPiles = [True,False]
        self.Game.PlayedThisTurnPlayer1 = ['Whatever1','Whatever2']

        self.assertEqual(self.Game.EndOfTurn(),1)
        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.hand)
        self.assertListEqual(self.Game.Player1.deck,self.PLAYER1DECK)   
        self.Game.ActivePlayer = 1
        self.Game.PlayedThisTurnPlayer1 = ['Whatever1','Whatever2']

        self.Game.Player1.hand = []
        self.assertEqual(self.Game.EndOfTurn(),1)
        self.assertTrue(self.Game.Player2.GameOver)

    def test_CheckIfLoose(self):
        # TODO THIS TEST MUST BE PERFECT FOR THE IMPLEMENTATION FO THE RL ALGORITHM
        # 2 things to check : that it is exact (no FP or FN) : 
        #                   : that it doesn't impact the game after except for the value of Playern.Gameover: DONE

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        # obvious case with cards only in the overlap interval : 
        # the test case where player 1 cannot play on his own piles (not even 1 card)
        self.Game.Player1.hand = TheGame.CreateListOfCards([32,34,36,38,37,35],self.color1)
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,40],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,30],self.color1) 
        print(self.Game.Player2.PileDOWN)
        print(self.Game.Piles['2DOWN'])

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                        "1DOWN" : self.Game.Player1.PileDOWN,
                        "2UP" : self.Game.Player2.PileUP,
                        "2DOWN" : self.Game.Player2.PileDOWN}

        self.assertTrue(self.Game.CheckIfLoose(PlayerSelected))
        self.assertTrue(self.Game.Player1.GameOver)     

        self.assertEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([32,34,36,38,37,35],self.color1))

        #reset the Gameover for the player 1
        self.Game.Player1.GameOver = False

        # a bit less obvious case : 
        # the test case where player 1 cannot ( play 2 cards on his own piles AND cannot play 1 card on oppo piles)        
        self.Game.Player1.hand = TheGame.CreateListOfCards([8,17,19,38,39,43],self.color1)
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,44],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,16],self.color1) 
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,8],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,43],self.color2) 

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                        "1DOWN" : self.Game.Player1.PileDOWN,
                        "2UP" : self.Game.Player2.PileUP,
                        "2DOWN" : self.Game.Player2.PileDOWN}

        self.assertTrue(self.Game.CheckIfLoose(PlayerSelected))
        self.assertTrue(self.Game.Player1.GameOver)    

        #reset the Gameover for the player 1
        self.Game.Player1.GameOver = False

        # a bit less obvious case with cards only in the overlap interval except for 1 
        # it will be 1 card on the personal piles + 1 card on the oppo piles
        self.Game.Player1.hand = TheGame.CreateListOfCards([32,15,36,38,37,35],self.color1)
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,40],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,30],self.color1) 
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,8],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,37],self.color2) 

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                        "1DOWN" : self.Game.Player1.PileDOWN,
                        "2UP" : self.Game.Player2.PileUP,
                        "2DOWN" : self.Game.Player2.PileDOWN}

        self.assertFalse(self.Game.CheckIfLoose(PlayerSelected))
        self.assertFalse(self.Game.Player1.GameOver)  

        # checks that the game state hasn't changed
        self.assertEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([32,15,36,38,37,35],self.color1))
        self.assertEqual(self.Game.Player1.PileUP,TheGame.CreateListOfCards([1,40],self.color1))
        self.assertEqual(self.Game.Player1.PileDOWN,TheGame.CreateListOfCards([60,30],self.color1))
        self.assertEqual(self.Game.Player2.PileUP,TheGame.CreateListOfCards([1,8],self.color2))
        self.assertEqual(self.Game.Player2.PileDOWN,TheGame.CreateListOfCards([60,37],self.color2))

        #reset the Gameover for the player 1
        self.Game.Player1.GameOver = False

        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        # test for player 2
        # a bit less obvious case with cards only in the overlap interval except for 1 
        # it will be 1 card on the personal piles + 1 card on the oppo piles
        self.Game.Player2.hand = TheGame.CreateListOfCards([32,39,36,38,37,35],self.color2)
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,49],self.color2)
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,30],self.color2) 
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,8],self.color1)
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,37],self.color1) 

        self.Game.Piles = {"1UP" : self.Game.Player1.PileUP,
                        "1DOWN" : self.Game.Player1.PileDOWN,
                        "2UP" : self.Game.Player2.PileUP,
                        "2DOWN" : self.Game.Player2.PileDOWN}

        self.assertFalse(self.Game.CheckIfLoose(PlayerSelected))
        self.assertFalse(self.Game.Player2.GameOver)  

    def test_Undo(self):

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.color1)
        self.Game.Piles['1UP'] = TheGame.CreateListOfCards([1,13],self.color1)
        self.Game.Piles['1DOWN'] = TheGame.CreateListOfCards([60,51],self.color1)
        self.Game.Piles['2UP'] = TheGame.CreateListOfCards([1,5,6],self.color2)
        self.Game.Piles['2DOWN'] = TheGame.CreateListOfCards([60,53,49],self.color2)    
        self.Game.Player1.PileUP =   self.Game.Piles['1UP']
        self.Game.Player1.PileDOWN =   self.Game.Piles['1DOWN']
        self.Game.Player2.PileUP =   self.Game.Piles['2UP']
        self.Game.Player2.PileDOWN =   self.Game.Piles['2DOWN']


        self.Game.Play('1UP',TheGame.Card(14,self.Game.color1),PlayerSelected)
        self.Game.Play('1UP',TheGame.Card(16,self.Game.color1),PlayerSelected)
        print(self.Game.PlayedThisTurnPlayer1)
        self.assertEqual(self.Game.PlayedThisTurnPlayer1, [(TheGame.Card(14, 'Gold'), '1UP'), (TheGame.Card(16, 'Gold'), '1UP')])
        self.assertEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([2,18,47,57],self.color1))
        self.Game.Undo()
        self.assertEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([2,18,47,57,16],self.color1))
        self.assertEqual(self.Game.PlayedThisTurnPlayer1, [(TheGame.Card(14, 'Gold'), '1UP')])
        self.Game.Undo()
        self.assertEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([2,18,47,57,16,14],self.color1))
        self.assertEqual(self.Game.PlayedThisTurnPlayer1,[])