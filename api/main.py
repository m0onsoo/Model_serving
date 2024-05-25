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

app = FastAPI()

@app.get("/")
def root():
    return {"Default": "Hello World-!"}


@app.get("/recommend")
def recommend(user: int):
    # 'Data' 폴더와 'user_embedding.csv' 파일의 경로를 설정합니다.
    data_folder = os.path.join(current_dir, '..', 'Data')

    # 파일 경로 출력 (확인용)
    print(f"File path: {data_folder}")


    # 단일 유저 추천 결과
    user_path = os.path.join(data_folder, 'user_embedding.csv')
    u_emb = pd.read_csv(user_path, index_col='user_id')

    restaurant_path = os.path.join(data_folder, 'user_embedding.csv')
    r_emb = pd.read_csv(restaurant_path, index_col="user_id")

    # string 형식을 python list로 변환
    u_emb['embedding']=u_emb['embedding'].apply(ast.literal_eval)
    r_emb["embedding"] = r_emb["embedding"].apply(ast.literal_eval)

    try:
        u_emb.drop(columns='Unnamed: 0',inplace=True)
        r_emb.drop(columns='Unnamed: 0',inplace=True)
    except:
        pass

    activate_f=nn.Sigmoid()
    # 전체 레스토랑에 대한 임베딩 텐서화
    tmp=[]
    for i in range(len(r_emb)):
        tmp.append(r_emb.loc[i,'embedding'])
    rst_embedding_matrix=torch.tensor(tmp)




    user_embedding_vector=torch.tensor(u_emb.loc[user,'embedding'])
    
    # user = request.files['user']
    one_user_predict=activate_f(torch.matmul(user_embedding_vector,rst_embedding_matrix.t()))
    _, one_user_rating=torch.topk(one_user_predict,k=100)
    result_user = np.array(one_user_rating).tolist()

    result_dict = {
        'user_num':user,
        'result':result_user
    }


    return json.dumps(result_dict)



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)