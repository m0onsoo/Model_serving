import os
import pymysql
import pandas as pd
import ast
from dotenv import  load_dotenv


load_dotenv()  # .env 파일을 불러와 환경 변수 설정

"""
MODEL_HOST = 'capstone-db.c9mguk040cbf.us-east-1.rds.amazonaws.com'
MODEL_PORT = 3306
MODEL_USER = 'model'
MODEL_PW = '1234'
DB = 'palette'
"""

# 환경 변수에서 DB 접근 정보 가져오기
MODEL_HOST = os.getenv('MODEL_HOST')
MODEL_PORT = int(os.getenv('MODEL_PORT'))
MODEL_USER = os.getenv('MODEL_USER')
MODEL_PW = os.getenv('MODEL_PW')
DB = os.getenv('DB')

# SQL Database에 연결
def DB_CONNECT():
    conn = pymysql.connect(
        host = MODEL_HOST,
        port = MODEL_PORT,
        user = MODEL_USER,
        passwd = MODEL_PW,
        db = DB,
        charset = 'utf8mb4'
    )

    cursor = conn.cursor()

    return cursor

def DATA_LOADER():
    # 현재 파일(main.py)의 디렉토리 경로를 가져옵니다.
    current_dir = os.path.dirname(__file__)

    # 'Data' 폴더 경로 설정
    data_folder = os.path.join(current_dir, '..', 'Data')

    # 유저/레스토랑 임베딩 로드
    user_path = os.path.join(data_folder, 'user_embedding.csv')
    user_embedding = pd.read_csv(user_path, index_col='user_id')

    restaurant_path = os.path.join(data_folder, 'rst_embedding.csv')
    restaurant_embedding = pd.read_csv(restaurant_path, index_col="user_id")

    # string 형식을 python list로 변환
    user_embedding['embedding'] = user_embedding['embedding'].apply(ast.literal_eval)
    restaurant_embedding["embedding"] = restaurant_embedding["embedding"].apply(ast.literal_eval)

    try:
        user_embedding.drop(columns='Unnamed: 0',inplace=True)
        restaurant_embedding.drop(columns='Unnamed: 0',inplace=True)
    except:
        pass

    return user_embedding, restaurant_embedding