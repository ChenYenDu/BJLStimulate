from generateCards import BJLCardSets
import random
import time

class BJLStimulator(BJLCardSets):
    
    def __init__(self):
        super().__init__()
        # self.cardSets = self.generateCardSet()[:40]
        # self.cardCollect  = [ self.getRealCards(card) for card in self.cardSets ]

    def getNumber(self, card):
        return 10 if (int(card[2:])) // 10  else int(card[2:])

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
            

    def getRealCards(self, card):
        color, number = card.split('-')
        for c, r in {'4': "黑桃", '3':'紅心', '2': '方塊', '1': '梅花'}.items():
            color = color.replace(c, r)
        return '-'.join([color, number])
        
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
        
        # return cardCollect, roundRecord, roadRecord
        return roundRecord, roadRecord, bankerRound, playerRound, cardSets

    def randomReBuild(self, bankerRound, playerRound, lessCards):
        
        # 先決定從庄還是從閑開始
        currentWinner = "庄" if random.randint(0, 100) % 2 else "閑"
        
        # 確定總局數
        totalRounds = len(bankerRound) + len(playerRound)

        # 取局索引 -> currentWinner 不同, 取局的 list 也要不同
        roundDict = {
            "庄": bankerRound,
            "閑": playerRound
        }

        # 存最後結果
        result = []

        # 用來記長龍, 開發完成 commet 
        n = 1

        # 直到所有的局都被取完才結束迴圈
        while totalRounds > 0:

            print('===== current round: %s =====' % {n})
            print('===== current winner: %s =====' % {currentWinner})
            
            # 本長龍總共幾局: 1 ~ 6 
            # 主管給定條件
            roundNumber = random.randint(1, 6)
            
            # 紀錄本長龍每局的詳細結果
            # 才能使用逆反工程
            currentRecord = []
            
            # 
            while roundNumber > 0 and len(roundDict[currentWinner]) > 0:
                print("------   current round number less: %s -----" % {roundNumber})
                print("------   current list length less: %s -----" % {len(roundDict[currentWinner])})
                sampleIndex = random.randint(0, len(roundDict[currentWinner])-1)
                print("------ sampling index: %s -----" % {sampleIndex})
                tt = roundDict[currentWinner].pop(sampleIndex)
                print(tt)
                currentRecord.append(tt)

                roundNumber -= 1
                totalRounds -= 1

            print(currentRecord)
            result.append(currentRecord)

            if currentWinner == "庄":
                currentWinner = "閑"
            else:
                currentWinner = "庄"
            
            if roundNumber > 0:
                break
            
            n += 1
        
        result.append(roundDict[currentWinner])

        return result

    def reverseBuildFunction(self, randRound, lessCards):
        pass


            
            

                

        
    


