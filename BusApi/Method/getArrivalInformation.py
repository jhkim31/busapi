import requests
from pprint import pprint
import xmltodict
import json

resultMsg = [
    '정상처리', 
    '오류'
]   


# 0 : 정상처리
# 1 : 남은 버스 없음.  

def getArrivalInformation(stationId):
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&stationId=' + str(stationId))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    pprint(jsons)
    
    resultData = {}
    busArrivalList = []
    resultBody = {}
    resultHeader= {}
    
    if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0":         # 정상 
        print("정상처리")
        lists = jsons['response']['msgBody']['busArrivalList']                                  #2개이상이면 배열로오고 1개이면 단일 객체로 오는 객체임 
        if type(lists) == type(list()):
            for item in lists:
                tmp = {}
                tmp['routeId'] = item['routeId']
                tmp['flag'] = item['flag']
                tmp['locationNo1'] = item['locationNo1']
                tmp['predictTime1'] = item['predictTime1']
                if item['locationNo2'] is None:
                    tmp['locationNo2'] = "nil"
                    tmp['predictTime2'] = "nil"
                else:
                    tmp['locationNo2'] = item['locationNo2']
                    tmp['predictTime2'] = item['predictTime2']
                busArrivalList.append(tmp)
                resultBody['busArrivalList'] = busArrivalList
        else:
            tmp = {}
            tmp['routeId'] = lists['routeId']
            tmp['flag'] = lists['flag']
            tmp['locationNo1'] = lists['locationNo1']
            tmp['predictTime1'] = lists['predictTime1']
            if lists['locationNo2'] is None:
                tmp['locationNo2'] = "nil"
                tmp['predictTime2'] = "nil"
            else:
                tmp['locationNo2'] = lists['locationNo2']
                tmp['predictTime2'] = lists['predictTime2']
            busArrivalList.append(tmp)
            resultBody['busArrivalList'] = busArrivalList
                        
        resultHeader['resultCode'] = '0'
        resultHeader['resultMsg'] = resultMsg[0]
        
        
    else:
        if data.status_code != 200:
            print("통신 오류 ")
        elif jsons['response']['msgHeader']['resultCode'] == "4":
            print("Value Error")
        else :
            print("알 수 없는 오류")
        resultHeader['resultCode'] = '1'
        resultHeader['resultMsg'] = resultMsg[1]
        
    resultData['resultHeader'] = resultHeader
    resultData['resultBody'] = resultBody
    print('resultData ------------------------------------------------------------------')
    pprint(resultData)
    return resultData
    
