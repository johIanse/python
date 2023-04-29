import os
import requests
​
credentials = os.environ.get('xpz')
if credentials:
  username, userpass = credentials.split('&')
  
url = "https://xiaopz.top/php/x.php"
​
data1 = {
    'username': username,
    'userpass': userpass,
    'c': 'users'
}
​
response1 = requests.post(url, data=data1)
​
if response1.status_code == 200:
  parts = response1.text.split(':')
  if len(parts) > 2:
        token = parts[2].strip().strip('"}')
        
​
        headers = {
          'Host': 'xiaopz.top',
          'referer': 'https://xiaopz.top/',
        }
        
        cookies = {
          'name': username,
          'pass': userpass,
          'token': token,
        }
​
        data2 = {
          'token': token,
          'c': 'Signin',
        }
​
        response = requests.post(url, headers=headers,cookies=cookies,data=data2)
print(response.text)
​