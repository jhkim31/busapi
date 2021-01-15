from flask import Flask
from flask import request
from Method.getRouteInfo import getRouteInfo
from Method.getStationInfo import getStationInfo
from Method.getNearlyStationList import getNearlyStationList
from Method.getArrivalInformation import getArrivalInformation
from Method.getCurrentLocation import getCurrentLocation


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/', methods=['GET'])
def hello_world():
    returnData = {}
    returnData['KIm'] = '김'
    return returnData
 
@app.route('/getRouteInfo')
def getRoute():    
    routeId = request.args.get('routeId')
    return getRouteInfo(routeId)

@app.route('/getStationInfo')
def getStation():
    mobileNo = request.args.get('mobileNo')
    stationId = request.args.get('stationId')
    return getStationInfo(mobileNo, stationId)

@app.route('/getNearlyStationList')
def getNearlyStation():
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    return getNearlyStationList(latitude = latitude, longitude = longitude)

@app.route('/getArrivalInformation')
def getArrival():
    stationId = request.args.get('stationId')
    return getArrivalInformation(stationId)
@app.route('/getCurrentLocation')
def getCurrent():
    routeId = request.args.get('routeId')
    return getCurrentLocation(routeId)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug= True)
    

    
