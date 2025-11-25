import random
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


app04 = APIRouter()

# 2. 内存存储验证码：key=用户标识（如手机号/邮箱），value=(验证码字符串, 生成时间戳)
# 生产环境建议替换为 Redis（支持分布式、自动过期）
verify_code_store = {}

# 3. 请求模型（定义接口入参格式，自动校验）
class SendCodeRequest(BaseModel):
    user_id: str  

class CheckCodeRequest(BaseModel):
    user_id: str  # 与发送时的用户标识一致
    input_code: str  # 用户输入的4位验证码（如"0015"）


@app04.post("/send", summary="发送验证码")
def send_code(req: SendCodeRequest):
    user_id = req.user_id
    
    
    rand_num = random.randint(1, 9999)
    verify_code = str(rand_num).zfill(4)
    
    # 存储验证码+生成时间（覆盖旧验证码，避免重复）
    verify_code_store[user_id] = (verify_code, time.time())
    
    
    print(f"【验证码通知】向用户 {user_id} 发送验证码：{verify_code}（60秒内有效）")
    
    
    return {
        "code": 200,
        "message": "验证码已发送，60秒内有效",
        "user_id": user_id
    }

@app04.post("/check", summary="校验")
def check_code(req: CheckCodeRequest):
    user_id = req.user_id
    input_code = req.input_code  
    
    
    if user_id not in verify_code_store:
        return {
            "code": 400,
            "message": "请先注册用户"
        }
    
    stored_code, create_time = verify_code_store[user_id]
    current_time = time.time()
    
    
    if current_time - create_time > 60:
       
        del verify_code_store[user_id]
        return {
            "code": 400,
            "message": "验证码已过期，请重新发送"
        }
    
    
    if input_code != stored_code:
        return {
            "code": 400,
            "message": "验证码错误，请重新输入"
        }
    
    
    del verify_code_store[user_id]
    
    return {
        "code": 200,
        "message": "验证码校验通过！"
    }