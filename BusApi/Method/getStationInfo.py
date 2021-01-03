import requests
from pprint import pprint
import xmltodict
import json



resultMsg = ['정상처리', '정류소 통신 에러', '정류소 정보 에러', '노선 리스트 통신 에러', '노선 리스트 정보 에러', '관할지역이 아닙니다.', '노선 리스트 value Error']    

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
    print(data.status_code)
    
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    print(jsons['response']['msgHeader']['resultCode'])
    item = {}
    if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0":
        print("pass!!")
       
        if type(jsons['response']['msgBody']['busStationList']) == type(list()):
            for i in jsons['response']['msgBody']['busStationList']:
                if i['stationId'] == stationId:
                    item = i
        else:
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
        
        resultHeader['resultCode'] = '0'
        resultHeader['resultMsg'] = resultMsg[0]
        
        throughRouteList = []
    
        data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice/route?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&stationId=' + str(stationId))
        dicts = xmltodict.parse(data.text)
        jsons = json.loads(json.dumps(dicts))
        
        print(data.status_code)
        print(jsons['response']['msgHeader']['resultCode'])
        
        if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0" and resultBody['districtCd'] == "2":
            if type(jsons['response']['msgBody']['busRouteList']) == type(list()):
                for route in jsons['response']['msgBody']['busRouteList']:
                    tmp = {}
                    tmp['routeId'] = route['routeId']
                    tmp['routeName'] = route['routeName']
                    throughRouteList.append(tmp)
            else:
                tmp['routeId'] = jsons['response']['msgBody']['busRouteList']['routeId']
                tmp['routeName'] = jsons['response']['msgBody']['busRouteList']['routeName']
                throughRouteList.append(tmp)

            resultBody['throughRouteList'] = throughRouteList    
        else :
            if data.status_code != 200:
                print("통신에러 ")
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
        if code.status_code != 200:
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
    pprint(resultData)
    return resultData

# pprint(getStationInfo(38553))

