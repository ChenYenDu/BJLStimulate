import random
from itertools import product

class BJLVer2:
    colors = [ str(ele) for ele in range(1, 5)]
    numbers = [ str(ele) for ele in range(1, 14)]

    all_cards = [ '-'.join(ele) for ele in product(colors, numbers) ]*8

    def __init__(self):
        self.shuffled = self.shuffledCards()

    def shuffledCards(self):
        shuffledCards = random.sample(self.all_cards, 416)
        return shuffledCards
    
    def cutCards(self, position):
        return self.shuffled[position:] + self.shuffled[:position]

    def getNumber(self, card):
        # 撲克牌點數 -> 百家樂點數
        return 10 if (int(card[2:])) // 10  else int(card[2:])

    def getPoint(self, cards):
        # 計算手牌點數
        point = sum([self.getNumber(ele) for ele in cards]) % 10
        return point

    def getWinner(self, pc, bc, sc):
        '''
            pc: playerCards
            bc: bankCards
            sc = substituteCards
        '''
        
        try:
            playerPoint = sum([
                self.getNumber(ele) for ele in pc
            ] ) % 10
        except:
            print("player point calculation error")


        
        try:
            bankerPoint = sum([
                self.getNumber(ele) for ele in bc
            ] ) % 10
        except:
            print("banker point calculation error")

        playerAdd = None
        prevPlayerPoint = playerPoint

        try: 
            if playerPoint <= 5:
                # 閑點數小於等於 5 補牌
                # prevPlayerPoint = playerPoint
                playerAdd = sc.pop(0)
                playerPoint = (playerPoint + self.getNumber(playerAdd)) % 10
                pc.append(playerAdd)
        except:
            print("player add card error")

        try:
            if bankerPoint <= 5:
                # 庄 點數小於 5 補牌
                bankerAdd = sc.pop(0)
                bankerPoint = (bankerPoint + self.getNumber(bankerAdd)) % 10
                bc.append(bankerAdd)

            elif bankerPoint == 6:
                # 如果閑補牌 且 補牌為 6 或 7 
                # 庄補牌
                if prevPlayerPoint <= 5 and playerAdd in [6, 7]:
                    bankerPoint = (bankerPoint + self.getNumber(sc.pop(0))) % 10
                    bc = bc.append(sc.pop(0))
            else:
                pass
        except:
            print('banker add card error')
            print("player: ", pc, r"\n\rbanker: ", bc, r"\n\rsc: ", sc)
        
        winner = '閑' if playerPoint > bankerPoint else '和' if playerPoint == bankerPoint else '庄'

        return playerPoint, bankerPoint, winner, pc, bc, sc

    def pointAfterAdd(self, pointBefore, addedCard):
        # 計算補牌後點數
        return (pointBefore + self.getNumber(addedCard)) % 10

    def getRoad(self, cardSets):
                
        pleyerWin = 0
        dealerWin = 0

        roundRecord = []
        bankerRound = []
        playerRound = []
        roadRecord = []

        playerCards = []
        bankerCards = []
        substituteCards = []

        n = 0
        
        while cardSets and len(cardSets) > 6:
            subLength = len(substituteCards)
            # print("")
            # print("---- Round ", n, ' starts ----')

            # 補牌剩餘情況: 目前寫死
            if subLength == 0:
                playerCards.append(cardSets.pop(0))
                bankerCards.append(cardSets.pop(0))
                playerCards.append(cardSets.pop(0))
                bankerCards.append(cardSets.pop(0))
                substituteCards += cardSets[0:2]
                del cardSets[0:2]

            elif subLength == 1:
                playerCards.append(substituteCards.pop(0))
                bankerCards.append(cardSets.pop(0))
                playerCards.append(cardSets.pop(0))
                bankerCards.append(cardSets.pop(0))
                substituteCards += cardSets[0:2]
                del cardSets[0:2]

            else:
                playerCards.append(substituteCards.pop(0))
                bankerCards.append(substituteCards.pop(0))
                playerCards.append(cardSets.pop(0))
                bankerCards.append(cardSets.pop(0))
                substituteCards += cardSets[0:2]
                del cardSets[0:2]


            # 計算點數 判斷輸贏
            playerPoint, bankerPoint, winner, playerCards, bankerCards, substituteCards = self.getWinner(playerCards, bankerCards, substituteCards)
            # print("    --> Winner Calculated....")

            # 存牌局結果
            currentRecord = {
                    "閑": playerCards,
                    "庄": bankerCards,
                    "補": substituteCards,
                    'pp': playerPoint,
                    'bp': bankerPoint,
                    'winner': winner,
                }
            
            
            # 存牌局結果
            roundRecord.append(currentRecord)

            if winner == "庄":
                bankerRound.append(currentRecord)
            
            if winner == "閑":
                playerRound.append(currentRecord)

            if winner == "和":
                picker = random.randint(0, 10)
                if picker % 2 :
                    bankerRound.append(currentRecord)
                else:
                    playerRound.append(currentRecord)
                
            # 存 庄閑贏 算路圖
            roadRecord.append(winner)

            n += 1
            playerCards = []
            bankerCards = []
        
        # return roundRecord, roadRecord, bankerRound, playerRound
        return roadRecord

    def roadLoop(self):
        
        # 迴圈跑切排算路
        result = {}

        for pos in range(190, 241):
            
            cuttedCard = self.cutCards(pos)
            result[str(pos)] = self.getRoad(cuttedCard)

        return result

# bjl = BJLVer2()
# temp = bjl.roadLoop()
# print(temp)