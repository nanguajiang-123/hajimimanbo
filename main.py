# from app01 import app01
# from app02 import app02
# from app03 import app03
# from app04 import app04
# from app05 import app05
#from app06 import app06
from app07 import app07
from fastapi import FastAPI
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="statics"))


# app.include_router(app01,tags=["01 文件上传"])
# app.include_router(app02,tags=["02 requst对象"])
# app.include_router(app03,tags=["03 相应参数模型"])
# app.include_router(app04,tags=["04 生成随机验证码"])
# app.include_router(app05,tags=["05 多个验证码验证"])
# app.include_router(app06,tags=["06 多个验证码验证加锁"])
app.include_router(app07,tags=["07 使用SQLite存储验证码"])

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)