import requests
import json

url = "https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens"
HEADERS = { "Content-Type": "application/json" }
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
print(res.headers['X-Subject-Token'])