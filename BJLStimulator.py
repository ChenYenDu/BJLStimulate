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

    def randomBuild(self):
        '''
        根據需求計算牌組:
        1. 計算至少70局
        2. 長龍最多 5 ~ 6
        3. 單跳最多 5 ~ 6
        '''

        # 創造牌組, 洗牌增加隨機性
        cards = self.shuffleCard(self.generateCardset())

        result = [] # 存花色點數
        rounds = [] # 存每局贏家
        details = []

        # 決定第一條長龍贏家
        currentWinner = random.choice(["庄", "閑"])

        # 單跳次數計算器
        singleJumpCount = 0

        # 重建牌組直到牌不夠一局無法成組
        while len(cards) >= 6:
            
            # 決定長龍長度, 隨機後亂訂公式
            # longCount = longCount = (int(random.randint(1, 1000) * 0.341516172) * 1206 - 1) % 6 + 1
            longCount = random.randint(1, 6)

            # 如果沒有連續出現 長度 1 的長龍
            # 單跳計算器歸 0
            if longCount != 1:
                singleJumpCount = 0
            else:
                # 連續出現 長度 1 的龍
                # 單跳計算器 + 1
                singleJumpCount += 1

            # 組建每局牌的無限迴圈
            while longCount > 0:

                # 在牌組張數不足 6 不成局時, 結束無限迴圈
                if len(cards) < 6:
                    break
                
                player = [] # 存單局 閑 牌組
                banker = [] # 存單局 庄 牌組

                popIndex = [self.randPop(cards) for _ in range(4)] # 隨機從牌組取 4 張牌

                # 先隨機發 4 張牌
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

                canBeEven = True
                # 如果和局, 用 7:3 決定是否保留開局 (留:2, 去: 8), 避免和局過多
                if winner == "和":
                    canBeEven = random.choices([True, False], [1,9])

                # 牌局成立
                if winner == currentWinner or canBeEven:
                    longCount -= 1  # 長龍剩餘局數 -1
                    rounds.append(winner) # 紀錄庄閑和結果
                    details.append({
                        'player': player.copy(),
                        'banker': banker.copy(),
                        'winner': winner,
                    })

                    for i in range(3): # 迴圈重建牌組
                        if player:
                            result.append(player.pop(0))
                        if banker:
                            result.append(banker.pop(0))
                else:
                    cards.extend(player)
                    cards.extend(banker)
                
                if longCount == 0:
                    # 當迴圈剩餘長度歸 0
                    # 隨機給訂新的長度
                    # 長龍 庄閑 互換
                    # longCount = (int(random.randint(1, 1000) * 0.341516172) * 1206 - 1) % 6 + 1
                    longCount = random.randint(1, 6)

                    # 如果單跳次數大於等於 3 調整長龍長度的選擇
                    if singleJumpCount >= 3:
                        longCount = random.randint(1, 6)

                    currentWinner = "庄" if currentWinner == "閑" else "閑"

        return result, rounds, cards, details

    def reverseCut(self, cardsets, position):
        # 回復切牌前結果
        frontPart = cardsets[ (-1 * position) : ]
        endPart = cardsets[ : ( -1 * position) ]
        return frontPart + endPart



rBJL = ReverseBJL()
rBJL.randomBuild()

