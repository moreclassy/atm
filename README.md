# atm
atm project

# Getting Started
## python3 with virtualenv
- 작업 디렉토리로 이동 후 가상환경 venv 설치(python 3.8)
  - `python3 -m venv venv`
- 가상환경 active
  - `source venv/bin/activate`

# structure
## atm_service.py
- atm 서비스 클래스
- atm의 카드 읽기, 입금, 출금 기능 수행

## bank_service.py
- 은행 api를 호출

## cash_bin.py
- atm의 현금통

## data.py
- 은행 api의 database mocking

## exception.py
- custom exceptions

## model.py
- data model
- 계좌 정보를 다루는 Account 모델 정의

## test.py
- 테스트 코드

# test
- 프로젝트 루트에서 `python -m unittest` 실행
