import requests

API_KEY = "AIzaSyBxNbXv6fBE9ms_4M2ljNpmha3seETkBgw"

url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

r = requests.get(url)

print(r.json())