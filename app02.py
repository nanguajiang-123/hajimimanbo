from typing import Annotated, List

from fastapi import FastAPI, APIRouter,Header, File,UploadFile,Request
from pydantic import BaseModel

app02 = APIRouter()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []
@app02.post("/items")
async def items(request:Request):
    print("URL:",request.url)
    print("Method:",request.method)
    print("Headers:",request.headers)
    return {"method": request.method, "url": str(request.url), "headers": dict(request.headers),"cookies": request.cookies}

