from typing import Annotated, List, Optional

from fastapi import FastAPI, APIRouter,Header, File,UploadFile
from pydantic import BaseModel, Field

app01 = APIRouter()


class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    # 使用 Optional[...] 替代 `str | None`，以兼容 Python < 3.10
    if_modified_since: Optional[str] = None
    traceparent: Optional[str] = None
    # 避免可变默认值，使用 Field(default_factory=list)
    x_tag: List[str] = Field(default_factory=list)


@app01.post("/files")
async def get_files(files:List[bytes]=File()):
    for file in files:
        print("file size:",len(file))
    return {
        "file":len(files)
    }


@app01.post("/uploadfile")
async def get_uploadfile(file:UploadFile):
    print("file filename:",file.filename)
    return {
        "file":len(file.filename)
    }


@app01.post("/uploadfiles")
async def get_uploadfiles(files:List[UploadFile]):
    print("files",len(files))
    return {"names":
        [file.filename for file in files]
    }