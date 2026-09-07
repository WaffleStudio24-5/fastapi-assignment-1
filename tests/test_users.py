import pytest
import json
from fastapi.testclient import TestClient

from src.dto import CreateUserRequest
from src.dto import UserResponse
from src.main import app, user_db

client = TestClient(app)

# Test for create user

def test_create_user(
    create_user_req: dict,
    client: TestClient
):
    res = client.post("/api/users", json=create_user_req)
    res_json = res.json()
    
    assert res_json["user_id"] is not None
    assert res_json["name"] == create_user_req["name"]
    assert res_json["phone_number"] == create_user_req["phone_number"]
    assert res_json["height"] == create_user_req["height"]

def test_create_user_with_bio(
    create_user_req_with_bio: dict,
    client: TestClient
):
    res = client.post("/api/users", json=create_user_req_with_bio)
    res_json = res.json()

    assert res_json["user_id"] is not None
    assert res_json["name"] == create_user_req_with_bio["name"]
    assert res_json["phone_number"] == create_user_req_with_bio["phone_number"]
    assert res_json["height"] == create_user_req_with_bio["height"]
    assert res_json["bio"] == create_user_req_with_bio["bio"]

def test_create_user_invalid_number(
    create_user_req_invalid_number: dict[str, str | float],
    client: TestClient
):
    res = client.post("/api/users", json=create_user_req_invalid_number)
    
    assert res.status_code != 200

# 이름 없을 때
def test_create_user_with_no_name(client: TestClient):
    req = {
        "phone_number": "010-1234-5678",
        "height": 180.5
    }
    res = client.post("/api/users", json=req)

    assert res.status_code != 200

# Phone_number 없을 때
def test_create_user_with_no_phone_number(client: TestClient):
    req = {
        "name": "FastAPI",
        "height": 180.5
    }
    res = client.post("/api/users", json=req)

    assert res.status_code != 200

# Phone_number 형식 틀릴 때
def test_create_user_with_invalid_phone_number(client: TestClient):
    req = {
        "name": "FastAPI",
        "phone_number": "01012345678",
        "height": 180.5
    }
    res = client.post("/api/users", json=req)

    assert res.status_code != 200

# phone_number가 int로 주어졌을 때
def test_create_user_with_int_phone_number(client: TestClient):
    req = {
        "name": "FastAPI",
        "phone_number": 1012345678,
        "height": 180.5
    }
    res = client.post("/api/users", json=req)

    assert res.status_code != 200

# height가 없을 때
def test_create_user_with_no_height(client: TestClient):
    req = {
        "name": "FastAPI",
        "phone_number": "010-1234-5678"
    }
    res = client.post("/api/users", json=req)

    assert res.status_code != 200

# height가 str으로 주어졌을 때
def test_create_user_with_str_height(client: TestClient):
    req = {
        "name": "FastAPI",
        "phone_number": "010-1234-5678",
        "height": "180.5"
    }
    res = client.post("/api/users", json=req)

    if res.status_code != 422:
        res_json = res.json()
        assert res_json["name"] == "FastAPI"
        assert res_json["phone_number"] == "010-1234-5678"
        assert isinstance(res_json["height"], float)
        assert res_json["height"] == 180.5
    else:
        assert res.status_code == 422

# bio가 500자를 넘을 때
def test_create_user_with_long_bio(client: TestClient):
    long_bio = "a" * 501
    req = {
        "name": "FastAPI",
        "phone_number": "010-1234-5678",
        "height": 180.5,
        "bio": long_bio
    }
    res = client.post("/api/users", json=req)

    assert res.status_code != 200

# 두 가지 이상의 조건을 만족하지 못할 때
def test_create_user_with_multiple_invalid_fields(client: TestClient):
    req = {
        "phone_number": "01012345678",
        "height": "eighty"
    }
    res = client.post("/api/users", json=req)

    assert res.status_code != 200

# Test for get user by id

def test_create_and_get_user_by_id(
    create_user_req: dict,
    client: TestClient
):
    create_response = client.post("/api/users", json=create_user_req)
    created_id = create_response.json()["user_id"]
    
    res = client.get(f"/api/users/{created_id}")
    res_json = res.json()

    assert res.status_code == 200
    assert res_json["user_id"] == created_id
    assert res_json["name"] == create_user_req["name"]
    assert res_json["phone_number"] == create_user_req["phone_number"]
    assert res_json["height"] == create_user_req["height"]

# 없는 id로 조회할 때
def test_get_user_by_nonexistent_id(client_with_multiple_users: TestClient):
    res = client_with_multiple_users.get("/api/users/9999")
    assert res.status_code != 200



# Test for get users with query string

def test_get_users_with_query(
    client_with_multiple_users: TestClient
):
    res = client_with_multiple_users.get("/api/users?min_height=166.3&max_height=175.3")
    res_json = res.json()
    
    assert res.status_code == 200
    assert len(res_json) == 10

    for user in res_json:
        assert (user['height'] >= 165.3 and user['height'] <= 175.3)

# 조건 만족시키는 user가 없을 때
def test_get_users_with_no_matching_users(
    client_with_multiple_users: TestClient
):
    res = client.get("/api/users?min_height=300&max_height=400")
    res_json = res.json()
    assert res.status_code == 200
    assert len(res_json) == 0