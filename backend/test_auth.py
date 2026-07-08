import urllib.request
import json

def test_auth():
    url_reg = "http://127.0.0.1:8000/auth/register"
    data_reg = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123"
    }
    
    headers = {"Content-Type": "application/json"}
    
    # 1. Register
    print("Testing /auth/register...")
    req = urllib.request.Request(url_reg, data=json.dumps(data_reg).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode("utf-8"))
            print(f"Register Success! Response: {res}")
    except Exception as e:
        if hasattr(e, 'read'):
            print(f"Register Failed: {e.code} - {e.read().decode('utf-8')}")
        else:
            print(f"Register Failed: {e}")
            
    # 2. Login
    print("\nTesting /auth/login...")
    url_login = "http://127.0.0.1:8000/auth/login"
    # FastAPI OAuth2PasswordRequestForm expects form data: username and password
    data_login = urllib.parse.urlencode({
        "username": "test@example.com",
        "password": "password123"
    }).encode("utf-8")
    
    headers_login = {"Content-Type": "application/x-www-form-urlencoded"}
    req_login = urllib.request.Request(url_login, data=data_login, headers=headers_login, method="POST")
    try:
        with urllib.request.urlopen(req_login) as response:
            res = json.loads(response.read().decode("utf-8"))
            print(f"Login Success! Response: {res}")
    except Exception as e:
        if hasattr(e, 'read'):
            print(f"Login Failed: {e.code} - {e.read().decode('utf-8')}")
        else:
            print(f"Login Failed: {e}")

if __name__ == "__main__":
    test_auth()
