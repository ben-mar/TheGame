import unittest
import copy
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

        self.color = {'P1' : 'Gold', 'P2' : 'Silver'}

    def test_DeepcopyForCheckIfLoose(self):

        self.Game = TheGame.Game()
        self.Game.DeepcopyForCheckIfLoose()

        # we competely change the value of the 1UP pile and we insure the copy hasn't changed
        self.Game.Player1.PileUP = []

        self.assertEqual(self.Game.CopyPlayer1PileUP, TheGame.CreateListOfCards([1],self.Game.color['P1']))

        ##### TO GET RID OFF #####

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2
        PlayerSelected = 2


        self.Game.Player2.hand = TheGame.CreateListOfCards([20,34,36,38,49,57],self.Game.color['P2'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.Game.color['P2'])      

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.Game.DeepcopyForCheckIfLoose()
        print("copy played this turn :",self.Game.CopyPlayedThisTurn)
        print("played this turn :",self.Game.CopyPlayedThisTurn)
        self.Game.Play("P2_DOWN",TheGame.Card(36,'Silver'),PlayerSelected)
        print("copy played this turn :",self.Game.CopyPlayedThisTurn)  
        print("played this turn :",self.Game.PlayedThisTurn)      
        ##### END : TO GET RID OFF #####

    def test_LoadDeepCopyForCheckIfLoose(self):

        """
        Here the test must ensure that the loaded copy can de changed without imacting the backup created by DeepcopyForCheckIfLoose
        """

        self.Game = TheGame.Game()

        # let's modify the game state just a bit
        self.Game.Player1.PileUP.append(TheGame.Card(number = 10, color = self.Game.color['P1']))

        # DeepCopy 
        self.Game.CopyPlayer1PileUP = copy.deepcopy(self.Game.Player1.PileUP)
        self.Game.CopyPlayer1PileDOWN = copy.deepcopy(self.Game.Player1.PileDOWN)
        self.Game.CopyPlayer1Hand = copy.deepcopy(self.Game.Player1.hand)
        self.Game.CopyPlayer2PileUP = copy.deepcopy(self.Game.Player2.PileUP)
        self.Game.CopyPlayer2PileDOWN = copy.deepcopy(self.Game.Player2.PileDOWN)
        self.Game.CopyPlayer2Hand = copy.deepcopy(self.Game.Player2.hand)

        self.Game.CopyPlayedThisTurn = copy.deepcopy(self.Game.PlayedThisTurn)
        self.Game.CopyPlayedOnOpponnentPiles = copy.deepcopy(self.Game.PlayedOnOpponnentPiles)  


        self.Game.LoadDeepCopyForCheckIfLoose()
        self.assertEqual(self.Game.CopyPlayedThisTurn,{'P1': [], 'P2': []})
        self.assertEqual(self.Game.PlayedThisTurn,{'P1': [], 'P2': []})
        self.Game.PlayedThisTurn['P' + str(self.Game.ActivePlayer)].append((TheGame.Card(36,'Silver'),"P2_DOWN"))
        self.assertEqual(self.Game.CopyPlayedThisTurn,{'P1': [], 'P2': []})
        self.assertEqual(self.Game.PlayedThisTurn,{'P1': [(TheGame.Card(36,'Silver'), 'P2_DOWN')], 'P2': []})  


        self.Game.LoadDeepCopyForCheckIfLoose()
        self.assertEqual(self.Game.Piles['P1_UP'],TheGame.CreateListOfCards([1,10],self.Game.color['P1']))

        self.Game.Piles['P1_UP'].append(TheGame.Card(number = 14, color = self.Game.color['P1']))

        # we ensure the Pile has changed but not the backup
        self.assertEqual(self.Game.Piles['P1_UP'],TheGame.CreateListOfCards([1,10,14],self.Game.color['P1']))
        self.assertEqual(self.Game.CopyPlayer1PileUP,TheGame.CreateListOfCards([1,10],self.Game.color['P1']))

    def test_sort(self):

        self.Game = TheGame.Game()   
        self.PlayerSelected = 1
        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.Game.color['P1'])    
        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}

        self.Game.SortHand(2,TheGame.Card(57,self.Game.color['P1']),self.PlayerSelected)
        self.assertEqual(self.Game.Hands['P1'],TheGame.CreateListOfCards([2,14,57,16,18,47],self.Game.color['P1'])   )


    def test_rule(self):

        self.Game = TheGame.Game()

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,30],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5],self.Game.color['P2']) 
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53],self.Game.color['P2'])
        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                    "P1_DOWN" : self.Game.Player1.PileDOWN,
                    "P2_UP" : self.Game.Player2.PileUP,
                    "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.assertTrue(self.Game.rule('P1_UP',TheGame.Card(3,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('P1_UP',TheGame.Card(59,'gold'),PlayOnHisOwnPile = True))
        self.assertFalse(self.Game.rule('P1_DOWN',TheGame.Card(56,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('P1_DOWN',TheGame.Card(20,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('P1_DOWN',TheGame.Card(40,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('P2_UP',TheGame.Card(3,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('P2_UP',TheGame.Card(6,'gold'),PlayOnHisOwnPile = False))
        self.assertTrue(self.Game.rule('P2_DOWN',TheGame.Card(56,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('P2_DOWN',TheGame.Card(52,'gold'),PlayOnHisOwnPile = False))


        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.Game.color['P2'])
        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                    "P1_DOWN" : self.Game.Player1.PileDOWN,
                    "P2_UP" : self.Game.Player2.PileUP,
                    "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.assertTrue(self.Game.rule('P1_UP',TheGame.Card(3,'silver'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('P1_UP',TheGame.Card(59,'gold'),PlayOnHisOwnPile = False))
        self.assertTrue(self.Game.rule('P1_DOWN',TheGame.Card(56,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('P1_DOWN',TheGame.Card(1,'gold'),PlayOnHisOwnPile = False))
        self.assertFalse(self.Game.rule('P2_UP',TheGame.Card(3,'gold'),PlayOnHisOwnPile = True))
        self.assertFalse(self.Game.rule('P2_UP',TheGame.Card(6,'gold'),PlayOnHisOwnPile = True))
        self.assertTrue(self.Game.rule('P2_DOWN',TheGame.Card(59,'gold'),PlayOnHisOwnPile = True))
        self.assertFalse(self.Game.rule('P2_DOWN',TheGame.Card(52,'gold'),PlayOnHisOwnPile = True))


    def test_checkAction(self):

        self.Game = TheGame.Game()

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5],self.Game.color['P2']) 
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53],self.Game.color['P2'])

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                            "P1_DOWN" : self.Game.Player1.PileDOWN,
                            "P2_UP" : self.Game.Player2.PileUP,
                            "P2_DOWN" : self.Game.Player2.PileDOWN}

        PlayerSelected = 1

        self.assertTrue(self.Game.CheckAction('P1_UP',TheGame.Card(3,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('P1_UP',TheGame.Card(59,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('P1_DOWN',TheGame.Card(56,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('P1_DOWN',TheGame.Card(1,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('P2_UP',TheGame.Card(3,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('P2_UP',TheGame.Card(6,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('P2_DOWN',TheGame.Card(56,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('P2_DOWN',TheGame.Card(52,'gold'),PlayerSelected))


        self.Game.ActivePlayer = 2
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.Game.color['P2'])
        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                            "P1_DOWN" : self.Game.Player1.PileDOWN,
                            "P2_UP" : self.Game.Player2.PileUP,
                            "P2_DOWN" : self.Game.Player2.PileDOWN}

        PlayerSelected = 2

        self.assertTrue(self.Game.CheckAction('P1_UP',TheGame.Card(3,'silver'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('P1_UP',TheGame.Card(59,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('P1_DOWN',TheGame.Card(56,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('P1_DOWN',TheGame.Card(1,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('P2_UP',TheGame.Card(3,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('P2_UP',TheGame.Card(6,'gold'),PlayerSelected))
        self.assertTrue(self.Game.CheckAction('P2_DOWN',TheGame.Card(59,'gold'),PlayerSelected))
        self.assertFalse(self.Game.CheckAction('P2_DOWN',TheGame.Card(52,'gold'),PlayerSelected))


    def test_put(self):

        self.Game = TheGame.Game()
        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.Game.color['P2'])

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                    "P1_DOWN" : self.Game.Player1.PileDOWN,
                    "P2_UP" : self.Game.Player2.PileUP,
                    "P2_DOWN" : self.Game.Player2.PileDOWN}

        # the player 2 puts on player 1's pile Up the number 5 < 13 : Works !
        self.Game.Put('P1_UP',TheGame.Card(5,self.Game.color['P1']),PlayerSelected)
        self.assertListEqual(self.Game.Piles['P1_UP'],TheGame.CreateListOfCards([1,13,5],self.Game.color['P1']))

        # the player 2 already played on opponent piles : Doesn't work ! Moreover the card is too high to be put on this pile (59 >5)
        self.Game.Put('P1_UP',TheGame.Card(59,self.Game.color['P1']),PlayerSelected)
        self.assertListEqual(self.Game.Piles['P1_UP'],TheGame.CreateListOfCards([1,13,5],self.Game.color['P1']))

        # the player 2 already played on opponent piles : Doesn't work !
        self.Game.Put('P1_DOWN',TheGame.Card(56,self.Game.color['P1']),PlayerSelected)
        self.assertListEqual(self.Game.Piles['P1_DOWN'],TheGame.CreateListOfCards([60,51],self.Game.color['P1']))

        # let's reset the played on opponent piles for player 2
        self.Game.PlayedOnOpponnentPiles['P2'] = False

        self.Game.Put('P1_UP',TheGame.Card(2,self.Game.color['P2']),PlayerSelected)
        self.assertListEqual(self.Game.Piles['P1_UP'],TheGame.CreateListOfCards([1,13,5],self.Game.color['P1'])+[TheGame.Card(2,self.Game.color['P2'])])

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        self.Game.Put('P1_DOWN',TheGame.Card(46,self.Game.color['P1']),PlayerSelected)
        self.assertListEqual(self.Game.Piles['P1_DOWN'],TheGame.CreateListOfCards([60,51,46],self.Game.color['P1']))

        self.Game.Put('P1_DOWN',TheGame.Card(56,self.Game.color['P1']),PlayerSelected)
        self.assertListEqual(self.Game.Piles['P1_DOWN'],TheGame.CreateListOfCards([60,51,46,56],self.Game.color['P1']))


        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Put('P2_UP',TheGame.Card(3,self.Game.color['P2']),PlayerSelected)
        self.assertListEqual(self.Game.Piles['P2_UP'], TheGame.CreateListOfCards([1,5,6],self.Game.color['P2']))
        
        self.Game.Put('P2_UP',TheGame.Card(14,self.Game.color['P2']),PlayerSelected)
        self.Game.Put('P2_UP',TheGame.Card(21,self.Game.color['P2']),PlayerSelected)
        self.Game.Put('P2_UP',TheGame.Card(11,self.Game.color['P2']),PlayerSelected)
        self.assertEqual(self.Game.Piles['P2_UP'], TheGame.CreateListOfCards([1,5,6,14,21,11],self.Game.color['P2']))


    def test_play(self):


        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.Game.color['P1'])
        self.Game.Player2.hand = TheGame.CreateListOfCards([20,34,36,38,49,57],self.Game.color['P2'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.Game.color['P2'])      

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.Game.Play('P2_UP',TheGame.Card(20,self.Game.color['P2']),PlayerSelected)
        self.assertListEqual(self.Game.Hands['P2'],TheGame.CreateListOfCards([34,36,38,49,57],self.Game.color['P2']))
        self.assertListEqual(self.Game.Piles['P2_UP'],TheGame.CreateListOfCards([1,5,6,20],self.Game.color['P2']))
        self.assertListEqual(self.Game.PlayedThisTurn['P2'],[(TheGame.Card(20,self.Game.color['P2']),'P2_UP')])

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        self.Game.Play('P1_DOWN',TheGame.Card(57,self.Game.color['P1']),PlayerSelected) # won't work
        self.Game.Play('P1_DOWN',TheGame.Card(47,self.Game.color['P1']),PlayerSelected)
        self.Game.Play('P1_DOWN',TheGame.Card(57,self.Game.color['P1']),PlayerSelected)
        self.assertListEqual(self.Game.Hands['P1'],TheGame.CreateListOfCards([2,14,16,18],self.Game.color['P1']))
        self.assertListEqual(self.Game.Piles['P1_DOWN'],TheGame.CreateListOfCards([60,51,47,57],self.Game.color['P1']))


    def test_Concede(self):

        self.Game = TheGame.Game()
        self.assertFalse(self.Game.GameOver['P1'])
        self.assertFalse(self.Game.GameOver['P2'])


        self.Game.Concede()
        self.assertTrue(self.Game.GameOver['P1'])
        self.assertFalse(self.Game.GameOver['P2'])


        self.Game.ActivePlayer = 2
        self.Game.Concede()
        self.assertTrue(self.Game.GameOver['P1'])
        self.assertTrue(self.Game.GameOver['P2'])

    def test_ChangeActivePlayer(self):

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 1
        self.Game.ChangeActivePlayer()
        self.assertEqual(self.Game.ActivePlayer,2)
        self.Game.ChangeActivePlayer()
        self.assertEqual(self.Game.ActivePlayer,1)
    
    def test_DrawEndOfTurn(self):

        self.Game = TheGame.Game()
        self.Game.Player1.deck = TheGame.CreateListOfCards([5,23,15,58,46],self.Game.color['P1'])
        self.Game.Player2.deck = TheGame.CreateListOfCards([5,32,9,51,53,48],self.Game.color['P2'])
        self.Game.Player1.hand = TheGame.CreateListOfCards([2,3],self.Game.color['P1'])
        self.Game.Player2.hand = TheGame.CreateListOfCards([7,52,45],self.Game.color['P2'])

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : True}

        self.PLAYER1HAND = TheGame.CreateListOfCards([2,3,58,46],self.Game.color['P1'])
        self.PLAYER2HAND = TheGame.CreateListOfCards([7,52,45,51,53,48],self.Game.color['P2'])

        self.Game.DrawEndOfTurn()

        self.assertListEqual(self.PLAYER1HAND,self.Game.Player1.hand)
        self.assertListEqual(self.Game.Player1.deck,TheGame.CreateListOfCards([5,23,15],self.Game.color['P1']))

        self.Game.ActivePlayer = 2
        self.Game.DrawEndOfTurn()

        self.assertListEqual(self.PLAYER2HAND,self.Game.Player2.hand)
        self.assertListEqual(self.Game.Player2.deck,TheGame.CreateListOfCards([5,32,9],self.Game.color['P2']))

    def test_HasTheRightToEndTurn(self):

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.Game.color['P1'])
        self.Game.Player2.hand = TheGame.CreateListOfCards([20,34,36,38,49,57],self.Game.color['P2'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.Game.color['P2'])      

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}
        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}

        self.Game.Play('P2_UP',TheGame.Card(20,self.Game.color['P2']),PlayerSelected)
        self.assertEqual(self.Game.HasTheRightToEndTurn(),0)

        self.Game.Play('P2_UP',TheGame.Card(34,self.Game.color['P2']),PlayerSelected)
        self.assertEqual(self.Game.HasTheRightToEndTurn(),1)        

    def test_EndOfTurn(self):
        self.Game = TheGame.Game()

        self.Game.Player1.deck = TheGame.CreateListOfCards([5,23,15,58,46],self.Game.color['P1'])
        self.Game.Player2.deck = TheGame.CreateListOfCards([5,32,9,51,53,48],self.Game.color['P2'])
        self.Game.Player1.hand = TheGame.CreateListOfCards([2,3],self.Game.color['P1'])
        self.Game.Player2.hand = TheGame.CreateListOfCards([7,52,45],self.Game.color['P2'])

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : True}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.PLAYER1HAND = TheGame.CreateListOfCards([2,3,58,46],self.Game.color['P1'])
        self.PLAYER1DECK = TheGame.CreateListOfCards([5,23,15],self.Game.color['P1'])

        self.PLAYER2HAND = TheGame.CreateListOfCards([7,52,45,51,53,48],self.Game.color['P2'])
        self.PLAYER2DECK = TheGame.CreateListOfCards([5,32,9],self.Game.color['P2'])

        self.assertEqual(self.Game.EndOfTurn(),0)

        self.Game.PlayedThisTurn['P1']= ['Whatever1','Whatever2']
        self.assertEqual(self.Game.EndOfTurn(),1)

        self.assertListEqual(self.PLAYER1HAND,self.Game.Hands['P1'])
        self.assertListEqual(self.Game.Player1.deck,self.PLAYER1DECK)
        self.assertDictEqual(self.Game.PlayedOnOpponnentPiles,{'P1' : False, 'P2' : False})
        self.assertEqual(self.Game.ActivePlayer,2)

        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : True}
        self.Game.PlayedThisTurn['P2'] = ['Whatever1','Whatever2']

        self.assertEqual(self.Game.EndOfTurn(),1)
        self.assertListEqual(self.PLAYER2HAND,self.Game.Hands['P2'])
        self.assertListEqual(self.Game.Player2.deck,self.PLAYER2DECK)      
        self.assertDictEqual(self.Game.PlayedOnOpponnentPiles,{'P1' : False, 'P2' : False})
        self.assertEqual(self.Game.ActivePlayer,1)

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,3,58],self.Game.color['P1'])
        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        
        self.PLAYER1HAND = TheGame.CreateListOfCards([2,3,58,5,23,15],self.Game.color['P1'])
        self.PLAYER1DECK = []

        self.Game.PlayedOnOpponnentPiles = {'P1' : True, 'P2' : False}
        self.Game.PlayedThisTurn['P1'] = ['Whatever1','Whatever2']

        self.assertEqual(self.Game.EndOfTurn(),1)
        print(self.Game.Hands['P1'])
        self.assertListEqual(self.PLAYER1HAND,self.Game.Hands['P1'])
        self.assertListEqual(self.Game.Player1.deck,self.PLAYER1DECK)   
        self.Game.ActivePlayer = 1
        self.Game.PlayedThisTurn['P1'] = ['Whatever1','Whatever2']

        self.Game.Hands['P1'] = []
        self.assertEqual(self.Game.EndOfTurn(),1)
        self.assertTrue(self.Game.GameOver['P2'])

    def test_CheckIfLoose(self):
        # TODO THIS TEST MUST BE PERFECT FOR THE IMPLEMENTATION FOR THE RL ALGORITHM
        # 2 things to check : that it is exact (no FP or FN) : 
        #                   : that it doesn't impact the game after except for the value of Gameover: DONE

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        self.Game.Player1.hand = TheGame.CreateListOfCards([32,34,36,38,37,35],self.Game.color['P1'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,20],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,30],self.Game.color['P1']) 


        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.assertFalse(self.Game.CheckIfLoose(PlayerSelected))


        # obvious case with cards only in the overlap interval : 
        # the test case where player 1 cannot play on his own piles (not even 1 card)
        self.Game.Player1.hand = TheGame.CreateListOfCards([32,34,36,38,37,35],self.Game.color['P1'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,40],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,30],self.Game.color['P1']) 


        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}


        self.assertTrue(self.Game.CheckIfLoose(PlayerSelected))
        self.assertTrue(self.Game.GameOver['P1'])     

        self.assertEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([32,34,36,38,37,35],self.Game.color['P1']))

        #reset the Gameover for the player 1
        self.Game.GameOver['P1'] = False

        # a bit less obvious case : 
        # the test case where player 1 cannot ( play 2 cards on his own piles AND cannot play 1 card on oppo piles)        
        self.Game.Player1.hand = TheGame.CreateListOfCards([8,17,19,38,39,43],self.Game.color['P1'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,44],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,16],self.Game.color['P1']) 
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,8],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,43],self.Game.color['P2']) 

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.assertTrue(self.Game.CheckIfLoose(PlayerSelected))
        self.assertTrue(self.Game.GameOver['P1'])    

        #reset the Gameover for the player 1
        self.Game.GameOver['P1'] = False

        # a bit less obvious case with cards only in the overlap interval except for 1 
        # it will be 1 card on the personal piles + 1 card on the oppo piles
        self.Game.Player1.hand = TheGame.CreateListOfCards([32,15,36,38,37,35],self.Game.color['P1'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,40],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,30],self.Game.color['P1']) 
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,8],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,37],self.Game.color['P2']) 

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.assertFalse(self.Game.CheckIfLoose(PlayerSelected))
        self.assertFalse(self.Game.GameOver['P1'])  

        # checks that the game state hasn't changed
        self.assertEqual(self.Game.Player1.hand,TheGame.CreateListOfCards([32,15,36,38,37,35],self.Game.color['P1']))
        self.assertEqual(self.Game.Player1.PileUP,TheGame.CreateListOfCards([1,40],self.Game.color['P1']))
        self.assertEqual(self.Game.Player1.PileDOWN,TheGame.CreateListOfCards([60,30],self.Game.color['P1']))
        self.assertEqual(self.Game.Player2.PileUP,TheGame.CreateListOfCards([1,8],self.Game.color['P2']))
        self.assertEqual(self.Game.Player2.PileDOWN,TheGame.CreateListOfCards([60,37],self.Game.color['P2']))

        #reset the Gameover for the player 1
        self.Game.GameOver['P1'] = False

        self.Game.ActivePlayer = 2
        PlayerSelected = 2

        # test for player 2
        # a bit less obvious case with cards only in the overlap interval except for 1 
        # it will be 1 card on the personal piles + 1 card on the oppo piles
        # 38  on pile  DOWN  of player  1, then :  39  on pile  UP  of player  2

        self.Game.Player2.hand = TheGame.CreateListOfCards([32,39,36,38,37,35],self.Game.color['P2'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,49],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,30],self.Game.color['P2']) 
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,8],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,37],self.Game.color['P1']) 

        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.assertFalse(self.Game.CheckIfLoose(PlayerSelected))
        self.assertFalse(self.Game.GameOver['P2'])  

        # Here we want to check that if One of the players has lost but goes back with Undo he hasn't lost 

        # First he plays the card in the wrong order :
        self.Game.Play('P1_DOWN',TheGame.Card(39,self.color['P2']),PlayerSelected)

        # he is therefore loosing :
        self.assertTrue(self.Game.CheckIfLoose(PlayerSelected))
        self.assertTrue(self.Game.GameOver['P2'])        

        self.Game.Undo()

        # he is not loosing anymore:
        self.assertFalse(self.Game.CheckIfLoose(PlayerSelected))
        self.assertFalse(self.Game.GameOver['P2'])          

        # Now he plays the card in the correct order :
        self.Game.Play('P1_DOWN',TheGame.Card(38,self.color['P2']),PlayerSelected)

        # he is therefore not loosing :
        self.assertFalse(self.Game.CheckIfLoose(PlayerSelected))
        self.assertFalse(self.Game.GameOver['P2'])  



    def test_Undo(self):

        self.Game = TheGame.Game()

        self.Game.ActivePlayer = 1
        PlayerSelected = 1

        self.Game.Player1.hand = TheGame.CreateListOfCards([2,14,16,18,47,57],self.Game.color['P1'])
        self.Game.Player1.PileUP = TheGame.CreateListOfCards([1,13],self.Game.color['P1'])
        self.Game.Player1.PileDOWN = TheGame.CreateListOfCards([60,51],self.Game.color['P1'])
        self.Game.Player2.PileUP = TheGame.CreateListOfCards([1,5,6],self.Game.color['P2'])
        self.Game.Player2.PileDOWN = TheGame.CreateListOfCards([60,53,49],self.Game.color['P2'])  
        self.Game.Piles = {"P1_UP" : self.Game.Player1.PileUP,
                        "P1_DOWN" : self.Game.Player1.PileDOWN,
                        "P2_UP" : self.Game.Player2.PileUP,
                        "P2_DOWN" : self.Game.Player2.PileDOWN}

        self.Game.Hands = {'P1' : self.Game.Player1.hand, 'P2' : self.Game.Player2.hand}
        self.Game.PlayedOnOpponnentPiles = {'P1' : False, 'P2' : False}
        self.Game.PlayedThisTurn = {'P1' : [], 'P2' : []}

        self.Game.Play('P2_DOWN',TheGame.Card(57,self.Game.color['P1']),PlayerSelected)
        self.Game.Play('P1_UP',TheGame.Card(16,self.Game.color['P1']),PlayerSelected)

        self.assertEqual(self.Game.PlayedThisTurn['P1'], [(TheGame.Card(57, 'Gold'), 'P2_DOWN'), (TheGame.Card(16, 'Gold'), 'P1_UP')])
        self.assertEqual(self.Game.Hands['P1'],TheGame.CreateListOfCards([2,14,18,47],self.Game.color['P1']))
        self.assertTrue(self.Game.PlayedOnOpponnentPiles['P1'])
        self.Game.Undo()
        self.assertEqual(self.Game.Hands['P1'],TheGame.CreateListOfCards([2,14,18,47,16],self.Game.color['P1']))
        self.assertEqual(self.Game.PlayedThisTurn['P1'], [(TheGame.Card(57, 'Gold'), 'P2_DOWN')])
        self.assertTrue(self.Game.PlayedOnOpponnentPiles['P1'])
        self.Game.Undo()
        self.assertEqual(self.Game.Hands['P1'],TheGame.CreateListOfCards([2,14,18,47,16,57],self.Game.color['P1']))
        self.assertEqual(self.Game.PlayedThisTurn['P1'],[])
        self.assertFalse(self.Game.PlayedOnOpponnentPiles['P1'])        