import requests
from pprint import pprint
import xmltodict
import json

def getRouteInfo(routeId):
    
    
    
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&routeId=' + str(routeId))    
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    
#     pprint(jsons['response']['msgBody']['busRouteInfoItem'])
    
    operationInfo = {}
    
    routeId = jsons['response']['msgBody']['busRouteInfoItem']['routeId']
    routeName = jsons['response']['msgBody']['busRouteInfoItem']['routeName']
    
    operationInfo['downFirstTime'] = jsons['response']['msgBody']['busRouteInfoItem']['downFirstTime']
    operationInfo['downLastTime'] = jsons['response']['msgBody']['busRouteInfoItem']['downLastTime']
    operationInfo['startStationId'] = jsons['response']['msgBody']['busRouteInfoItem']['startStationId']
    operationInfo['startStationName'] = jsons['response']['msgBody']['busRouteInfoItem']['startStationName']
    operationInfo['startMobileNo'] = jsons['response']['msgBody']['busRouteInfoItem']['startMobileNo']
    operationInfo['endStationId'] = jsons['response']['msgBody']['busRouteInfoItem']['endStationId']
    operationInfo['endStationName'] = jsons['response']['msgBody']['busRouteInfoItem']['endStationName']
    operationInfo['endMobileNo'] = jsons['response']['msgBody']['busRouteInfoItem']['endMobileNo']
    operationInfo['upFirstTime'] = jsons['response']['msgBody']['busRouteInfoItem']['upFirstTime']
    operationInfo['upLastTime'] = jsons['response']['msgBody']['busRouteInfoItem']['upLastTime']
    operationInfo['peekAlloc'] = jsons['response']['msgBody']['busRouteInfoItem']['peekAlloc']
    operationInfo['nPeekAlloc'] = jsons['response']['msgBody']['busRouteInfoItem']['nPeekAlloc']
    
    returnData = {}
    returnData['routeId'] = routeId
    returnData['routeName'] = routeName
    returnData['operationInfo'] = operationInfo
    
    
    
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busrouteservice/station?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&routeId=' + str(routeId))    
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    stationLists = []
#     pprint(jsons['response']['msgBody']['busRouteStationList'])
    
    for station in jsons['response']['msgBody']['busRouteStationList']:
        tmp = {}
        tmp['stationId'] = station['stationId']
        tmp['stationName'] = station['stationName']
        try:
            tmp['mobileNo'] = station['mobileNo']
        except:
            tmp['mobileNo'] = 'via'
        tmp['turnYn'] = station['turnYn']
        tmp['stationSeq'] = station['stationSeq']
        stationLists.append(tmp)
          
    returnData['stationLists'] = stationLists
    
    return returnData
