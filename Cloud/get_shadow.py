import requests
import json

url = "https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens"
HEADERS = {"Content-Type": "application/json"}
FormData = {
 "auth": {
  "identity": {
   "methods": [
    "password"
   ],
   "password": {
    "user": {
      "name": "qqqb",
      "password": "wan13688007964",
      "domain": {
       "name": "hid_nh5y032_-g3izl8"
      },
    }
   }
  }
 }
}


res = requests.post(url=url,data=json.dumps(FormData),headers=HEADERS)
res = res.headers['X-Subject-Token']

url = "https://iotda.cn-north-4.myhuaweicloud.com/v5/iot/666a6920c2c0cb155cc412f3/devices/666a6920c2c0cb155cc412f3_Hispark_CalosCan/shadow"
HEADERS = {'content-type': 'application/json', 'X-Auth-Token':res}
res_2 = requests.get(url=url,headers=HEADERS)
print(json.dumps(res_2.json(), indent=1))

response_data = res_2.json()


shadow_list = response_data.get('shadow', [])

first_shadow = shadow_list[0]
reported = first_shadow.get('reported', {})
time = reported.get('event_time')
properties = reported.get('properties', {})
control_module = properties.get('ControlModule')

print(control_module)
print(time)
