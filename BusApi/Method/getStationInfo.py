import requests
from pprint import pprint
import xmltodict
import json

def getStationInfo(mobileNo):
    
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&keyword=' + str(mobileNo))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    
#     pprint(jsons['response']['msgBody']['busStationList'])
    
    stationId = jsons['response']['msgBody']['busStationList']['stationId']
    stationName = jsons['response']['msgBody']['busStationList']['stationName']
    x = jsons['response']['msgBody']['busStationList']['x']
    y = jsons['response']['msgBody']['busStationList']['y']
    mobileNo = jsons['response']['msgBody']['busStationList']['mobileNo']
    throughRouteList = []
    
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&stationId=' + str(stationId))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    
#     pprint(jsons['response']['msgBody']['busRouteList'])
    
    for route in jsons['response']['msgBody']['busRouteList']:
        tmp = {}
        tmp['routeId'] = route['routeId']
        tmp['routeName'] = route['routeName']
        throughRouteList.append(tmp)
        
#     pprint(throughRouteList)
    
    tmp = {}
    tmp['stationId'] = stationId
    tmp['stationName'] = stationName
    tmp['mobileNo'] = mobileNo
    coordinate = {}
    coordinate['latitude'] = y
    coordinate['longitude'] = x
    tmp['coordinate'] = coordinate
    tmp['throughRouteList'] = throughRouteList

    return tmp

# pprint(getStationInfo(38553))

