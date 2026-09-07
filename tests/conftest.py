from typing import Generator

import pytest
from fastapi.testclient import TestClient

from src.dto import CreateUserRequest
from src.main import user_db, app

@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as client:
        yield client
    
    client.close()


@pytest.fixture
def user_list() -> dict[int, dict]:
    user_db.clear()
    
    for i in range(1, 21):
        user_db[i] = {
            "name": f"이름{i}",
            "phone_number": f"010-1234-0000",
            "height": (165.3+i)
        }
        
    return user_db

@pytest.fixture
def create_user_req() -> dict:
    return {
        "name": "김와플",
        "phone_number": "010-1234-5678",
        "height": 175.5
    }

@pytest.fixture
def create_user_req_with_bio() -> dict:
    return {
        "name": "이와플",
        "phone_number": "010-1111-2222",
        "height": 182.5,
        "bio": "안녕하세요"
    }

@pytest.fixture
def create_user_req_invalid_number() -> dict[str, str | float]:
    return {
        "name":"김와플",
        "phone_number":"01012341234",
        "height":181.5
    }

@pytest.fixture
def client_with_multiple_users() -> Generator[TestClient, None, None]:
    with TestClient(app, raise_server_exceptions=False) as client:
        user_db.clear()
        for i in range(1, 21):
            req = {
                "name": f"이름{i}",
                "phone_number": f"010-1234-0000",
                "height": (165.3+i),
                "bio": f"안녕하세요! 저는 {i}번째 사용자입니다."
            }
            client.post("/api/users/", json=req)
        yield client
    
    client.close()