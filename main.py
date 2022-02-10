from flask import escape
from pylib.googleadmin import authService

        
escopo = ['https://www.googleapis.com/auth/admin.directory.device.chromeos']
servico = authService(escopo,"cred.json","lucas@gsaladeaula.com.br").getService('admin','directory_v1')
def updateChromeInfo(request):
    content_type = request.headers['content-type']
    if content_type == 'application/json':
        request_json = request.get_json(silent=True)
        if request_json and 'device_id' in request_json:
            device_id = request_json['device_id'] or None
            lat = request_json['lat'] or None
            lon = request_json['lon'] or None
            print("É json")
        else:
            raise ValueError("JSON is invalid, or missing a 'name' property")
    r = servico.chromeosdevices().update(
        customerId = 'my_customer',
        # deviceId  = "ff12b7bf-9de2-470e-a84b-32ec498c8b54",#args['device_id'], lucas chrome
        deviceId  = device_id,
        body={"annotatedLocation":"{}-{}".format(lat,lon) }
    ).execute()
    return {"id":r.get('deviceId','N/A')},201