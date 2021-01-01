import requests
from pprint import pprint
import xmltodict
import json

def getStationInfo(mobileNo, stationId):
    
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&keyword=' + str(mobileNo))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    item = {}
    pprint(jsons['response']['msgBody']['busStationList'])
    if type(jsons['response']['msgBody']['busStationList']) == type(list()):
        for i in jsons['response']['msgBody']['busStationList']:
            if i['stationId'] == stationId:
                item = i
    else:
        item = jsons['response']['msgBody']['busStationList']
    pprint(item)
    print('debug')
    stationIds = item['stationId']
    stationName = item['stationName']
    x = item['x']
    y = item['y']
    mobileNo = item['mobileNo']
    
    throughRouteList = []
    
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&stationId=' + str(stationId))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    pprint(jsons)
    
#     pprint(jsons['response']['msgBody']['busRouteList'])
    
    for route in jsons['response']['msgBody']['busRouteList']:
        tmp = {}
        tmp['routeId'] = route['routeId']
        tmp['routeName'] = route['routeName']
        throughRouteList.append(tmp)
        
#     pprint(throughRouteList)
    
    tmp = {}
    tmp['stationId'] = stationIds
    tmp['stationName'] = stationName
    tmp['mobileNo'] = mobileNo
    coordinate = {}
    coordinate['latitude'] = y
    coordinate['longitude'] = x
    tmp['coordinate'] = coordinate
    tmp['throughRouteList'] = throughRouteList

    return tmp

# pprint(getStationInfo(38553))

