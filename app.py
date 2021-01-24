import eel
import random
from BJLVer2 import BJLVer2

@eel.expose
def getMultiRoad():
    
    BJL = BJLVer2()
    multiRoad = BJL.roadLoop()
    realCard = BJL.shuffled

    return {'multiRoad': multiRoad, 'realCard': realCard}

eel.init('web', allowed_extensions=['.js', '.html', '.css'])
eel.start('ver2.html')