import eel
import random
from BJLVer2 import BJLVer2

@eel.expose
def getMultiRoad(n=10, longLen=None, maxSingleLen=None, maxDoubleLen=None, okRate=0.5):
    
    BJL = BJLVer2()
    # multiRoad = BJL.roadLoop()
    multiRoad = BJL.getMultiSets(
        n=10, longLen=longLen, maxSingleLen=maxSingleLen, 
        maxDoubleLen=maxDoubleLen, okRate=0.5
    )

    # return {'multiRoad': multiRoad, 'realCard': realCard}
    return {'multiRoad': multiRoad}

eel.init('web', allowed_extensions=['.js', '.html', '.css'])
eel.start('version_2.html')