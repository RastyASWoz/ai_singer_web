import requests

# file_path = "C:\\Users\\33029\\Music\\vlc-record-2024-09-27-23h10m36s-moon gun-.wav"

# # 测试recv接口
# url = "http://127.0.0.1:5000/recv"
# files = {'file': open(file_path, 'rb')}
# response = requests.post(url, files=files)
# print(response.json())

# 测试send接口
url = "http://127.0.0.1:5000/send"
data = {
    'target_url': 'http://127.0.0.1:5000/recv',
    'filename': 'moon_gun.wav'
}
response = requests.post(url, json=data)

print(response.json())

