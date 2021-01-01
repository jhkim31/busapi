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
    try:
        operationInfo['downFirstTime'] = jsons['response']['msgBody']['busRouteInfoItem']['downFirstTime']
        #옵션값 
    except:
        
        operationInfo['downFirstTime'] = "제공되지 않습니다."
    try: 
        operationInfo['downLastTime'] = jsons['response']['msgBody']['busRouteInfoItem']['downLastTime']
        #옵션값 
    except:
        operationInfo['downLastTime'] = "제공되지 않습니다."
        
    operationInfo['startStationId'] = jsons['response']['msgBody']['busRouteInfoItem']['startStationId']
    #필수값 
    operationInfo['startStationName'] = jsons['response']['msgBody']['busRouteInfoItem']['startStationName']
    #필수값
    try:
        operationInfo['startMobileNo'] = jsons['response']['msgBody']['busRouteInfoItem']['startMobileNo']
        # 옵션값 
    except:
        operationInfo['startMobileNo'] = "제공되지 않습니다." 
        
    
    operationInfo['endStationId'] = jsons['response']['msgBody']['busRouteInfoItem']['endStationId']
    #필수값 
    operationInfo['endStationName'] = jsons['response']['msgBody']['busRouteInfoItem']['endStationName']
    #필수값
    try:
        operationInfo['endMobileNo'] = jsons['response']['msgBody']['busRouteInfoItem']['endMobileNo']
        #옵션값 
    except:
        operationInfo['endMobileNo'] = "제공되지 않습니다."
    
    try:
        operationInfo['upFirstTime'] = jsons['response']['msgBody']['busRouteInfoItem']['upFirstTime']
        #옵션값 
    except:
        operationInfo['upFirstTime'] = "제공되지 않습니다."
    
    try:
        operationInfo['upLastTime'] = jsons['response']['msgBody']['busRouteInfoItem']['upLastTime']
        #옵션값 
    except:
        operationInfo['upLastTime'] = "제공되지 않습니다."
        
    try:
        operationInfo['peekAlloc'] = jsons['response']['msgBody']['busRouteInfoItem']['peekAlloc']
        #옵션값 
    except:
        operationInfo['peekAlloc'] = "제공되지 않습니다."
        
    try:
        operationInfo['nPeekAlloc'] = jsons['response']['msgBody']['busRouteInfoItem']['nPeekAlloc']
    except:
        operationInfo['nPeekAlloc'] = "제공되지 않습니다. "
    
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
