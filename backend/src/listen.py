import sseclient

messages = sseclient.SSEClient('http://localhost:5500/listen')

for msg in messages:
    print(msg)
