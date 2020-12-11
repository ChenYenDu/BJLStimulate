import eel
import random
from BJLStimulator import ReverseBJL

rBJL = ReverseBJL()

@eel.expose
def getRoad(cut):
    if cut not in list(range(2, 416)):
        cut = random.randint(2, 414)

    result, rounds, cards, details = rBJL.randomBuild() 
    result = rBJL.reverseCut(result + cards, cut) # 逆轉切牌結果 -> 產生原始牌型
    del cards
    return {
            "results": result,
            "rounds": rounds,
            "details": details,
        }

eel.init('web', allowed_extensions=['.js', '.html', '.css'])
eel.start('index.html')