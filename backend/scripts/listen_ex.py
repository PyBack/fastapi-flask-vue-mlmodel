# server sent event listen client example
import sseclient

# messages = sseclient.SSEClient('http://localhost:5500/listen')
messages = sseclient.SSEClient('http://localhost:5500/api/v2/ml_model/eps-predict-result')


for msg in messages:
    print(msg)
