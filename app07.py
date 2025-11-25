import random
import time
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import threading
import sqlite3 


app07 = APIRouter()



class SignUpRequest(BaseModel):
    user_id: str  
    user_password_new: str
    user_password_poor:str

class returnMessage(BaseModel):
    user_id:str
    return_code:str



class SignInRequest(BaseModel):
    user_id: str  
    user_password: str



@app07.post("/send",summary="发送校验码")
def send_code(req: SignUpRequest):
    if req.user_password_new != req.user_password_poor:
        return {"code":400,"message":"两次输入密码不一致，请重新输入"}
    rand_num = random.randint(1, 9999)
    verify_code = str(rand_num).zfill(4)
    start_time = time.time()
    conn=sqlite3.connect('user_information.db')
    cursor=conn.cursor()
    cursor .execute('''CREATE TABLE IF NOT EXISTS USER
       (USER_ID TEXT PRIMARY KEY     NOT NULL,
        USER_PASSWORD TEXT       NOT NULL,
        START_TIME  REAL    NOT NULL,
        CHECK_CODE  TEXT         NOT NULL
                );''')
    cursor.execute("INSERT INTO USER (USER_ID,USER_PASSWORD,START_TIME,CHECK_CODE) VALUES (?, ?, ?, ?)", (req.user_id, req.user_password_new,start_time,verify_code))
    conn .commit()
    conn .close()
    return {
        "code": 200,
        "message": "验证码已发送，60秒内有效",
        "user_id": req.user_id,
        "check_code":verify_code
    }


@app07.post("/check", summary="校验")
def check_code(req: returnMessage):
    conn=sqlite3.connect('user_information.db')
    cursor=conn.cursor()
    cursor.execute("SELECT CHECK_CODE,START_TIME FROM USER WHERE USER_ID=?", (req.user_id,))
    row = cursor.fetchone()
    #cursor.fetchone() 返回 None 表示没有查询到对应的用户,要不然就是返回元组对应着每一个主键后面跟着的值
    if row is None:
        return {"code":400,"message":"用户不存在，请先注册"}
        
    stored_code, create_time = row
    current_time = time.time()
    if current_time - create_time > 60:
        cursor.execute("DELETE FROM USER WHERE USER_ID=?", (req.user_id,))
        conn .commit()
        return {"code":400,"message":"验证码已过期，请重新获取"}
    if req.return_code != stored_code:
        cursor.execute("DELETE FROM USER WHERE USER_ID=?", (req.user_id,))
        conn .commit()
        return {"code":400,"message":"验证码错误，请重新输入"}
    cursor.close
    return {"code":200,"message":"验证码校验成功，注册成功"}


@app07.post("/login", summary="用户登录")
def  login_in(req: SignInRequest):
    conn=sqlite3.connect('user_information.db')
    cursor=conn.cursor()
    cursor.execute("SELECT USER_PASSWORD FROM USER WHERE USER_ID=?", (req.user_id,))
    row = cursor.fetchone()
    if row is None:
        return {"code":400,"message":"用户不存在，请先注册"}
    stored_password = row[0]
    if req.user_password!= stored_password:
        return {"code":400,"message":"密码错误，请重新输入"}
    cursor.close
    return {"code":200,"message":"登录成功"}


