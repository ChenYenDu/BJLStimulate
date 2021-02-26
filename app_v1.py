import eel
import random
from BJLStimulator import ReverseBJL

rBJL = ReverseBJL()

@eel.expose
def getRoad(cut ,maxLength, singleJumpTimes, singleJumpMax, doubleJumpTimes, doubleJumpMax):
    if cut not in list(range(2, 416)):
        cut = random.randint(2, 414)

    result, rounds, cards, details = rBJL.randomBuild(
        maxLength = maxLength,
        singleJumpTimes = singleJumpTimes,
        singleJumpMax = singleJumpMax,
        doubleJumpTimes = doubleJumpTimes,
        doubleJumpMax = doubleJumpMax
    )       
    result = rBJL.reverseCut(result + cards, cut) # 逆轉切牌結果 -> 產生原始牌型
    del cards
    return {
            "results": result,
            "rounds": rounds,
            "details": details,
        }

eel.init('web', allowed_extensions=['.js', '.html', '.css'])
eel.start('version_1.html')