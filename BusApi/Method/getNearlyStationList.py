import requests
from pprint import pprint
import xmltodict
import json

def getNearlyStationList(latitude, longitude):
    data = requests.get('http://openapi.gbis.go.kr/ws/rest/busstationservice/searcharound?serviceKey=yt0l1Mg%2FKtX60m%2B69cYQn%2BOIKLJEq3NMxGQDtVon3JJMgJMV4aRyIEChiBKM1Gi6EzwmOeP1dNQRSRTlPg9cvg%3D%3D&x=' + str(longitude) + '&y=' + str(latitude))
    dicts = xmltodict.parse(data.text)
    jsons = json.loads(json.dumps(dicts))
    
    returnData = {}
    
    returnData['nearlyStationList'] = jsons['response']['msgBody']['busStationAroundList']
    
    return returnData
        
    
    
    
    
