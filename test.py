import os
import random
from stimulator import BJLStimulator

clear = lambda: os.system('cls')
bjl = BJLStimulator()


def randomBuild():

    colors = list(map(lambda ele: str(ele), range(1, 5)))
    numbers = list(map(lambda ele: str(ele), range(1, 14)))

    cards = []
    for color in colors:
        cards += map(lambda ele: '-'.join([color, ele]), numbers)
    
    cards = cards * 8

    def randPop():
        return cards.pop(random.randint(0, len(cards)-1))

    def countPoint(pointa, pointb):
        return (pointa + bjl.getNumber(pointb)) % 10

    result = [] # 存花色點數
    rounds = [] # 存每局贏家

    # 決定第一條長龍的長度
    currentWinner = "庄" if random.randint(1, 10) % 2 else "閑"

    # 單跳次數
    singleJumpCount = 0

    # 重建牌組直到牌無法成組
    while len(cards) >= 6:
        
        # 決定長龍長度, 隨機後亂訂公式
        # longCount = longCount = (int(random.randint(1, 1000) * 0.341516172) * 1206 - 1) % 6 + 1
        longCount = random.choices([1,2,3,4,5,6,7], [13, 27, 33, 22, 11, 7, 1])[0]

        if longCount != 1:
            singleJumpCount = 0
        else:
            singleJumpCount += 1

        while longCount > 0:
            if len(cards) < 6:
                break
            
            player = [] 
            banker = []
            popIndex = []

            for i in range(4):
                popIndex.append(randPop())

            # 先隨機發 4 張牌
            while popIndex:
                if popIndex:
                    player.append(popIndex.pop())
                if popIndex:
                    banker.append(popIndex.pop())
            
            # 計算前 2 張點數
            playerPoint = bjl.getPoint(player)
            bankerPoint = bjl.getPoint(banker)
            doPlayerAddCard = playerPoint < 6

            # 補牌規則
            # 閒家只要小於 6 就補牌
            if doPlayerAddCard:
                playerAddCard = randPop()
                playerPoint = countPoint(playerPoint, playerAddCard)
                player.append(playerAddCard)
            
            # 莊家補牌規則
            # 莊家 > 6: 不補牌
            if bankerPoint <= 6:
                if bankerPoint == 6:     # 莊家 = 6
                    if doPlayerAddCard:  # 閒家補排 
                        if playerPoint in [6, 7]:  # 閒家補牌後點數: 6, 7 -> 補牌
                            bankerAddCard = randPop() 
                            bankerPoint = countPoint(bankerPoint, bankerAddCard)
                            banker.append(bankerAddCard)

                elif bankerPoint == 5:   # 莊家 = 5:
                    if doPlayerAddCard:  # 閒家補牌
                        if playerPoint in [4,5,6,7]:   #閒家補牌後點數: 4, 5, 6, 7 -> 補牌
                            bankerAddCard = randPop()
                            bankerPoint = countPoint(bankerPoint, bankerAddCard)
                            banker.append(bankerAddCard)

                    else:   # 閒家不補牌, 莊家直接補牌
                        bankerAddCard = randPop()
                        bankerPoint = countPoint(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)

                elif bankerPoint == 4: # 莊家 = 4
                    if doPlayerAddCard: # 閒家補牌
                        if playerPoint not in [0, 1, 8, 9]: # 閒家補牌後點數:0,1,8,9 -> 補牌
                            bankerAddCard = randPop()
                            bankerPoint = countPoint(bankerPoint, bankerAddCard)
                            banker.append(bankerAddCard)

                    else: # 閒家不補牌, 莊家直接補牌
                        bankerAddCard = randPop()
                        bankerPoint = countPoint(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)

                elif bankerPoint == 3: # 莊家 = 3
                    if doPlayerAddCard: 
                        if playerPoint != 8:  # 閒家補牌後點數只要不為 8 -> 補牌
                            bankerAddCard = randPop()
                            bankerPoint = countPoint(bankerPoint, bankerAddCard)
                            banker.append(bankerAddCard)

                    else: # 閒家不補牌, 莊家直接補牌
                        bankerAddCard = randPop()
                        bankerPoint = countPoint(bankerPoint, bankerAddCard)
                        banker.append(bankerAddCard)

                else: # 莊家 <= 2, 直接補牌
                    bankerAddCard = randPop()
                    bankerPoint = countPoint(bankerPoint, bankerAddCard)
                    banker.append(bankerAddCard)

            # 確認贏家
            winner = "閑" if playerPoint > bankerPoint else "和" if playerPoint == bankerPoint else "庄"

            # 如果和局, 用 7:3 決定是否保留開局 (留:8, 去: 2), 避免和局過多
            if winner == "和":
                canBeEven = random.choices([True, False], [8, 2])

            # 牌局成立
            if winner == currentWinner or winner == "和":
                longCount -= 1  # 長龍剩餘局數 -1
                rounds.append(winner) # 紀錄庄閑和結果
                for i in range(3): # 迴圈重建牌組
                    if player:
                        result.append(player.pop(0))
                    if banker:
                        result.append(banker.pop(0))
            else:
                cards.extend(player)
                cards.extend(banker)
            
            if longCount == 0:
                # longCount = (int(random.randint(1, 1000) * 0.341516172) * 1206 - 1) % 6 + 1
                longCount = random.choices([1,2,3,4,5,6,7], [13, 27, 33, 22, 11, 7, 1])[0]
                if singleJumpCount >= 3:
                    longCount = random.choices([2,3,4,5,6])[0]
                currentWinner = "庄" if currentWinner=="閑" else "閑"

    return result, rounds, cards         


            

            

