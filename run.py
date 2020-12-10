import eel
from stimulator import BJLStimulator

bjl = BJLStimulator()

@eel.expose
def shuffle():
    cards = bjl.shuffleCards()
    return cards


@eel.expose
def cutCards(cut, cards):
    cardSets = bjl.cutCards(cards, cut)

    rounds, roads, bankers, players, remains = bjl.getRoad(cardSets)

    return [rounds, roads, bankers, players, remains]

eel.init('web', allowed_extensions=['.js', '.html', '.css'])
eel.start('index.html')