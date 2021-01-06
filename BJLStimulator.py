import random
import os

class ReverseBJL:
    
    def __init__(self):
        pass

    def generateCardset(self, setNumber=8):
        # 創造牌組
        # 花色, 號碼
        colors = list(map(lambda ele: str(ele), range(1, 5)))
        numbers = list(map(lambda ele: str(ele), range(1, 14)))

        cards = []

        # 迴圈造牌
        for color in colors:
            cards += map(lambda ele: '-'.join([color, ele]), numbers)
        
        # 變成 8 副牌
        cards = cards * setNumber
        return cards

    def shuffleCard(self, cardset):
        # 洗牌
        shuffledCards = random.sample(cardset, 416)
        return shuffledCards

    def getNumber(self, card):
        # 撲克牌點數 -> 百家樂點數
        return 10 if (int(card[2:])) // 10  else int(card[2:])

    def getPoint(self, cards):
        # 計算手牌點數
        point = sum([self.getNumber(ele) for ele in cards]) % 10
        return point

    def randPop(self, cardset):
        # 隨機挑牌
        if len(cardset) > 2:
            return cardset.pop(random.randint(1, len(cardset)-1))
        else:
            return cardset.pop()

    def pointAfterAdd(self, pointBefore, addedCard):
        # 計算補牌後點數
        return (pointBefore + self.getNumber(addedCard)) % 10


    def randomBuild(self, maxLength=6, singleJumpMax=0, doubleJumpMax=0):
        
        # 創造排組, 洗牌增加隨機性
        cards = self.shuffleCard(self.generateCardset())

        result = []   # 存花色點數
        rounds = []   # 存每局贏家
        details = []  # 存每局細節

        # 決定初始贏家 (庄 | 閑)
        currentWinner = random.choice(['庄', '閑'])

        # 單跳相關
        singleBalls = 0       # 單球長龍連續出現次數
        singleJumpCount = 0   # 單跳次數計算. 最後應該跟 singleJumpMax 一樣

        # 雙跳相關
        doubleBalls = 0       # 雙球長龍連續出現次數
        doubleJumpCount = 0   # 雙跳次數計算, 最後應該跟 doubleJumpMax 一樣

        # 建立隨機選長龍長度 array, 避免重複計算的效能問題
        allLength = [ele for ele in range(1, singleJumpMax+1)]          # 全部
        noSingle = list(filter(lambda ele: ele != 1, allLength))         # 去 1
        noDouble = list(filter(lambda ele: ele != 2, allLength))        # 去 2
        noSaD = list(filter(lambda ele: ele not in (1, 2), allLength))  # 去 1,2

        # 重建牌組直到牌無法構成一局
        while len(cards) >= 6:

            # 決定長龍程度, 必須小心單跳, 雙跳 不可以過多
            singleNotAllowed = (singleBalls < 4 and singleJumpCount == singleJumpMax) # 不可出 1
            doubleNotAllowed = (doubleBalls < 4 and doubleJumpCount == doubleJumpMax) # 不顆出 2

            # 判斷 singleNotAllowed, doubleNotAllowed 去決定取數的array
            if singleNotAllowed and doubleNotAllowed:
                longCount = random.choice(noSaD)
            elif singleNotAllowed and not doubleNotAllowed:
                longCount = random.choice(noSingle)
            elif doubleNotAllowed and not singleNotAllowed:
                longCount = random.choice(noDouble)
            else:
                longCount = random.choice(allLength)
            
            currentLength = longCount

            # 組建每局的迴圈
            while longCount > 0:

                # 排組張數不足6, 不成局時, 結束迴圈
                if len(cards) < 6:
                    break

                # 計算這條長龍的和局次數, 避免都是和局的 bug
                evenCount = 0

                player = []  # 存單局 閑 牌組
                banker = []  # 存單局 庄 牌組

                # 隨機從牌組取 4 張牌
                popIndex = [self.randPop(cards) for _ in range(4)]

                # 隨機給牌
                while popIndex:
                    if popIndex:
                        player.append(popIndex.pop())
                    if popIndex:
                        banker.append(popIndex.pop())
                    
                # 計算前 2 張點數
                playerPoint = self.getPoint(player)
                bankerPoint = self.getPoint(banker)

                # 判斷閑是否補牌
                doPlayerAddCard = playerPoint < 6

                # 補牌規則
                # 閒家只要小於 6 就補牌
                if doPlayerAddCard:
                    playerAddCard = self.randPop(cards)
                    playerPoint = self.pointAfterAdd(playerPoint, playerAddCard)
                    player.append(playerAddCard)
                
                # 莊家補牌規則
                # 莊家 > 6: 不補牌
                if bankerPoint <= 6:
                    if bankerPoint == 6:     # 莊家 = 6
                        if doPlayerAddCard:  # 閒家補排 
                            if playerPoint in [6, 7]:  # 閒家補牌後點數: 6, 7 -> 補牌
                                bankerAddCard = self.randPop(cards) 
                                bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                                banker.append(bankerAddCard)

                    elif bankerPoint == 5:   # 莊家 = 5:
                        if doPlayerAddCard:  # 閒家補牌
                            if playerPoint in [4,5,6,7]:   #閒家補牌後點數: 4, 5, 6, 7 -> 補牌
                                bankerAddCard = self.randPop(cards)
                                bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                                banker.append(bankerAddCard)

                        else:   # 閒家不補牌, 莊家直接補牌
                            bankerAddCard = self.randPop(cards)
                            bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                            banker.append(bankerAddCard)

                    elif bankerPoint == 4: # 莊家 = 4
                        if doPlayerAddCard: # 閒家補牌
                            if playerPoint not in [0, 1, 8, 9]: # 閒家補牌後點數:0,1,8,9 -> 補牌
                                bankerAddCard = self.randPop(cards)
                                bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                                banker.append(bankerAddCard)

                        else: # 閒家不補牌, 莊家直接補牌
                            bankerAddCard = self.randPop(cards)
                            bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                            banker.append(bankerAddCard)

                    elif bankerPoint == 3: # 莊家 = 3
                        if doPlayerAddCard: 
                            if playerPoint != 8:  # 閒家補牌後點數只要不為 8 -> 補牌
                                bankerAddCard = self.randPop(cards)
                                bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                                banker.append(bankerAddCard)

                        else: # 閒家不補牌, 莊家直接補牌
                            bankerAddCard = self.randPop(cards)
                            bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                            banker.append(bankerAddCard)

                    else: # 莊家 <= 2, 直接補牌
                        bankerAddCard = self.randPop(cards)
                        bankerPoint = self.pointAfterAdd(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)

                # 確認贏家
                winner = "閑" if playerPoint > bankerPoint else "和" if playerPoint == bankerPoint else "庄"

                # 如果 "和", 用 1:9 (留:棄) 決定是否保留, 避免和局過多
                canBeEven = False
                if currentLength > (evenCount+1):
                    if winner == "和":
                        canBeEven = random.choices([True, False], [1, 9])
                        if canBeEven:
                            evenCount += 1
                            
                # 牌局成立
                if winner == currentWinner or canBeEven:
                    longCount -=1 # 長龍剩餘局數 -1
                    rounds.append(winner) # 紀錄庄閑和結果
                    details.append({
                        'player': player.copy(),
                        'banker': banker.copy(),
                        'winner': winner,
                    })

                    for i in range(3):
                        if player:
                            result.append(player.pop(0))
                        if banker:
                            result.append(banker.pop(0))
                


                
                    

            

        return result, rounds, details


    def reverseCut(self, cardsets, position):
        # 回復切牌前結果
        frontPart = cardsets[ (-1 * position) : ]
        endPart = cardsets[ : ( -1 * position) ]
        return frontPart + endPart



rBJL = ReverseBJL()
rBJL.randomBuild()

