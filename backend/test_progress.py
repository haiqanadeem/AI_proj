import requests

base_url = "http://localhost:8000"
user_data = {
    "name": "Test User",
    "email": "testprogress@example.com",
    "password": "password123"
}

print("Registering...")
r1 = requests.post(f"{base_url}/auth/register", json=user_data)
print(r1.status_code, r1.text)

print("Logging in...")
r2 = requests.post(f"{base_url}/auth/login", data={"username": "testprogress@example.com", "password": "password123"})
print(r2.status_code, r2.text)

if r2.status_code == 200:
    token = r2.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nFetching progress...")
    r3 = requests.get(f"{base_url}/progress", headers=headers)
    print("Status:", r3.status_code)
    print("Body:", r3.text)

    print("\nFetching recommendation...")
    r4 = requests.get(f"{base_url}/progress/recommend", headers=headers)
    print("Status:", r4.status_code)
    print("Body:", r4.text)
else:
    print("Login failed, cannot fetch progress")
