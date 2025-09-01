import pytest
import requests

BASE_URL = "http://127.0.0.1:8000/"

@pytest.fixture(scope="session")
def auth_token():
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "info@theonemind.kr",
        "password": "Another12trongP@ss!"
    })
    assert response.status_code == 200, "Login failed!"
    return response.json()['accessToken']

@pytest.fixture()
def auth_headers(auth_token):
    return {"Authorization": f"Bearer {auth_token}"}

@pytest.fixture
def new_admin_payload():
   return {
      "username": "testuser",
      "name": "John",
      "surname": "Asatryan",
      "email": "testuser@example.com",
      "image_url": "https://example.com/image.png",
      "password": "Password123!",
      "sensitive_info": {
        "country": "USA",
        "city": "New York",
        "state": "NY",
        "street": "5th Avenue",
        "zip_code": "10001"
        },
      "phone_number": "+99222225",
      "role": "admin"
    }

@pytest.fixture
def admin_login():
  return {
    "email": "testuser@example.com",
    "password": "Password123!"
  }
   
@pytest.fixture
def new_user_payload():
  return {
    "username": "newuser34",
    "name": "Alice",
    "surname": "Smith",
    "email": "alice.smith5678@example.com",
    "image_url": "https://example.com/profile.jpg",
    "password": "SecurePass456!",
    "sensitive_info": {
      "country": "UK",
      "city": "London",
      "state": "England",
      "street": "Baker Street",
      "zip_code": "NW1 6XE"
    },
    "phone_number": "+441632960960",
    "role": "admin"
    }

@pytest.fixture
def new_user_login():
  return {
    "email": "alice.smith5678@example.com",
    "password": "SecurePass456!"
  }

@pytest.fixture
def another2_user_payload():
  return {
    "username": "testuser998",
    "name": "Bob",
    "surname": "Johnson",
    "email": "info@theonemind.kr",
    "image_url": "https://example.com/avatar.png",
    "password": "Another12trongP@ss!",
    "sensitive_info": {
      "country": "US",
      "city": "New York",
      "state": "NY",
      "street": "5th Avenue",
      "zip_code": "10001"
    },
    "phone_number": "+1212558851234",
    "role": "admin"
    }

@pytest.fixture
def another2_login():
  return {
    "email": "info@theonemind.kr",
    "password": "Another12trongP@ss!"
  }
