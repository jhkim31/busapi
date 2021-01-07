import requests
from pprint import pprint
import xmltodict
import json

resultMsg = ['정상처리', '남은 버스가 없습니다', '노선 ID value Error', '정거장리스트 통신 에러', '노선 리스트 정보 에러', '관할지역이 아닙니다.', '노선 ID value Error']    


# 0 : 정상처리
# 1 : 남은 버스가 없습니다.
# 2 : 노선 ID value Error 
# 3 : 정거장리스트 통신 에러
# 4 : 관할지역 아님 
# 5 : 노선ID value Error
# 9 : 알수없는 오류입니다.

def getArrivalInformation(stationId):
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busarrivalservice/station?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&stationId=' + str(stationId))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    resultData = {}
    busArrivalList = []
    resultBody = {}
    resultHeader= {}
    if jsons['response']['msgHeader']['resultCode'] == "0":
        lists = jsons['response']['msgBody']['busArrivalList']
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
                
                resultHeader['resultCode'] = '0'
                resultHeader['resultMsg'] = resultMsg[0]
                
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
            
        resultData['resultHeader'] = resultHeader
        resultData['resultBody'] = resultBody
            
    elif jsons['response']['msgHeader']['resultCode'] == "4":
        resultHeader['resultCode'] = '1'
        resultHeader['resultMsg'] = resultMsg[1]
        resultData['resultHeader'] = resultHeader
    pprint(resultData)
    return resultData
    