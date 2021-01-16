import requests
from pprint import pprint
import xmltodict
import json

resultMsg = [
    '정상처리',
    '오류'
]    
    
def getCurrentLocation(routeId):
    resultHeader = {}
    resultBody = {}
    resultData = {}
    tmp = {}
    busLocationList = []
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/buslocationservice?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&routeId=' + str(routeId))
        
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    
    pprint(jsons)

    item = {}
    if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0":             # 정상 호출
        resultHeader['resultCode'] = '0'
        resultHeader['resultMsg'] = resultMsg[0] 
        
        if type(jsons['response']['msgBody']['busLocationList']) == type(list()):                    # 정상 호출 and 배열로 올때 (2개 이상)
            for item in jsons['response']['msgBody']['busLocationList']:
                tmp= {}
                tmp['stationId'] = item["stationId"]
                tmp['stationSeq'] = item['stationSeq']
                tmp['remainSeatCnt'] = item['remainSeatCnt']
                busLocationList.append(tmp)
        else:                                                                                           #1개만 올때 
            tmp['stationId'] = jsons['response']['msgBody']['busLocationList']['stationId']
            tmp['stationSeq'] = jsons['response']['msgBody']['busLocationList']['stationSeq']
            tmp['remainSeatCnt'] = jsons['response']['msgBody']['busLocationList']['remainSeatCnt']
            busLocationList.append(tmp)
            
        resultBody['busLocationList'] = busLocationList
        
    else:
        resultHeader['resultCode'] = '1'
        resultHeader['resultMsg'] = resultMsg[1]
        
    resultData['resultHeader'] = resultHeader
    resultData['resultBody'] = resultBody    
        
    return resultData

# pprint(getStationInfo(38553))

