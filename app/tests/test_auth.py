import requests
from app.tests.conftest import BASE_URL

def test_register_user(another2_user_payload):
    response = requests.post(f"{BASE_URL}/auth/register", json=another2_user_payload)#json=payload)
    print(f"Register Response: {response.status_code}, {response.text}")
    assert response.status_code in [200, 201], f"Failed to register user: {response.text}"
    assert "id" in response.json()
    
    # Automatically verify the user after registration for testing
    import sqlite3
    conn = sqlite3.connect('test.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_verified = 1 WHERE email = ?', (another2_user_payload['email'],))
    conn.commit()
    conn.close()

def test_login_user(another2_login):
    response = requests.post(f"{BASE_URL}/auth/login", json=another2_login)
    print(f"Login Response: {response.status_code}, {response.text}")
    assert response.status_code == 200, f"Login failed: {response.text}"
    assert "accessToken" in response.json()