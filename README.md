# 百家樂牌組模擬器

---

## Version1
  
### 目標

生成1副符合條件的牌組, 每一副牌組由8副撲克牌組成共416張牌, 依設定的切牌位置切牌後要符合篩選條件。

### 篩選條件

1. __切牌位置__: 切牌的位置, 用來回復切牌前原始牌組。
2. __最長長龍__: 單一條路可以容許最長龍。
3. __單跳出現次數__: 單跳Pattern可以出現的次數。
4. __單跳連續次數__: 連續出現單跳的次數最高上限。
5. __雙跳出現次數__: 雙跳Pattern可以出現的次數。
6. __雙跳連續次數__: 連續出現雙跳的次數最高上限。

### 回傳結果

``` python
{
    results: [...], # a list, with length as 416, code of cards.
    rounds: [...], # a list, with length as 416, code of winner.
}
```

## Version2

### 目標

生成10副牌組, 每一副牌組要從第190張牌一直切牌到第240張牌,並計51個切牌位置符合篩選條件的比例, 比例至少要佔50%以上。

### 篩選條件

1. __最高長龍__: 單一路的最高上限
2. __最長單跳__: 連續單跳出現的最高上限
3. __最長雙跳__: 連續雙跳出現的最高上限

### 回傳結果

``` python
{
    A0: {
        gCount: 39,       # 符合條件的切牌位置數量
        matched: [...],   # 符合的切牌位置, 前端用來標記使用
        maxX: 5,          # x 座標的最大值, 前端畫圖使用
        maxY: 25,         # y 座標的最大值, 前端畫圖使用
        rate: 0.9,        # 符🈴️條件的切牌位置所佔比例
        realCard: [...],  # 416張牌, 按順序排列
        roads: [...],     # 每條路的統計和畫圖相關資訊(座標, 顏色...) 
    }
    ...
    A9: {...}
}
```

## How to use

1. Install required package with pip ```pip install -r requirement.txt```

2. Run with ```python app_v1.py``` or ```python app_v2.py``` depends on with version you want.
