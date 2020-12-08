import os
import random
from stimulator import BJLStimulator

clear = lambda: os.system('cls')
bjl = BJLStimulator()
roundRecord, roadRecord, bankerRound, playerRound, cardSets = bjl.getRoad(bjl.shuffleCards())

def reverseBuildFunction(roundResult):
    banker = roundResult['庄']   
    player = roundResult['閑']

    result = []

    n = 0

    while n < 3:
        if player:
            result.append(player.pop(0))
        
        if banker:
            result.append(banker.pop(0))

        n += 1
    
    return result


def randomReBuild(bankerRound, playerRound, lessCards):
        
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
        
        if roundDict[currentWinner]:
            result.append(roundDict[currentWinner])

        #  要做倒組工程 需要從最後一副牌一路倒回
        # reverseCards = []

        return result          
                
def randomBuild():
    cards = bjl.all_cards
    
    result = []

    currentWinner = "庄" if random.randint(1, 10) % 2 else "閑"

    while len(cards) >= 6:
        
        # 決定長龍長度
        longCount = random.randint(1, 6)

        while longCount > 0:
            if len(cards) < 6:
                break
            
            player = []
            banker = []
            popIndex = [ cards.pop(random.randint(0, len(cards)-1)) for i in range(4) ]

            while popIndex:
                if popIndex:
                    player.append(cards.pop())

            
