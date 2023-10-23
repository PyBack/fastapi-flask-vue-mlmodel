# signal post example
import json
import requests


BASE = "http://localhost:5500/api/v2/"

payload = {'ticker': 'AAPL',
           'data': {'predict_eps': 0.45}
          }

headers = {'Content-Type': 'application/json'}
response = requests.post(BASE + 'ml_model/eps-predict-request', json=payload)

print(response.json(), response.status_code)
