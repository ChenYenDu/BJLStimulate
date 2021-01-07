import random
import math

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

    def longCountDistribute(self, maxLength=6):
        half = maxLength // 2
        formulaSize = 20 // maxLength 
        
        return [ math.floor(random.random() * formulaSize * ((ele + 1 ) if ele < half else (ele -1))) for ele in range(1, maxLength+1)]


    def randomBuild(self, maxLength=6, singleJumpTimes=0, singleJumpMax=0, doubleJumpTimes=0, doubleJumpMax=0):
        """
        1. maxLength: 最高長龍
        2. singleJumpTimes: 單跳出現的次數
        3. singleJumpMax: 單跳最高長度
        4. doubleJumpTimes: 雙跳出現的次數
        5. doubleJumpTimes: 雙跳最高長度
        """
        # 創造排組, 洗牌增加隨機性
        cards = self.shuffleCard(self.generateCardset())

        result = []  # 存花色點數
        rounds = []
        details = []
        
        # 最終結果
        # numRounds = [random.randint(1, maxLength) for _ in range(25)]
        numRounds = [random.choices(list(range(1, maxLength+1)), self.longCountDistribute(maxLength))[0] for _ in range(30)   ]

        # 全部可取用index
        allRange = list(range(30-max([singleJumpMax, doubleJumpMax])))

        # 嵌入單跳
        for sAdd in range(singleJumpTimes):
            tempPos = random.choice(allRange)
            tempLen = random.randint(4, singleJumpMax)
            if numRounds[tempPos-1] == 1:
                numRounds[tempPos-1] = random.randint(2, maxLength)
            if numRounds[(tempPos+tempLen)] == 1:
                numRounds[(tempPos+tempLen)] = random.randint(2,maxLength)
            allRange = list(filter(lambda ele: ele not in range(tempPos-2, tempPos+tempLen+2), allRange) )
            numRounds = numRounds[:tempPos] + [1]*tempLen + numRounds[(tempPos+tempLen):]
        
        # 嵌入雙跳
        for dAdd in range(doubleJumpTimes):
            tempPos = random.choice(allRange)
            tempLen = random.randint(4, doubleJumpMax)
            if numRounds[tempPos-1] == 1:
                numRounds[tempPos-1] = numRounds[(tempPos+tempLen)] = random.choice(
                    list(
                        filter(lambda ele: ele != 2, list(range(1, maxLength+1)))
                    )
                )
            if numRounds[(tempPos+tempLen)] == 2:
                numRounds[(tempPos+tempLen)] = random.choice(
                    list(
                        filter(lambda ele: ele != 2, list(range(1, maxLength+1)))
                    )
                )
            allRange = list(filter(lambda ele: ele not in range(tempPos-2, tempPos+tempLen+2), allRange) )
            numRounds = numRounds[:tempPos] + [2]*tempLen + numRounds[(tempPos+tempLen):]

        # 決定第一長龍的贏家 
        currentWinner = random.choice(['庄', '閑'])

        # 重建群組, 直到牌無法成局
        while len(cards) >= 6 and numRounds:

            # 取得長龍長度
            longCount = numRounds.pop(0)
            
            # 組建每局牌的無限迴圈
            while longCount > 0:

                # 在牌組張數不足 6 不成局時, 結束無限迴圈
                if len(cards) < 6:
                    break
            
                player = [] # 存單局 閑 牌組
                banker = [] # 存單局 庄 牌組

                popIndex = [self.randPop(cards) for _ in range(4)]

                # 隨機發 4 張牌
                while popIndex:
                    if popIndex:
                        player.append(popIndex.pop())
                    if popIndex:
                        banker.append(popIndex.pop())
                
                # 計算前 2 張點數
                playerPoint = self.getPoint(player)
                bankerPoint = self.getPoint(banker)

                # 判斷 閑 是否補牌
                doPlayerAddCard = playerPoint < 6

                # 補牌規則
                # 閑家只要小於6 就補牌
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

                # 如果和局, 用 1:9 決定是否保留 (留:1, 去:9)
                canBeEven = False
                if winner == "和":
                    canBeEven = random.choices([True, False], [21, 79])[0]
                
                if winner == currentWinner or canBeEven:
                    rounds.append(winner)
                    details.append({
                        'player': player.copy(),
                        'banker': banker.copy(),
                        'winner': winner,
                    })

                    # 和局 longCount 不減1
                    if not canBeEven:
                        longCount -= 1
                    
                    for i in range(3):
                        if player:
                            result.append(player.pop(0))
                        if banker:
                            result.append(banker.pop(0))
                
                else:
                    cards.extend(player)
                    cards.extend(banker)
                
                if longCount == 0:
                    if numRounds:
                        longCount = numRounds.pop(0)
                        currentWinner = "庄" if currentWinner == "閑" else "閑"
                    else:
                        break
                    
                
        return result, rounds, cards, details


    def reverseCut(self, cardsets, position):
        # 回復切牌前結果
        frontPart = cardsets[ (-1 * position) : ]
        endPart = cardsets[ : ( -1 * position) ]
        return frontPart + endPart



rBJL = ReverseBJL()
# rBJL.randomBuild(maxLength=6, singleJumpTimes=1, singleJumpMax=6, doubleJumpTimes=1, doubleJumpMax=5)
# print(rBJL.longCountDistribute(maxLength=6))
random.randrange(0,1)