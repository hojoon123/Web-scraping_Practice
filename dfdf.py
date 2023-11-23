import requests

api_key = "123"
user_id = "rhzn5512"

url = f"https://solved.ac/api/v3/user/show?apiKey={api_key}&handle={user_id}"
response = requests.get(url).json()
response['rank']
response['tier']
response['rating']
response['exp']
print(response['rank'])
print(response['tier'])
print(response['rating'])
print(response['exp'])
print(response)