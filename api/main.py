import uvicorn
from fastapi import FastAPI
import pandas as pd
import ast
import json
import torch
from torch import nn
import numpy as np
import os
# import functions
import pymysql
from dotenv import load_dotenv

load_dotenv()  # .env 파일을 불러와 환경 변수 설정

# 환경 변수에서 DB 접근 정보 가져오기
MODEL_HOST = os.getenv('MODEL_HOST')
MODEL_PORT = os.getenv('MODEL_PORT')
MODEL_USER = os.getenv('MODEL_USER')
MODEL_PW = os.getenv('MODEL_PW')
DB = os.getenv('DB')

MODEL_HOST = 'capstone-db.c9mguk040cbf.us-east-1.rds.amazonaws.com'
MODEL_PORT = 3306
MODEL_USER = 'model'
MODEL_PW = '1234'
DB = 'palette'


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

# DB에 연결
cursor = DB_CONNECT()

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

# 활성 함수 정의
activate_f = nn.Sigmoid()

# 전체 레스토랑에 대한 임베딩 텐서화
embeddings_list = restaurant_embedding['embedding'].tolist()
embeddings_tensor = torch.tensor(embeddings_list)

app = FastAPI()

# Default Screen
@app.get("/")
def root():
    return {"Default": "Hello World-!"}


# 단일 유저 추천
@app.get("/recommend")
async def recommend(user: int):
    # 유저 임베딩 텐서화
    user_embedding_vector = torch.tensor(user_embedding.loc[user,'embedding'])
    
    # 단일 유저 추론
    one_user_predict = activate_f(torch.matmul(user_embedding_vector,embeddings_tensor.t()))
    _, one_user_rating = torch.topk(one_user_predict, k=100)
    result_restaurant_list = np.array(one_user_rating).tolist()

    result_dict = {
        "user_num": user,
        "result": result_restaurant_list
    }

    return json.dumps(result_dict)


# 커플 유저 추천
@app.get("/recommend/couple")
async def recommend_couple(user1: int, user2: int):
    # 각 유저의 임베딩 텐서화
    user1_embedding_vector = torch.tensor(user_embedding.loc[user1,'embedding'])
    user2_embedding_vector = torch.tensor(user_embedding.loc[user2,'embedding'])

    # 커플 임베딩 생성
    couple_embedding_vector = torch.mul(user1_embedding_vector, user2_embedding_vector)
    
    # 커플 유저 결과 추론
    couple_user_predict = activate_f(torch.matmul(couple_embedding_vector, embeddings_tensor.t()))
    _, couple_user_rating = torch.topk(couple_user_predict,k=50)
    result_restaurant_list = np.array(couple_user_rating).tolist()

    # sql문에 넣을 id들의 집합
    ids_query = ', '.join(map(str, result_restaurant_list))

    # 결과값에 매칭되는 RST/CAFE/BAR인지의 types 리스트 요청
    sql = f"SELECT type FROM restaurant WHERE restaurant_id IN ({ids_query})"
    cursor.execute(sql)
    types = cursor.fetchall()

    # 결과값 음식점/카페/술집 분리
    RST, CAFE, BAR = [], [], []
    for result_id, type in zip(result_restaurant_list, types):
        category = type[0]

        if category == 'RST':
            RST.append(result_id)
        elif category == 'CAFE':
            CAFE.append(result_id)
        else:
            BAR.append(result_id)


    # 결과값 딕셔너리화
    result_dict = {
        "RST": RST,
        "CAFE": CAFE,
        "BAR": BAR
    }

    return result_dict


# main
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)