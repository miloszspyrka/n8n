from fastapi import FastAPI, Request
import requests
import json
import time

app = FastAPI()

@app.post("/")
async def run_script(request: Request):
    input_data = await request.json()
    token = input_data.get('token', '')
    version = input_data.get('version', '')
    url = version

    headers = { "your": "headers" }  # <-- uzupełnij swoimi
    all_results = []

    for p in range(1, 30):
        params = {"t": "active", "group": "mozna-zyc-2634", "p": str(p)}
        time.sleep(1)
        response = requests.get(url, params=params, headers=headers)
        try:
            data = response.json()
        except ValueError:
            data = {"status": response.status_code, "text": response.text}
        all_results.append(data)

    def find_users(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if key == "users" and isinstance(value, list):
                    return value
                result = find_users(value)
                if result:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = find_users(item)
                if result:
                    return result
        return None

    users = find_users(all_results)
    users2 = users[0].get("member", {}).get("Pierwszy User Member Invite Email") if users else None

    return {
        "liczba_users": len(users) if users else 0,
        "pierwszy_user": users[0] if users else "Nie znaleziono users",
        "member": users2
    }
