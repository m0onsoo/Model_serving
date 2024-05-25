import uvicorn
from fastapi import FastAPI
import pandas as pd
import ast
import json
import torch
from torch import nn
import numpy as np
import os


# 현재 파일(main.py)의 디렉토리 경로를 가져옵니다.
current_dir = os.path.dirname(__file__)

# 'Data' 폴더 경로 설정
data_folder = os.path.join(current_dir, '..', 'Data')

# 유저/레스토랑 임베딩 로드
user_path = os.path.join(data_folder, 'user_embedding.csv')
user_embedding = pd.read_csv(user_path, index_col='user_id')

restaurant_path = os.path.join(data_folder, 'user_embedding.csv')
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
    user2_embedding_vector = torch.tensor(user_embedding.loc[user1,'embedding'])

    # 커플 임베딩 생성
    couple_embedding_vector = torch.mul(user1_embedding_vector, user2_embedding_vector)
    
    # 커플 유저 결과 추론
    couple_user_predict = activate_f(torch.matmul(couple_embedding_vector, embeddings_tensor.t()))
    _, couple_user_rating = torch.topk(couple_user_predict,k=100)
    result_restaurant_list = np.array(couple_user_rating).tolist()

    # 결과값 딕셔너리화
    result_dict = {
        "user1": user1,
        "user2": user2,
        "result": result_restaurant_list
    }

    return result_dict


# main
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)