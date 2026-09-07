# FastAPI 세미나 과제 1

본 과제에서는 세미나에서 배우지 않은 내용이 나올 수 있습니다. 과제를 수행하면서 모르는 부분이 있으면 AI에게 물어보거나 검색을 통해 스스로 해결해보세요. 단 AI에게 생성을 요청하지는 말아주세요. 또는 #fastapi-잡담 채널에서 질문해도 좋습니다. 답을 알려드리지는 않지만 방향을 잡아드릴 수 있습니다.

## 과제 목표

- HTTP 요청의 Path Parameter, Query Parameter, Body를 원하는 형태로 파싱할 수 있다.

- Pydantic을 사용하여 데이터의 유효성을 검증하고 원하는 형태로 HTTP 응답을 생성할 수 있다.

## 준비 사항

- 모든 과제는 `python 3.12` 버전을 사용할 것을 전제로 합니다.  오늘 실습 시간에 설치한 `uv`를 이용해 `python 3.12` 버전을 설치하세요.
    - `uv python install 3.12` 명령어로 `python 3.12` 버전을 설치할 수 있습니다.

- 과제의 스켈레톤 코드와 수행에 필요한 라이브러리, 모듈 목록은 기본으로 제공됩니다.
    - 스켈레톤 코드는 레포지토리에 기본적으로 포함되어 있습니다.
    - 라이브러리, 모듈 목록은 레포지토리의 `uv.lock` 파일에 내장되어 있습니다.
        - `uv venv` 명령어를 통해 가상환경을 생성한 후,
        - `uv sync` 명령어를 통해 `uv.lock` 파일에 있는 명시된 라이브러리, 모듈들이 가상환경에 설치됩니다.
        - `uv.lock`에서 저희가 사전에 명시한 라이브러리, 모듈 외에는 활용하지 말아주세요(`uv add`, `pip install` 사용 금지)
 
- `uv` 설치 및 사용에 관한 구체적인 내용은 [`uv` 공식문서](https://docs.astral.sh/uv/)를 참조하세요.

## 과제 요구사항 

사용자의 회원정보를 관리하는 API를 구현합니다.

데이터베이스를 아직 배우지 않았기 때문에, 이번 과제에서는 In-memory 방식으로 데이터를 저장하고 관리합니다. (즉, 서버를 껐다 켜면 데이터가 초기화됩니다.)

데이터베이스 대신에 파이썬 딕셔너리(`user_db`)를 이용하고 `user_db`에 다음과 같은 형식으로 저장됩니다.

```JSON
{
    "user_id": {
        "name": "string",
        "phone_number": "string",
        "height": "float",
        "bio": "string"
    }
}
```

### 예시
```
{
  1: {
    "name": "김와플",
    "phone_number": "010-1234-5678",
    "height": 175.5,
    "bio": "안녕하세요"
  },
  2: {
    "name": "이서버",
    "phone_number": "010-1111-2222",
    "height": 172.3
  }
}
```

### 1. 회원 정보 등록 API
`POST /api/users`

사용자의 프로필 정보를 받아 등록하는 API입니다. 사용자 등록 시 user_id는 1부터 시작해 순차적으로 증가합니다.

**요청 본문 (Request Body)** 은 JSON 형식이며, 다음 필드를 포함해야 합니다.

- `name (str)`: 필수값입니다.

- `phone_number (str)`: 필수값이며, 010-XXXX-XXXX 형식이어야 합니다. 형식이 맞지 않으면 에러를 반환해야 합니다.

- `height (float)`: 필수값입니다.

- `bio (str)`: 선택값이며(필수 아님), 500자를 넘을 수 없습니다. 500자를 넘으면 에러를 반환해야 합니다.

요청 예시
```
{
  "name": "김와플",
  "phone_number": "010-1234-5678",
  "height": 175.5,
  "bio": "안녕하세요"
}
```

**성공 응답 (Success Response)**

응답 본문은 등록된 사용자의 전체 정보를 포함하는 DTO(Data Transfer Object) 형식이어야 합니다. 서버에서 생성된 user_id를 포함해야 합니다.

응답 예시
```JSON
{
  "user_id": 1,
  "name": "김와플",
  "phone_number": "010-1234-5678",
  "height": 175.5,
  "bio": "안녕하세요 컴퓨터공학과에 재학중인 김와플입니다."
}
```


**실패 응답 (Error Response)**

- 필수 필드가 누락되거나, 데이터 형식이 잘못된 경우 422 Unprocessable Entity를 반환하도록 합니다. 따로 처리를 할 필요는 없고, Pydantic 모델의 유효성 검사를 통과하지 못했을 때 422 Unprocessable Entity가 발생합니다.

- phone_number 형식이 올바르지 않거나(010-XXXX-XXXX 형태), bio의 길이가 500자를 초과하는 경우 적절한 메시지와 함께 ValueError를 raise하도록 합니다.

(힌트) 
- pydantic의 모델 내에서 특정 필드 값을 검증하기 위해서 field_validator 데코레이터를 사용해보세요.
- phone_number 형식을 검증하기 위해서 python 내장 모듈인 re 모듈을 사용해 보세요.

### 2. 특정 회원 정보 조회 API
`GET /api/users/{user_id}`

user_id를 Path Parameter로 받아 특정 회원의 정보를 반환하는 API입니다.

**성공 응답 (Success Response)**

응답 본문은 해당 user_id를 가진 사용자의 전체 정보(회원 등록 API의 성공 응답과 동일한 DTO)를 포함해야 합니다.

**실패 응답 (Error Response)**

해당 user_id를 가진 사용자가 존재하지 않을 경우, 적절한 메세지와 함께 ValueError을 raise하도록 합니다.

### 3. 키(height)로 회원 필터링 API
`GET /api/users`

사용자의 키(height)를 기준으로 필터링하여 조건에 맞는 사용자 목록을 반환하는 API입니다.

min_height와 max_height를 Query Parameter로 받습니다.

예시: /api/users?min_height=170&max_height=180

**성공 응답 (Success Response)**

min_height 이상, max_height 이하의 키를 가진 모든 사용자의 정보가 다음과 같은 리스트 형태로 반환되어야 합니다.

min_height가 170이고, max_height가 180인 경우

```JSON
[
  {
    "user_id": 2,
    "name": "김와플",
    "phone_number": "010-8765-4321",
    "height": 175.0,
    "bio": "안녕하세요. 어쩌고저쩌고"
  },
  {
    "user_id": 4,
    "name": "이서버",
    "phone_number": "010-1111-2222",
    "height": 172.3,
    "bio": null
  }
]
```

조건에 맞는 사용자가 없다면 빈 리스트([])를 반환합니다.

## 제출 방법
과제 수락 시 생성된 레포지터리의 `main` 브랜치에 완성된 코드를 push하세요.

**(주의⚠️) Feedback PR 은 머지하지 마세요!!**
