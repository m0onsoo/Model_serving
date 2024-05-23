from flask import Flask, jsonify, request
import json
import numpy as np

import pandas as pd
# import inference
# import dataloader
import world
# from tensorboardX import SummaryWriter
import time
from os.path import join
import ast
import torch
from torch import nn
app = Flask(__name__)


# m = inference.model_fn()
# dataset = dataloader.Loader(path="../data/gowalla")
# w : SummaryWriter = SummaryWriter(
#                                     join(world.BOARD_PATH, time.strftime("%m-%d-%Hh%Mm%Ss-") + "-" + world.comment)
#                                     )
u_emb = pd.read_csv("../user_embedding.csv",index_col='user_id')
r_emb = pd.read_csv("../rst_embedding.csv", index_col="user_id")
u_emb['embedding']=u_emb['embedding'].apply(ast.literal_eval)
r_emb["embedding"] = r_emb["embedding"].apply(ast.literal_eval)
try:
    u_emb.drop(columns='Unnamed: 0',inplace=True)
    r_emb.drop(columns='Unnamed: 0',inplace=True)
except:
    pass
# result = np.array(inference.transform_fn(dataset, m, w, world.config["multicore"]))

activate_f=nn.Sigmoid()
# 전체 레스토랑에 대한 임베딩 텐서화
tmp=[]
for i in range(len(r_emb)):
    tmp.append(r_emb.loc[i,'embedding'])
rst_embedding_matrix=torch.tensor(tmp)
# 

@app.route('/')
def hello():
    # a = {'result':result[0,:]}
    
    return "Light GCN Recommendation Model"


@app.route('/predict', methods=['GET'])
def predict():
    if request.method == "GET":
        # 1. url을 입력으로 받아서
        user = request.args.get('user')
        user = int(user)

        user_embedding_vector=torch.tensor(u_emb.loc[user,'embedding'])
        
        # user = request.files['user']
        one_user_predict=activate_f(torch.matmul(user_embedding_vector,rst_embedding_matrix.t()))
        _, one_user_rating=torch.topk(one_user_predict,k=100)
        result_user = np.array(one_user_rating).tolist()

        result_dict = {
            'user_num':user,
            'result':result_user
        }
    # http://127.0.0.1:5000/predict?user=n (이 링크로 접속 시 결과가 뜸. n은 n번째 유저)
    return json.dumps(result_dict)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
