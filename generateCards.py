from random import sample, randint, shuffle

class BJLCardSets:
    colors = list(map(lambda ele: str(ele), range(1, 5)))
    numbers = list(map(lambda ele: str(ele), range(1, 14)))

    # all_cards = []

    # for deck in decks:
    #     all_cards += map(lambda ele: '-'.join([deck, ele]), cards)

    def __init__(self):
        all_cards = []
        for color in self.colors:
            all_cards += map(lambda ele: '-'.join([color, ele]), self.numbers)
        self.all_cards = all_cards * 8
        
    
    def shuffleCards(self):
        # python 內置 random.shuffle 可以打亂 list
        # 打亂排組
        shuffledCards = sample(self.all_cards, 416)
        return shuffledCards
    
    def cutCards(self, shuffled, position=None):
        # 如果沒有給定切牌位置
        # 隨機從 2 ~ 415 給一個整數
        if position is None:
            position = randint(2, 415)

        # 給定切排位置後, 前後排組互調
        finalCardSet = shuffled[position:] + shuffled[:position]

        return finalCardSet

    def generateCardSet(self, position=None):
        return self.cutCards( [ ele for ele in self.shuffleCards()],  position)
         
