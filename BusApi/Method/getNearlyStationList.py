import requests
from pprint import pprint
import xmltodict
import json


resultMsg = [
    '정상 처리',
    '오류'
]

# 0 : 정상처리
# 1 : 네트워크 오류
# 2 : 결과없음 
# 3 : 알 수 없는 오류 

def getNearlyStationList(latitude, longitude):
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice/searcharound?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&x=' + str(longitude) + '&y=' + str(latitude))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    pprint(jsons)
    resultHeader = {}
    resultBody = {}
    returnData = {}
    nearlyStationList = []
    if data.status_code == 200 and jsons['response']['msgHeader']['resultCode'] == "0":         # 정상
        print(jsons['response']['msgHeader']['resultCode'])
        try:
            if jsons['response']['msgHeader']['resultCode'] == '0' :                
                for station in jsons['response']['msgBody']['busStationAroundList']:
                    if station['mobileNo'] != '00000':
                        nearlyStationList.append(station)
                resultBody['nearlyStationList'] = nearlyStationList    
                resultHeader['resultCode'] = '0'
                resultHeader['resultMsg'] = resultMsg[0]
            else:
                print("결과가 없습니다.")
                resultHeader['resultCode'] = '1'
                resultHeader['resultMsg'] = resultMsg[1]
                
        except Exception as e:
            print(e)
            print("알 수 없는 오류 ")
            resultHeader['resultCode'] = '1'
            resultHeader['resultMsg'] = resultMsg[1]
    else:                       
        print("통신오류, ValueError") 
        resultHeader['resultCode'] = '1'
        resultHeader['resultMsg'] = resultMsg[1]
 
    returnData['resultHeader'] = resultHeader
    returnData['resultBody'] = resultBody 
    print("returnData =--------------------------------------------------------------------------------------------------------------------------------------")
    pprint(returnData)
    
    return returnData
