import random
import time
import threading
from dataclasses import dataclass
from typing import Dict, Tuple, Optional,List
from fastapi import FastAPI,APIRouter
from pydantic import BaseModel,Field
import threading
store_lock = threading.Lock()

app05 = APIRouter()
verify_code_store = {}
class sendcodeRequest(BaseModel):
    user_id: List[str]=[]

class checkcodeRequest(BaseModel):
    dict_user: Dict[str,int]=Field(default={})

@app05.post("/sendcode")
def send_code_to_user(req:sendcodeRequest):
    #with store_lock:
        for user_ids in req.user_id:
            rand_num = random.randint(1, 9999)
            verify_code = str(rand_num).zfill(4)
            start_time=time.time()
            verify_code_store[user_ids] = (verify_code, start_time)
            print(f"【验证码通知】向用户 {user_ids} 发送验证码：{verify_code}（60秒内有效）")
        return verify_code_store


@app05.post("/checkcode")
def check_code_to_user(req:checkcodeRequest):
    #with store_lock:
        results = {}
        for user_id in req.dict_user.keys():
            input_code = req.dict_user[user_id]
            if user_id not in verify_code_store:
                results[user_id] = {
                "code": 400,
                "message": f"用户{user_id}请先注册用户"
            }
                continue
            stored_code, create_time = verify_code_store[user_id]
            current_time = time.time()
            if current_time - create_time > 60:
                results[user_id] = {
                "code": 400,
                "message": f"用户{user_id}验证码已过期，请重新获取"
            }
                continue
            if input_code != stored_code:
                results[user_id] ={
                "code": 400,
                "message": f"用户{user_id}验证码错误，请重新输入"
            }
                continue
            results[user_id] = {
            "code": 200,
            "message": f"用户{user_id}验证码校验成功"
        }
        return results   