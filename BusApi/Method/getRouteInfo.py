import requests
from pprint import pprint
import xmltodict
import json

resultMsg = [
    '정상처리', 
    '운영정보 통신 에러', 
    '노선 ID value Error', 
    '정거장리스트 통신 에러', 
    '관할지역이 아닙니다.'
]    


# 0 : 정상처리
# 1 : 운영정보 통신 에러
# 2 : 노선 ID value Error 
# 3 : 정거장리스트 통신 에러
# 4 : 관할지역 아님 
# 9 : 알수없는 오류입니다.
def getRouteInfo(routeId):
    
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busrouteservice/info?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&routeId=' + str(routeId))    
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    operationInfo = {}
    resultData = {}
    resultHeader = {}
    resultBody = {}    
    if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0":
        routeId = jsons['response']['msgBody']['busRouteInfoItem']['routeId']
        routeName = jsons['response']['msgBody']['busRouteInfoItem']['routeName']
        districtCd = jsons['response']['msgBody']['busRouteInfoItem']['districtCd']
        
        try:
            operationInfo['downFirstTime'] = jsons['response']['msgBody']['busRouteInfoItem']['downFirstTime']
            # 옵션값 
        except:
            operationInfo['downFirstTime'] = "제공되지 않습니다."
            
        try: 
            operationInfo['downLastTime'] = jsons['response']['msgBody']['busRouteInfoItem']['downLastTime']
            # 옵션값 
        except:
            operationInfo['downLastTime'] = "제공되지 않습니다."
            
        operationInfo['startStationId'] = jsons['response']['msgBody']['busRouteInfoItem']['startStationId']
        # 필수값 
        operationInfo['startStationName'] = jsons['response']['msgBody']['busRouteInfoItem']['startStationName']
        # 필수값
        try:
            operationInfo['startMobileNo'] = jsons['response']['msgBody']['busRouteInfoItem']['startMobileNo']
            # 옵션값 
        except:
            operationInfo['startMobileNo'] = "제공되지 않습니다." 
        
        operationInfo['endStationId'] = jsons['response']['msgBody']['busRouteInfoItem']['endStationId']
        # 필수값 
        operationInfo['endStationName'] = jsons['response']['msgBody']['busRouteInfoItem']['endStationName']
        # 필수값
        try:
            operationInfo['endMobileNo'] = jsons['response']['msgBody']['busRouteInfoItem']['endMobileNo']
            # 옵션값 
        except:
            operationInfo['endMobileNo'] = "제공되지 않습니다."
        
        try:
            operationInfo['upFirstTime'] = jsons['response']['msgBody']['busRouteInfoItem']['upFirstTime']
            # 옵션값 
        except:
            operationInfo['upFirstTime'] = "제공되지 않습니다."
        
        try:
            operationInfo['upLastTime'] = jsons['response']['msgBody']['busRouteInfoItem']['upLastTime']
            # 옵션값 
        except:
            operationInfo['upLastTime'] = "제공되지 않습니다."
            
        try:
            if jsons['response']['msgBody']['busRouteInfoItem']['peekAlloc'] == "0":
                operationInfo['peekAlloc'] = "제공되지 않습니다."
            else:
                operationInfo['peekAlloc'] = jsons['response']['msgBody']['busRouteInfoItem']['peekAlloc']
            # 옵션값 
        except:
            operationInfo['peekAlloc'] = "제공되지 않습니다."
            
        try:
            if operationInfo['nPeekAlloc'] == jsons['response']['msgBody']['busRouteInfoItem']['nPeekAlloc'] == "0":
                operationInfo['nPeekAlloc'] = "제공되지 않습니다."
            else:
                operationInfo['nPeekAlloc'] = jsons['response']['msgBody']['busRouteInfoItem']['nPeekAlloc']
        except:
            operationInfo['nPeekAlloc'] = "제공되지 않습니다. "
            
        resultBody['routeId'] = routeId
        resultBody['routeName'] = routeName
        resultBody['operationInfo'] = operationInfo
        resultBody['districtCd'] = districtCd
        
        resultHeader['resultCode'] = "0"
        resultHeader['resultMsg'] = resultMsg[0]
        
        data = requests.get('http://openapi.gbis.go.kr/ws/rest/busrouteservice/station?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&routeId=' + str(routeId))    
        dicts = xmltodict.parse(data.text)
        jsons = json.loads(json.dumps(dicts))
        stationLists = []
        if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0" and resultBody['districtCd'] == "2":
            for station in jsons['response']['msgBody']['busRouteStationList']:
                tmp = {}
                tmp['stationId'] = station['stationId']
                tmp['stationName'] = station['stationName']
                tmp['districtCd'] = station['districtCd']
                try:
                    tmp['mobileNo'] = station['mobileNo']
                except:
                    tmp['mobileNo'] = 'via'
                tmp['turnYn'] = station['turnYn']
                tmp['stationSeq'] = station['stationSeq']
                stationLists.append(tmp)
                  
            resultBody['stationLists'] = stationLists
            
        elif data.status_code != 200:
            resultHeader['resultCode'] = "3"
            resultHeader['resultMsg'] = resultMsg[3]
            
        elif resultBody['districtCd'] != "2":
            resultHeader['resultCode'] = "4"
            resultHeader['resultMsg'] = resultMsg[4]
            
        elif jsons['response']['msgHeader']['resultCode'] != "0":
            resultHeader['resultCode'] = "2"
            resultHeader['resultMsg'] = resultMsg[2]
            
        else:
            resultHeader['resultCode'] = "9"
            resultHeader['resultMsg'] = "알 수 없는 오류입니다."

        
    else:
        if data.status_code != 200:
            resultHeader['resultCode'] = "1"
            resultHeader['resultMsg'] = resultMsg[1]
        elif jsons['response']['msgHeader']['resultCode'] != "0":
            resultHeader['resultCode'] = "2"
            resultHeader['resultMsg'] = resultMsg[2]
            
        else:
            resultHeader['resultCode'] = "9"
            resultHeader['resultMsg'] = "알 수 없는 오류입니다."
            
    
    resultData['resultHeader'] = resultHeader
    resultData['resultBody'] = resultBody
    return resultData
