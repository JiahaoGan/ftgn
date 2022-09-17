import logging
import json

from flask import request, jsonify, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/rubiks', methods=['POST'])
def rubiks():
    data = request.get_json()
    step=data.get("ops")
    bigboard=data.get("state")
    board = []
    stepsA = {"Ui": [0, [4, 3, 2, 1]], "U": [0, [1, 2, 3, 4]], "D": [-1, [4, 3, 2, 1]], "Di": [-1, [1, 2, 3, 4]]}
    stepsB = {"Ri": [-1, [0, 4, 5, 2]], "R": [-1, [2, 5, 4, 0]], "L": [0, [0, 4, 5, 2]], "Li": [0, [2, 5, 4, 0]]}
    stepsC = {"Fi": [[-1, 0, 0, -1], [0, 3, 5, 1]], "F": [[-1, -1, 0, 0], [0, 1, 5, 3]],
              "B": [[0, -1, -1, 0], [0, 3, 5, 1]], "Bi": [[0, 0, -1, -1], [0, 1, 5, 3]]}
    selfrote = {"Ui": -1, "Li": -2, "Fi": -3, "Ri": -4, "Bi": -5, "Di": -6, "U": 1, "L": 2, "F": 3, "R": 4, "B": 5,
                "D": 6}
    board.append(bigboard.get("u"))
    board.append(bigboard.get("l"))
    board.append(bigboard.get("f"))
    board.append(bigboard.get("r"))
    board.append(bigboard.get("b"))
    board.append(bigboard.get("d"))

    testep = ""

    for x in range(0, len(step)):
        if (step[x] == "i"):
            continue

        if (x != len(step) - 1):
            if (step[x + 1] == "i"):
                testep = step[x:x + 2]
            else:
                testep = step[x]
        else:
            testep = step[x]

        # print (testep)
        # print (selfrote.get(testep))
        if (int(selfrote.get(testep)) > 0):
            cur = selfrote.get(testep) - 1
            # print (cur)
            result = [list(reversed(col)) for col in zip(*board[cur])]
            board[cur] = result
        else:
            cur = 0 - (selfrote.get(testep) + 1)
            # print(cur)
            result = list(map(list, zip(*board[cur])))[::-1]
            board[cur] = result

        if (testep == "U" or testep == "Ui" or testep == "D" or testep == "Di"):
            helparray = stepsA.get(testep)[1]
            specolumn = stepsA.get(testep)[0]
            templist = []
            for x in range(3):
                if x == 0:
                    templist = board[helparray[0]][specolumn]
                board[helparray[x]][specolumn] = board[helparray[x + 1]][specolumn]
            board[helparray[-1]][specolumn] = templist;
        elif testep == "L" or testep == "Ri":
            specolumn = stepsB.get(testep)[0]
            if (specolumn == -1):
                backcolumn = 0
            else:
                backcolumn = -1

            templist = []
            for i in range(3):
                templist.insert(0, board[4][i][backcolumn])
                board[4][i][backcolumn] = board[5][2 - i][specolumn]
            # 以第5面作为起点
            for i in range(3):
                board[5][i][specolumn] = board[2][i][specolumn]
            # 接着第2面
            for i in range(3):
                board[2][i][specolumn] = board[0][i][specolumn]

            for i in range(3):
                board[0][i][specolumn] = templist[i]

        elif testep == "R" or testep == "Li":
            specolumn = stepsB.get(testep)[0]
            if (specolumn == -1):
                backcolumn = 0
            else:
                backcolumn = -1

            templist = []
            for i in range(3):
                templist.insert(0, board[4][i][backcolumn])
                board[4][i][backcolumn] = board[0][2 - i][specolumn]
            # 以第5面作为起点
            for i in range(3):
                board[0][i][specolumn] = board[2][i][specolumn]
            # 接着第2面
            for i in range(3):
                board[2][i][specolumn] = board[5][i][specolumn]

            for i in range(3):
                board[5][i][specolumn] = templist[i]

        elif testep == "Fi" or testep == "B":
            # stepsC = {"Fi": [[-1, 0, 0, -1], [0, 3, 5, 1]], "F": [[-1, -1, 0, 0], [0, 1, 5, 3]],
            #         "B": [[0, -1, -1, 0], [0, 3, 5, 1]], "Bi": [[0, 0, -1, -1], [0, 1, 5, 3]]}
            helparray = stepsC.get(testep)[1]
            helpcolumn = stepsC.get(testep)[0]
            specolumn = stepsC.get(testep)[0][0]
            # 统一在第0面设置temp
            temp = list(board[0][specolumn])

            # 第0面的行各点等于下一面的列
            for i in range(3):
                board[0][helpcolumn[0]][i] = board[3][i][helpcolumn[1]]

            # 第1面的列各点等于下一面的行,需要互换
            for i in range(3):
                board[3][i][helpcolumn[1]] = board[5][helpcolumn[2]][2 - i]

            # 第2面的行各点等于下一面的列
            for i in range(3):
                board[5][helpcolumn[2]][i] = board[1][i][helpcolumn[3]]

            # 第3面的列各点等于下一面的行
            for i in range(3):
                board[1][i][helpcolumn[3]] = temp[2 - i]

        else:
            # stepsC = {"Fi": [[-1, 0, 0, -1], [0, 3, 5, 1]], "F": [[-1, -1, 0, 0], [0, 1, 5, 3]],
            #         "B": [[0, -1, -1, 0], [0, 3, 5, 1]], "Bi": [[0, 0, -1, -1], [0, 1, 5, 3]]}
            helparray = stepsC.get(testep)[1]
            helpcolumn = stepsC.get(testep)[0]
            specolumn = stepsC.get(testep)[0][0]
            # 统一在第0面设置temp
            temp = list(board[0][specolumn])

            # 第0面的行各点等于下一面的列
            for i in range(3):
                board[0][helpcolumn[0]][i] = board[1][2 - i][helpcolumn[1]]

            # 第1面的列各点等于下一面的行,需要互换
            for i in range(3):
                board[1][i][helpcolumn[1]] = board[5][helpcolumn[2]][i]

            # 第2面的行各点等于下一面的列
            for i in range(3):
                board[5][helpcolumn[2]][i] = board[3][2 - i][helpcolumn[3]]

            # 第3面的列各点等于下一面的行
            for i in range(3):
                board[3][i][helpcolumn[3]] = temp[i]
        # else:
        #     # stepsC = {"Fi": [[-1, 0, 0, -1], [0, 3, 5, 1]], "F": [[-1, -1, 0, 0], [0, 1, 5, 3]],
        #     #         "B": [[0, -1, -1, 0], [0, 3, 5, 1]], "Bi": [[0, 0, -1, -1], [0, 1, 5, 3]]}
        #     helparray = stepsC.get(testep)[1]
        #     helpcolumn = stepsC.get(testep)[0]
        #     specolumn = stepsC.get(testep)[0][0]
        #     # 统一在第0面设置temp
        #     temp = list(board[0][specolumn])
        #
        #     # 第0面的行各点等于下一面的列
        #     for i in range(3):
        #         board[helparray[0]][helpcolumn[0]][i] = board[helparray[1]][i][helpcolumn[1]]
        #
        #     # 第1面的列各点等于下一面的行
        #     for i in range(3):
        #         board[helparray[1]][i][helpcolumn[1]] = board[helparray[2]][helpcolumn[2]][i]
        #
        #     # 第2面的行各点等于下一面的列
        #     for i in range(3):
        #         board[helparray[2]][helpcolumn[2]][i] = board[helparray[3]][i][helpcolumn[3]]
        #
        #     # 第3面的列各点等于下一面的行
        #     for i in range(3):
        #         board[helparray[3]][i][helpcolumn[3]] = temp[i]

    ans = {"u": board[0], "l": board[1], "f": board[2], "r": board[3], "b": board[4], "d": board[5]}
    return Response(json.dumps(ans), mimetype='application/json')