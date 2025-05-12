from fastapi import FastAPI
from fastapi.responses import JSONResponse
import requests
import json
import re

app = FastAPI()

@app.get("/")
def get_skool_data():
    # Dane logowania
    url = "https://api.skool.com/auth/login"
    payload = {
        "email": "Moznazyc@gmail.com",
        "password": "Moznazyc123!.."
    }
    headers = {
        "accept": "*/*",
        "accept-language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json",
        "origin": "https://www.skool.com",
        "priority": "u=1, i",
        "sec-ch-ua-platform": "Windows",
        "Cookie": "client_id=1a6cfcd10aab4115ab12fefcd866b912; auth_token=",
        "sec-fetch-site": "same-site",
        "referer": "https://www.skool.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
    }

    response = requests.post(url, headers=headers, json=payload)
    auth_token = response.headers.get("set-cookie", "").split("auth_token=")[-1].split(";")[0]

    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }

    response2 = requests.get("https://www.skool.com/mozna-zyc-2634", headers=headers2)
    html = response2.text

    match = re.search(r'__NEXT_DATA__"[^>]*>(\{.*?\})</script>', html)
    if match:
        json_data = json.loads(match.group(1))
        version = json_data.get('buildId')
    else:
        version = None

    members_url = f"https://www.skool.com/_next/data/{version}/mozna-zyc-2634/-/members.json?group=mozna-zyc-2634"

    return JSONResponse(content={
        "status_code": response.status_code,
        "auth_token": auth_token,
        "version": members_url
    })
