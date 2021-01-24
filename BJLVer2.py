import random
from itertools import product

class BJLVer2:
    colors = [ str(ele) for ele in range(1, 5)]
    numbers = [ str(ele) for ele in range(1, 14)]

    all_cards = [ '-'.join(ele) for ele in product(colors, numbers) ]*8

    def __init__(self):
        self.shuffled = self.shuffledCards()

    def shuffledCards(self):
        """
        洗牌功能
        """
        shuffledCards = random.sample(self.all_cards, 416)
        return shuffledCards
    
    def cutCards(self, position):
        """
        切牌功能
        """
        return self.shuffled[position:] + self.shuffled[:position]

    def getNumber(self, card):
        """
        計算單張牌的點數
        """
        return 10 if (int(card[2:])) // 10  else int(card[2:])

    def getPoint(self, cards):
        """
        計算牌組點數
        """
        point = sum([self.getNumber(ele) for ele in cards]) % 10
        return point
    
    def pointAfterAdd(self, pointBefore, addedCard):
        """
        計算補牌後點數
        pointBefore: 補牌前點數
        addedCard: 補牌
        """
        return (pointBefore + self.getNumber(addedCard)) % 10

    def getWinner(self, player, banker, backup):
        """
        計算當局贏家
        player: 閑家補牌前牌組
        banker: 莊家補牌前牌組
        backup: 補牌牌組
        """

        playerPoint = self.getPoint(player)
        bankerPoint = self.getPoint(banker)

        # 判斷 閑家 是否須要補牌
        doPlayerAddCard = playerPoint < 6

        # 補排規則
        # 閑家只要小於 6 就要補牌
        if doPlayerAddCard:
            playerAddCard = backup.pop(0)
            playerPoint = self.pointAfterAdd(playerPoint, playerAddCard)
            player.append(player.append(playerAddCard))
        
        # 莊家補牌規則
        # 莊家 > 6: 不補牌
        if bankerPoint <= 6:
            if bankerPoint == 6:       # 莊家 = 6
                if doPlayerAddCard:    # 閑家補牌
                    if playerPoint in [6, 7]:  # 閒家補牌後點數: 6, 7 -> 補牌
                        bankerAddCard = backup.pop(0)
                        bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)

            elif bankerPoint == 5:     # 莊家 = 5:
                if doPlayerAddCard:    # 閒家補牌
                    if playerPoint in [4,5,6,7]:  #閒家補牌後點數: 4, 5, 6, 7 -> 補牌
                        bankerAddCard = backup.pop(0)
                        bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)
                else:     # 閒家不補牌, 莊家直接補牌
                    bankerAddCard = backup.pop(0)
                    bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                    banker.append(bankerAddCard)
            
            elif bankerPoint == 4: # 莊家 = 4
                if doPlayerAddCard: # 閑家補牌
                    if playerPoint not in [0, 1, 8, 9]:   # 閒家補牌後點數:0,1,8,9 -> 補牌
                        bankerAddCard = backup.pop(0)
                        bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)
                else: # 閑家不補牌, 莊家直接補牌
                    bankerAddCard = backup.pop(0)
                    bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                    banker.append(bankerAddCard)
            
            elif bankerPoint == 3:  # 莊家 = 3
                if doPlayerAddCard:
                    if playerPoint != 8:
                        bankerAddCard = backup.pop(0)
                        bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)
                else: # 閒家不補牌, 莊家直接補牌
                    bankerAddCard = backup.pop(0)
                    bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                    banker.append(bankerAddCard)
            
            else: # 莊家 <= 2 直接補牌
                bankerAddCard = backup.pop(0)
                bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                banker.append(bankerAddCard)
            
        # 確認贏家
        winner = "閑" if playerPoint > bankerPoint else "和" if playerPoint == bankerPoint else "庄"

        return winner, player, banker, backup

    def getRoad(self, cards):
        """
        計算開出輸贏結果路詳細情況
        cardSets: 切牌後牌組
        """
        cardSets = cards.copy()
        rounds = []

        longCount = 0

        n = 0

        while len(cardSets) > 6:

            playerCards = []
            bankerCards = []
            backupCards = []
            
            while len(playerCards) < 2 and len(bankerCards) < 2:
                playerCards.append(cardSets.pop(0))
                bankerCards.append(cardSets.pop(0))
            
            for _ in range(2):
                backupCards.append(cardSets.pop(0))
            try:
                winner, playerCards, bankerCards, backupCards = self.getWinner(playerCards, bankerCards, backupCards)
            except:
                print(n)
                print("cards: ", cards)
                print("cardSets: ", cardSets)
                print("playerCard: ", playerCards)
                print('bankerCard: ', bankerCards)
                print('backupCards: ', backupCards)

            # rounds.append(winner)
            rounds.append({
                'player': playerCards,
                'banker': bankerCards,
                'winner': winner,
            })
            n += 1

            if len(backupCards) > 0:
                cards = backupCards + cards


        return rounds

    
    def getStatic(self, rou):

        rounds = [ele['winner'] for ele in rou]
        
        currX = 1
        currY = 1
        result = []

        maxY = 0
        maxSingleJump = 0
        maxDoubleJump = 0
        

        firstNotEven = list(filter(lambda ele: ele != "和", rounds))[0]

        currRecord = rounds.pop(0)
        
        tempRecord = {
            'x': currX,
            'y': currY,
            'result': currRecord,
            'fill': 'red' if currRecord == "閑" else "blue" if currRecord == "庄" else 'green'
        }

        result.append(tempRecord)

        currLWE = 1 # 紀錄單一路無和長度

        # 避免第一結果是 “和”
        # 指定為第一個非何得值
        if currRecord == "和":
            currRecord = firstNotEven
            currLWE = 0
        
        singleJump = 0
        doubleJump = 0

        while rounds:
            prevRecord  = currRecord
            currRecord = rounds.pop(0)

            # 後者不等於前者｜和
            if currRecord not in [prevRecord, "和"]:
                
                # 換路
                currX += 1
                currY = 1

                if currLWE != 1:
                    if singleJump > maxSingleJump:
                        maxSingleJump = singleJump
                    singleJump = 0
                else:
                    singleJump += 1

                if currLWE != 2:
                    if doubleJump > maxDoubleJump:
                        maxDoubleJump = doubleJump
                    doubleJump = 0
                else:
                    doubleJump += 1

                if  currLWE > maxY:
                    maxY = currLWE

                currLWE = 0
            
            else:
                currY += 1
                
                if currRecord != "和":
                    currLWE += 1
            
            result.append({
                'x': currX,
                'y': currY,
                'result': currRecord,
                'fill': 'red' if currRecord == "閑" else "blue" if currRecord == "庄" else 'green'
            })

        return {
            'result': result,
            'static': {'maxY':maxY, 'maxSingleJump': maxSingleJump, 'maxDoubleJump': maxDoubleJump}
            }

        

    def roadLoop(self):
        
        # 迴圈跑切排算路
        result = {}

        for pos in range(190, 241):
            
            cuttedCard = self.cutCards(pos)
            roads = self.getRoad(cuttedCard)
            maps = self.getStatic(roads)
            result[str(pos)] = {'road': roads, 'maps':maps, 'cards': cuttedCard}

        return result

# bjl = BJLVer2()
# bjl.getRoad(bjl.shuffled)
# temp = bjl.roadLoop()
# print(temp)