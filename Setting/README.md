# Initial Setting
pyenv로 가상환경을 생성하고 poetry로 라이브러리 버전을 관리합니다.

## Getting Started
FastAPI 서버를 EC2에 올려 모델 서빙을 구현합니다.

### Prerequisites
파이썬 가상환경 버전을 3.9.6으로 통일하기 위해 버전을 설치합니다.
'''
pyenv install 3.9.6
'''
해당 프로젝트에서만 사용할 로컬 파이썬 버전을 설정하고 가상환경을 생성합니다.
'''
# local 파이썬 버전 설정
pyenv local 3.9.6

# Poetry로 가상환경 생성
poetry env use python3

# 가상환경 활성화
poetry shell

# 가상환경 비활성화
poetry deactivate
'''

### poetry install
pyproject.toml에 저장된 내용에 기반해 라이브러리 설치
'''
poetry install
'''

### FastAPI 서버 실행
FastAPI 서버를 실행하는 코드입니다.
http://127.0.0.1:8000/docs에서 API 문서를 확인할 수 있습니다.
'''
poetry run uvicorn backend.main:app
'''

## 라이브러리 추가 설치/삭제
poetry add 뒤에 라이브러리 이름을 적어주면 자동으로 호환되는 버전을 다운받습니다.
이는 pyporject.toml에 추가됩니다.
'''
# example
poetry add fastapi
'''
특정 라이브러리를 삭제할 때는 poetry remove를 사용합니다.
'''
poetry remove libray-name
'''


## Reference
poetry와 pyenv를 사용한 개발 환경 세팅
* [Poetry 공식 docs](https://python-poetry.org/docs/)
* [Poetry 파이썬 개발 환경 구축 1](https://velog.io/@hj8853/Poetry%EB%A5%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EC%97%AC-%EA%B0%80%EC%83%81%ED%99%98%EA%B2%BD-%EB%A7%8C%EB%93%A4%EA%B8%B0)
* [Poetry 파이썬 개발 환경 구축 2](https://velog.io/@whattsup_kim/Python-%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%99%98%EA%B2%BD-%EA%B5%AC%EC%B6%95%ED%95%98%EA%B8%B0-2-Poetry)
* [Poetry 파이썬 개발 환경 구축 3](https://kkangsg.tistory.com/108)