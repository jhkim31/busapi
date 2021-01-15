import requests
from pprint import pprint
import xmltodict
import json



resultMsg = [
    '정상처리', 
    '정류소 정보를 가져오던 중 통신 에러가 발생했습니다.', 
    '정류소 정보를 가져오던 중 value Error가 발생했습니다. 관할지역이 아닐 수 있습니다.', 
    '노선 리스트를 가져오던 중 통신 에러가 발했습니다.', 
    '관할 지역이 아닙니다 (서울 / 인천) ', 
    '노선 리스트를 가져오던 중 value Error가 발생했습니다.' 
]    

# 0 : 정상처리
# 1 : 정류소 통신에러
# 2 : 정류소 정보 에러 
# 3 : 노선리스트 통신 에러
# 4 : 관할지역 아님 
# 5 : 노선 리스트 value Error
 
    
def getStationInfo(mobileNo, stationId):
    tmp = {}
    resultHeader = {}
    resultBody = {}
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&keyword=' + str(mobileNo))
    
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    
    pprint(jsons)

    item = {}
    if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0":             # 정상 호출 
        if type(jsons['response']['msgBody']['busStationList']) == type(list()):                    # 정상 호출 and 배열로 올때 (2개 이상)
            for i in jsons['response']['msgBody']['busStationList']:
                if i['stationId'] == stationId:                                     
                    item = i                                                                        # mobileNo가 같은 2개이상의 정류장에서 Id로 한 정류장 특정  
        else:                                                                                       # 정상 호출  and 하나만 올때 (1개)
            item = jsons['response']['msgBody']['busStationList']
            
        pprint(item)
        resultBody['stationId'] = item['stationId']
        resultBody['stationName'] = item['stationName']
        coordinate = {}
        coordinate['latitude'] = item['y']
        coordinate['longitude'] = item['x']
        resultBody['coordinate'] = coordinate
        resultBody['mobileNo'] = item['mobileNo']
        resultBody['districtCd'] = item['districtCd']
        resultBody['regionName'] = item['regionName']
        
        throughRouteList = []
    
        data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&stationId=' + str(stationId))
        dicts = xmltodict.parse(data.text)
        jsons = json.loads(json.dumps(dicts))
        
        if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0" and resultBody['districtCd'] == "2":      #정상 진행 시 리스트를 받기위해 추가로 다른 api에 호출 (정상진행) 
            if type(jsons['response']['msgBody']['busRouteList']) == type(list()):                                                  #배열 (2개 이상 올때)    
                for route in jsons['response']['msgBody']['busRouteList']:
                    tmp = {}
                    tmp['routeId'] = route['routeId']
                    tmp['routeName'] = route['routeName']
                    tmp['staOrder'] = route['staOrder']
                    throughRouteList.append(tmp)
            else:                                                                                                                       #1개만 올때 
                tmp['routeId'] = jsons['response']['msgBody']['busRouteList']['routeId']
                tmp['routeName'] = jsons['response']['msgBody']['busRouteList']['routeName']
                tmp['staOrder'] = jsons['response']['msgBody']['busRouteList']['staOrder']
                throughRouteList.append(tmp)
                
            resultHeader['resultCode'] = '0'                                                            # 정상호출시 리턴코드 0
            resultHeader['resultMsg'] = resultMsg[0]
                 
            resultBody['throughRouteList'] = throughRouteList                                           # 정상 진행 
        else :
            if data.status_code != 200:                                                                                         # 리스트 통신 에
                print("통신에러")
                resultHeader['resultCode'] = '3'
                resultHeader['resultMsg'] = resultMsg[3]
            elif resultBody['districtCd'] != "2":
                print("관할지역이 아닙니다 (서울 또는 인천)")
                print(resultBody['districtCd'])
                resultHeader['resultCode'] = '4'
                resultHeader['resultMsg'] = resultMsg[4]
            else:
                print('노선 리스트 value Error')
                resultHeader['resultCode'] = '5'
                resultHeader['resultMsg'] = resultMsg[5]
        
    else:
        if data.status_code != 200:
            print("통신오류")
            resultHeader['resultCode'] = '1'
            resultHeader['resultMsg'] = resultMsg[1]
        else:
            print("value Error")
            resultHeader['resultCode'] = '2'
            resultHeader['resultMsg'] = resultMsg[2]
    

            
    resultData = {}
    resultData['resultHeader'] = resultHeader
    resultData['resultBody'] = resultBody
    print('resultData ------------------------------------------------------------------')
    pprint(resultData)
    return resultData

# pprint(getStationInfo(38553))

