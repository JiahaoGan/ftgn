import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/cryptocollapz', methods=['POST'])
def cryptocollapz():
    data = request.get_json()
    #得到一个list
    result=process(data)
    logging.info("data sent for evaluation {}".format(data))
    logging.info("My result :{}".format(result))
    return json.dumps(result)


def process(data):
    dp=[0 for i in range(1000000)]
    result=[]
    for li in data:
        lineresult=[]
        for lii in li:
            if (dp[lii]!=0):
                lineresult.append(dp[lii])
            else:
                lineresult.append(calc(lii,dp))
        result.append(lineresult)

    # print (result)
    return result


def calc(ii,dp):
    i=ii+1
    i=i-1
    mp=set()

    while (i not in mp):
        if (dp[i]!=0):
            mp.add(dp[i])
            break;
        mp.add(i)

        if (i%2==1):
            i=3*i+1
        else:
            i=i/2
            i=int(i)
    dp[ii]=int(max(mp))
    return dp[ii]