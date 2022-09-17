import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/rubiks', methods=['POST'])
def rubiks():
    data = request.get_json()
    step=data.get("ops")
    bigboard=data.get("state")
    board=[]
    steps={"Ui": [0, [4, 3, 2, 1]], "U": [0, [1, 2, 3, 4]], "D": [-1, [4, 3, 2, 1]], "Di": [-1, [1, 2, 3, 4]]}
    board.append(bigboard.get("u"))
    board.append(bigboard.get("l"))
    board.append(bigboard.get("f"))
    board.append(bigboard.get("r"))
    board.append(bigboard.get("b"))
    board.append(bigboard.get("d"))

    testep=""
    for x in range(0, len(step)):
        if (x != len(step) - 1):
            if (step[x + 1] == "i"):
                testep = step[x:x + 2]
            elif (step[x] == "i"):
                continue
            else:
                testep = step[x]
        else:
            testep = step[x]


        if (testep=="U" or testep=="Ui" or testep=="D" or testep=="Di"):
            helparray=steps.get(testep)[1]
            specolumn=steps.get(testep)[0]
            templist=[]
            for x in range(3):
                if x==0:
                    templist=board[helparray[0]][specolumn]
                board[helparray[x]][specolumn]=board[helparray[x+1]][specolumn]

            board[helparray[-1]][specolumn]=templist;

        print (board)
    return json.dumps(board)