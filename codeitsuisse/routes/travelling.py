import logging
import json

from flask import request, jsonify,Response

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/travelling-suisse-robot', methods=['POST'] )
def travelling():
    # headers = {'Content-type': 'application/json'}
    data = request.get_json()
    prodata = data.split("\n")
    l = len(prodata)
    w = len(prodata[0])

    charList = [[] for i in range(26)]
    for m in range(l):
        for n in range(w):
            if prodata[m][n] != " ":
                charList[ord(prodata[m][n]) - 65].append([m, n])
    print(charList)
    orig = charList[ord("X") - 65][0]
    goal = "CODEITSUISSE"
    ppath = []

    for i in goal:
        print(i)
        pos_point = charList[ord(i) - 65]
        min = 0
        print(pos_point)
        minsum = abs(pos_point[0][0] - orig[0]) + abs(pos_point[0][1] - orig[1])
        for i in range(len(pos_point)):
            point = pos_point[i]
            s = abs(point[0] - orig[0]) + abs(point[1] - orig[1])
            if (s > minsum):
                min = i
                minsum = s
        ppath.append(s * "S" + "P")
        orig = list(pos_point[min])
        del (pos_point[min])
    str1 = ""
    for i in ppath:
        str1 += i

    return json.dumps(str1)